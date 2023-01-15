# References:
# https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
# https://pyimagesearch.com/2021/08/30/detecting-and-ocring-digits-with-tesseract-and-python/
# https://www.ShellHacks.com


from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import pytesseract
import easyocr
import numpy as np
import cv2
import matplotlib.pyplot as plt
from selenium import webdriver
import calendar;
import time;
import pyautogui
import keyboard
import re #REGEX

# Counting thingy
import random
import numpy as np

# HTTP POST
import requests

# TELE
def send_to_telegram(message):

    apiToken = '5987706548:AAE89QD39pc_skzmSUYYTtGZg4xgcwQVSwc'
    chatID = '-877502094'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

arr = [0 for _ in range(21)]
chk_arr = [0 for _ in range(21)]
curr = 1 # curent tick
prev = 1 # last tick
mem = 1 # prev floor
counter = 0
offend = -1
flag = False # check if stop is same stop ('A'*5 = 'A'*n, n > 5)

# PyTesserect
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
image_path = r'C:\Users\tanhs\Workspace\Projects\PythonScripts\hackandroll\imgs\latest_img.png'

firstx = 0
firsty = 0
secx = 0
secy = 0

while True:  # making a loop
    if keyboard.is_pressed('1'):
        firstx = pyautogui.position()[0]
        firsty = pyautogui.position()[1]
        break
while True:  # making a loop
    if keyboard.is_pressed('2'):
        secx = pyautogui.position()[0]
        secy = pyautogui.position()[1]
        break
print(f"{firstx}, {firsty}, {secx}, {secy}")

while True:
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    im = pyautogui.screenshot()

    # Processing
    left = firstx
    top = firsty
    right = secx
    bottom = secy
    
    #Grayscale
    im = im.crop((left, top, right, bottom))
    im = im.convert('L')

    #Sharpened
    enhancer = ImageEnhance.Contrast(im) 
    im = enhancer.enhance(3)

    im = im.filter(ImageFilter.GaussianBlur(radius=2))
    im = im.filter(ImageFilter.SMOOTH_MORE)
    im = im.filter(ImageFilter.EDGE_ENHANCE)
    
    display(im)    
    
    # PYTESSERACT
    text = pytesseract.image_to_string(im, config='--psm 7 digits')
    print(f"text: {text}")
    if (text=="" or not any(c.isdigit() for c in text)):
        time.sleep(0.33)
        continue
    
    curr = int(re.findall("\d+", text)[0])
    print("Current Floor:", curr)
    if curr > 21:
        time.sleep(0.33)
        continue
        
    
    if prev == curr:
        counter += 1
    else:
        counter = 1
    if prev == curr and mem < curr and counter > 8:
        chk_arr[curr-1] = 1
        if flag == False and chk_arr[curr-2]==1:
            arr[curr-1] += 1
            arr[curr-2] += 1
            arr[0] = 0
            flag = True
    if prev != curr:
        mem = prev
        flag = False
        chk_arr[curr-3] = 0
    prev = curr
    print(arr)
    if max(arr) != 0:
        max_offending_floor = np.argmax(arr)+1
        print("Max Offending Floor:", max_offending_floor)
        if offend != max_offending_floor:
            r = requests.post('http://192.168.137.157:80/post', data="{'floor':"+str(max_offending_floor)+"}")
            print("POST SENT")
            send_to_telegram(f"OFFENDING FLOOR: {max_offending_floor}, NUMBER OF OFFENCES: {arr[max_offending_floor-1]}")
            print("TELEGRAM SENT")
            offend = max_offending_floor            
    time.sleep(0.33)
    

