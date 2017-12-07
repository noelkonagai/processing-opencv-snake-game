import random, os
add_library('opencv_processing')
add_library('video')
add_library('minim')

minim = Minim(this)

path = os.getcwd()

cam = ""
opencv = ""
lowerb = 22
upperb = 70

#the bounding pixel values
#up control
uLow = 0
uHigh = 200

#down control
dLow = 400
dHigh = 600

#right control, camera mirrors
rLow = 0
rHigh = 333 #these have to be integers for them to be in range

#left control, camera mirrors
lLow = 666 #these have to be integers for them to be in range
lHigh = 1000

recieveNewCommand = True

class Tile:
    def __init__(self,r,c,v):
        self.r = r
        self.c = c
        self.v = v
        self.img = ''

class Game:
    def __init__(self, numRows,numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.board = []
        self.values = []
        
        for r in range(self.numRows):
            for c in range(self.numCols):
                self.board.append(Tile(r,c,'w'))
                
        self.dir = 1
        self.place = 775
        self.body = [775]
        self.createFood()
        self.hungry = False
        self.sound = minim.loadFile(path+'/eating.mp3')
        self.oversound = minim.loadFile(path+'/gameover.mp3')
        self.state = 'menu'
        self.newgame = False
        self.soundcheck = 1 
        self.speed = 1
        
        #The attributes to stage level changes
        self.control = 'normal'
        self.speedControl = 4
        self.won = False
        self.lost = False
        self.gameover = False 

    def loadImages(self):
        for t in self.board:
            t.img = loadImage(path + '/'+str(t.v)+'.jpg')
            
        self.gameoverImg = loadImage(path + '/gameover.png')
        self.winningImg = loadImage(path + "/winning.png")
        self.returnImg = loadImage(path + '/return.png')
        # if self.soundcheck == 1:
        #     self.gamesound = minim.loadFile(path+'/doraemon.mp3')
        # self.gamesound.loop()
    
    def createFood(self):
        self.t = random.choice(self.board)
        while self.t in self.body:
            self.t = random.choice(self.board)
        self.t.v = 'b'
        self.t.img = loadImage(path+'/b.jpg')
    
    def menu(self):
        textAlign(LEFT)
        background(182,182,180)
        textSize(60)
        fill(255)
        text ('Main Menu',500,150)
        textSize(35)
        fill(255)
        text('Directions',560,250)
        textSize(35)
        fill(255)
        text('Play Game',560,350)
        
    def directions(self):
        textAlign(LEFT)
        background(182,182,180)
        fill(255)
        textSize(35)
        text('Directions', 300, 150)
        textSize(14)
        fill(255)
        text('This is a motion controlled Snake game. \n' +
             'You will use <object> to move the snake in \n' +
             'the right direction. When you start the \n' +
             'game, you will see a red dot in the screen \n' +
             'that helps you coordinate better your movements. \n' +
             'When you move the <object> up, down, right, or \n' +
             'left the red dot on the screen will move with you. \n' +
             'To move the snake into the direction you want, \n' +
             'you have to make the corresponding movements. \n' +
             'For moving UP, you need to move the <object> up \n' +
             'as well. The interface will give you a feedback by \n' +
             'lighting up the upper part of the game in red.',300,180)
        textSize(35)
        fill(255)
        text('Play game', 300, 460)
        fill(255)
        
    def move(self, placeAugment, direction):
        self.place += placeAugment
        
        #The case when the snake ate itself
        if self.place in self.body:
            self.lost = True 
        
        #The case when the snake is alive
        if self.lost == False:
            self.body.insert(0, self.place)
            self.checkIfAlive(direction)
            
            if self.lost == False:
                self.board[(self.body[-1])].img = loadImage(path+'/w.jpg')
                self.board[self.place].img = loadImage(path+'/b.jpg')

                if self.board[self.place].v != 'b':
                    self.body.pop()

                elif self.board[self.place].v == 'b':
                    self.t.v = 'w'
                    self.hungry = True
                    self.sound = minim.loadFile(path+'/eating.mp3')
                    self.sound.play()
    
    def checkIfAlive(self, direction):

            if direction == 'R':
                if self.place % self.numCols == 0:
                    self.lost = True
            if direction == 'L':
                if (self.place + 1) % self.numCols == 0:
                    self.lost = True
            if direction == 'U':
                if self.board[self.place].r == (self.numRows - 1):
                    self.lost = True
            if direction == 'D':
                if self.place >= (self.numRows * self.numCols):
                    self.lost = True
    
    def updateSpeed(self):
        
        if len(self.body) == 1 or len(self.body) == 4:
            self.speedControl = 4
        if len(self.body) == 2 or len(self.body) == 5:
            self.speedControl = 3
        if len(self.body) == 3 or len(self.body) == 6:
            self.speedControl = 2
            
    def update(self):
        
        #Moves the snake every time self.speed becomes one
        self.updateSpeed()
        
        if self.speed == 1:
            
            if self.dir == 1:
                self.move(1, 'R')
            elif self.dir == -1:
                self.move(-1, 'L')
            elif self.dir == 2:
                self.move(-self.numCols, 'U')
            elif self.dir == -2:
                self.move(self.numCols, 'D')
            if self.hungry == True:
                self.createFood()
                self.hungry = False
        
        #Using modulo division, the speed of the snake is slowed down
        self.speed = (self.speed + 1) % self.speedControl
        
        if len(self.body) >= 4:
            self.control = "inverse"
            
        #When the player reaches level 6, winning condition is achieved
        if len(self.body) == 6:
            self.won = True
       
    def display(self):
        if self.lost == False:
            self.update()

        for t in self.board:
            image(t.img,t.c*20,t.r*20)
        
        fill(255)
        textSize(80)
        textAlign(CENTER)
        text('MENU',1150,325)
        textSize(40)
        text('return home',1150,400)
        text('play again',1150,475)

        #display gameover image when the player loses
        if self.lost == True:
            image(self.gameoverImg, 70, 40)
            self.state = "gameover"
        
        if self.won == True:
            image(self.winningImg, 70, 40)
            # self.state = "gameover"

        #case to switch up hand-motion control instructions

g = Game(30,50)

def setup():
    global opencv, cam
    
    frameRate(64)
    size(g.numCols*20+320,g.numRows*20)
    background(0)
    g.loadImages()

#size of the canvas is 1320 x 600
    
    cam = Capture(this, 1280, 800)
    opencv = OpenCV(this, 1280, 800)
    opencv.useColor (HSB)
    cam.start()
    
def draw():
    if g.state == 'menu':
        background(0)
        g.menu()
        
    elif g.state == 'play':
        
        # fill(255)
        
        g.display()
        
        #Basic UI feedback on levels and controls
        textSize(20)
        textAlign(LEFT)
        text('Controls: ' + g.control, 15, 30)
        text('Level: ' + str(len(g.body)), 15, 60)
        
    elif g.newgame == True:
        background(0)
        g.__init__(30,50)
        g.loadImages()
        g.menu()
        
    elif g.state == 'directions':
        background(0)
        g.directions()
        
        
    if cam.available():
        cam.read()

    opencv.loadImage(cam);
    opencv.useColor(HSB);
    
    image (cam, 1000,0, 320, 180)
    
    opencv.setGray(opencv.getH().clone())
    opencv.inRange(lowerb, upperb)
    histogram = opencv.findHistogram(opencv.getH(), 255)
    cnts = opencv.findContours()
    
    global recieveNewCommand
    
    if len(cnts) > 0:

        for c in cnts:
            if c.area() > 12000 and (g.state == 'play' or g.state == 'directions'):
                r = c.getBoundingBox()
                xPos = r.x
                yPos = r.y
                
                fill(220,20,60)
                noStroke()  #Dot that indicates where the center of the object is
                ellipse(1000+(xPos + r.width/2) / 4, (yPos + r.height/2) / 4.44, 10/4, 10/4.44)
                ellipse(1000-(xPos), yPos, 10,10)
                
                noFill()
                stroke (255,255,0) #perhaps no ellipse is better
                ellipse(1000+(xPos+r.width/2)/4, (yPos+r.height/2)/4.44, r.width/4, r.height/4.44)
                
                if xPos in range(333,666) and yPos in range(200,400):
                    print("I'M IN THE MIDDLE")
                    drawCenterSafeZone()
                    recieveNewCommand = True
                
                if xPos in range(lLow,lHigh):
                    
                    #Keep drawing the direction indicator
                    drawDirectionIndicator(0, 0, 333, 600)
                    
                    #Allow command to be recieved
                    if recieveNewCommand == True:
                        drawDirectionIndicator(0, 0, 333, 600)
                        print("LEFT")
                        
                        if g.control == "normal":
                            g.dir = -1
                        
                        if g.control == "inverse":
                            g.dir = 1

                        recieveNewCommand = False
                
                if xPos in range(rLow, rHigh):
                    
                    #Keep drawing the direction indicator
                    drawDirectionIndicator(666, 0, 333, 600)
                    
                    if recieveNewCommand == True:
                        drawDirectionIndicator(666, 0, 333, 600)
                        print("RIGHT")
                        
                        if g.control == "normal":
                            g.dir = 1
                        
                        if g.control == "inverse":
                            g.dir = -1
                            
                        recieveNewCommand = False
                    
                if yPos in range(uLow, uHigh):
                    
                    drawDirectionIndicator(0, 0, 1000, 200)
                    
                    if recieveNewCommand == True:
                        drawDirectionIndicator(0, 0, 1000, 200)
                        print("UP")
                        
                        if g.control == "normal":
                            g.dir = 2
                        
                        if g.control == "inverse":
                            g.dir = -2
                            
                        recieveNewCommand = False
                
                if yPos in range(dLow, dHigh):
                    
                    drawDirectionIndicator(0, 400, 1000, 200)
                    
                    if recieveNewCommand == True:
                        drawDirectionIndicator(0, 400, 1000, 200)
                        print("DOWN")
                        
                        if g.control == "normal":
                            g.dir = -2
                        
                        if g.control == "inverse":
                            g.dir = 2
                        
                        recieveNewCommand = False
                    
def drawDirectionIndicator(xFloat, yFloat, boxWidth, boxHeight):
    noStroke()
    fill(220, 20, 60, 30)
    rect(xFloat, yFloat, boxWidth, boxHeight)
    
    #draws the center safe zone while outside of it
    noStroke()
    fill(255, 255, 255, 30)
    rect(333, 200, 333, 200)
    
def drawCenterSafeZone():
    stroke(255)
    noFill()
    rect(333, 200, 333, 200)
    
        
def mouseClicked():
    print(mouseX, mouseY)
    if g.state == 'menu' and 560<=mouseX<=910 and 300<=mouseY<=400:
        g.state = 'play'
    elif g.state == 'menu' and 560<=mouseX<=910 and 200<=mouseY<=300:
        g.state = 'directions'
    elif g.state == 'gameover' and 1000<=mouseX<=1320 and 350<=mouseY<=425:
        g.newgame = True
        minim.stop()
    elif g.state == 'gameover' and 1000<=mouseX<=1320 and 425<=mouseY<=500:
        g.dir = 1
        g.lost = False 
        for t in g.board:
            t.v = 'w'
            t.img = loadImage(path+'/w.jpg')
        g.place = 856
        g.body = [856]
        g.createFood()
        g.hungry = False
        g.sound = minim.loadFile(path+'/eating.mp3')
        g.oversound = minim.loadFile(path+'/gameover.mp3')
        g.state = 'play'
        g.newgame = False
    elif g.state == 'directions' and 300<=mouseX<=470 and 430<=mouseY<=470:
        g.state = 'play'
    elif g.state == 'play' and 1030<= mouseX <= 1270 and 370 <= mouseY <= 400:
        g.state = 'menu'

def keyPressed():
    if keyCode == LEFT:
        g.dir = -1
    elif keyCode == RIGHT:
        g.dir = 1
    elif keyCode == DOWN:
        g.dir = -2
    elif keyCode == UP:
        g.dir = 2