from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class MyStatsHandler(BaseHandler):
    def get(self):
        self.render("mystats.html")
