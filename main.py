from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

import math

LabelBase.register(name="blocks", fn_regular="blocks.ttf")

class Global():
    level = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,2,2,0,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]

    entities = []
    blocks = []
    enemies = []
    block_size = 32
    levelNumber = 0

globals = Global()

class Rect():
    def __init__(self,x=0,y=0,w=32,h=32):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center_x = x-w/2
        self.center_y = y-h/2

    def rect(self):
        return self.x,self.y,self.w,self.h

    def position(self,x,y):
        self.x = x
        self.y = y
        self.center_x = x+self.w/2
        self.center_y = y+self.h/2

    def move(self,x,y):
        self.x += x
        self.y += y
        self.center_x += x
        self.center_y += y

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.x + self.state.x, target.rect.y + self.state.y

    def update(self, target_rect, root):
        self.state = self.camera_func(self.state, target_rect, root)

def complex_camera(camera, target_rect, root):
    l, t, _, _ = target_rect.rect()
    _, _, w, h = camera.rect()
    l, t, _, _ = -l+root.width/2, -t+root.height/2, w, h

    l = min(0, l)                           # sy scrolling at the x edge
    l = max(-(camera.w-root.width), l)   # sy scrolling at the right edge
    t = max(-(camera.h-root.height), t) # sy scrolling at the bottom
    t = min(0, t)                           # sy scrolling at the y
    return Rect(l, t, w, h)

class Player(Widget):
    # pos = ()
    rect = Rect(0,0,32,32)
    xvel = 0
    yvel = 0
    onGround = False
    actionQueue = []

    def init(self,x,y,w,h):
        self.rect.position(x,y)
        self.size = w,h
        self.rect.w = w-1
        self.rect.h = h-1

    def update(self,pos):

        self.onGround = False

        self.rect.move(self.xvel, 0)
        self.collide(self.xvel, 0)
        self.rect.move(0, self.yvel)
        self.collide(0, self.yvel)
        self.pos = pos

        if self.xvel > 1:
            self.xvel += -0.5
        elif self.xvel < -1:
            self.xvel += 0.5
        else:
            self.xvel = 0

        if not self.onGround:
            self.yvel -= 1
            if self.yvel > 100:
                self.yvel = 100
        else:
            if len(self.actionQueue) > 0:
                self.xvel += self.actionQueue[::-1][0][0]
                self.yvel += self.actionQueue[::-1][0][1]
                self.actionQueue.remove(self.actionQueue[::-1][0])

    def move(self,xvel,yvel):

        # somethingInWay = False
        # for entity in globals.entities:
        #     if entity.rect.x == self.rect.x + xvel and entity.rect.y == self.rect.y + yvel:
        #         somethingInWay = True
        #
        # if not somethingInWay:
        #     self.rect.x += xvel
        #     self.rect.y += yvel
        self.rect.x += xvel
        self.rect.y += yvel

    def moveUntilBlocked(self,xvel,yvel):
        while True:
            somethingInWay = False
            for entity in globals.entities:
                if entity.rect.x == self.rect.x + xvel and entity.rect.y == self.rect.y + yvel:
                    somethingInWay = True

            if not somethingInWay:
                self.rect.x += xvel
                self.rect.y += yvel
            else:
                break

    def collide(self, xvel, yvel):
        for block in globals.blocks:
            if (self.rect.x > block.rect.x and self.rect.x < (block.rect.x + block.rect.w)) or (self.rect.x + self.rect.w > block.rect.x and self.rect.x + self.rect.w < (block.rect.x + block.rect.w)):
                if (self.rect.y > block.rect.y and self.rect.y < block.rect.y + block.rect.h) or (self.rect.y+self.rect.h > block.rect.y and self.rect.y+self.rect.h < block.rect.y + block.rect.h):
                    if xvel > 0:
                        self.rect.x = block.rect.x-self.rect.w
                        # self.xvel = self.xvel/1.5
                    elif xvel < 0:
                        # self.rect.position(block.rect.x+block.rect.w,self.rect.y)
                        self.rect.x = block.rect.x+block.rect.w
                        # self.xvel = self.xvel/1.5
                    elif yvel < 0:
                        self.onGround = True
                        self.yvel = 0
                        self.rect.y = block.rect.y+block.rect.h
                    elif yvel > 0:
                        self.yvel = 0
                        self.rect.y = block.rect.y-self.rect.h


