from handlers.base import BaseHandler
from tornado import gen
import momoko

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class BlocksHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
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

            cursor = yield momoko.Op(self.db.execute, operation)
            blocks = cursor.fetchall()

            rendered = self.render_string('blocks.html', blocks=blocks)
            self.write(rendered)
        except Exception as error:
            self.write(str(error))

        self.finish()
