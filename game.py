#FIICODE - Team owo
#Author: Oica Andra-Maria (dinosaph)
#Faculty of Computer Science, UAIC, Iasi

#IMPORTS
import random
import os, pygame
import pygameMenu
from pygameMenu.locals import *
import gameActors as act

#GLOBALS
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
spritesCollection = pygame.sprite.Group()
miscSprites = pygame.sprite.Group()
transitionSprites = pygame.sprite.Group()
storySprites = pygame.sprite.Group()
GAME_STATE = { "holdingBear" : False, "safeToLoad" : False, "loadedBear" : False, "loading" : False, "loadingUp" : False, "launching" : False, "flying" : False, "intended" : False}
spritesStates = {}
screen = []
SOUNDS = []
RUNNING, IN_SCENE, TELEPORTING, SKIP = (True, True, False, False)
INTRO = False
CURRENT_SCENE = 0
CURRENT_POS = 100
CURRENT_SUN_POS = -200
CURRENT_SUN_SCENE = -1
CURRENT_STORY_FRAME = 0
MAX_SCENES = 3
THROW_POWER, CURRENT_POWER, MAX_POWER = (0, 0, 700)

def prepareIntro():
    global storySprites, spritesStates

    spritesStates["story"] = ["intro1.png", "story2.png", "story3.png", "story4.png", "story5.png", "story6.png", "story7.png", "story8.png", "story9.png", "menu.png"]
    slide = act.gameObj(spritesStates["story"][0])
    skip = act.gameObj("skip.png")
    storySprites.add(slide, skip)

def preparePlayground():
    global spritesCollection, spritesStates, transitionSprites, miscSprites

    spritesStates["scene"] = ["scene.png", "scene.png", "scene.png", "scene.png", "scene.png", "scene.png"]
    spritesStates["distance"] = ["dist0.png", "dist1.png", "dist2.png", "dist3.png", "dist4.png", "dist5.png", "dist6.png", "dist7.png", "dist8.png", "dist9.png", "dist10.png"]
    spritesStates["sunDist"] = ["sun0.png", "sun1.png", "sun2.png", "sun3.png", "sun4.png", "sun5.png", "sun6.png", "sun7.png", "sun8.png", "sun9.png", "sun10.png"]
    spritesStates["ice"] = ["ice.png"]
    spritesStates["bros"] = ["bros.png"]
    spritesStates["sun"] = ["sun.png"]

    bg = act.gameObj(spritesStates["scene"][0])
    ice = act.gameObj(spritesStates["ice"][0])
    bros = act.gameObj(spritesStates["bros"][0])
    sun = act.gameObj(spritesStates["sun"][0])
    distance = act.gameObj(spritesStates["distance"][0])
    sunDist = act.gameObj(spritesStates["sunDist"][0])

    sunDist.rect.y = 10
    brosInitialX, brosInitialY = (850, 280)
    bros.rect.x, bros.rect.y = (brosInitialX, brosInitialY)

    spritesCollection.add(bg, sun, ice, bros, distance, sunDist)
    miscSprites.add(sun)

    tr = act.gameObj("transition.png")
    transitionSprites.add(tr, distance, sun)

def prepareCatapult():
    global spritesCollection, spritesStates, CURRENT_SCENE
    
    spritesStates["catapult"] = ["catapult.png", "catapult2.png", "catapult3.png", "catapult_last.png"]
    catapultWidth, catapultHeight = (450, 250)
    catapultInitialX, catapultInitialY = (400, 10)
    catapult = act.gameObj(spritesStates["catapult"][0])
    catapult.resizeImg(catapultWidth, catapultHeight)
    catapult.rect.x, catapult.rect.y = (catapultInitialX, catapultInitialY)

    spritesCollection.add(catapult)

def changeCatapult(img_file):
    global spritesCollection

    catapult = spritesCollection.sprites()[6]
    catapultWidth, catapultHeight = (450, 250)
    catapult.changeState(img_file)
    catapult.resizeImg(catapultWidth, catapultHeight)

