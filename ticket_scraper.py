import argparse
import requests
from collections import defaultdict
from datetime import datetime, timedelta

this_week_sales = {'total': 0}
total_sales = {'total': 0}

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
      promo_code = attendee["promotional_code"]["code"]
      order_date = datetime.strptime(attendee["created"], "%Y-%m-%dT%H:%M:%SZ")
      if order_date >= datetime.now() - timedelta(days=7):
        sold_this_week = True
      
      total_sales['total'] += 1
      if promo_code in total_sales:
        total_sales[promo_code] += 1
      else:
        total_sales[promo_code] = 1

      if sold_this_week:
         this_week_sales['total'] += 1
         if promo_code in this_week_sales:
           this_week_sales[promo_code] += 1
         else:
           this_week_sales[promo_code] = 1
       
    
    if data["pagination"]["has_more_items"]:
      page += 1
    else:
      break

  print(this_week_sales)
  print(total_sales)

def main():
  parser = argparse.ArgumentParser(description='Aggregate Eventbrite attendee data by promotional code')
  parser.add_argument('event_id', help='ID of the Eventbrite event')
  parser.add_argument('token', help='Eventbrite API token')
  args = parser.parse_args()

  get_attendees(args.event_id, args.token)


#TODO: make sure it mails on error/or maybe pings on discord
if __name__ == '__main__':
  main()

