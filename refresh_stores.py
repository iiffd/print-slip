import requests
import datetime


def refresh_stores():
    ''' Refreshes stores for shipstation api '''
    api_key = 'db35920edb384162bbecd52d40a7a781'
    api_secret = 'd6b01ee7d5074ce29243e9fd07c71763'

    store_ids = [222824, 222533, 251496, 246700, 230923]

    today = datetime.date.today()
    refresh_date = today.strftime('%m-%d-%Y')
    print refresh_date
    # Refreshes each store
    for store_id in store_ids:
        r = requests.post('https://ssapi.shipstation.com/stores/refreshstore?storeId='+str(store_id)+'&refreshDate='+refresh_date, auth=(api_key, api_secret))
        print r.json()


if __name__ == '__main__':
    refresh_stores()
