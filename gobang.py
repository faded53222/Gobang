import pygame
import sys
import time
import random
GREY=(111,111,111)
WHITE=(255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = (800,800)
game_size=(15,15)
cube_height=screen_size[0]/game_size[0]
cube_width=screen_size[1]/game_size[1]
chess_vec1=[]
chess_vec2=[]
candidate_pos_list1=[]
candidate_pos_list2=[]
pos_dic={}
class one_pos():
	def __init__(self,pos_x,pos_y):
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.occupied=0
		self.from_count=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
		self.neighbor_pos=[(pos_x,pos_y+1),(pos_x+1,pos_y+1),(pos_x+1,pos_y),(pos_x+1,pos_y-1),(pos_x,pos_y-1),(pos_x-1,pos_y-1),(pos_x-1,pos_y),(pos_x-1,pos_y+1)]
	def occupy(self,occupied):
		self.occupied=occupied
		if self in candidate_pos_list1:
			candidate_pos_list1.remove(self)
		if self in candidate_pos_list2:
			candidate_pos_list2.remove(self)
		for i in range(len(self.neighbor_pos)):
			if self.neighbor_pos[i][0]>=0 and self.neighbor_pos[i][0]<game_size[0] and self.neighbor_pos[i][1]>=0 and self.neighbor_pos[i][1]<game_size[1]:
				count_sum=self.from_count[occupied-1][i]+self.from_count[occupied-1][(i+4)%8]+1
				if pos_dic[self.neighbor_pos[i]].occupied==0:
					pos_dic[self.neighbor_pos[i]].from_count[occupied-1][i]=count_sum
				if pos_dic[self.neighbor_pos[i]].occupied==occupied:
					dt_x=self.neighbor_pos[i][0]-self.pos_x
					dt_y=self.neighbor_pos[i][1]-self.pos_y
					for j in range(2,max(game_size[1],game_size[1])):
						temp_pos=(self.pos_x+j*dt_x,self.pos_y+j*dt_y)
						if temp_pos[0]<0 or temp_pos[0]>=game_size[0] or temp_pos[1]<0 or temp_pos[1]>=game_size[1]:
							break 
						if pos_dic[temp_pos].occupied==occupied:
							continue
						if pos_dic[temp_pos].occupied==0:							
							pos_dic[temp_pos].from_count[occupied-1][i]=count_sum
						break
		for i in range(4):
			if self.from_count[occupied-1][i]+self.from_count[occupied-1][(i+4)%8]>=4:
				return 1			
def draw_lines(screen):
	for i in range(1,game_size[0]):
		pygame.draw.aaline(screen, WHITE,(i*cube_height,0),(i*cube_height,screen_size[1]),5)
	for i in range(1,game_size[1]):
		pygame.draw.aaline(screen, WHITE,(0,i*cube_width),(screen_size[0],i*cube_width),5)
def draw_cubes(screen):
	for each in chess_vec1:
		pygame.draw.rect(screen,[255,255,255],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
	for each in chess_vec2:
		pygame.draw.rect(screen,[0,0,0],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
if __name__ == "__main__":
	for i in range(game_size[0]):
		for j in range(game_size[1]):
			a_pos=one_pos(i,j)
			pos_dic[(i,j)]=a_pos
	pygame.init()
	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption("gobang")
	FPS=30
	clock = pygame.time.Clock()
	turn=0
	win_lab=0
	while True:
		clock.tick(FPS)
		if pygame.mouse.get_pressed()[0] and win_lab==0:
		#if pygame.mouse.get_pressed()[0]:
		#when you delete 'and win_lab==0' game won't end after someone win,so you can fullfill the screem for fun
			pos=pygame.mouse.get_pos()
			pos_=(int(pos[1]/cube_height),int(pos[0]/cube_width))
			if pos_dic[pos_].occupied==0:
				if turn==0:
					chess_vec1.append(pos_)
				if turn==1:
					chess_vec2.append(pos_)
				win_detect=pos_dic[pos_].occupy(turn+1)
				if win_detect==1:
					print('player',turn+1,' win')
					win_lab=1
				turn=(turn+1)%2
		screen.fill(GREY)
		draw_lines(screen)
		draw_cubes(screen)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
