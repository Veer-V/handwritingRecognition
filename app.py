import pygame
import sys
from pygame.locals import *
from keras.models import load_model
import cv2
import numpy as np
WINDOWSIZEX = 640
WINDOWSIZEY = 480
BOUNDRYINC = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


IMAGESAVE = False

MODEL = load_model("bestmodel.h5")

LABELS ={0:"Zero",1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven",8:"Eight", 9:"Nine"}

# initialize our pygame
pygame.init()
FONT = pygame.font.Font("freesansbold.ttf", 18)
DISPLAYSURFACE = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))

#WHILE_INT = DISPLAYURF.mp_rgb(WHITE)
pygame.display.set_caption("Digit Board")

iswriting = False

number_xcord = []
number_ycord = []
imag_cnt =  1
PREDICT = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting:
            xcord, ycode = event.pos
            pygame.draw.circle(DISPLAYSURFACE, WHITE, (xcord, ycode),4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycode)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)

            rect_min_y = number_ycord[0] - BOUNDRYINC
            rect_max_y = min(number_ycord[-1] + BOUNDRYINC, WINDOWSIZEY)


            rect_min_x, rect_max_x = max(number_xcord[0]-BOUNDRYINC, 0), min(WINDOWSIZEX, number_xcord[-1]+BOUNDRYINC)
            #rect_min_y, rect_max_y = max(number_ycord[0]-BOUNDRYINC), min(number_ycord[-1]+BOUNDRYINC, WINDOWSIZEY)

            number_xcord = []
            number_ycord = []

            img_arr = np.array(pygame.PixelArray(DISPLAYSURFACE))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)


            #img_arr = np.array(pygame.PixelArray(DISPLAYSURFACE))[rect_min_x:rect_min_x,rect_min_y:rect_max_y].T.astype(np.float32)

            if IMAGESAVE:
                cv2.imwrite("image.png")
                imag_cnt +=1

            if PREDICT:
                image = cv2.resize(img_arr, (28, 28))
                image = np.pad(image,(10,10),'constant', constant_values = 0 )
                image = cv2.resize(image, (28, 28) )/255

                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])

                textSurface = FONT.render(label, True, RED,  WHITE)
                textRecobj = textSurface.get_rect()
                textRecobj.left , textRecobj.bottom = rect_min_x, rect_max_y

                DISPLAYSURFACE.blit(textSurface, textRecobj)

            if event.type == KEYDOWN:
                if event.unicode == "n":
                    DISPLAYSURFACE.fill(BLACK)

        pygame.display.update()