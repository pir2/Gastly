import datetime
import logging

from peewee import Proxy, CharField, BooleanField, DateTimeField, DoubleField, Proxy, Model, SqliteDatabase
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import RetryOperationalError

db_proxy = Proxy()

class BaseModel(Model):
  class Meta:
    database = db_proxy

class Account(BaseModel):
  username = CharField(unique=True)
  password = CharField()
  email = CharField(max_length=75, unique=True)
  
  trainer_name = CharField(null=True)
  tutorial_encounter_complete = BooleanField(default=False)
  tutorial_complete = BooleanField(default=False)
  banned = BooleanField(default=False)
  
  creation_date = DateTimeField(default=datetime.datetime.now)
  
  last_latitude = DoubleField(null=True)
  last_longitude = DoubleField(null=True)
  last_login_date = DateTimeField(null=True)
  
  last_captcha_date = DateTimeField(null=True)
  
  
  @staticmethod
  def get_ready():
    query = (Account
             .select()
             .where((Account.trainer_name != None) &
                    (Account.tutorial_encounter_complete == True) &
                    (Account.tutorial_complete == True) &
                    (Account.banned == False)))
    
    return query
  
  @staticmethod
  def get_not_ready():
    query = (Account
             .select()
             .where(((Account.trainer_name == None) |
                    (Account.tutorial_encounter_complete == False) |
                    (Account.tutorial_complete == True)) &
                    (Account.banned == False)))
             
    return query

def init_database(args):
  class MyRetryDB(RetryOperationalError, PooledMySQLDatabase):
    pass

  if args.db_type == 'mysql':
    print 'Connecting to MySQL database on %s:%i' % (args.db_host, args.db_port)
    db = MyRetryDB(
      args.db_name,
      user=args.db_user,
      password=args.db_pass,
      host=args.db_host,
      port=args.db_port,
      max_connections=args.db_max_connections,
      stale_timeout=300)
  else:
    print 'Connecting to local SQLite database on %s' % args.db
    db = SqliteDatabase(args.db)
    
  db_proxy.initialize(db)

  return db
  
def create_tables(db):
  db.connect()
  db.create_tables([Account], safe=True)
  db.close()