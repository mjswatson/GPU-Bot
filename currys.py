max_price=800
max_time=5
min_price=600
wait_time=15
dont_use_manufacturer=['pny']
email='michaeljswatson@yahoo.co.uk'
password='Shite1234'
postcode='Claines'
card_no=5352550117023017
name='Michael J S Watson'
month='07'
year=22
code=975

import requests
import json
import pyautogui
import pynput
import cv2
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller
from functions import *
from random import randrange
from random import random
keyboard=Controller()

'set up browser'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
browser = webdriver.Chrome(chrome_options=options)
browser.get("https://www.google.com")
wait_time_base=wait_time
not_bought=True
refreshes=0
found=0
refresh_fast=0
breaking=False
while not_bought:
    unneeded=False
    
    if breaking:
        'if has had to break restart browser to clear anything from old loop'
        browser.close()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(chrome_options=options)
        browser.get("https://www.google.com")

    breaking=False
    'check for stock'
    url = "https://www.currys.co.uk/gbuk/rtx-3080/components-upgrades/graphics-cards/324_3091_30343_xx_ba00013562-bv00313767/xx-criteria.html"
    payload = {}
    headers = {
      'Cookie': 'TS01e1f0f7=01dec1a268e5c03dfb4ea87e9a11a9d6dafd636390d381fbd4401d0de9c0bfd6e13bf8235ab3cf02aa3c0704bb8ac7defd5c280053'
    }
    while True:
        try:
            response = requests.request("GET", url, headers=headers, data = payload)
            break
        except:
            time.sleep(20)
        
    location=response.text.find("homeDeliveryAvailable")
    refreshes=refreshes+1
    
    'process results'
    if response.text.find('homeDeliveryUnavailable')<0 and location<0:
        'strange results so load page and process'
        address=queue_buster(dont_use_manufacturer,max_price,min_price,url,browser)
        #wait_time=1
        refresh_fast=refreshes
    elif location>0:
        'normal but found'
        address=text_process(response.text,dont_use_manufacturer,max_price,min_price,location)
    else:
        'nothing found and normal'
        wait_time=wait_time_base
        address='non available'

    if refreshes>refresh_fast+20:
        wait_time=wait_time_base
    
    if address!='non available':
        found=found+1
        pushbullet_message('Available!!', address)
        
        'using html add product to basket and navigate to basket'
        browser.get(address)
        start_time=float(time.perf_counter())
        'deal with cookies pop up if there'
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
                if i==10:
                    break
        
        'wake screen up'
        pyautogui.keyDown('w')
        pyautogui.keyUp('w')
        maximise_window('Chrome')
        'add to basket from image of button'
        add_basket_loc=pyautogui.locateCenterOnScreen('basket_button.JPG',confidence=0.75)
        'if image not found scroll down and try again until found'
        while add_basket_loc==None:
            keyboard.press(Key.page_down)
            time.sleep(1)
            add_basket_loc=pyautogui.locateCenterOnScreen('basket_button.JPG',confidence=0.75)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
            browser.refresh()
            add_basket_loc=pyautogui.locateCenterOnScreen('basket_button.JPG',confidence=0.75)

        if breaking:
            continue
        
        pyautogui.moveTo(add_basket_loc.x,add_basket_loc.y)
        pyautogui.click()
        
        'continue to basket'
        goto_basket_loc=pyautogui.locateCenterOnScreen('continue_to_basket.JPG',confidence=0.75)
        while goto_basket_loc==None:
            goto_basket_loc=pyautogui.locateCenterOnScreen('continue_to_basket.JPG',confidence=0.75)
            if pyautogui.locateCenterOnScreen('goto checkout.JPG',confidence=0.9)!=None:
                unneeded=True
                break
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if not unneeded and goto_basket_loc!=None:
            pyautogui.moveTo(goto_basket_loc.x,goto_basket_loc.y)
            pyautogui.click()
        elif not unneeded and goto_basket_loc==None:
            browser.refresh()

        if breaking:
            continue

        time.sleep(1)
        goto_basket_loc=pyautogui.locateCenterOnScreen('continue_to_basket.JPG',confidence=0.75)
        while goto_basket_loc!=None:
            goto_basket_loc=pyautogui.locateCenterOnScreen('continue_to_basket.JPG',confidence=0.75)
            'wiggle mouse randomly'
            x_go=randrange(1920)
            y_go=randrange(1080)
            pyautogui.moveTo(x_go,y_go)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
        'go to checkout'
        time.sleep(2)
        goto_checkout_loc=pyautogui.locateCenterOnScreen('goto checkout.JPG',confidence=0.9)
        while goto_checkout_loc==None:
            goto_checkout_loc=pyautogui.locateCenterOnScreen('goto checkout.JPG',confidence=0.9)

            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
        pyautogui.moveTo(goto_checkout_loc.x,goto_checkout_loc.y)
        pyautogui.click()
        
        'input postcode'
        goto_postcode_loc=pyautogui.locateCenterOnScreen('postcode.JPG',confidence=0.9)
        while goto_postcode_loc==None:
            goto_postcode_loc=pyautogui.locateCenterOnScreen('postcode.JPG',confidence=0.9)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
        pyautogui.moveTo(goto_postcode_loc.x,goto_postcode_loc.y)
        pyautogui.click()
        'send letters'
        pyautogui.write(postcode)
        time.sleep(1)
        keyboard.press(Key.enter)
        time.sleep(0.5)
        keyboard.press(Key.enter)
        'click location'
        #local=pyautogui.locateCenterOnScreen('Claines.JPG',confidence=0.9)
        #while local==None:
         #   local=pyautogui.locateCenterOnScreen('Claines.JPG',confidence=0.9)
          #  time1=time.perf_counter()
           # time1=float(time1)-start_time
            #if time1>max_time*60:
            #    breaking=True
            #    break
        #if breaking:
         #   continue
        #pyautogui.moveTo(local.x,local.y)
        #pyautogui.click()

        'select free delivery'
        time.sleep(1)
        goto_delivery_loc=pyautogui.locateCenterOnScreen('free delivery.JPG',confidence=0.8)
        i=0
        while goto_delivery_loc==None:
            i=i+1
            goto_delivery_loc=pyautogui.locateCenterOnScreen('free delivery.JPG',confidence=0.8)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
            if i==10:
              keyboard.press(Key.enter)
              
        pyautogui.moveTo(goto_delivery_loc.x,goto_delivery_loc.y)
        pyautogui.click()

        'log in'
        'email'
        time.sleep(1)
        i=0
        goto_email_loc=pyautogui.locateCenterOnScreen('email_enter.JPG',confidence=0.9)
        while goto_email_loc==None:
            i=i+1
            goto_email_loc=pyautogui.locateCenterOnScreen('email_enter.JPG',confidence=0.9)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
            if (i/5).is_integer():
                goto_delivery_loc=pyautogui.locateCenterOnScreen('free delivery.JPG',confidence=0.8)
                if goto_delivery_loc!=None:
                    pyautogui.moveTo(goto_delivery_loc.x,goto_delivery_loc.y)
                    pyautogui.click()
                    time.sleep(1)
        if breaking:
            continue    
        pyautogui.moveTo(goto_email_loc.x,goto_email_loc.y)
        pyautogui.click()
        pyautogui.write(email)
        keyboard.press(Key.enter)
        keyboard.press(Key.enter)
        'password'
        time.sleep(1)
        i=0
        goto_password_loc=pyautogui.locateCenterOnScreen('password_enter.JPG',confidence=0.9)
        while goto_password_loc==None:
            i=i+1
            print(i)
            goto_password_loc=pyautogui.locateCenterOnScreen('password_enter.JPG',confidence=0.9)
            if i>20:
                keyboard.press(Key.enter)
            
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
            if (i/5).is_integer():
                goto_email_loc=pyautogui.locateCenterOnScreen('email_enter.JPG',confidence=0.9)
                if goto_email_loc!=None:
                    pyautogui.moveTo(goto_email_loc.x,goto_email_loc.y)
                    pyautogui.click()
                    pyautogui.write(email)
                    keyboard.press(Key.enter)
        if breaking:
            continue        
        pyautogui.moveTo(goto_password_loc.x,goto_password_loc.y)
        pyautogui.click()
        pyautogui.write(password,interval=0.025)
        keyboard.press(Key.enter)
        print('selecting payment')

        'select payment method'
        time.sleep(2)
        goto_card_loc=pyautogui.locateCenterOnScreen('card_button.JPG',confidence=0.9)
        while goto_card_loc==None:
            goto_card_loc=pyautogui.locateCenterOnScreen('card_button.JPG',confidence=0.9)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
        pyautogui.moveTo(goto_card_loc.x,goto_card_loc.y)
        pyautogui.click()

        'wait until page loaded'
        i=0
        check_load=pyautogui.locateCenterOnScreen('card_input_loaded.JPG',confidence=0.9)
        while check_load==None:
            i=i+1
            check_load=pyautogui.locateCenterOnScreen('card_input_loaded.JPG',confidence=0.9)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
            if (i/5).is_integer():
                goto_card_loc=pyautogui.locateCenterOnScreen('card_button.JPG',confidence=0.9)
                if goto_card_loc!=None:
                    pyautogui.moveTo(goto_card_loc.x,goto_card_loc.y)
                    pyautogui.click()
        if breaking:
            continue            
        time1=time.perf_counter()
        time1=float(time1)-start_time
        if time1<=max_time*60:
            'fill in card details'
            card_number=browser.find_element_by_id('cardNumber')
            card_number.send_keys(card_no)
            card_name=browser.find_element_by_id('cardholderName')
            card_name.send_keys(name)
            expiry_month=browser.find_element_by_id('expiryMonth')
            expiry_month.send_keys(month)
            expiry_year=browser.find_element_by_id('expiryYear')
            expiry_year.send_keys(year)        
            security=browser.find_element_by_id('securityCode')
            security.send_keys(code)        

        goto_checkout_loc=pyautogui.locateCenterOnScreen('pay.JPG',confidence=0.8)
        while goto_checkout_loc==None:
            goto_checkout_loc=pyautogui.locateCenterOnScreen('pay.JPG',confidence=0.8)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
        pyautogui.moveTo(goto_checkout_loc.x,goto_checkout_loc.y)
        'instert click here'
        
        time1=time.perf_counter()
        time1=float(time1)-start_time
        if time1<=max_time*60:
            not_bought=False
            body='Purchase sucessfully made, bot now closing down. Link: '+address
            pushbullet_message('Purchase Made', body)
    now=datetime.datetime.now()       
    time.sleep((0+randrange(0,wait_time))*random())
    print(refreshes,found,now)     


