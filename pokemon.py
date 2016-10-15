#coding:utf-8
import pygame, sys
from pygame.locals import *
import ctypes  # An included library with Python install.
import random

red = (255,  0,  0)

width = 640
height = 480
p_height = 105
p_width = 70
px = (width - p_width) / 2
py = height - p_height
jwstate = 0 #지우상태(이미지)
enemys_cols = 4
enemys_rows = 8
enemyWidth = 44
enemyHeight = 50
enemyPadding = 20
enemyOffsetTop = 30
enemyOffsetLeft = 25
elh = 62 #상대레이저height
dely = 2 #상대레이저속도
el_width = 27 #상대레이저이미지 가로사이즈
el_height = 62 #상대레이저이미지 세로사이즈
de = 0 #적 움직이는 방향
dly = 2 #내 레이저 속도
keys = [False, False,False]
enemys = []
level = 1
bullets = []
bangs = []
life = 3
h_width = 30
lifes = []
finaltime = pygame.time.get_ticks()
wait = 250
lifecheck = False #lifes함수를 삭제하고 life변수값을 내리기위해
level = 1
count = enemys_cols*enemys_rows
gamestate = 1
lazersize = 20 #내 레이저 이미지 크기
lasthp = 25

jiwoo=pygame.image.load("jw.png")
jiwoo2=pygame.image.load("jw2.png")
fika=pygame.image.load("fika.png")
vapo=pygame.image.load("vapo.png")
arc=pygame.image.load("arceus.png")
pkb=pygame.image.load("pokeball.png")
elec=pygame.image.load("elec.png")
elec2=pygame.image.load("elec2.png")
elec3=pygame.image.load("elec3.png")
heart=pygame.image.load("heart.png")
gameover=pygame.image.load("gameover.jpg")
bg1=pygame.image.load("bg1.jpg")
bg2=pygame.image.load("bg2.jpg")
bg3=pygame.image.load("bg3.png")
lv1=pygame.image.load("lv1.png")
lv2=pygame.image.load("lv2.png")
lv3=pygame.image.load("lv3.png")
clear=pygame.image.load("clear.jpg")

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('pokemon_INVADER')

pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1,0.0)

fontObj = pygame.font.SysFont('Courier',20)

def enemysInit():
	global enemys_cols, enemys_rows, enemyWidth, enemyHeight, enemyPadding, enemyOffsetTop, enemyOffsetLeft

	for r in range(enemys_rows):
		for c in range(enemys_cols):
			state = 1
			x = enemyOffsetLeft + r*(enemyPadding + enemyWidth)
			y = enemyOffsetTop + c*enemyHeight
			oneenemy = [x, y, state]
			enemys.append(oneenemy)

def drawenemys(enemy):
	global enemys
	for e in enemys:
		if e[2] == 1 :
			screen.blit(enemy,(e[0],e[1]))

def enemymove(wall,sp):
	global enemys_cols, enemys_rows, enemyWidth, enemyHeight, enemyPadding, enemyOffsetTop, enemyOffsetLeft, de
	if(enemys[0][0] < 0):
		de = 0
	if(enemys[wall][0]+enemyWidth > width):
		de = 1
	for b in enemys:
		if(de == 1):
			b[0] = b[0]-sp
		if(de == 0):
			b[0] = b[0]+sp

def banginit(n):
	global elx,ely,elh,bang,enemys
	i = random.randrange(0,n)
	state = True
	x = enemys[i][0]+2
	y = 180
	el=[x,y,state]
	bangs.append(el)

def drawbang(png):
	global bangs,dely
	for b in bangs:
		if(b[2] == True):
			b[1] += dely
			screen.blit(png,(b[0],b[1]))
		if( b[1] >= height):
			b[2] = False
			bangs.remove(b)

def drawpaddle(x, y):
	global p_width,p_height
	pygame.draw.rect(screen, red, [x, y, p_width, p_height], 2)
	if(jwstate==0):
		screen.blit(jiwoo,(x,y))
	if(jwstate==1):
		screen.blit(jiwoo2,(x,y))

def lazerinit():
	global px,py,bullets,wait,finaltime,jwstate
	if (pygame.time.get_ticks() - finaltime >= wait):
		state = True
		x = px + 40
		y = py + 40
		lz=[x,y,state]
		bullets.append(lz)
		jwstate=1
		finaltime = pygame.time.get_ticks()

def drawlazer():
	global bullets,dly
	for b in bullets:
		if(b[2] == True):
			b[1] -= dly
			#pygame.draw.circle(screen , GREEN, (b[0], b[1]), 7, 0)
			screen.blit(pkb,(b[0],b[1]))
		if( b[1] <= 0):
			b[2] = False
			bullets.remove(b)

def lifeInit():
	global life,heart,width,h_width
	for l in range(life): #0,1,2
		state = 1
		x = width - h_width - l*h_width
		y = 0
		alife = [x, y, state]
		lifes.append(alife)

def drawlifes():
	global life,heart,width,h_width,r_width,lifecheck
	for l in lifes:
		if lifecheck == True:
			lifes.remove(l)
			lifecheck = False
		if l[2] == 1:
			screen.blit(heart,(l[0],l[1]))

