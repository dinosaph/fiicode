#FIICODE - Team owo
#Author: Oica Andra-Maria (dinosaph)
#Faculty of Computer Science, UAIC, Iasi

#IMPORTS
import os, pygame
import gameActors as act

#GLOBALS
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
spritesCollection = pygame.sprite.Group()
miscSprites = pygame.sprite.Group()
GAME_STATE = { "holdingBear" : False, "safeToLoad" : False, "loadedBear" : False, "loading" : False, "loadingUp" : False, "launching" : False, "flying" : False}
spritesStates = {}
screen = []
RUNNING = True
THROW_POWER, CURRENT_POWER, MAX_POWER = (0, 0, 300)

def preparePlayground():
    global spritesCollection, spritesStates

    spritesStates["scene"] = ["scene.png"]
    bg = act.gameObj(spritesStates["scene"][0])
    spritesCollection.add(bg)


def prepareCatapult():
    global spritesCollection, spritesStates
    
    spritesStates["catapult"] = ["catapult.png", "catapult2.png", "catapult3.png", "catapult_last.png"]
    catapultWidth, catapultHeight = (450, 250)
    catapultInitialX, catapultInitialY = (400, 10)
    catapult = act.gameObj(spritesStates["catapult"][0])
    catapult.resizeImg(catapultWidth, catapultHeight)
    catapult.rect.x, catapult.rect.y = (catapultInitialX, catapultInitialY)

    spritesCollection.add(catapult)

def changeCatapult(img_file):
    global spritesCollection

    catapult = spritesCollection.sprites()[1]
    catapultWidth, catapultHeight = (450, 250)
    catapult.changeState(img_file)
    catapult.resizeImg(catapultWidth, catapultHeight)

def prepareLilBear():
    global spritesCollection, spritesStates

    spritesStates["lilBear"] = ["lilbear.png", "lilbear_hangin.png", "lilbear_zzz.png"]
    # lilBearWidth, lilBearHeight = ()
    lilBearInitialX, lilBearInitialY = (100, 300)
    lilBear = act.gameObj("lilbear.png")
    lilBear.rect.x, lilBear.rect.y = (lilBearInitialX, lilBearInitialY)

    print(spritesStates["lilBear"])
    spritesCollection.add(lilBear)

def preparePressureBar():
    global spritesCollection, miscSprites
    RED = (255, 0, 0)
    barSize = 20
    barInitialX, barInitialY = (0, 130)
    pressureBar = act.miscBlock(RED, barSize, barSize)
    pressureBar.rect.y = barInitialY

    miscSprites.add(pressureBar)

def gameInit():
    global SCREEN_WIDTH, SCREEN_HEIGHT, spritesCollection, screen

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Global Warming')

    preparePlayground()
    prepareCatapult()
    prepareLilBear()
    preparePressureBar()

def startGame():
    global RUNNING

    while RUNNING:
        playGame()

def loadPressureBar(color = (255, 0, 0)):
    global miscSprites, spritesCollection, THROW_POWER, CURRENT_POWER, GAME_STATE, MAX_POWER

    pressureBar = miscSprites.sprites()[0]
    pressureBar.changeColor(color)
    spritesCollection.add(pressureBar)

    THROW_POWER += 1
    CURRENT_POWER = min(30, int(THROW_POWER)) * 10

    # print(THROW_POWER)
    if CURRENT_POWER < MAX_POWER :
        if GAME_STATE["loadingUp"]:
            pressureBar.resizeSelf(CURRENT_POWER)
        else:
            pressureBar.resizeSelf(MAX_POWER - CURRENT_POWER + 10)
    else:
        if GAME_STATE["loadingUp"]:
            GAME_STATE["loadingUp"] = False
        else:
            GAME_STATE["loadingUp"] = True
        THROW_POWER = 0
        CURRENT_POWER = 0

def removePressureBar():
    global miscSprites, spritesCollection

    pressureBar = miscSprites.sprites()[0]
    spritesCollection.remove(pressureBar)

def refreshScreen():
    global spritesCollection, screen

    spritesCollection.update()
    spritesCollection.draw(screen)
    pygame.display.flip()

def playGame():
    global RUNNING, screen, miscSprites ,spritesCollection, spritesStates, GAME_STATE, THROW_POWER

    catapult = spritesCollection.sprites()[1]
    bear = spritesCollection.sprites()[2]
    pressureBar = miscSprites.sprites()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if pygame.mouse.get_pressed()[0]:
            if bear.rect.collidepoint(event.pos):
                GAME_STATE["holdingBear"] = True
        else:
            GAME_STATE["holdingBear"] = False
        if bear.rect.colliderect(catapult):
            GAME_STATE["safeToLoad"] = True
        else:
            GAME_STATE["safeToLoad"] = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if GAME_STATE["loadedBear"]:
                GAME_STATE["loading"] = True
                GAME_STATE["launching"] = True
                GAME_STATE["loadedBear"] = False
        else:
            GAME_STATE["loading"] = False
    
    if not GAME_STATE["flying"] :
        if GAME_STATE["holdingBear"]:
            bear.changeState(spritesStates["lilBear"][1])
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bear.rect.x, bear.rect.y = mouse_x, mouse_y
        else:
            if GAME_STATE["safeToLoad"] and not GAME_STATE["launching"]:
                bear.rect.x, bear.rect.y = (400, 80)
                bear.changeState(spritesStates["lilBear"][2])
                GAME_STATE["loadedBear"] = True
                GAME_STATE["safeToLoad"] = False
            elif GAME_STATE["loadedBear"]:
                loadPressureBar()
            elif GAME_STATE["loading"]:
                loadPressureBar((0, 255,0))
                changeCatapult(spritesStates["catapult"][1])
                bear.rect.y = 120
            else:
                if not GAME_STATE["launching"]:
                    bear.changeState(spritesStates["lilBear"][0])
                    bear.rect.x, bear.rect.y = (100, 300)
                    removePressureBar()
                else:
                    removePressureBar()
                    changeCatapult(spritesStates["catapult"][2])
                    refreshScreen()
                    bear.rect.x, bear.rect.y = (460, -50)
                    changeCatapult(spritesStates["catapult"][3])
                    refreshScreen()
                    bear.changeState(spritesStates["lilBear"][1])
                    bear.rect.x, bear.rect.y = (800, -20)
                    GAME_STATE["launching"] = False
                    GAME_STATE["flying"] = True
    else:
        bear.rect.x += 10

    refreshScreen()

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    gameInit()
    startGame()

if __name__ == "__main__":
    main()