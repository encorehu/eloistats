from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class UserStatsHandler(BaseHandler):
    def get(self, addr):
        #logger.debug(locals())
        #locals().pop('self')
        #a=locals()
        #a.pop('self')
        if addr:
            self.render("userstats.html", addr=addr)
        else:
            self.render("mystats.html")

class UserStatsLuckGraphHandler(BaseHandler):
    def get(self):
        self.render("index.html")
