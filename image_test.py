import pyautogui
import cv2

'go to checkout'
goto_checkout_loc=pyautogui.locateCenterOnScreen('loaded_page.JPG',confidence=0.95)
while goto_checkout_loc==None:
    goto_checkout_loc=pyautogui.locateCenterOnScreen('loaded_page.JPG',confidence=0.95)
    print(goto_checkout_loc)
pyautogui.moveTo(goto_checkout_loc.x,goto_checkout_loc.y+100)
