def queue_buster(bad_brand,max_price,min_price,address,browser):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains

    browser.get(address)
    
    'process page data'
    price=browser.find_elements_by_class_name('amount')
    link=browser.find_elements_by_class_name('productTitle')
    avail=browser.find_elements_by_class_name('channels-availability')
    links_store=[]
    price_values=[]

    for element in price:

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
        if loc>0:
            price_use=element[:loc]
        price_use=price_use.replace('£','')
        price_use=float(price_use)
        if min_price<=price_use<=max_price:
            price_values.append(price_use)
        else:
            element.next()
            continue

        'store product page'
        address=link[index].get_attribute('innerHTML')
        loc_start=address.find('href="')
        loc_end=address.find('"',loc_start,len(address))
        address=address[loc_start:loc_end]
        link_store.append(address)

    if price_values==[]:
        address_use='non available'
        
    price_best=min(price_values)
    address_use=link_store[price_values.index(price_best)]

print(address_use)
    

