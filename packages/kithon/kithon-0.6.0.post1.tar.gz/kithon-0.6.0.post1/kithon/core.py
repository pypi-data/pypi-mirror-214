import ast
from collections import defaultdict
from pathlib import Path
from itertools import product
import yaml
try:
    from hy.lex import hy_parse
except ImportError:
    is_hy_supported = False
else:
    is_hy_supported = True
try:
    from coconut.convenience import parse, setup
except ImportError:
    is_coconut_supported = False
else:
    is_coconut_supported = True
from jinja2 import Template
from .node import Node
from . import types, __path__


def visitor(func):
    setattr(Transpiler, func.__name__, func)
    annotations = func.__annotations__['tree']
    if isinstance(annotations, tuple):
        for ann in annotations:
            Transpiler.elements[ann] = func
    else:
        Transpiler.elements[annotations] = func
    return func

class dont_render:
    def __init__(self, node):
        self.dont_render = True
        self.node = node

class Transpiler:
    elements = {}

    def __init__(self, lang='', templs=''):
        self.templates = {}
        self.get_lang('python')
        if lang:
            self.get_lang(lang)
        if templs:
            self.load_templs(templs)
        self.nl = 0
        self.mod_name = '__main__'
        self.namespace = '__main__'
        self.variables = {
            '__main__': {'type': types.types['module']('__main__')}
        }
        self.strings = []
        self.temp_var_counts = defaultdict(int)
        self.used = set([])
        self.ctx = [None]

    def new_var(self, full_name, _type):
        if str(_type) in self.variables:
            self.variables.update({
                full_name + name.removeprefix(_type): var
                for name, var in self.variables.items()
                if name.startswith(_type)
            })
        self.variables.update({
            full_name: {
                'own': full_name,
                'type': _type,
                'immut': True
            }
        })


    def get_macro(
            self, own='', _type=None,
            selector='{_}', is_reducing=False
    ):
        macro = {}
        if own:
            own = selector.format(_=own)
            macro = self.templates.get(own, {})
        if not macro and _type is not None:
            if isinstance(_type, tuple):
                type_chain = product(
                    *map(types.type_simplification, _type)
                )
            else:
                type_chain = types.type_simplification(_type)
            for t in type_chain:
                own = selector.format(_=t)
                _macro = self.templates.get(own, {})
                if is_reducing:
                    macro = _macro | macro
                elif _macro:
                    return _macro, own
        return macro, own


    def use(self, name):
        self.used.add(name)
        return ''

    def get_temp_var(self, base_name='temp'):
        """Get a unique temporary variable name."""
        self.temp_var_counts[base_name] += 1
        return f'{base_name}_{self.temp_var_counts[base_name]}'

    def previous_ns(self):
        if self.namespace == '__main__':
            return '__main__'
        return self.namespace[:self.namespace.rfind('.')]

    def node(self, **kwargs):
        return Node(env=self, **kwargs)

    def get_lang(self, lang):
        _dir = Path(__path__[0]).parent / 'translators' / lang
        if not _dir.exists():
            raise ValueError(f'{lang} is not supported')
        for templs in _dir.glob('**/*.tp'):
            self.load_templs(templs.open().read())

    def load_templs(self, templates):
        templates = yaml.load(
            templates.expandtabs(2),
            Loader=yaml.FullLoader
        )
        if not templates:
            return
        for name, template in templates.items():
            self.add_templ(name, template)

    def add_templ(self, name, template):
        if name not in self.templates:
            self.templates[name] = {'meta': {}}
        if name in ['types', 'operators']:
            self.templates[name] = template
        elif name == 'meta':
            self.templates['meta'].update(template)
        elif isinstance(template, str):
            self.templates[name].update({'tmp': Template(template)})
        elif isinstance(template, bool) and not template:
            self.templates[name].update({'tmp': ''})
        elif template is None:
            self.templates[name].update({'tmp': None})
        elif isinstance(template, dict):
            for field, value in template.items():
                keywords = [
                    'type', 'import_code', 'code',
                    'alt_name', 'ret_type', 'meta',
                    'decorate', 'args', 'access'
                ]
                if field == 'tmp':
                    self.add_templ(name, value)
                elif field in keywords:
                    self.templates[name].update({field: value})
                else:
                    self.add_templ(f'{name}.{field}', value)

    def visit(self, tree, **kw):
        if isinstance(tree, Node):
            return tree
        if isinstance(tree, (int, str, float, bool)):
            tree = ast.Constant(value=tree)
        if type(tree) not in self.elements:
            return self.node()
        node = self.elements.get(type(tree))(
            self, tree,
            **(kw or {})
        )
        node.ast = tree
        return node

    def generate(self, code, lang='py', mode='main'):
        self.mod_name = mode
        if mode not in ['main', 'block']:
            self.namespace = mode
            self.variables |= {
                mode: {'type': types.types['module'](mode)}
            }
        if lang == 'py':
            tree = ast.parse(code).body
        elif lang == 'hy':
            if not is_hy_supported:
                raise Exception(
                    "requires hy library\n"
                    "\trun 'python -m pip install kithon[add-langs]' to fix"
                )
            tree = hy_parse(code)[1:]
        elif lang == 'coco':
            if not is_coconut_supported:
                raise Exception(
                    "requires coconut library\n"
                    "\trun 'python -m pip install kithon[add-langs]' to fix"
                )
            setup(target='sys')
            tree = ast.parse(parse(code, 'block')).body
        if mode == 'eval':
            return self.visit(tree[0].value).render()
        else:
            for block in map(self.visit, tree):
                if not block:
                    continue
                self.strings.extend(block.render().split('\n'))
        if mode != 'block':
            code = self.templates['main']['tmp'].render(
                _body=self.strings,
                body='\n'.join(self.strings),
                env=self
            )
            if mode == 'main':
                self.variables = {
                    '__main__': {'type': types.types['module']('__main__')}
                }
                self.temp_var_counts = defaultdict(int)
        else:
            code = '\n'.join(self.strings)
        self.nl = 0
        self.namespace = '__main__'
        self.strings = []
        self.used = set([])
        return code
