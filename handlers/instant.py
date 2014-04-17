from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)

class InstantdataHandler(BaseHandler):
    def get(self):
        self.render("livedata.json")
