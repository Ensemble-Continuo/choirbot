# Forgive me what I do, for I am not a python developer

import discord
import os
import argparse
from ticket_stats import get_attendees
import sys 

# ID of channel to post to
channel_id = 1167171723058225212


intents = discord.Intents.default()
client = discord.Client(command_prefix="!", intents=intents)

@client.event
async def on_ready():
  print("Logged in!")
  await client.get_channel(channel_id).send(this_week_sales)
  
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
