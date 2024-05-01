# Forgive me what I do, for I am not a python developer

import discord
import os
import argparse
from ticket_stats import get_attendees
import sys 
from datetime import date

# ID of channel to post to
channel_id = 1229467756852936714 # test channel: 1167171723058225212

intents = discord.Intents.default()
client = discord.Client(command_prefix="!", intents=intents)

def print_data():
  # Sort first by this week sales, then all time sales. (None) goes at the bottom of the list.
  sort_sales = sorted(sales.items(), key=lambda item: -1*(1000*item[1]['this_week'] + item[1]['all_time'] + (-999999 if item[0] == "(None)" else 0)))
  
  tstr = ''
  tstr += '🎉 Ticket sales leaderboard for ' + date.today().strftime('%B %d, %Y') + ' 🎉 \n'
  tstr += '\n```'
  tstr += '\nPromo code          |  Total  |  7d change '
  tstr += '\n-------------------------------------------'

  for key, value in sort_sales:
    if key == 'total':
      continue
    code_str = (key[:18] + '..') if len(key) > 18 else key
    code_str = code_str.ljust(20,' ')
    total_str = str(sales[key]['all_time']).ljust(8)
    
    this_week_str = str(sales[key]['this_week'])
    
    tstr += '\n' + code_str + '| ' + total_str + '| ' + this_week_str
  tstr += '\n```'
  tstr += '\nTotal tickets sold: ' + str(sales['total']['all_time'])
  return tstr

@client.event
async def on_ready():
  print("Logged in!")
  
  message = print_data()
  print('')
  print(message)
  print('')
  await client.get_channel(channel_id).send(message)

  # Produces an ugly exception message because discord bots are meant to be run continuously
  print('\n\n✨ you should ignore this error message ✨')
  sys.exit()

parser = argparse.ArgumentParser(description='Aggregate Eventbrite attendee data by promotional code')
parser.add_argument('event_id', help='ID of the Eventbrite event')
parser.add_argument('eventbrite_token', help='Eventbrite API token')
parser.add_argument('discord_token', help='Discord API token')
args = parser.parse_args()

sales = get_attendees(args.event_id, args.eventbrite_token)

print(sales)

client.run(args.discord_token)
