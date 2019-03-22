#FIICODE - Team owo
#Author: Oica Andra-Maria (dinosaph)
#Faculty of Computer Science, UAIC, Iasi

import os, pygame
import gameActors as act

screen = []
RUNNING = True
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)
spritesCollection = []
pressureBar = []

def gameInit():
    global SCREEN_WIDTH, SCREEN_HEIGHT, spritesCollection, screen, bg_img, pressureBar
    bg_img = pygame.image.load(os.path.join("images", "scene.png"))
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Global Warming')
    spritesCollection = pygame.sprite.Group()
    lilBear = act.gameObj("lilbear.png")
    lilBear.rect.x, lilBear.rect.y = (100, 200)
    tool = act.gameObj("catapult.png")
    tool.resizeImg(450, 250)
    tool.rect.x, tool.rect.y = (400, 10)
    pressureBar = act.miscBlock((255,0,0),20,20)
    pressureBar.rect.y = 130
    spritesCollection.add(tool, lilBear)
    print(spritesCollection)

def startGame():
    global RUNNING, screen, spritesCollection, bg_img, pressureBar
    holdingBear = False
    readyToLoad = False
    bearLoaded = False
    tool = spritesCollection.sprites()[0]
    bear = spritesCollection.sprites()[1]
    MAX_POWER = 300
    throwPower, currentPressure = (0, 0)
    loadingUp = True
    holdingSpace = False
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                holdingSpace = True
            else:
                holdingSpace = False
                pressureBar.changeColor((255,0,0))
            if pygame.mouse.get_pressed()[0]:
                if bear.rect.collidepoint(event.pos):
                    holdingBear = True
                    if bear.rect.colliderect(tool):
                        # print("safe")
                        readyToLoad = True
                    else:
                        readyToLoad = False
            else:
                holdingBear = False
                # bear.changeState("lilbear_rawr.png")
                bear.changeState("lilbear.png")
                # readyToLoad = False
        if holdingBear:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bear.rect.x, bear.rect.y = mouse_x, mouse_y
            bear.changeState("lilbear_hangin.png")
            # pressureBar.resizeSelf(20)
        elif readyToLoad:
            bear.rect.x, bear.rect.y = (400, 80)
            bear.changeState("lilbear_zzz.png")
            # readyToLoad = False
            spritesCollection.add(pressureBar)
            bearLoaded = True
            if holdingSpace:
                pressureBar.changeColor((0,255,0))
                tool.changeState("catapult2.png")
                tool.resizeImg(450, 250)
                bear.rect.y += 40
            throwPower += 1
            currentPressure = min(30, int(throwPower)) * 10
            print(throwPower)
            if currentPressure < MAX_POWER :
                if loadingUp:
                    pressureBar.resizeSelf(currentPressure)
                else:
                    pressureBar.resizeSelf(MAX_POWER - currentPressure + 10)
            else:
                if loadingUp:
                    loadingUp = False
                else:
                    loadingUp = True
                throwPower = 0
                currentPressure = 0
        else:
            bear.rect.x, bear.rect.y = (100, 300)
            pressureBar.resizeSelf(20)
            spritesCollection.remove(pressureBar)
        screen.blit(bg_img, (0,0))
        spritesCollection.update()
        spritesCollection.draw(screen)
        pygame.display.flip()

def main():
    pygame.init()
    gameInit()
    startGame()

if __name__ == "__main__":
    main()