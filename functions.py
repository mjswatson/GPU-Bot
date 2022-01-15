def pushbullet_message(title, body):
    import requests
    import json
    msg = {"type": "note", "title": title, "body": body}
    TOKEN = 'o.93prO6fn0Qm0lZ27bT1YxhhrPaCvhAme'
    resp = requests.post('https://api.pushbullet.com/v2/pushes', 
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error',resp.status_code)
    else:
        print ('Message sent')

def queue_buster(bad_brand,max_price,min_price,address,browser):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    import pyautogui
    import time

    browser.get(address)
    'deal with cookies popup if there'
    i=0
    cookies=browser.find_elements_by_id('onetrust-accept-btn-handler')
    if cookies!=[]:
        browser.find_element_by_id('onetrust-accept-btn-handler').click()
    else:
        while cookies==[]:
            i=i+1
            cookies=browser.find_elements_by_id('onetrust-accept-btn-handler')
            if cookies!=[]:
                browser.find_element_by_id('onetrust-accept-btn-handler').click()
            if i==15:
                break
    maximise_window('Chrome')
        
    'process page data'
    price=browser.find_elements_by_class_name('amounts')
    link=browser.find_elements_by_class_name('productTitle')
    avail=browser.find_elements_by_class_name('channels-availability')
    links_store=[]
    price_values=[]
    
    for element in price:

        index=price.index(element)
        
        'check_if_available'
        available=avail[index].get_attribute('innerText')
        available=available.split('\n')[0]
        available=available.lower()
        deliverable=available.find('not')
        if deliverable>=0:
            continue

            'process out brands'
        brand=link[index].get_attribute('innerText')
        brand=brand.split(" ")[0]
        if brand in bad_brand:
            continue

        'process price into float and skip if not too high'
        loc=element.text.find('£')
        'remove save text'
        loc2=element.text.find('.',loc)
        price_use=element.text[loc+1:loc2+2]
        if price_use=="":
            price_use='0'
        price_use=price_use.replace('£','')
        price_use=float(price_use.replace(',',''))
        if min_price<=price_use<=max_price:
            price_values.append(price_use)
        else:
            continue

        'store product page'
        address=link[index].get_attribute('innerHTML')
        loc_start=address.find('href="')+len('href="')
        loc_end=address.find('"',loc_start,len(address))
        address=address[loc_start:loc_end]
        links_store.append(address)
    if price_values==[]:
        address_use='non available'
    else:   
        price_best=min(price_values)
        print(price_values)
        address_use=links_store[price_values.index(price_best)]
    
    return(address_use)
    

def text_process(text,bad_brand,max_price,min_price,location):

    price_location=[]
    price_store=[]
    address_store=[]
    'get all prices and find the smallest'
    number_available=text.count('isHomeDelivery":true')
    if number_available==0:
        address='non available'
    else:
        count=0
        while count< number_available:
            count=count+1
            'get price to check'
            price_location1=(text.rfind('"price">',0,location))
            price_location2=text.find('£',price_location1,location)
            price=text[price_location2+1:price_location2+6]
            price=float(price.replace(',',''))
            location=text.find('isHomeDelivery":true',location+len('isHomeDelivery":true'))
            if min_price<=price<=max_price:
                price_store.append(price)
                price_location.append(price_location2)
            
        unacceptable=True
        'while there are items to check'
        while unacceptable:
            if price_store==[]:
                address='non available'
                break
            price_use=min(price_store)
            index=price_store.index(price_use)
            price_location1=price_location[index]
            'if within bounds get html to product'
            html_start=text.rfind('href="',0,price_location1)+len('href="')
            html_end=text.find('"',html_start,price_location1)
            address=text[html_start:html_end]
            'check if from a black list brand'
            if bad_brand!=[]:
                for element in bad_brand:
                    if address.find(element)>0:
                        price_store.remove(price_use)
                        del price_location[index]
                        price_use=max_price+1
                        break
                    if element==bad_brand[len(bad_brand)-1]:
                        unacceptable=False
            else:
                unacceptable=False

    return(address)

def maximise_window(name):
    import pygetwindow
    a=pygetwindow.getAllTitles()
    for x in a:
            there=x.find(name)
            if there>0:
                    break
    chrome = pygetwindow.getWindowsWithTitle(x)[0]
    chrome.restore()
    chrome.maximize()


def check_ccl():
    import requests
    start_url='https://www.cclonline.com'
    url2 = "https://www.cclonline.com/category/401/PC-Components/CPU-Processors/Intel-Processors/"
    payload={}
    headers = {
  'Cookie': '__cfduid=df1c8835ce72a01ad0cb026a74c06bbcd1608591631; ASP.NET_SessionId=t5heleeuv5ba4vwmu4u53kgu'
}

    response = requests.request("GET", url2, headers=headers, data=payload)

    is_there=response.text.count('AddToBasket')
    print(is_there)
    if is_there>0:
        i=0
        loc=0
        while i<is_there:
            loc=response.text.find('AddToBasket',loc,len(response.text))
            address_start=response.text.rfind('href',0,loc)+len('href="')
            address_end=end_address=response.text.find('">',address_start)-len('#bundles')
            url=response.text[address_start:end_address]
            url=start_url+url
            print(url)
            i=i+1
            loc=loc++len('AddToBasket')
            pushbullet_message('CCL Available!',url)
                
