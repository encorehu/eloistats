from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class LiveDataHandler(BaseHandler):
    def get(self):
        self.render("livedata-main.js")
