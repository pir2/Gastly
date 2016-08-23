import time
import csv

from gastly import random_account, get_account_ready
from gastly.models import init_database, create_tables, Account
from gastly.utils import get_args

args = get_args()

def create():
  while True:
    try:
      while True:
        try:
          db.connect()
          break
        except Exception as e:
          print e, 'Retrying...'
      
      try:
        while True:
            random_account(args.email)
      finally:
        db.close()
    except KeyboardInterrupt:
      break
    except Exception as e:
      print e, 'Retrying...'
      
def verify():
  while True:
    try:
      while True:
        try:
          db.connect()
          break
        except Exception as e:
          print e, 'Retrying...'
      
      try:
        while True:
          accounts = Account.get_not_ready()
          if len(accounts) == 0:
            time.sleep(args.login_delay)
          for a in accounts:
            get_account_ready(a, args.location)
            time.sleep(args.login_delay)
      finally:
        db.close()
    except KeyboardInterrupt:
      break
    except Exception as e:
      print e, 'Retrying...'
      
def main():
  db = init_database(args)
  
  create_tables(db)

  if args.action == 'create':
    create()
  elif args.action == 'verify':
    verify()
 