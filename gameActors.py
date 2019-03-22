import os, pygame

class gameObj(pygame.sprite.Sprite):
    def __init__(self, img_file):
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", img_file))
        self.rect = self.image.get_rect()
    def changeState(self, img_file):
        self.image = pygame.image.load(os.path.join("images", img_file))
        # self.rect = self.image.get_rect()
    def resizeImg(self, new_width, new_height):
        self.image = pygame.transform.scale(self.image, (new_width, new_width))

class miscBlock(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width, self.height = (width, height)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
    def resizeSelf(self, changeX):
        self.image = pygame.transform.scale(self.image, (changeX, self.height))
    def changeColor(self, color):
        self.image.fill(color)
