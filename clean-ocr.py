import cv2
import numpy as np
import imutils
import pytesseract
import tkinter as tk
from tkinter import scrolledtext
import sys

#TODO: be able to visualize the selection as we drag it
#TODO: accept path-to-image as script argument



class Rectangles:
    """Utility for multiple OCR reads"""

    drawn_rectangles = []

    def __init__(self, initial_x, initial_y, ultimate_x, ultimate_y):
        self.init_x = initial_x
        self.init_y = initial_y
        self.ult_x = ultimate_x
        self.ult_y = ultimate_y
        Rectangles.drawn_rectangles.append(self)
        print(f"drawn rectangles: {len(Rectangles.drawn_rectangles)}")

    @classmethod
    def clear(cls):
        cls.drawn_rectangles.clear()

"""Rectangle drawing pre-requisites"""
drawing = False
mode = True
initial_x, initial_y = 0,0
ultimate_x, ultimate_y = 0,0

"""Image path and resizing"""
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

"""Necessary tesseract config"""
# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def main_loop():

    Rectangles.clear() # Necessary for subsequent restarts.

    def draw_rect(event,final_x,final_y,flags,param):
        """We need this func inside the main_loop so we can restart in case of a wrongly drawn area"""

        global initial_x, initial_y, drawing, mode, ultimate_x, ultimate_y

        if event == cv2.EVENT_LBUTTONDOWN:
            """Rectangle start"""
            drawing = True
            initial_x,initial_y = final_x,final_y
        
        elif event == cv2.EVENT_LBUTTONUP:
            """Rectangle finish"""
            drawing = False
            if mode == True:
                cv2.rectangle(img_resize,(initial_x,initial_y),(final_x,final_y),(255,255,50), thickness=2)
                ultimate_x, ultimate_y = final_x, final_y
                print(
                    f"Initial points: {initial_x},{initial_y} ||"
                    f"Final points: {ultimate_x},{ultimate_y}")
                Rectangles(initial_x, initial_y, ultimate_x, ultimate_y)

    print("start")
    cv2.destroyAllWindows()
    cv2.namedWindow('image')
    img_resize = imutils.resize(img, height=1000)

    while(1):

        cv2.setMouseCallback('image', draw_rect)
        cv2.imshow('image',img_resize)
        k = cv2.waitKey(1) & 0xFF

        if k == 27: # ESCAPE KEY
            sys.exit()

        if k == 13: # ENTER KEY
            print("OCR'ing...")
            if len(Rectangles.drawn_rectangles) == 0:
                text_widget = scrolledtext.ScrolledText(root)
                text = pytesseract.image_to_string(img_resize)
                text_widget.insert(tk.END, text)
                
                #### COLOR
                for line_index, line in enumerate(text.splitlines()):
                    for letter_index, letter in enumerate(line):
                        if letter.isdigit():
                            start = f"{line_index + 1}.{letter_index}"
                            end = f"{line_index + 1}.{letter_index + 1}"
                            text_widget.tag_add("highlight_number", start, end)
                        
                        if letter == "$":
                            start = f"{line_index + 1}.{letter_index}"
                            end = f"{line_index + 1}.{letter_index + 1}"
                            text_widget.tag_add("highlight_$", start, end)

                        if not letter.isalpha():
                            start = f"{line_index + 1}.{letter_index}"
                            end = f"{line_index + 1}.{letter_index + 1}"
                            text_widget.tag_add("highlight", start, end)
                ####

                text_widget.tag_configure("highlight", foreground="red")
                text_widget.tag_configure("highlight_number", foreground="blue")
                text_widget.tag_configure("highlight_$", foreground="green")
                text_widget.pack()

            else:
                for rectangle in Rectangles.drawn_rectangles:
                    cropImg = img_resize[rectangle.init_y:y+rectangle.ult_y, rectangle.init_x:x+rectangle.ult_x]
                    text_widget = scrolledtext.ScrolledText(root, height=10)
                    text = pytesseract.image_to_string(cropImg)
                    text_widget.insert(tk.END, text)

                    #### COLOR
                    for line_index, line in enumerate(text.splitlines()):
                        for letter_index, letter in enumerate(line):
                            if letter.isdigit():
                                start = f"{line_index + 1}.{letter_index}"
                                end = f"{line_index + 1}.{letter_index + 1}"
                                text_widget.tag_add("highlight_number", start, end)
                            
                            if letter == "$":
                                start = f"{line_index + 1}.{letter_index}"
                                end = f"{line_index + 1}.{letter_index + 1}"
                                text_widget.tag_add("highlight_$", start, end)

                            if not letter.isalpha():
                                start = f"{line_index + 1}.{letter_index}"
                                end = f"{line_index + 1}.{letter_index + 1}"
                                text_widget.tag_add("highlight", start, end)
                    ####

                    text_widget.tag_configure("highlight", foreground="red")
                    text_widget.tag_configure("highlight_number", foreground="blue")
                    text_widget.tag_configure("highlight_$", foreground="green")
                    text_widget.pack()        

            root.mainloop()
            break

        if k == 8: # BACKSPACE KEY
            """Restart from clean image"""
            print("returning...")
            main_loop()
            break
            

main_loop()
cv2.destroyAllWindows()

"""
Might be useful later on...
if k == 32: # SPACE BAR KEY
if k == 13: # ENTER KEY
if k == 8: # RETURN KEY
"""
