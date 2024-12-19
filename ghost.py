
from random import random
from shutil import move
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
import random

class Ghosts(object):
    def __init__(self, nodes, amount):
        self.ghosts_list = list()
        for i in range(0,amount):
            rand_node = random.randint(0, len(nodes)-1)
            self.ghosts_list.append(Ghost(nodes[rand_node], i, random.randint(0,3)))
            
    def update_ghosts(self, dt, pacman):
        for ghost in self.ghosts_list:
            ghost.update(dt, pacman)

    def render_ghosts(self, screen):
        for ghost in self.ghosts_list:
            ghost.render(screen)

class Ghost(object):
    def __init__(self, node, ghost_number, ghost_type):
        self.name = "Ghost"+str(ghost_number)
        self.directions = {UP:Vector2(0, -1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0), STOP:Vector2()}
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        if ghost_type == 0:
            self.color = GREEN
        elif ghost_type == 1:
            self.color = BLUE
        elif ghost_type == 2:
            self.color = CYAN
        else:
            self.color = PINK
        self.node = node
        self.initial_node = node
        self.setPosition()
        self.target = node
        self.cur_move_index=0
        self.ghost_type = ghost_type

    def setPosition(self):
        self.position = self.node.position.copy()

    def respawn(self, pacman):
        self.node = self.initial_node
        self.setPosition()
        self.direction = STOP
        self.target = self.node
        self.cur_move_index = self.ghost_move_index(pacman)

    def distance_from_pac(self, pacman):
        distance = round(((self.position.x - pacman.position.x)**2 + (self.position.y - pacman.position.y)**2)**0.5)
        return distance

    def random_move(self):
        direction_list = [-1, 1, -2, 2]
        move_index = random.randint(0,3)
        while self.node.neighbors[direction_list[move_index]] == None:
           move_index = random.randint(0,3)
        return move_index
        
    def BFS_first_move(self, target_node):
        queue = []
        visited = dict()
    
        node = self.node
        queue.append(node)
        visited[node] = None

        first = None
        while queue:
            current_node = queue.pop(0)
        
            for neighbor in current_node.neighbors.values():
                if neighbor and neighbor not in visited:
                    visited[neighbor] = current_node
                
                    if neighbor == target_node:
                        first_move = neighbor
                        while visited[first_move] != self.node:
                            first_move = visited[first_move]
                        first = first_move

                    queue.append(neighbor)
    
        return first



    def follow_pacman(self, pacman):
        direction_list = [-1, 1, -2, 2]
        #losowo wybiera czy idzie w poziomie czy w pionie
        choice = random.randint(0,1)
        move_index = 0
        found = False

        #patrzy czy jest w nodzie startowym pacmana, jesli nie to do niego idzie, jesli tak to idzie juz w kierunku pac mana
        if pacman.node != self.node:
            target_node = self.BFS_first_move(pacman.node)
            for i in range(1,4):
                if self.node.neighbors[direction_list[move_index]] != None:
                    if self.node.neighbors[direction_list[move_index]] == target_node:
                        found=True
                        break
                    else:
                        move_index=i
            if found!=True:
                move_index = self.random_move()
        else:
            choice_made = False
            iteration=0
            while choice_made==False:
                if iteration < 3:
                    if choice == 0:
                        if self.position.x > pacman.node.position.x:
                            move_index = 3
                        elif self.position.x < pacman.node.position.x:
                            move_index = 2  
                    
                        if self.node.neighbors[direction_list[move_index]] != None:
                            choice_made=True
                        else:
                            choice = 1

                    else:
                        if self.position.y > pacman.node.position.y:
                            move_index = 1
                        elif self.position.y < pacman.node.position.y:
                            move_index = 0  
                    
                        if self.node.neighbors[direction_list[move_index]] != None:
                            choice_made=True
                        else:
                            choice = 0
                else: #jak nie moze pojsc za nim wg schematu to idzie w losowym dostępnym kierunku
                    move_index = self.random_move()
                    choice_made=True
                iteration+=1
            
        return move_index


    def front_pacman(self, pacman):
        direction_list = [-1, 1, -2, 2]
        #losowo wybiera czy idzie w poziomie czy w pionie
        choice = random.randint(0,1)
        move_index = 0
        found = False
        
       #patrzy czy jest w nodzie docelowym pacmana, jesli nie to do niego idzie, jesli tak to idzie juz w kierunku pac mana
        if pacman.target != self.node:
            target_node = self.BFS_first_move(pacman.target)
            for i in range(1,4):
                if self.node.neighbors[direction_list[move_index]] != None:
                    if self.node.neighbors[direction_list[move_index]] == target_node:
                        found=True
                        break
                    else:
                        move_index=i
            if found!=True:
                move_index = self.random_move()
            
        else:
            choice_made = False
            iteration=0
            while choice_made==False:
                if iteration < 3:
                    if choice == 0:
                        if self.position.x > pacman.target.position.x:
                            move_index = 3
                        elif self.position.x < pacman.target.position.x:
                            move_index = 2  
                    
                        if self.node.neighbors[direction_list[move_index]] != None:
                            choice_made=True
                        else:
                            choice = 1

                    else:
                        if self.position.y > pacman.target.position.y:
                            move_index = 1
                        elif self.position.y < pacman.target.position.y:
                            move_index = 0  
                    
                        if self.node.neighbors[direction_list[move_index]] != None:
                            choice_made=True
                        else:
                            choice = 0
                else: #jak nie moze pojsc do niegp wg schematu to idzie w losowym dostępnym kierunku
                    move_index = self.random_move()
                    choice_made=True
                iteration+=1
                
        return move_index
                                    
            
            
    def ghost_move_index(self, pacman):
        direction_list = [-1, 1, -2, 2]
        move_index = random.randint(0,3)

        if self.ghost_type == 0: #typ 0 - jak pacman daleko to losowo, jak blisko to do niego  
            if self.distance_from_pac(pacman) > 400:
                while self.node.neighbors[direction_list[move_index]] == None:
                    move_index = random.randint(0,3)
            else:
                move_index = self.follow_pacman(pacman)
                
        elif self.ghost_type == 1: #typ 1 - zawsze do pacmana
            move_index = self.follow_pacman(pacman)
        elif self.ghost_type == 2: #typ 2  - przed pacmana    
            move_index = self.front_pacman(pacman)
        else:
            move_index = self.random_move()        
        return move_index

    def update(self, dt, pacman):
        random_direction_list = [-1, 1, -2, 2]

        self.position += self.directions[random_direction_list[self.cur_move_index]]*self.speed*dt
        
        # direction = self.directions[random_direction_list[self.cur_random_index]]
        if self.overshotTarget():
            self.node = self.target
            self.cur_move_index = self.ghost_move_index(pacman)
            self.target = self.node.neighbors[random_direction_list[self.cur_move_index]]
            self.direction = self.directions[random_direction_list[self.cur_move_index]]
            self.setPosition()  

    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    #sprawdza czy pacman minal wezel docelowy, do ktorego sie zbliza
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
