from elasticsearch_dsl import DocType, Nested, field


class MessageIndex(DocType):
    room = field.Keyword()
    user = field.Text()
    created = field.Date()
    message = field.Text()
    status = field.Text()
    tags = Nested(
        properties=
        {
            'tags': field.Text()
        }
    )

    class Meta:
        index = 'Message'
