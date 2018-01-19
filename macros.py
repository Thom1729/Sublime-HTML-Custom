from YAMLMacros.lib.syntax import rule, meta
from YAMLMacros.lib.arguments import foreach, argument

def open_tag(name, **rest):
    ret = rule(
        match=r'(?i)(<)(%s)' % name,
        captures={
            1: 'punctuation.definition.tag.begin.html',
            2: 'entity.name.tag.html',
        },
    )

    ret.update(**rest)
    return ret

def close_tag(name):
    return rule(
        match=r'(?i)(</)(%s)' % name,
        captures={
            1: 'punctuation.definition.tag.begin.html',
            2: 'entity.name.tag.html',
        },
        set='tag-end',
    )

def void_tag(name, *, meta_scope=None, attributes='attributes'):
    return open_tag(
        name,
        push=[
            meta(meta_scope or 'meta.element.%s.html' % name),
            [
                { 'include': 'tag-end-void' },
                { 'include': attributes },
            ],
        ],
    )

def tag(name, *, meta_scope=None, attributes='attributes', contents='normal'):
    return open_tag(
        name,
        push=[
            meta(meta_scope or 'meta.element.%s.html' % name),
            [
                close_tag(name),
                { 'include': contents },
            ],
            [
                { 'include': 'tag-end' },
                { 'include': attributes },
            ],
        ]
    )

def break_on_tag(expr):
    return rule(
        match=r'(?i)(?=<(?:%s))' % expr,
        pop=True,
    )