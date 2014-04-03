import pygame, sys
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
MAXSPEED = 7
JUMPSPEED = -12
clock = pygame.time.Clock()

def main():
	#variables
	global DISPLAYSURF
	speed = 0
	gravity = 1
	milliseconds = 0
	mousex = 0
	mousey = 0
	xPrime = 0
	yPrime = 0
	mousePress = False
	targetLocked = False
	moveRight = False
	moveUp = False
	moveDown = False
	moveLeft = False
	redTarget = Target(40,570, 30, 30, RED)
	obstacles = []
	obstacles.append(Target(120, 570, 30, 30, BLUE))
	obstacles.append(Target(180, 520, 30, 80, BLUE))
	obstacles.append(Target(120, 300, 100, 30, BLUE))
	tarHand = TargetHandler()

	
	#pygameInit
	pygame.init()
	
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption ('Necromancer!!')
	while True:
		DISPLAYSURF.fill(WHITE)
		#Event Handler
		for event in pygame.event.get():
			if event.type == QUIT:
					pygame.quit()
					sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_w:
					moveUp = True
				if event.key == K_s:
					moveDown = True
				if event.key == K_d:
					moveRight = True
				if event.key == K_a:
					moveLeft = True										
			elif event.type == KEYUP:
				if event.key == K_w:
					moveUp = False
				if event.key == K_s:
					moveDown = False
				if event.key == K_d:
					moveRight = False
				if event.key == K_a:
					moveLeft = False			
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONDOWN:
				mousex, mousey = event.pos
				mousePress = True
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mousePress = False
				
		#Code to carry the target with the mouse	
		if mousePress:
			if tarHand.checkMouseCollision(redTarget, mousex, mousey):
				if not targetLocked:
					xPrime = mousex
					yPrime = mousey
					print "X and Y prime set"
				targetLocked = True
				redTarget.setColor(BLUE)
		else:
			targetLocked = False
			redTarget.setColor(RED)

		if targetLocked:
			redTarget.setX(mousex - xPrime + redTarget.getX())
			redTarget.setY(mousey - yPrime + redTarget.getY())
			xPrime = mousex
			yPrime = mousey
		else:
			speed = speed + gravity
			if speed > MAXSPEED:
				speed = MAXSPEED
			tarHand.move(redTarget, obstacles, 0, speed)
		
		#Receives user input and moves block
		if moveRight:
			tarHand.move(redTarget, obstacles, 3, 0)
		if moveDown:
			tarHand.move(redTarget, obstacles, 0, 3)
		if moveUp:
			speed = JUMPSPEED
			tarHand.move(redTarget, obstacles, 0, speed)
			moveUp = False
		if moveLeft:
			tarHand.move(redTarget, obstacles, -3, 0)
			
		#Elements in game are drawn	
		redTarget.display()
		for obstacle in obstacles:
			obstacle.display()
		#Updates display
		pygame.display.update()
		milliseconds += clock.tick_busy_loop(60)
			

class Target:
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		return

	def display(self):
		pygame.draw.rect(DISPLAYSURF, self.color, (self.x, self.y, self.width, self.height))
		return
		
	def getRect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)

	
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
	def getColor(self):
		return self.color	
	def getRight(self):
		return self.x + self.width
	def getBottom(self):
		return self.y + self.height
		
	def setColor(self, color):
		self.color = color
		return
	def setX(self, x):
		self.x = x
		return
	def setY(self, y):
		self.y = y
	def setWidth(self, width):
		self.width = width
	def setHeight(self, height):
		self.height = height
	
class TargetHandler:
	def checkMouseCollision(self, target, x, y):
		targetRect = target.getRect()
		return targetRect.collidepoint(x, y)
	
	
	def move(self, target, obstacles, x, y):
		oldX = target.getX()
		oldY = target.getY()
		newX = x + target.getX()
		newY = y + target.getY()
		targetLeft = False
		targetRight = False
		targetTop = False
		targetBottom = False
		
		if newY > HEIGHT - target.getHeight():
			target.setY(HEIGHT - target.getHeight())
		elif newY < 0:
			target.setY(0)
		else:
			target.setY(newY)
				
		if newX > WIDTH - target.getWidth():
			target.setX(WIDTH - target.getWidth())
		elif newX < 0:
			target.setX(0)
		else:
			target.setX(newX)
			
		for obstacle in obstacles:
			if newX + target.getWidth()  <= obstacle.getX() + MAXSPEED:
				targetLeft = True
			elif newX + MAXSPEED >= obstacle.getRight():
				targetRight = True
			if newY + target.getHeight() <= obstacle.getY() + MAXSPEED:
				if target.getRight() > obstacle.getX() and target.getX() < obstacle.getRight():
					targetTop = True
			elif newY >= obstacle.getBottom() + JUMPSPEED:
				if target.getRight() > obstacle.getX() and target.getX() < obstacle.getRight():
					targetBottom = True				
			
			if targetTop:
				if newY + target.getHeight() > obstacle.getY():
					target.setY(obstacle.getY() - target.getHeight())
			elif targetBottom:
				if newY < obstacle.getBottom():
					target.setY(obstacle.getBottom())			
			elif targetLeft:
				if newX + target.getWidth() > obstacle.getX():
					target.setX(obstacle.getX() - target.getWidth())
			elif targetRight:
				if newX < obstacle.getRight():
					target.setX(obstacle.getRight())

			targetLeft = False
			targetRight = False
			targetTop = False	
			targetBottom = False		

		
		return

		
if __name__ == '__main__':
    main()


