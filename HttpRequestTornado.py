import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from tornado import web, ioloop


class HttpRequest:
    def __init__(self, GA, port, thread_pool):
        # thread_pool -> ThreadPoolExecutor

        try:
            server_app = web.Application([(
                r".*",  # match all
                HttpRequestHandler,
                {"GA": GA, "thread_pool": thread_pool}
            )])
            server_app.listen(port)

            GA.logger.log("Listening on Port: {}. Max Threads: {}".format(
                port, thread_pool._max_workers
            ))

            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()


class HttpRequestHandler(web.RequestHandler):
    def initialize(self, GA, thread_pool):
        self.GA = GA # initialing class object that contains handle methods for requests
        self.thread_pool = thread_pool

    @web.asynchronous
    def get(self):
        self.thread_pool.submit(self.respond)

    def respond(self):
        uri = self.request.uri
        if uri in ["/favicon.ico", "/"]:
            self.finish()
            return

        self.GA.logger.log(uri)

        parsed_url = urlparse(uri)
        parsed_query = parse_qs(parsed_url.query)

        args = json.loads(parsed_query["args"][0]) if "args" in parsed_query else {}
        method = "http_" + parsed_url.path[1:]

        ret = json.dumps(
            self.GA.__getattribute__(method)(args),
            sort_keys=False,
            indent=4,
            separators=(',', ': '),
            default=lambda obj: obj.isoformat('T') if type(obj) is datetime else None,
            skipkeys=True
        )

        self.set_header('Content-Type', 'application/json')
        self.write(ret)
        self.finish()