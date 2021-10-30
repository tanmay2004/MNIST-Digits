# https://www.geeksforgeeks.org/ocr-of-handwritten-digits-opencv/

import numpy as np
import pygame, cv2, sys
from pygame.locals import *
from PIL import Image

# Read the image
image = cv2.imread('digits.png')

# gray scale conversion
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

# We will divide the image into 5000 small dimensions of size 20x20 
divisions = list(np.hsplit(i,100) for i in np.vsplit(gray_img,50)) 
NP_array = np.array(divisions)

# Preparing train_data
train_data = NP_array.reshape(-1,400).astype(np.float32) 

# Create 10 different labels for each type of digit 
k = np.arange(10)
train_labels = np.repeat(k,500)[:,np.newaxis]

# Initiate kNN classifier and train it
knn = cv2.ml.KNearest_create()
knn.train(train_data, cv2.ml.ROW_SAMPLE, train_labels)


def get_resize_arr(sc):
    img = Image.fromarray(sc)
    img.thumbnail((20, 20))
    img = img.rotate(90, expand=True)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    # img.show() # Invalid Registry Error
    np_arr_sc = np.array(img)
    return np_arr_sc.reshape(1, 400).astype(np.float32)


def get_digit(screen):
    arr_sc = pygame.surfarray.array2d(screen)
    reshaped_arr = get_resize_arr(arr_sc)
    
    ret, output, neighbours, distance = knn.findNearest(reshaped_arr, k = 5)
    print("The AI guesses your number as:", int(output[0][0]))
    
    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    WIDTH = 1 # Subject to Change

    screen = pygame.display.set_mode((400, 400), 0, 32)
    pygame.display.set_caption("Handwritten Digit Recognition!")
    screen.fill(BLACK)

    mouse_position = (0, 0)
    last_pos = None
    drawing = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                get_digit(screen)

            elif event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   get_digit(screen)

            elif event.type == MOUSEMOTION:
                if drawing:
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        pygame.draw.line(screen, WHITE, last_pos, mouse_position, WIDTH)
                    last_pos = mouse_position
                    
            elif event.type == MOUSEBUTTONUP:
                last_pos = None
                drawing = False
                
            elif event.type == MOUSEBUTTONDOWN:
                last_pos = pygame.mouse.get_pos()
                drawing = True

        pygame.display.update()


if __name__ == "__main__":
    main()
