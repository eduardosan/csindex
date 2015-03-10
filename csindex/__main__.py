#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import sys
import logging
from csindex import sync
from csindex import config

config.setup_config()

log = logging.getLogger()

if __name__ == "__main__":

    daemon = sync.Sync(pidfile=config.PIDFILE_PATH)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('starting daemon ...')
            daemon.run()
        elif 'stop' == sys.argv[1]:
            print('stopping daemon ...')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print('restarting daemon ...')
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)