import os, sys, pygame, uuid
from pygame.locals import *
from PIL import Image

def save_screen(digit, sc):
    sc_arr = pygame.surfarray.array2d(sc)
    img = Image.fromarray(sc_arr)
    img.thumbnail((20, 20))
    
    img = img.rotate(90, expand=True)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    filename = str(uuid.uuid4())
    img.save("data/" + digit + "/" + filename + ".png", "PNG")

    global IMG_SAVED_COUNTER
    IMG_SAVED_COUNTER += 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 2 # Subject to Change

print("\nPress SPACE each time to save your digit drawing!")
DIGIT = input("Enter digit you want to draw: ")
IMG_SAVED_COUNTER = 0

try:
    os.mkdir(DIGIT)
except:
    pass

pygame.init()

pygame.display.set_caption("Personalized Digit Recognition!")
screen = pygame.display.set_mode((400, 400), 0, 32)
screen.fill(BLACK)

mouse_position = (0, 0)
last_pos = None
drawing = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
            elif event.key == K_SPACE:
                save_screen(DIGIT, screen)
                screen.fill(BLACK)

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

print(f"\nA total of {IMG_SAVED_COUNTER} handwritten digit samples have been saved under the '{DIGIT}' label!")
pygame.quit()
sys.exit()