def prepareBears():
    global spritesCollection, spritesStates, miscSprites

    spritesStates["lilBear"] = ["lilbear.png", "lilbear_hangin.png", "lilbear_zzz.png", "lilbear_flying.png"]
    spritesStates["momma"] = ["momma.png"]

    lilBearInitialX, lilBearInitialY = (100, 400)
    mommaInitialX, mommaInitialY = (700, 300)
    lilBear = act.gameObj(spritesStates["lilBear"][0])
    momma = act.gameObj(spritesStates["momma"][0])
    lilBear.rect.x, lilBear.rect.y = (lilBearInitialX, lilBearInitialY)
    momma.rect.x, momma.rect.y = (mommaInitialX, mommaInitialY)

    miscSprites.add(momma)
    miscSprites.add(lilBear)
    spritesCollection.add(lilBear)

def preparePressureBar():
    global spritesCollection, miscSprites
    RED = (255, 0, 0)
    barSize = 20
    barInitialX, barInitialY = (0, 50)
    pressureBar = act.miscBlock(RED, barSize, barSize)
    pressureBar.rect.y = barInitialY

    miscSprites.add(pressureBar)

def prepareSounds():
    global SOUNDS, INTRO

    if INTRO:
        pygame.mixer.music.load(os.path.join("sounds", "intro2.mp3"))
    else:
        pygame.mixer.music.load(os.path.join("sounds", "ingame.mp3"))
    throw = pygame.mixer.Sound(os.path.join("sounds", "throw2.wav"))
    # smolRawr = pygame.mixer.Sound()
    # SOUNDS.append(smolRawr)
    SOUNDS.append(throw)

def gameInit():
    global SCREEN_WIDTH, SCREEN_HEIGHT, spritesCollection, screen

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Global Warming')

    prepareIntro()
    preparePlayground()
    prepareCatapult()
    preparePressureBar()
    prepareBears()
    prepareSounds()

def startGame():
    global RUNNING, CURRENT_SCENE, MAX_SCENES, SKIP, INTRO, CURRENT_SUN_POS, miscSprites

    # menuWindow = pygame.image.load(os.path.join("images", "scene.png"))
    # menu = pygameMenu.Menu(menuWindow, 100, 100, font="8BIT", title="MENU", bgfun=None)

    if not INTRO:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

    while RUNNING:
        # events = pygame.event.get()
        if INTRO:
            while not SKIP:
                playStory()
        resetScene()
        while IN_SCENE:
            if CURRENT_SCENE < MAX_SCENES:
                playScene(CURRENT_SCENE)
            else:
                playLastScene()
        while TELEPORTING:
            # print("here")
            doTransition()

        # menu.mainloop(events)
    pygame.mixer.music.stop()

def loadPressureBar(color = (255, 0, 0)):
    global miscSprites, spritesCollection, THROW_POWER, CURRENT_POWER, GAME_STATE, MAX_POWER

    pressureBar = miscSprites.sprites()[1]
    pressureBar.changeColor(color)
    spritesCollection.add(pressureBar)

    THROW_POWER += 1
    CURRENT_POWER = min(70, int(THROW_POWER)) * 20

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

    pressureBar = miscSprites.sprites()[1]
    spritesCollection.remove(pressureBar)

def refreshScreen():
    global spritesCollection, screen

    spritesCollection.update()
    spritesCollection.draw(screen)
    pygame.display.flip()

def refreshScreenTransition():
    global transitionSprites, screen

    transitionSprites.update()
    transitionSprites.draw(screen)
    pygame.display.flip()

def resetScene():
    global GAME_STATE, IN_SCENE, spritesCollection, spritesStates, miscSprites, CURRENT_SCENE, MAX_SCENES

    IN_SCENE = True
    changeCatapult(spritesStates["catapult"][0])

    GAME_STATE["holdingBear"] = False
    GAME_STATE["safeToLoad"] = False
    GAME_STATE["loadedBear"] = False
    GAME_STATE["loading"] = False
    GAME_STATE["loadingUp"] = False
    GAME_STATE["launching"] = False
    GAME_STATE["flying"] = False

    #Last scene
    if CURRENT_SCENE == MAX_SCENES:
        bear = miscSprites.sprites()[3]
        #Removing penguins, catapult, lilbear, pressure bar
        spritesCollection.remove(spritesCollection.sprites()[3])
        spritesCollection.remove(spritesCollection.sprites()[5])
        spritesCollection.remove(bear)
        spritesCollection.remove(miscSprites.sprites()[1])
        #Adding momma bear, lilbear
        spritesCollection.add(miscSprites.sprites()[2])
        spritesCollection.add(bear)
        #Resseting lilbear position
        bear.rect.x, bear.rect.y = (100, 300)

def refreshStory():
    global storySprites, screen

    storySprites.update()
    storySprites.draw(screen)
    pygame.display.flip()

