# coding: -*-utf-8-*-
import tornado.web

class Filed(tornado.web.UIModule):

    allow_type = ('string', 'datetime',)

    def __init__(self, handler, **kwargs):
        super(Filed, self).__init__(self, handler)
        self.id = int(kwargs['id'])
        self.field_name = kwargs['field_name']
        self.display_name = kwargs['display_name']
        self.query_id = kwargs['query_id']
        self.data_type = kwargs['data_type']
        self.default_value = kwargs['default_value']

    def render(self):
        if self.data_type == 'datetime':
            return self.render_string('controls/input_temp.html',
                                      display_name=self.display_name,
                                      field_name=self.field_name)
        else:
            return self.render_string('controls/input_temp.html',
                                      display_name=self.display_name,
                                      field_name=self.field_name)


