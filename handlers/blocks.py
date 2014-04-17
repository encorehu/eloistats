from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class BlocksHandler(BaseHandler):
    def get(self):
        self.render("blocks.html")
