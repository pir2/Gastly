from pgoapi import PGoApi
import time

from .utils import get_args, jitter_location

args = get_args()

class PokemonSession(object):
  def __init__(self, username, password, position):
    self._api = PGoApi()
    self.username = username
    self.password = password
    self.set_position(position)
    
  def is_logged_in(self):
    if self._api._auth_provider and self._api._auth_provider._ticket_expire:
      remaining_time = self._api._auth_provider._ticket_expire / 1000 - time.time()
      if remaining_time > 60:
        return True
        
    return False
    
  def _ensure_ticket(self):
    if self.is_logged_in() == False:
      if self._api._auth_provider:
        self.login()
        
  def set_position(self, position):
    if args.jitter:
      position = jitter_location(position)
      
    self.position = position
    self._api.set_position(*position)
    
  def login(self):
    self._api.login('ptc', self.username, self.password)
    
  def complete_tutorial(self):
    self._ensure_ticket()
    
    self._api.mark_tutorial_complete(
      tutorials_completed=0,
      send_marketing_emails=False,
      send_push_notifications=False
    )
    
  def assign_trainer_name(self, trainer_name):
    self._ensure_ticket()
    
    response = self._api.check_codename_available(codename=trainer_name)
    if response['responses']['CHECK_CODENAME_AVAILABLE']['is_assignable'] == False:
      return False
      
    self._api.claim_codename(codename=trainer_name)
    
    return True
    
  def complete_tutorial_encounter(self, pokemon_id):
    self._ensure_ticket()
    
    self._api.encounter_tutorial_complete(pokemon_id=pokemon_id)