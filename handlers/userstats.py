from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class UserStatsHandler(BaseHandler):
    def get(self, addr):
        #logger.debug(locals())
        #locals().pop('self')
        #a=locals()
        #a.pop('self')
        cmd = self.get_argument("cmd",None)
        start = self.get_argument("start",0)
        back = self.get_argument("back",604800)
        res = self.get_argument("res",1)
        logging.info(cmd)
        if addr:
            if cmd:
                if cmd == 'hashgraph':
                    self.render("userhashrategraph.txt", addr=addr)
                elif cmd == 'balancegraph':
                    self.render("userbalancegraph.txt", addr=addr)
                else:
                    self.write("")
            else:
                self.render("userstats.html", addr=addr)
        else:
            self.render("mystats.html")

class UserStatsLuckGraphHandler(BaseHandler):
    def get(self):
        self.render("pullluckgraph.txt")

class UserStatsHashrateGraphHandler(BaseHandler):
    def get(self):
        self.render("pullhashrategraph.txt")
