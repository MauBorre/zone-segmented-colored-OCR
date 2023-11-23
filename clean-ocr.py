import cv2
import numpy as np
import imutils
import pytesseract
import tkinter as tk
from tkinter import scrolledtext


"""Rectangle drawing procedure"""
drawing = False
mode = True
initial_x, initial_y = 0,0
ultimate_x, ultimate_y = 0,0

def draw_rect(event,final_x,final_y,flags,param):

    global initial_x, initial_y, drawing, mode, ultimate_x, ultimate_y

    if event == cv2.EVENT_LBUTTONDOWN:
        """Rectangle start"""
        drawing = True
        initial_x,initial_y = final_x,final_y
    
    #TODO: be able to visualize the rectangle while we drag it
    
    #elif event == cv2.EVENT_MOUSEMOVE:
        #if drawing == True:
            #if mode == True:
                #cv2.rectangle(cache,(initial_x,initial_y),(final_x,final_y),(0,255,0), thickness=2)
                #a=final_x
                #b=final_y
                #if a != final_x | b != final_y: # Es el interior del rectangulo
                    # "transparentar"
                    # cv2.rectangle(img,(initial_x,initial_y),(final_x,final_y),(), -1)
    
    elif event == cv2.EVENT_LBUTTONUP:
        """Rectangle finish"""
        drawing = False
        if mode == True:
            cv2.rectangle(img_resize,(initial_x,initial_y),(final_x,final_y),(255,255,50), thickness=2)
            ultimate_x, ultimate_y = final_x, final_y
            print(f"Initial points: {initial_x},{initial_y}")
            print(f"Final points: {ultimate_x},{ultimate_y}")


"""Image path and resizing utility"""
img_path = "./image.jpg"
cv2.namedWindow('image')
img = cv2.imread(img_path)
img_resize = imutils.resize(img, height=1000)
y=0
x=0

"""Canvas for overlay. Unused yet"""
canvas = np.zeros_like(img_resize, dtype=np.uint8)
canvas.fill(255)

"""TKinter init"""
root = tk.Tk()
def close_window(event=None):
    root.destroy()
root.bind('<Escape>', close_window)
text_widget = scrolledtext.ScrolledText(root)
text_widget.pack()

"""Necessary tesseract config"""
# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def main_loop():

    while(1):

        cv2.setMouseCallback('image', draw_rect)
        cv2.imshow('image',img_resize)
        k = cv2.waitKey(1) & 0xFF

        if k == 27: # ESCAPE KEY
            break

        if k == 13: # ENTER KEY
            print("OCR'ing...")
            try:
                cropImg = img_resize[initial_y:y+ultimate_y, initial_x:x+ultimate_x]
                text = pytesseract.image_to_string(cropImg)
                text_widget.insert(tk.END, text)
                root.mainloop()
                
            except:
                text = pytesseract.image_to_string(img_resize)
                text_widget.insert(tk.END, text)
                root.mainloop()
                
            # start_clean_again()

        if k == 8: # BACKSPACE KEY
            print("returning...")
            # TODO: erease the rectangle or restart
            #main_loop()
            

main_loop()
cv2.destroyAllWindows()

"""
Might be useful later on...
if k == 32: # SPACE BAR KEY
if k == 13: # ENTER KEY
if k == 8: # RETURN KEY
"""
