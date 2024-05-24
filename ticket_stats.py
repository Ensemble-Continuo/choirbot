import argparse
import requests
from collections import defaultdict
from datetime import datetime, timedelta
import discord

sales = {'total': {'this_week': 0, 'all_time': 0}}

def get_attendees(event_id, token):
  url = f"https://www.eventbriteapi.com/v3/events/{event_id}/attendees/"
  headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }
  page = 1
  
  while True:
    params = {
      "page": page,
      "expand": "promotional_code"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    
    for attendee in data["attendees"]:
      promo_code = ''
      sold_this_week = False
      promo_code = '(None)'

      if "promotional_code" in attendee and attendee["promotional_code"] is not None:
          promo_code = attendee["promotional_code"]["code"]
      order_date = datetime.strptime(attendee["created"], "%Y-%m-%dT%H:%M:%SZ")
      if order_date >= datetime.now() - timedelta(days=7):
        sold_this_week = True
      
      sales['total']['all_time'] += 1
      if promo_code in sales:
        sales[promo_code]['all_time'] += 1
      else:
        sales[promo_code] = {'all_time': 1, 'this_week': 0}

      if sold_this_week:
         sales['total']['this_week'] += 1
         sales[promo_code]['this_week'] += 1
       
    
    if data["pagination"]["has_more_items"]:
      page += 1
    else:
      break
  
  return sales

