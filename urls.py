from handlers.foo import FooHandler
from handlers.index import IndexHandler
from handlers.mystats import MyStatsHandler
from handlers.blocks import BlocksHandler
from handlers.topcontributors import TopContributorsHandler
from handlers.userstats import UserStatsHandler,UserStatsLuckGraphHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/foo", FooHandler),
    (r"/mystats", MyStatsHandler),
    (r"/blocks", BlocksHandler),
    (r"/topcontributors", TopContributorsHandler),
    (r"/userstats", UserStatsHandler),
    (r"/userstats/poolluckgraph", UserStatsLuckGraphHandler),
    (r"/userstats/\w*", UserStatsHandler),
    (r"/instantscripts/[\w\.]*", FooHandler),
]
