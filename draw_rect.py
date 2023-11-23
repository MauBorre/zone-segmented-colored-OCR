import cv2
import numpy as np
import imutils


drawing = False
mode = True
initial_x, initial_y = -1,-1
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
                # Rectangulo feed
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
            cv2.rectangle(img_resize,(initial_x,initial_y),(final_x,final_y),(255,255,50), thickness=2) # CAPTURA FINAL
            ultimate_x, ultimate_y = final_x, final_y
            print(f"Initial points: {initial_x},{initial_y}")
            print(f"Final points: {ultimate_x},{ultimate_y}")
        
"""Unused canvas for now"""
canvas = np.zeros((512,512,1), dtype=np.uint8) # <- CANVAS
canvas.fill(255)

"""Image path and resizing utility"""
img_path = "./image.jpg"
img = cv2.imread(img_path)
img_resize = imutils.resize(img, height=950)
cv2.namedWindow('image')
y=0
x=0

while(1):

    cv2.setMouseCallback('image', draw_rect)
    cv2.imshow('image',img_resize)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: # ESCAPE KEY
        break
    if k == 32: # SPACE BAR KEY
        print("cutting...")
        cropImg = img_resize[initial_y:y+ultimate_y, initial_x:x+ultimate_x]
        cv2.imshow("cropped", cropImg)

cv2.destroyAllWindows()
