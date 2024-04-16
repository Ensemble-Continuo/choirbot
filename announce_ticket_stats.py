# Forgive me what I do, for I am not a python developer

import discord
import os
import argparse
from ticket_stats import get_attendees
import sys 
from datetime import date

# ID of channel to post to
channel_id = 1229467756852936714

intents = discord.Intents.default()
client = discord.Client(command_prefix="!", intents=intents)

def print_data():
  sort_sales = sorted(total_sales.items(), key=lambda item: -1*item[1])
  
  tstr = '\n🎉 Ticket sales leaderboard for ' + date.today().strftime('%B %d, %Y') + ' 🎉 \n\n'
  tstr += '```  Promo code          |  Total  |  7-day change  '
  tstr += '\n-------------------------------------------------'
  for key, value in sort_sales:
    if key == 'total':
      continue
    code_str = key.ljust(22,' ')
    total_str = str(total_sales[key]).ljust(8)
    this_week_str = str(this_week_sales[key])
    tstr += '\n' + code_str + '| ' + total_str + '| ' + this_week_str
  tstr += '```'
  return tstr

@client.event
async def on_ready():
  print("Logged in!")
  await client.get_channel(channel_id).send(print_data())
  
  # there's probably a more graceful way to disconnect 
  sys.exit()


parser = argparse.ArgumentParser(description='Aggregate Eventbrite attendee data by promotional code')
parser.add_argument('event_id', help='ID of the Eventbrite event')
parser.add_argument('eventbrite_token', help='Eventbrite API token')
parser.add_argument('discord_token', help='Discord API token')
args = parser.parse_args()

this_week_sales,total_sales = get_attendees(args.event_id, args.eventbrite_token)

print(this_week_sales)
print(total_sales)

client.run(args.discord_token)