class Jumper(Widget):
    # pos = ()
    rect = Rect(0,0,32,32)
    xvel = 0
    yvel = 0
    onGround = False
    actionQueue = []
    angle = 0

    def init(self,x,y,w,h):
        self.rect.position(x,y)
        self.size = w,h
        self.rect.w = w-1
        self.rect.h = h-1

    def update(self,pos):

        self.onGround = False

        if self.xvel > 16:
            self.xvel = 16
        if self.xvel < -16:
            self.xvel = -16

        self.rect.move(self.xvel, 0)
        self.collide(self.xvel, 0)
        self.rect.move(0, self.yvel)
        self.collide(0, self.yvel)
        self.pos = pos

        if self.xvel > 1:
            self.xvel += -0.5
        elif self.xvel < -1:
            self.xvel += 0.5
        else:
            self.xvel = 0

        if not self.onGround:
            self.yvel -= 1
            if self.yvel > 100:
                self.yvel = 100
        else:
            if len(self.actionQueue) > 0:
                self.xvel += self.actionQueue[::-1][0][0]
                self.yvel += self.actionQueue[::-1][0][1]
                self.actionQueue.remove(self.actionQueue[::-1][0])

    def autoGo(self, playerX, playerY):

        if ((playerX-self.rect.x >= 0) and (playerY-self.rect.y <= 0)):
            turn = -90-self.angle-math.degrees(math.atan2((self.rect.y-playerY),(self.rect.x-playerX)))
        if ((playerX-self.rect.x <= 0) and (playerY-self.rect.y >= 0)):
            turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.y-playerY),(self.rect.x-playerX)))))
        if ((playerX-self.rect.x >= 0) and (playerY-self.rect.y >= 0)):
            turn = -90-self.angle-math.degrees(math.atan2((self.rect.y-playerY),(self.rect.x-playerX)))
        if ((playerX-self.rect.x <= 0) and (playerY-self.rect.y <= 0)):
            turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.y-playerY),(self.rect.x-playerX)))))

        self.angle += turn
        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360
        if len(self.actionQueue) <= 1:

            distance = ((self.rect.x - playerX) + (self.rect.y - playerY))**2

            self.actionQueue.append([(distance/10000)*math.sin(math.radians(abs(self.angle))), (distance/10000)*math.cos(math.radians(abs(self.angle)))])

    def move(self,xvel,yvel):
        self.rect.x += xvel
        self.rect.y += yvel

    def collide(self, xvel, yvel):
        for block in globals.blocks:
            if (self.rect.x > block.rect.x and self.rect.x < (block.rect.x + block.rect.w)) or (self.rect.x + self.rect.w > block.rect.x and self.rect.x + self.rect.w < (block.rect.x + block.rect.w)):
                if (self.rect.y > block.rect.y and self.rect.y < block.rect.y + block.rect.h) or (self.rect.y+self.rect.h > block.rect.y and self.rect.y+self.rect.h < block.rect.y + block.rect.h):
                    if xvel > 0:
                        self.rect.x = block.rect.x-self.rect.w
                        # self.xvel = self.xvel/1.5
                    elif xvel < 0:
                        # self.rect.position(block.rect.x+block.rect.w,self.rect.y)
                        self.rect.x = block.rect.x+block.rect.w
                        # self.xvel = self.xvel/1.5
                    elif yvel < 0:
                        self.onGround = True
                        self.yvel = 0
                        self.rect.y = block.rect.y+block.rect.h
                    elif yvel > 0:
                        self.yvel = 0
                        self.rect.y = block.rect.y-self.rect.h


