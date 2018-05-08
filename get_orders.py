import requests


def get_orders_data():
    # Get's orders data from shipstation api
    api_key = 'db35920edb384162bbecd52d40a7a781'
    api_secret = 'd6b01ee7d5074ce29243e9fd07c71763'

    r = requests.get('https://ssapi.shipstation.com/orders?orderStatus=awaiting_shipment', auth=(api_key, api_secret))
    orders = r.json()

    orders_list = [order for order in orders['orders']]
    return orders_list


def get_active_stores():
    # Get's list of active stores from shipstation api
    api_key = 'db35920edb384162bbecd52d40a7a781'
    api_secret = 'd6b01ee7d5074ce29243e9fd07c71763'

    r = requests.get('https://ssapi.shipstation.com/stores?', auth=(api_key, api_secret))
    for store in r.json():
        print store


if __name__ == '__main__':
    get_orders_data()