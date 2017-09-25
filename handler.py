import json

from tornado.web import RequestHandler, HTTPError
import torndb


class BaseHandler(RequestHandler):

    def __init__(self, application, *args, **kwargs):
        super(BaseHandler, self).__init__(application, *args, **kwargs)
        self.db = self.settings["db"]

    def initialize(self):
        pass


class ApiReportHandler(BaseHandler):
    def get(self, *args, **kwargs):
        items = self.db.query("select id, name from query")
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(items))


class ReportHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pk = kwargs.get("id", None)
        if not pk:
            HTTPError(404)
        sql = "select * from query where id=%s"
        report = self.db.get(sql, pk)
        rpt_name = report['name']
        data = self.db.query(report['script'])
        table_headers = []

        if len(data)>0 :
            table_headers = data[0].keys()

        self.render('report.html', name=rpt_name, headers=table_headers, data=data)


class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class CustomHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pk = kwargs.get('id', None)
        data = {
            "id": 0,
            "name": "",
            "tpye": "",
            "script": ""
        }
        if pk:
            data = self.db.get("select * from query where id=%s", pk)

        items = self.db.query("select id, name from query")

        self.render('custom.html', entity=data, items=items)

    def post(self, *args, **kwargs):
        pk = kwargs.get('id', None)
        name = self.get_body_arguments('name')
        script = self.get_body_arguments('script')
        type = self.get_body_arguments('type')

        if pk:
            sql = "update query set name=%s,script=%s,type=%s where id=%s"
            self.db.execute(sql, name, script, type, pk)
        else:
            sql = "insert into query(name, script, type) values (%s, %s, %s)"
            pk = self.db.execute(sql, name, script, type)

        self.redirect('/custom/'+ str(pk))

