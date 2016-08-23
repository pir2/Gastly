import sys
import argparse
import re
import random
import math

import geopy
import geopy.distance

# Apply a location jitter
def jitter_location(location=None, maxMeters=10):
    origin = geopy.Point(location[0], location[1])
    b = random.randint(0, 360)
    d = math.sqrt(random.random()) * (float(maxMeters) / 1000)
    destination = geopy.distance.distance(kilometers=d).destination(origin, b)
    return (destination.latitude, destination.longitude, location[2])

def memoize(function):
  memo = {}

  def wrapper(*args):
    if args in memo:
        return memo[args]
    else:
        rv = function(*args)
        memo[args] = rv
        return rv
  return wrapper

@memoize
def get_args():
  def parse_unicode(bytestring):
    decoded_string = bytestring.decode(sys.getfilesystemencoding())
    return decoded_string
    
  def parse_location(bytestring):
    decoded_string = parse_unicode(bytestring)
    
    prog = re.compile("^(\-?\d+\.\d+),?\s?(\-?\d+\.\d+)$")
    res = prog.match(decoded_string)
    
    return (float(res.group(1)), float(res.group(2)), 0)
    
  parser = argparse.ArgumentParser(description='Manages accounts.')
  parser.add_argument('action', type=parse_unicode, choices=['verify', 'create'])
  parser.add_argument('-l', '--location', type=parse_location,
                      help='Location, must be coordinates.')
  parser.add_argument('-e', '--email', type=parse_unicode,
                      help='Email address.')
  parser.add_argument('-j', '--jitter', help='Apply random -9m to +9m jitter to location',
                        action='store_false', default=True)
  parser.add_argument('-ld', '--login-delay',
                      help='Time delay between each account verification.',
                      type=float, default=5)
  parser.add_argument('-rd', '--request-delay',
                      help='Time delay between each request.',
                      type=int, default=3)
  parser.add_argument('-D', '--db',
          help='Database filename',
                      default='gastly.db')
  parser.add_argument('--db-type',
          help='Type of database to be used (default: sqlite)',
                      default='sqlite')
  parser.add_argument('--db-name', help='Name of the database to be used')
  parser.add_argument('--db-user', help='Username for the database')
  parser.add_argument('--db-pass', help='Password for the database')
  parser.add_argument('--db-host', help='IP or hostname for the database')
  parser.add_argument('--db-port', help='Port for the database', type=int, default=3306)
  parser.add_argument('--db-max-connections', help='Max connections for the database',
                      type=int, default=5)
  parser.set_defaults(DEBUG=False)

  args = parser.parse_args()
  
  if args.action == 'verify':
    if args.location is None:
      parser.print_usage()
      print(sys.argv[0] + ": error: arguments -l/--location is required")
      sys.exit(1)
  elif args.action == 'create':
    if args.email is None:
      parser.print_usage()
      print(sys.argv[0] + ": error: arguments -e/--email is required")
      sys.exit(1)

  return args