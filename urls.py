from handlers.foo import FooHandler
from handlers.index import IndexHandler
from handlers.mystats import MyStatsHandler
from handlers.blocks import BlocksHandler
from handlers.topcontributors import TopContributorsHandler
from handlers.userstats import UserStatsHandler,UserStatsLuckGraphHandler,UserStatsHashrateGraphHandler
from handlers.instantscripts import LiveDataHandler
from handlers.instant import InstantdataHandler
from handlers.api import ApiHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/foo", FooHandler),
    (r"/mystats", MyStatsHandler),
    (r"/blocks", BlocksHandler),
    (r"/topcontributors", TopContributorsHandler),
    (r"/userstats", UserStatsHandler),
    (r"/poolluckgraph", UserStatsLuckGraphHandler),
    (r"/poolhashrategraph", UserStatsHashrateGraphHandler),
    (r"/userstats/(\w*)", UserStatsHandler),
    (r"/instant/livedata.json", InstantdataHandler),
    (r"/instantscripts/livedata.js", LiveDataHandler),
    (r"/instantscripts/livedata-main.js", LiveDataHandler),
    (r"/api/v1/", ApiHandler),
    (r"/api/v1/\w*", ApiHandler),
]
