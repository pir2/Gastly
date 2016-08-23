import datetime
import random
import string
import time

import ptcaccount2
from pgoapi import PGoApi
from .models import Account
from .session import PokemonSession
from .utils import get_args

args = get_args()

class Pokedex:
  Bulbasaur = 1
  Charmander = 4
  Squirtle = 7
  
STARTER_POKEMON = (Pokedex.Bulbasaur, Pokedex.Charmander, Pokedex.Squirtle)

def _random_string(length=15):
  return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])
                                      
def create_account(username, password, email, birth_date):
  ptcaccount2.create_account(username, password, email, birth_date)
  
  account = Account.create(
    username=username,
    password=password,
    email=email
  )
  
  return account
  
def get_account_ready(account, position):
  session = PokemonSession(
    account.username,
    account.password,
    position
  )
  
  session.login()
  if args.request_delay:
    time.sleep(args.request_delay)
  
  try:
    account.last_latitude = position[0]
    account.last_longitude = position[1]
    account.last_login_date = datetime.datetime.now()
  
    if account.tutorial_encounter_complete == False:
      pokemon_id = random.choice(STARTER_POKEMON)
      session.complete_tutorial_encounter(pokemon_id)
      account.tutorial_encounter_complete = True
      
      if args.request_delay:
        time.sleep(args.request_delay)
    
    if account.tutorial_complete == False:
      session.complete_tutorial()
      account.tutorial_complete = True
      
      if args.request_delay:
        time.sleep(args.request_delay)
    
    if account.trainer_name == None:
      trainer_name = _random_string(12)
      while not session.assign_trainer_name(trainer_name):
        trainer_name = _random_string(12)
        
        if args.request_delay:
          time.sleep(args.request_delay)
      account.trainer_name = trainer_name
  finally:
    account.save()
    
def random_account(email):
  account_data = ptcaccount2.random_account(email=email, email_tag=True)
  
  account = Account.create(
    username=account_data['username'],
    password=account_data['password'],
    email=account_data['email']
  )
  
  return account
   
  