max_price=830
max_time=5
min_price=600
wait_time=15
dont_use_manufacturer=['pny']
email=''
password=''
postcode=''
card_no=''
name=''
month='...'
year=''
code=''

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
from mss import mss
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

while not_bought:
    unneeded=False
    breaking=False
    'check for stock'
    url = "https://www.currys.co.uk/gbuk/4k-monitors/pc-monitors/pc-monitors/354_3057_30059_xx_ba00012894-bv00311096/xx-criteria.html"
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
        
    location=response.text.find('isHomeDelivery":true')
    refreshes=refreshes+1
    
    'process results'
    if response.text.find('"available":false')<0 and location<0:
        'strange results so load page and process'
        address=queue_buster(dont_use_manufacturer,max_price,min_price,url,browser)
        wait_time=1
        refresh_fast=refreshes
    elif location>0:
        'normal but found'
        address=text_process(response.text,dont_use_manufacturer,max_price,min_price,location)
    else:
        'nothing found and normal'
        wait_time=wait_time_base
        address='non available'

    if refreshes>refresh_fast+50:
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
        with mss() as sct:
            screen=sct.shot()
        add_basket_loc=pyautogui.locate('basket_button.JPG',screen,confidence=0.75)
        'if image not found scroll down and try again until found'
        while add_basket_loc==None:
            keyboard.press(Key.page_down)
            time.sleep(0.5)
            screen=sct.shot()
            add_basket_loc=pyautogui.locate('basket_button.JPG',screen,confidence=0.75)

        pyautogui.moveTo(add_basket_loc.left+(add_basket_loc.width/2),add_basket_loc.top+(add_basket_loc.height/2))
        pyautogui.click()

        screen=sct.shot()
        goto_basket_loc=pyautogui.locate('continue_to_basket.JPG',screen,confidence=0.75)
        while goto_basket_loc==None:
            screen=sct.shot()
            goto_basket_loc=pyautogui.locate('continue_to_basket.JPG',screen,confidence=0.75)
            goto_checkout_loc=pyautogui.locate('goto checkout.JPG',screen,confidence=0.9)
            if goto_checkout_loc!=None:
                unneeded=True
                break
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
            
        if not unneeded:
            ' if its needed then click it and find the next button'
            pyautogui.moveTo(goto_basket_loc.left+(goto_basket_loc.width/2),goto_basket_loc.top+(goto_basket_loc.height/2))
            pyautogui.click()

            screen=sct.shot()
            goto_checkout_loc=pyautogui.locate('goto checkout.JPG',screen,confidence=0.9)
            while goto_checkout_loc==None:
                screen=sct.shot()
                goto_checkout_loc=pyautogui.locate('goto checkout.JPG',screen,confidence=0.9)
                time1=time.perf_counter()
                time1=float(time1)-start_time
                if time1>max_time*60:
                    breaking=True
                    break

        'just click the next button'
        pyautogui.moveTo(goto_checkout_loc.left+(goto_checkout_loc.width/2),goto_checkout_loc.top+(goto_checkout_loc.height/2))
        pyautogui.click()
            
        
        'input postcode'
        loc=browser.find_element_by_id('delivery_location')
        loc.click()
        'send letters'
        pyautogui.write(postcode)
        'click location'
        screen=sct.shot()
        local=pyautogui.locate('Claines.JPG',screen,confidence=0.9)
        while local==None:
            screen=sct.shot()
            local=pyautogui.locate('Claines.JPG',screen,confidence=0.9)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
        if breaking:
            continue
        pyautogui.moveTo(local.left+(local.width/2),local.top+(local.height/2))
        pyautogui.click()

        'select free delivery'
        deliver=browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[3]/div[1]/button')
        deliver.click()

        'log in'
        'email'
        email_box=browser.find_element_by_name('email')
        email_box.send_keys(email)
        email_box.send_keys(Keys.ENTER)
        'password'
        pass_box=browser.find_element_by_name('password')
        pass_box.send_keys(password)
        pass_box.send_keys(Keys.ENTER)

        'select payment method'
        card=browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div/div[4]/div[2]/div[2]/div[2]/div[2]/div[1]/button')
        card.click()

        'wait until page loaded'
        i=0
        screen=sct.shot()
        check_load=pyautogui.locateCenterOnScreen('card_input_loaded.JPG',screen,confidence=0.9)
        while check_load==None:
            i=i+1
            screen=sct.shot()
            check_load=pyautogui.locateCenterOnScreen('card_input_loaded.JPG',screen,confidence=0.9)
            time1=time.perf_counter()
            time1=float(time1)-start_time
            if time1>max_time*60:
                breaking=True
                break
            if (i/5).is_integer():
                screen=sct.shot()
                goto_card_loc=pyautogui.locateCenterOnScreen('card_button.JPG',screen,confidence=0.9)
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


