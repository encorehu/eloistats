from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class ApiHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write('{"error":"No command","stime":1397720695}')
