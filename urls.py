from handlers.foo import FooHandler
from handlers.index import IndexHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/foo", FooHandler),
    (r"/mystats", FooHandler),
    (r"/blocks", FooHandler),
    (r"/topcontributors", FooHandler),
    (r"/userstats", FooHandler),
    (r"/userstats/\w*", FooHandler),
]
