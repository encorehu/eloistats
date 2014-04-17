from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class TopContributorsHandler(BaseHandler):
    def get(self):
        self.render("topcontributors.html")