def mecrush():
	global bangs,p_width,p_height,px,py,lifes,enemyWidth,enemyHeight
	global el_width,el_height,life,lifecheck,enemys,bullets,count,level,lasthp
	for b in bangs:
		#print life
		me = pygame.Rect(px, py, p_width, p_height)
		objbang = pygame.Rect(b[0],b[1],el_width,el_height)
		if me.colliderect(objbang):
			#b[2] = False
			bangs.remove(b)
			lifecheck = True
			life -= 1
	for b in bullets:
		na = pygame.Rect(b[0],b[1]+2,lazersize,lazersize - 4)#+2,-4 : 히트박스 크기 축소 =list오류 해결
		for e in enemys:
			if(e[2] == 1):
				monster = pygame.Rect(e[0],e[1]+8,enemyWidth,enemyHeight-16)#+8,-16:히트박스 크기 축소
				if na.colliderect(monster):
					if(level == 1 or level == 2):
						e[2] = 0
						#enemys.remove(e) <<remove를 하면 e[0],e[28]이 삭제되기문에 왔다갔다 못함
						#b[2] = 0
						bullets.remove(b)
						count -= 1
					if level == 3:
						bullets.remove(b)
						lasthp -= 1

def hpdraw():
	global lasthp
	pygame.draw.rect(screen, red, [40, 20, lasthp*20, 20], 0)

enemysInit()
lifeInit()
lasttime = pygame.time.get_ticks()
waittime = random.randrange(500,1000)
while True:
	if level == 1:
		screen.blit(bg1,(0,0))
		screen.blit(lv1,(width-70,40))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_LEFT:
					keys[0] = True
				elif event.key == K_RIGHT:
					keys[1] = True
				elif event.key == K_SPACE:
					lazerinit()

			if event.type == pygame.KEYUP:
				if event.key == K_LEFT:
					keys[0] = False
				elif event.key == K_RIGHT:
					keys[1] = False
				elif event.key == K_SPACE:
					keys[2] = False
					jwstate=0

		if (keys[0] == True):
			px -= 3
			if (px < 0):
				px += 3
		if (keys[1] == True):
			px += 3
			if (px + p_width > width):
				px -= 3

		if (pygame.time.get_ticks() - lasttime >= waittime):
			banginit(32)
			lasttime =  pygame.time.get_ticks()
			waittime = random.randrange(500,1000)

		if life == 0:
			break

		drawlifes()
		mecrush()
		drawbang(elec)
		drawlazer()
		drawenemys(fika)
		drawpaddle(px,py)
		pygame.display.update()
		enemymove(28,0.4)

		if count == 0:
			dely = 1
			del bullets[:]
			bullets = []
			del enemys[:]
			enemys = []
			del bangs[:]
			bangs = []
			enemyWidth = 48
			enemys_cols = 4
			enemys_rows = 6
			enemyPadding = 35
			del lifes[:]
			lifes = []
			life = 3
			lifeInit()
			enemysInit()
			lasttime = pygame.time.get_ticks()
			waittime = random.randrange(500,1000)
			count = enemys_cols*enemys_rows
			level = 2



	if level == 2:
		screen.blit(bg2,(0,0))
		screen.blit(lv2,(width-70,40))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_LEFT:
					keys[0] = True
				elif event.key == K_RIGHT:
					keys[1] = True
				elif event.key == K_SPACE:
					lazerinit()

			if event.type == pygame.KEYUP:
				if event.key == K_LEFT:
					keys[0] = False
				elif event.key == K_RIGHT:
					keys[1] = False
				elif event.key == K_SPACE:
					keys[2] = False
					jwstate=0

		if (keys[0] == True):
			px -= 3
			if (px < 0):
				px += 2
		if (keys[1] == True):
			px += 3
			if (px + p_width > width):
				px -= 3

		if (pygame.time.get_ticks() - lasttime >= waittime):
			banginit(24)
			lasttime =  pygame.time.get_ticks()
			waittime = random.randrange(500,1000)

		if life == 0:
			break

		drawlifes()
		mecrush()
		drawbang(elec2)
		drawlazer()
		drawenemys(vapo)
		drawpaddle(px,py)
		pygame.display.update()
		enemymove(21,0.4)

		if count == 0:
			del bullets[:]
			bullets = []
			del enemys[:]
			enemys = []
			del bangs[:]
			bangs = []
			enemyWidth = 201
			enemyHeight = 200
			enemys_cols = 1
			enemys_rows = 1
			enemyPadding = 0
			el_width = 50
			el_height = 49
			del lifes[:]
			lifes = []
			life = 3
			lifeInit()
			enemysInit()
			lasttime = pygame.time.get_ticks()
			waittime = random.randrange(500,1000)
			level = 3


	if level == 3:
		screen.blit(bg3,(0,0))
		screen.blit(lv3,(width-70,40))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_LEFT:
					keys[0] = True
				elif event.key == K_RIGHT:
					keys[1] = True
				elif event.key == K_SPACE:
					lazerinit()

			if event.type == pygame.KEYUP:
				if event.key == K_LEFT:
					keys[0] = False
				elif event.key == K_RIGHT:
					keys[1] = False
				elif event.key == K_SPACE:
					keys[2] = False
					jwstate=0

		if (keys[0] == True):
			px -= 3
			if (px < 0):
				px += 2
		if (keys[1] == True):
			px += 3
			if (px + p_width > width):
				px -= 3

		if (pygame.time.get_ticks() - lasttime >= waittime):
			banginit(1)
			lasttime =  pygame.time.get_ticks()
			waittime = random.randrange(1000,1500)

		if life == 0:
			break

		drawlifes()
		hpdraw()
		mecrush()
		drawbang(elec3)
		drawlazer()
		drawenemys(arc)
		drawpaddle(px,py)
		pygame.display.update()
		enemymove(0,2)

		if lasthp <= 0:
			pygame.mixer.init()
			pygame.mixer.music.load("endm.mp3")
			pygame.mixer.music.play(-1,0.0)
			while True:
				screen.blit(clear,(0,0))
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						sys.exit()

pygame.mixer.init()
pygame.mixer.music.load("end.mp3")
pygame.mixer.music.play(-1,0.0)
screen.blit(gameover,(0,0))
pygame.display.update()
pygame.time.delay(4000)
pygame.quit()
sys.exit()
