# face detection and image extraction to text


from zipfile import ZipFile
from IPython.display import display
import PIL
import datetime
import sys

from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
word = input('Enter word search: ')
word = word.lower()
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
THUMB_SIZE = (100,100)

file_name = 'readonly/small_img.zip'
with ZipFile(file_name, 'r') as zip:
    for file in zip.infolist():
        clean_text = ''

       
        with zip.open(file) as png_file:
            img = Image.open(png_file)

            text = pytesseract.image_to_string(img)
            for char in text:
                if char not in punctuation:
                    clean_text = clean_text + char
                text = clean_text.lower()

            if word in text:
                print("Results found in file "  + file.filename)
                gray = cv.cvtColor(np.asarray(img), cv.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)
                pil_img = Image.fromarray(gray, mode="L")
                drawing = ImageDraw.Draw(pil_img)
                print(len(faces))
                contact_sheet = PIL.Image.new(img.mode, (THUMB_SIZE[0] * 5, THUMB_SIZE[1] * 2))
        
                box_x=0
                box_y=0
                
                for x,y,w,h in faces:
                    cropped_img = pil_img.crop((x,y,x+w,y+h))
                    cropped_img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
                     
                    contact_sheet.paste(cropped_img, (box_x,box_y))
                    if box_x + cropped_img.width == contact_sheet.width:
                        box_x = 0
                        box_y = box_y + cropped_img.height
                    else:
                        box_x = box_x + cropped_img.width
                    print(box_x,box_y)
               # contact_sheet = contact_sheet.resize((int(contact_sheet.width), int(contact_sheet.height/2)))
                print(contact_sheet.width)
                print(contact_sheet.height)
                display(contact_sheet)

#        break
