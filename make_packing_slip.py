from get_orders import get_orders_data
import re
import datetime
import sqlite3


def convert_none(var):
    if var is None:
        return ''
    else:
        return var


# Get's orders from shipstation api
orders_data = get_orders_data()

# Get list of previous orders to avoid duplicate print jobs
conn = sqlite3.connect('orders.db')
cur = conn.cursor()
cur.execute('SELECT * FROM Orders')
order_table_data = cur.fetchall()
stored_order_ids = []

for order_id, print_date in order_table_data:
    print order_id, print_date
    stored_order_ids.append(order_id)

# Testing variables
recipient_name = 'test'
recipient_company = 'test'
recipient_address = 'test'
order_number = 'test'
order_date = 'test'
username = 'test'
ship_date = ''
notes_to_buyer = ''
shipping_paid = 'test'
tax_amount = ''
order_tital = ''


for order_data in orders_data:
    items_html = ''
    print_date = datetime.date.today().strftime('%m/%d/%y')
    order_id = order_data['orderId']
    #if order_id in

    order_number = order_data['orderNumber']

    # Format shipTo address for slip
    city = order_data['shipTo']['city']
    street1 = order_data['shipTo']['street1']
    state = order_data['shipTo']['state']
    postal_code = order_data['shipTo']['postalCode']

    recipient_name = convert_none(order_data['shipTo']['name'])
    recipient_company = convert_none(order_data['shipTo']['company'])
    recipient_address = street1+'<br>'+state+', '+postal_code
    username = convert_none(order_data['customerUsername'])

    # Need to ask if I should have ship date at all
    #ship_date = time.strftime("%x")
    tax_amount = '${:,.2f}'.format(order_data['taxAmount'])
    order_total = '${:,.2f}'.format(order_data['orderTotal'])
    shipping_paid = '${:,.2f}'.format(order_data['shippingAmount'])
    _order_date = re.sub('T(.*)', '', order_data['orderDate'])
    order_date = datetime.datetime.strptime(_order_date, '%Y-%m-%d').strftime('%m/%d/%y')
    customer_notes = convert_none(order_data['customerNotes'])
    item_cost_total = 0

    # Getting store id
    store_id = order_data['advancedOptions']['storeId']
    stores = {
    222824: 'bigcommerce',
    222533: 'amazon',
    251496: 'hawklighting',
    246700: 'ebay',
    230923: 'walmart'
    }

    # If hawklighting, change name
    company_name = ''
    #print order_number, store_id

    if stores[store_id] == 'hawklighting':
        company_name = 'Hawk Lighting'
    else:
        company_name = 'DLC Lights'

    #if order_number == '417':
    #    print order_data

    # Iterates through Items
    items = order_data['items']
    for item in items:
        item_option = ''
        sku = item['sku']
        unit_price = '${:,.2f}'.format(item['unitPrice'])
        quantity = item['quantity']
        item_title = item['name']
        extended_price = '${:,.2f}'.format(item['unitPrice'] * item['quantity'])
        item_cost_total+= (item['unitPrice'] * quantity)

        # In case a coupon is added, deduct from order Total
        if item['unitPrice'] < 0:
            order_total = '${:,.2f}'.format(order_data['orderTotal']+(item['unitPrice']*quantity))

        # Iterates over options set if there is any
        if len(item['options']) > 0:
            for option in item['options']:
                item_option = option['name'] + ': ' + option['value']

        item_html = """<tr>
            <td class="sku">"""+sku+"""</td>
            <td>"""+item_title+"""<br>"""+item_option+"""</td>
            <td align="right" class="price">"""+unit_price+"""</td>
            <td align="center">"""+str(quantity)+"""</td>
            <td align="right" class="price">"""+extended_price+"""</td>
        </tr>"""
        items_html+=item_html

    sub_total = '${:,.2f}'.format(item_cost_total)

    html_file = """
    <!DOCTYPE html>
    <html>
    <head>
      <link rel="stylesheet" href="styles.css" type="text/css" media="all">
    </head>
    <body>

      <table cellspacing="0" cellpadding="2" border="0" style="width: 100%">
        <thead>
          <tr>
            <th colspan="5">
              Packing Slip
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="2" style="width: 4.5in" class="store-info">
              <div class="company-name">
                """+company_name+"""</div>
                <div>
                  6301 Orangethorpe ave
                  <br>Buena Park, CA 90620</div>
                </td>

              </tr>
              <tr>
                <td style="height: 0.15in">
                </td>
              </tr>
              <tr>
                <td align="right" style="width: 1in">
                  <b>Ship To:</b>
                </td>
                <td style="width: 3.5in; font-size: 14px">
                  <div>""" + recipient_name + """</div>
                  <div>""" + recipient_company + """</div>
                  <div>""" + recipient_address + """</div>
                </td>
                <td style="width: 2.5in">
                  <table cellspacing="0" border="0" class="order-info">
                    <tr>
                      <td align="right" class="label first">
                        <strong>Order #: </strong>
                      </td>
                      <td>
                        """ + order_number + """
                      </td>
                    </tr>
                    <tr>
                      <td align="right" class="label">
                        <strong>Date: </strong>
                      </td>
                      <td>
                        """ + order_date + """
                      </td>
                    </tr>
                    <tr>
                      <td align="right" class="label">
                        <strong>User: </strong>
                      </td>
                      <td>
                        """ + username + """
                      </td>
                    </tr>
                    <tr>
                      <td align="right" class="label last">
                        <strong>Ship Date: </strong>
                      </td>
                      <td>
                        """ + ship_date + """
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>


              <tr>
                <th align="left" style="width:1.5in" class="sku">
                  Item
                </th>
                <th align="left">
                  Description
                </th>
                <th align="right" style="width:0.75in" class="price">
                  Price
                </th>
                <th align="center" style="width:0.75in">
                  Qty
                </th>
                <th align="right" style="width:0.75in" class="price">
                  Ext. Price
                </th>
              </tr>"""+ items_html +"""</tbody>
    		<table align="right">
              <tbody>
                <tr>
                  <td rowspan="4" class="notes" >
                    """ + notes_to_buyer + """
                  </td>
                  <td align="right" style="width:1in" class="label price">
                    <strong>Sub Total: </strong
                  </td>
                  <td style="width:0.75in" align="right" class="price">"""+sub_total+"""</td>
                </tr>
                <tr class="tax">
                  <td align="right" class="label price">
                    <strong>Tax: </strong>
                  </td>
                  <td style="width:0.75in" align="right" class="price"> """ + tax_amount + """</td>
                </tr>
                <tr>
                  <td align="right" class="label price">
                    <strong>Shipping: </strong>
                  </td>
                  <td style="width:0.75in" align="right" class="price">""" + shipping_paid + """</td>
                </tr>
                <tr>
                  <td align="right" class="label price">
                    <strong>Total: </strong>
                  </td>
                  <td style="width:0.75in" align="right" class="price">"""+order_total+"""</td>
                </tr>
              </tbody>
    		</table>
          </table>
          <p align="center" style="font-size:11px">"""+customer_notes+"""</p>


    </body>
    </html>
    """
    filename = 'packing_slips/' + order_number + '.html'

    with open(filename, 'w') as f:
        f.write(html_file)

    # Saves order_id to prevent duplicate packings slips from printing
    cur.execute('''INSERT OR IGNORE INTO Orders (order_id, print_date)
    VALUES ( ?, ? )''', ( order_id, print_date ) )
    conn.commit()