class Block(Widget):
    def init(self,x,y,w=32,h=32):
        # self.rect.position(x,y)
        self.rect = Rect(x,y,w,h)
        self.size = self.rect.w,self.rect.h
        xvel = 0
        yvel = 0

    def update(self,pos):
        self.pos = pos

    # def position(self,x,y):
    #     self.rect = Rect(x,y,32,32)

class RunGame(Widget):
    blocks = []
    move_anchor = (0,0)
    start = True

    state = "beginGame"

    beginGameObjects = []

    def beginGame(self):
        beginLabel = Label(text='[color=000000]dig', markup=True, font_size='40sp', font_name="blocks")
        beginLabel.pos = (self.width/2-beginLabel.width/2, self.height/2-beginLabel.height/2)
        self.add_widget(beginLabel)
        self.beginGameObjects.append(beginLabel)
        self.state = "idle"

    def loadLevel(self,levelNumber):
        del globals.entities[:]
        del globals.blocks[:]
        globals.level = globals.level[::-1]
        # globals.block_size = self.height/len(globals.level)
        globals.block_size = self.width/len(globals.level[0]) * 1.2
        ###
        x = y = 0
        for row in globals.level:
            for col in row:

                if int(col) == 0:
                    b = Block()
                    b.init(x,y,globals.block_size, globals.block_size)

                    globals.entities.append(b)
                    globals.blocks.append(b)
                    self.add_widget(b)

                x += globals.block_size
            y += globals.block_size
            x = 0


        x = y = 0
        for row in globals.level:
            for col in row:

                if int(col) == 1:
                    self.player = Player()
                    self.player.init(x,y,globals.block_size, globals.block_size)
                    globals.entities.append(self.player)
                    self.add_widget(self.player)

                if int(col) == 3:
                    j = Jumper()
                    j.init(x,y,globals.block_size, globals.block_size)
                    globals.entities.append(j)
                    globals.enemies.append(j)
                    self.add_widget(j)

                x += globals.block_size
            y += globals.block_size
            x = 0
        ###

        self.state = "normalPlay"
        self.camera = Camera(complex_camera,globals.block_size*len(globals.level[0]),globals.block_size*len(globals.level))


    def update(self, dt):
        if self.state =="beginGame":
            self.beginGame()
        elif self.state =="idle":
            pass
        elif self.state == "loadLevel":
            self.loadLevel(globals.levelNumber)
        elif self.state == "normalPlay":
            self.camera.update(self.player.rect,self)
            self.player.update(self.camera.apply(self.player))
            for b in globals.blocks:
                b.update(self.camera.apply(b))
            for e in globals.enemies:
                e.update(self.camera.apply(e))
                e.autoGo(self.player.rect.x, self.player.rect.y)


    def on_touch_down(self,touch):
        if self.state == "normalPlay":
            self.move_anchor = (touch.x,touch.y)

    # def on_touch_move(self, touch):
    #     if touch.x < self.width/2:
    #         self.player.move(-0.1*(self.move_anchor[0]-touch.x),-0.1*(self.move_anchor[1]-touch.y))

    def on_touch_up(self,touch):
        if self.state == "idle":
            for item in self.beginGameObjects:
                self.remove_widget(item)
            self.state = "loadLevel"
        elif self.state == "normalPlay":
            # if -0.1*(self.move_anchor[0]-touch.x) > 15:
            #     self.player.move(globals.block_size,0)
            # elif -0.1*(self.move_anchor[0]-touch.x) < -15:
            #     self.player.move(-globals.block_size,0)
            # elif -0.1*(self.move_anchor[1]-touch.y) > 8:
            #     self.player.move(0,globals.block_size)
            # elif -0.1*(self.move_anchor[1]-touch.y) < -8:
            #     self.player.move(0,-globals.block_size)
            self.player.actionQueue.append([-0.07*(self.move_anchor[0]-touch.x),-0.07*(self.move_anchor[1]-touch.y)])

class Game(App):
    def build(self):
        game = RunGame()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

    def on_pause(self):
        return True

    def on_resume(self):
        return True

def main():
    Game().run()

if __name__ == '__main__':
    main()