def playStory():
    global RUNNING, SKIP, CURRENT_STORY_FRAME, spritesStates, storySprites

    frame = storySprites.sprites()[0]
    if CURRENT_STORY_FRAME < len(spritesStates["story"]):
        frame.changeState(spritesStates["story"][CURRENT_STORY_FRAME])
    CURRENT_STORY_FRAME += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            SKIP = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            SKIP = True

    if SKIP:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join("sounds", "ingame.mp3"))
        pygame.mixer.music.play(-1)
    else:
        if CURRENT_STORY_FRAME == len(spritesStates["story"]):
            storySprites.remove(storySprites.sprites()[1])
        refreshStory()
        pygame.time.wait(3000)

def playScene(sceneNumber):
    global RUNNING, CURRENT_POWER, CURRENT_POS, IN_SCENE, TELEPORTING, screen, miscSprites, spritesCollection, spritesStates, GAME_STATE, THROW_POWER, MAX_SCENES, CURRENT_SCENE, SOUNDS, CURRENT_SUN_POS, CURRENT_SUN_SCENE

    scene = spritesCollection.sprites()[0]
    scene.changeState(spritesStates["scene"][sceneNumber])
    catapult = spritesCollection.sprites()[6]
    bear = spritesCollection.sprites()[7]
    pressureBar = miscSprites.sprites()[0]
    sun = miscSprites.sprites()[0]

    if GAME_STATE["loading"]:
        CURRENT_POS = CURRENT_POWER
        print(CURRENT_POS)

    defaultLilbearX, defaultLilbearY = (CURRENT_POS, 350)
    lilbearLoadedX, lilbearLoadedY = (400, 80)
    chargedLilbearY = 120
    lilbearUpThrowX, lilbearUpThrowY = (460, -50)
    lilbearThrownX, lilbearThrownY = (800, -20)
    lilbearTranX, lilbearTranY = (-10, 150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            IN_SCENE = False
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if bear.rect.collidepoint((mouse_x, mouse_y)):
                GAME_STATE["holdingBear"] = True
                GAME_STATE["intended"] = True
        else:
            GAME_STATE["holdingBear"] = False
        if bear.rect.colliderect(catapult) and GAME_STATE["intended"]:
            GAME_STATE["safeToLoad"] = True
        else:
            GAME_STATE["safeToLoad"] = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if GAME_STATE["loadedBear"]:
                GAME_STATE["loading"] = True
                GAME_STATE["launching"] = True
                GAME_STATE["loadedBear"] = False
            else:
                GAME_STATE["launching"] = False
        else:
            GAME_STATE["loading"] = False
    
    if not GAME_STATE["flying"]:
        if GAME_STATE["holdingBear"]:
            bear.changeState(spritesStates["lilBear"][1])
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bear.rect.x, bear.rect.y = mouse_x, mouse_y
        else:
            if not bear.rect.colliderect(catapult):
                bear.changeState(spritesStates["lilBear"][0])
                bear.rect.x, bear.rect.y = (defaultLilbearX, defaultLilbearY)
            if GAME_STATE["safeToLoad"] and not GAME_STATE["launching"]:
                bear.rect.x, bear.rect.y = (lilbearLoadedX, lilbearLoadedY)
                bear.changeState(spritesStates["lilBear"][2])
                GAME_STATE["loadedBear"] = True
                GAME_STATE["safeToLoad"] = False
            elif GAME_STATE["loadedBear"]:
                loadPressureBar()
            elif GAME_STATE["loading"]:
                loadPressureBar((0, 255,0))
                changeCatapult(spritesStates["catapult"][1])
                bear.rect.y = chargedLilbearY
            else:
                if not GAME_STATE["launching"]:
                    bear.changeState(spritesStates["lilBear"][0])
                    bear.rect.x, bear.rect.y = (defaultLilbearX, defaultLilbearY)
                    removePressureBar()
                else:
                    removePressureBar()
                    changeCatapult(spritesStates["catapult"][2])
                    refreshScreen()
                    bear.rect.x, bear.rect.y = (lilbearUpThrowX, lilbearUpThrowY)
                    changeCatapult(spritesStates["catapult"][3])
                    refreshScreen()
                    bear.changeState(spritesStates["lilBear"][1])
                    bear.rect.x, bear.rect.y = (lilbearThrownX, lilbearThrownY)
                    GAME_STATE["launching"] = False
                    GAME_STATE["flying"] = True
                    SOUNDS[0].play()
    else:
        if bear.rect.colliderect(scene):
            bear.rect.x += 10
        else:
            CURRENT_SCENE = min(MAX_SCENES, int((((CURRENT_SCENE + 1) * 1000) + lilbearLoadedX + defaultLilbearX + CURRENT_POWER) / 1000))
            print(lilbearLoadedX, defaultLilbearX, CURRENT_POWER)
            print("Scene: ", CURRENT_SCENE)
            bear.rect.x, bear.rect.y = (lilbearTranX, lilbearTranY)
            IN_SCENE = False
            TELEPORTING = True

            if CURRENT_SUN_SCENE == -1:
                bear_sun_diff = ((CURRENT_SCENE * 1000) + CURRENT_POS) - CURRENT_SUN_POS
            else:
                bear_sun_diff = ((CURRENT_SCENE * 1000) + CURRENT_POS) - ((CURRENT_SUN_SCENE * 1000) + CURRENT_SUN_POS)
            CURRENT_SUN_POS = -bear_sun_diff

            pygame.time.wait(1500)

    updateSun()
    refreshScreen()

def updateSun():
    global spritesCollection, spritesStates, miscSprites, CURRENT_POS, CURRENT_SCENE, CURRENT_SUN_POS, CURRENT_SUN_SCENE

    scene = spritesCollection.sprites()[0]
    sun = miscSprites.sprites()[0]
    sunDist = spritesCollection.sprites()[5]
    bear = miscSprites.sprites()[3]

    if CURRENT_SUN_SCENE == -1:
        currentX = CURRENT_SUN_POS
        if sun.rect.colliderect(scene):
            CURRENT_SUN_SCENE = 0
    else:
        currentX = (CURRENT_SUN_SCENE * 1000) + CURRENT_SUN_POS
        CURRENT_SUN_SCENE = int(currentX / -1000)

    print("Sun current x: ", currentX)

    currentBearX = bear.rect.x
    print("Bear current x: ", currentBearX)
    if currentX < currentBearX - 20:
        CURRENT_SUN_POS += 1
        sun.rect.x = CURRENT_SUN_POS

    if CURRENT_SUN_SCENE > -1:
        sunDist.changeState(spritesStates["sunDist"][CURRENT_SUN_SCENE + 1])

    print("Sun is at scene: ", CURRENT_SUN_SCENE, CURRENT_SUN_POS)

    # CURRENT_SUN_POS = (CURRENT_SCENE * 1000) - (CURRENT_SUN_SCENE * 1000) - CURRENT_SUN_POS
    # sun.rect.x = CURRENT_SUN_POS


def heartFest():
    global spritesCollection

    heart = act.gameObj("heart.png")
    heartX = random.randint(200, 990)
    heartY = random.randint(10, 490)
    heart.rect.x, heart.rect.y = (heartX, heartY)
    spritesCollection.add(heart)

def playLastScene():
    global IN_SCENE, spritesCollection, spritesStates, RUNNING

    bear = spritesCollection.sprites()[6]
    momma = spritesCollection.sprites()[5]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            IN_SCENE = False
        if bear.rect.colliderect(momma) and pygame.key.get_pressed()[pygame.K_SPACE]:
            heartFest()

    if not bear.rect.colliderect(momma):
        bear.rect.x += 2
    else:
        bear.changeState(spritesStates["lilBear"][0])
        bear.rect.y = 320
        if len(spritesCollection.sprites()) > 7:
            for heart in spritesCollection.sprites()[4:]:
                heart.rect.y -= 1
                if heart.rect.y < 0:
                    spritesCollection.remove(heart)
    updateSun()
    refreshScreen()

def doTransition():
    global spritesCollection, transitionSprites, TELEPORTING, RUNNING, CURRENT_SCENE, spritesStates

    distance = transitionSprites.sprites()[1]
    scene = transitionSprites.sprites()[0]
    bear = spritesCollection.sprites()[7]
    transitionSprites.add(bear)
    distance.changeState(spritesStates["distance"][CURRENT_SCENE])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            TELEPORTING = False

    if bear.rect.colliderect(scene):
        bear.changeState(spritesStates["lilBear"][3])
        bear.rect.x += 10
    else:
        TELEPORTING = False

    # updateSun()
    refreshScreenTransition()

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    gameInit()
    startGame()

if __name__ == "__main__":
    main()