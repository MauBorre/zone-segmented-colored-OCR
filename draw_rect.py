import cv2
import numpy as np
import imutils

class Rectangulo():
    pass

drawing = False
mode = True
initial_x, initial_y = -1,-1
ultimate_x, ultimate_y = 0,0
descartable = Rectangulo

def draw_rect(event,final_x,final_y,flags,param):
    """
    debemos capturar las coordenadas dibujadas y aplicar:
    cropImg = rightImg[y:x, y+h:x+w]
    """
    #global initial_x, initial_y, drawing, mode, cache
    global initial_x, initial_y, drawing, mode, ultimate_x, ultimate_y

    if event == cv2.EVENT_LBUTTONDOWN:
        # guardar inicio de rectangulo
        drawing = True
        initial_x,initial_y = final_x,final_y
    
    
    #Todo esto podria servir para "previsualizar" el rectangulo antes de soltarlo
    #Pero como que no funciona muy bien...
    
    #elif event == cv2.EVENT_MOUSEMOVE:
        # incrementar "fin" de rectangulo
        #if drawing == True:
            #if mode == True:
                # Rectangulo feed
                #cv2.rectangle(cache,(initial_x,initial_y),(final_x,final_y),(0,255,0), thickness=2)
                #a=final_x
                #b=final_y
                #if a != final_x | b != final_y: # Es el interior del rectangulo
                    # "transparentar"
                    #cv2.rectangle(img,(initial_x,initial_y),(final_x,final_y),(), -1)
    
    elif event == cv2.EVENT_LBUTTONUP:
        # El rectangulo termino
        drawing = False
        if mode == True:
            #del descartable
            cv2.rectangle(img_resize,(initial_x,initial_y),(final_x,final_y),(255,255,50), thickness=2) # CAPTURA FINAL
            ultimate_x, ultimate_y = final_x, final_y
            print(f"Initial points: {initial_x},{initial_y}")
            print(f"Final points: {ultimate_x},{ultimate_y}")
        
    
canvas = np.zeros((512,512,1), dtype=np.uint8) # <- CANVAS
canvas.fill(255)
img_path = "./image.jpg"
img = cv2.imread(img_path)

cv2.namedWindow('image')
img_resize = imutils.resize(img, height=950)


#final_img = cv2.addWeighted(img, 0.4, canvas, 0.1,0)
#cache = img.copy()
y=0
x=0
h=ultimate_y
w=ultimate_x
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

