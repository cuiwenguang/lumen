import tornado.web
import tornado.ioloop
from tornado.options import define, parse_command_line, options
import torndb

from handler import (HomeHandler, CustomHandler,ApiReportHandler, ReportHandler)

define("port", 5000, type=int)
define("debug", default=True)

routers = [
    (r'/', HomeHandler),
    (r'^/custom/(?P<id>\d+)?', CustomHandler),
    (r'^/api/reports/', ApiReportHandler),
    (r'^/report/(?P<id>\d+)', ReportHandler),
]

settings = {
    "static_path": 'static',
    "template_path": "templates",
    "debug": options.debug
}


def main():
    parse_command_line()
    db = torndb.Connection('127.0.0.1', "mydb", user='root', password='123456')
    settings['db'] = db
    app = tornado.web.Application(routers, **settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

