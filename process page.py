def queue_buster(bad_brand,max_price,min_price,address)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

    browser.get(address)
    price=browser.find_elements_by_class_name('amount')
    link=browser.find_elements_by_class_name('productTitle')
    avail=browser.find_elements_by_class_name('channels-availability')
    links_store=[]
    price_values=[]

    for element in price

        index=price.index(element)
        
        'check_if_available'
        available=avail[index].get_attribute('innerText')
        available=available.split('n\\')[0]
        deliverable=available.find('not')
        if deliverable>0:
            element.next()
            continue

            'process out brands'
        brand=link[index].get_attribute('innerText')
        brand=brand.split(" ")[0]
            if brand in bad_brand:
                element.next()
                continue

        'process price into float and skip if not too high'
        loc=element.text.find('Save')
        'remove save text'
        if loc>0
            price_use=element[:loc]
        price_use=price_use.replace('£','')
        price_use=float(price_use)
        if min_price<=price_use<=max_price:
            price_values.append(price_use)
        else
            element.next()
            continue

        'store product page'
        address=link[index].get_attribute('innerHTML')
        loc_start=address.find('href="')
        loc_end=address.find('"',loc_start,len(address))
        address=address[loc_start:loc_end]
        link_store.append(address)


    price_best=min(price_values)
    address_use=link_store[price_values.index(price_best)]

return address_use
    
def text_process(text,bad_brand,max_price,min_price,location)

    price_location=[]
    price_store=[]
    'get all prices and find the smallest'
    number_available=response.text.count("homeDeliveryAvailable")
    while count< number_available:
        count=count+1
        'get price to check'
        price_location1=(response.text.rfind('"price">',0,location))
        price_location2=response.text.find('£',price_location1,location)
        price_location.append(price_location2)
        price=response.text[price_location2+1:price_location2+6]
        price=price.replace(',','')
        price_store.append(float(price))
        location=response.text.find("homeDeliveryAvailable",location+len("homeDeliveryAvailable"))
        unacceptable=True
        'while there are items to check'
    while unacceptable:
        price_use=min(price_store)
        index=price_store.index(price_use)
        price_location1=price_location[index]
        'if within bounds get html to product'
        html_start=response.text.rfind('href="',0,price_location1)+6
        html_end=response.text.find('"',html_start,price_location1)
        address=response.text[html_start:html_end]
        'check if from a black list brand'
        for element in dont_use_manufacturer:
            if address.find(element)>0:
                price_store.remove(price_use)
                del price_location[index]
                price_use=max_price+1
                break
            if element==dont_use_manufacturer[len(dont_use_manufacturer)-1]:
                unacceptable=False

    return(







