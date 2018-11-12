from config import Config
from db import Database
from email1 import email1
from sweeper import sweeper
from logger import initlogger
import datetime


def main(sweeper_name=None):
    now = datetime.datetime.now()
    initlogger('logs/' + now.strftime("%Y%m%d") + '/sweepers_' + now.strftime("%Y%m%d%H%M%S") + '.log')

    cred = Config('credentials.ini')
    em = email1(cred.get('server', 'email'), cred.get('username', 'email'), cred.get('password', 'email'))
    db = Database(cred.get('username', 'db'), cred.get('password', 'db'))

    swprs = Config('sweepers.ini')
    if sweeper_name:
        swpr_details = swprs[sweeper_name]
        swpr_details['name'] = sweeper_name
        s = sweeper(swpr_details, db, em)
        s.run()
    else:
        for swpr in eval(swprs.get('sweeper_list', 'sweepers')):
            swpr_details = swprs[swpr]
            swpr_details['name'] = swpr
            s = sweeper(swpr_details, db, em)
            s.run()


if __name__ == '__main__':
    main()
