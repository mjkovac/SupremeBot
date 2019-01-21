import datetime
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from Keys import pages, products


class Product:
    colour = ''
    name = ''
    size = ''
    link = ''

    def print_obj(self):
        print('=====')
        print('Color: ', self.colour)
        print('Name: ', self.name)
        print('Size: ', self.size)
        print('Link: ', self.link)
        print('=====', '\n')


def find_product(element):
    try:
        for page in pages:
            if page is products[element]['category']:
                req = requests.get(pages[page]).text
                soup = BeautifulSoup(req, 'html.parser')

                arr = []
                for div in soup.find_all('div', 'turbolink_scroller'):
                    for a in div.find_all('a', href=True, text=True):
                        new_product = None

                        if products[element]['name'] in a.text:
                            new_product = Product()
                            new_product.name = a.text
                            new_product.link = a['href']
                            arr.append(new_product)

                            if products[element]['colour'] is None:
                                return new_product

                        if products[element]['colour'] is not None:
                            for item in arr:
                                if item.link == a['href'] and a.text == products[element]['colour']:
                                    item.colour = a.text
                                    return item

    finally:
        print('find items end')
    return new_product


def order():
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome('./chromedriver', chrome_options=option)
    # driver.get('https://google.ca')

    # find all the items on the page and select the product
    start_time = datetime.datetime.now()
    print(start_time)
    for item in products:
        find_time = datetime.datetime.now()
        product = find_product(item)

        if product is not None:
            end_time = datetime.datetime.now()
            print('time to find product ', end_time - find_time)
            product.print_obj()
            driver.get(pages['base_url'] + product.link)
            try:
                # click the add to cart button
                driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()

                # click checkout button
                driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
            finally:
                print('added to cart and at checkout')
        else:
            print('didnt find product')

    #
    # # requests.post('ujs:submit-button', )
    # # fill form data
    # driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(user['name'])
    # driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(user['email'])
    # driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(user['tel'])
    # driver.find_element_by_xpath('//*[@id="bo"]').send_keys(user['address'])
    # driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(user['zip'])
    # driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(user['city'])

    if start_time < datetime.datetime.now():
        # print(datetime.datetime.now() - start_time)
        print('it took the webpage', datetime.datetime.now() - start_time, 'time to open')

    time.sleep(1)
    print('finished program')


if __name__ == '__main__':
    order()
