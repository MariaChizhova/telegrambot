import logging
import time

from bot import get_updates, process_new_message

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')

logger = logging.getLogger()

if __name__ == '__main__':
    last_update = 0
    while True:
        try:
            updates = get_updates(last_update)
        except:
            logger.error("Couldn't check for updates.")
            continue
        if updates:
            for update in updates:
                last_update = max(last_update, update['update_id'] + 1)
                process_new_message(update)