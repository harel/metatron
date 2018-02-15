"""
Schemas describe the different supported meta tag schemas and
the key names describing the attributes to expect.
For example, opengraph meta tags will contain the `og:name` tag
in a `property` attribute and the value in `content` while
`twitter` tags will be within a `name` attribute.

If the tag scheme is not supported it can be added in runtime
using the metatron.add_schema_spec
"""
SCHEMAS = {
    '': {
        'name': '',  # no schema
        'attribute': 'name',
        'value': 'content'
    },
    'og': {
        'name': 'og',
        'attribute': 'property',
        'value': 'content'
    },
    'twitter': {
        'name': 'twitter',
        'attribute': 'name',
        'value': 'content'
    }
}
