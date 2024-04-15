import argparse
import requests
from collections import defaultdict
from datetime import datetime, timedelta

def get_eventbrite_attendees(event_id, token):
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/attendees/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    attendees = []
    page = 1
    
    while True:
        params = {
            "page": page,
            "expand": "promotional_code"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        attendees.extend(data["attendees"])
        
        if data["pagination"]["has_more_items"]:
            page += 1
        else:
            break
    
    return attendees
    
def aggregate_attendees(attendees):
    promo_code_data = defaultdict(lambda: {'total_sold': 0, 'last_week_sold': 0})
    total_tickets_sold = 0
    tickets_sold_today = 0

    for attendee in attendees:
        promo_code = attendee.get("promotional_code", {}).get("code", "No Promo Code")

        promo_code_data[promo_code]['total_sold'] += 1
        total_tickets_sold += 1

        order_date = datetime.strptime(attendee["created"], "%Y-%m-%dT%H:%M:%SZ")
        if order_date >= datetime.now() - timedelta(days=7):
            promo_code_data[promo_code]['last_week_sold'] += 1

        if order_date.date() == datetime.now().date():
            tickets_sold_today += 1

    return promo_code_data, total_tickets_sold, tickets_sold_today

def main():
    parser = argparse.ArgumentParser(description='Aggregate Eventbrite attendee data by promotional code')
    parser.add_argument('event_id', help='ID of the Eventbrite event')
    parser.add_argument('token', help='Eventbrite API token')
    args = parser.parse_args()

    attendees = get_eventbrite_attendees(args.event_id, args.token)
    aggregated_data, total_tickets_sold, tickets_sold_today = aggregate_attendees(attendees)

    sorted_data = sorted(aggregated_data.items(), key=lambda x: x[1]['total_sold'], reverse=True)

    print(f"Tickets sold today: {tickets_sold_today}")
    print(f"Total tickets sold: {total_tickets_sold}\n")

    print("{:<30} | {:<10} | {:<15}".format("Promo Code", "Total Sold", "Last Week Change"))
    print("-" * 60)
    for promo_code, data in sorted_data:
        print("{:<30} | {:<10} | {:<15}".format(promo_code, data['total_sold'], data['last_week_sold']))

if __name__ == '__main__':
    main()

