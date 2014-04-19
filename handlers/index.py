from handlers.base import BaseHandler
from tornado import gen
import momoko
import logging
logger = logging.getLogger('boilerplate.' + __name__)


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        announce = self.render_string("announce.txt")
        try:
            #logger.debug(str(dir(self)))
            #logger.debug(str(self.db))
            #cursor = yield momoko.Op(self.db.execute, 'SELECT pg_sleep(%s);', (1,))
            #self.write('Query results: %s<br>\n' % cursor.fetchall())
            operation = '''select user_id,
            stats_blocks.id as blockid,
            confirmations,
            roundstart,
            acceptedshares,
            network_difficulty,
            time,
            keyhash,
            blockhash,
            height,
            date_part('epoch', NOW())::integer-date_part('epoch', time)::integer as age,
            date_part('epoch', time)::integer-date_part('epoch', roundstart)::integer as duration
            from %s.stats_blocks left join users on user_id=users.id
            where confirmations > 0 and server=%s order by time desc %s;'''  % (self.schema, self.server_id, 'limit 8')

            #sql = yield momoko.Op(self.db.mogrify, '''select *,stats_blocks.id as blockid,date_part('epoch', NOW())::integer-date_part('epoch', time)::integer as age,date_part('epoch', time)::integer-date_part('epoch', roundstart)::integer as duration from %s.stats_blocks left join users on user_id=users.id where confirmations > 0 and server=%s order by time desc %s;''' , (self.schema, self.server_id, 'limit 8'))
            self.write('SQL: %s<br>' % operation)

            cursor = yield momoko.Op(self.db.execute, operation)
            #logger.debug(str(dir(cursor)))
            #logger.debug(str(cursor.query))
            self.write('Query results: %s<br>\n' % 'aaa')
            blocks = cursor.fetchall()
            self.write('Query results: %s<br>\n' % 'bbb')

            rendered = self.render_string('index.html',announce=announce,blocks=blocks)
            self.write(rendered)
        except Exception as error:
            self.write(str(error))

        self.finish()
