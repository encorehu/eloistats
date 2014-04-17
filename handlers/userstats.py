from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class UserStatsHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class UserStatsLuckGraphHandler(BaseHandler):
    def get(self):
        self.render("index.html")
