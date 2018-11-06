# ---------------------------------------------------------------------------------------------------#
# Program Name: PAINT PROGRAM OOP ASSIGNMENT
# Programmer: Nick Tkachov
# Date: November 20, 2017
# Input: Options at the beginning of the game allow user to select SMALL,MEDIUM,LARGE grid sizes,
#           and grid or no grid. After that, the options are entered
#           and the user is allowed to draw using the various tools available:
#           BRUSH, FILL, ERASE - SIZES 1-5 - COLOR PALLET WITH 9 COLORS
# Processing: User inputs are processed, from the cell that they click on to the various
#             menu options that are selected. User save and load is also calculated
#             by parsing text file
# Output: Any changes made to the screen are instantly drawn in the loop
# ----------------------------------------------------------------------------------------------------#

#Class Cell(object)
#   Attributes:
#   height,width,x,y,color,border,row,column,rect
#
#
#   Methods:
#   draw()
#   on_mouse_hover()

#Class Grid(object)
#   Attributes:
#   color,screen_size,rows,columns,class_type,x,y,gap,height,width,cells,count
#
#
#   Methods:
#   draw()
#   draw_cells()
#   find_cell()

#Class Text_Render(object)
#   Attributes:
#   screen_size,surf,x,y,text,size,font,render
#
#
#   Methods:
#   draw()


#Class Menu(Cell)
#   Attributes:
#   same as cell +...
#   text,data,hint,font,render,selected
#
#
#   Methods:
#   draw()
#   on_mouse_click

#Class Pixel(Cell)
#   Attributes:
#   same as cell
#   
#
#
#   Methods:
#   on_mouse_click

#Class Tool_Load(Menu)
#   Attributes:
#   same as menu
#
#
#
#   Methods:
#   on_mouse_click + menu methods

#Class Tool_Load(Menu)
#   Attributes:
#   same as menu
#
#
#
#   Methods:
#   on_mouse_click + menu methods

#Class Menu_Grid(Grid)
#   Attributes:
#   same as menu +..
#   options,count,font,w,h,surf
#
#
#   Methods:
#   check_event,draw + grid methods

#Class Pallet(Menu_Grid)
#   Attributes:
#   same as Menu_Grid
#   
#
#
#   Methods:
#   draw

#Class PixelArt(Grid)
#   Attributes:
#   same as Grid
#   
#
#
#   Methods:
#   draw_grid
#   set_grid
#   check_event()



import pygame
from grid import Grid,Cell
from math import sqrt
from sys import exit

def fill(cell, grid, color, c): #Fill algorithm using recursion
    if cell.color == color and cell.color != c: #if color that you clicked on is not already that color AND is the same color as others
        cell.color = c
        cell.border = 0
        x = cell.row               #row of cell
        y = cell.column            #column of cell 
        if x < grid.rows-1:        #right
            fill(grid.find_cell(x+1,y), grid, color, c)     #fills squares to the right, same for ones on bottom
        if x > 0:                  #left
            fill(grid.find_cell(x-1,y), grid, color, c)
        if y < grid.columns-1:     #up
            fill(grid.find_cell(x,y+1), grid, color, c)
        if y > 0:                  #down
            fill(grid.find_cell(x,y-1), grid, color, c)

def draw_brush(cell,grid,c,amount):
    if cell.color != c:
        cell.color = c
        cell.border = 0
        x = cell.row
        y = cell.column
        if x < amount and x > -amount:     #right
            fill(grid.draw_brush(x+1,y), grid, c, amount)
        if x > amount and x < -amount:     #left
            fill(grid.draw_brush(x-1,y), grid, c, amount)
        if y < amount and y > -amount:     #up
            fill(grid.draw_brush(x,y+1), grid, c, amount)
        if y > amount and y < -amount:     #down
            fill(grid.draw_brush(x,y-1), grid, c, amount)
    
def set_cursor(screen,brush,tool): #allows for cursor to have custom shape
    x,y = pygame.mouse.get_pos()
    dynamic = brush_size * 10      #depending on brush size, the circle or square will be bigger
    if tool == 'ERASE':            #draws a square for erase  
        pygame.draw.rect(screen,WHITE,((x - (dynamic) /2,y - (dynamic) /2),(dynamic,dynamic)))
        pygame.draw.rect(screen,BLACK,((x - (dynamic) /2,y - (dynamic) /2),(dynamic,dynamic)),2)
    elif tool == 'FILL':           #draws a rectangle for fill  
        pygame.draw.rect(screen,brush,((x-10,y-5),(20,10)))
        pygame.draw.rect(screen,BLACK,((x-10,y-5),(20,10)),2)
    else:                          #draws a circle for brush
        pygame.draw.ellipse(screen,brush,((x - (dynamic) /2,y - (dynamic) /2),(dynamic,dynamic)))
        pygame.draw.ellipse(screen,BLACK,((x - (dynamic) /2,y - (dynamic) /2),(dynamic,dynamic)),2)

class Text_Render(object):
    def __init__(self,screen_size,x,y,text=None,size= 20):                      #text render class, allows text to be drawn
        self.screen_size = screen_size
        self.surf = pygame.Surface((self.screen_size[0],self.screen_size[1]))   
        self.surf.set_alpha(200)
        self.surf.fill((100,100,100))
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont("Arial", self.size, True)
        self.render = self.font.render(str(self.text),True,WHITE)
        
    def draw(self,surface):       #centers text                                         
        screen.blit(self.surf,(self.x,self.y))
        if self.text is not None:
            surface.blit(self.render,(self.screen_size[0]/2 - self.render.get_width()/2 + self.x
                                    ,(self.screen_size[1]/2 - self.render.get_height()/2) + self.y))

            
class Menu(Cell):                   #Menu pixel class, derived from cell
    def __init__(self,x,y,width,height,color,option=(None,None),font = 50):
        super().__init__(x,y,width,height,color)
        self.text = option[0]       #allows for custom text and data when clicked
        self.data = option[1]
        self.selected = False
        try: self.hint = option[2]  #a secret third option exists for text hints
        except: self.hint=self.data
        self.font = font
        self.hint_text = Text_Render([170,30],0,0,str(self.hint),25) #draws hint text
        if self.text is not None:                                    #if data exists, will print text, else will have just squares
            self.font = pygame.font.SysFont("Arial", self.font, False)
            self.render = self.font.render(str(self.text),True,WHITE)

    def draw(self,surface):
        if self.text is not None:   #will draw text if text is not set as none value
            surface.blit(self.render,(self.rect.width/2 - self.render.get_width()/2 + self.rect.x
                                    ,(self.rect.height/2 - self.render.get_height()/2) + self.rect.y))
        else:
            pygame.draw.rect(surface,self.color,self.rect,0) #else will draw a filled in square instead of empty (used for color pallet)
        pygame.draw.rect(surface,(255,255,255),self.rect,3)  #white border
        
        if self.selected:
            pygame.draw.rect(surface,(255,0,0),self.rect,5)
            
        self.hint_text.x, self.hint_text.y = pygame.mouse.get_pos() #positions hint on mouse
        if self.on_mouse_hover():
            self.hint_text.draw(surface)
            
    def on_mouse_click(self,others): #allows for a red selection box
        if self.on_mouse_hover():
            for x in others: x.selected = False 
            self.selected = True
        return self.on_mouse_hover()

class Tool_Save(Menu):              #save tool used to save paints
    def on_mouse_click(self,others):
        if self.on_mouse_hover():
            with open('data.txt','w') as file:
                for x in pixel_grid.cells:
                   file.write(str(x.color) + '\n') 
            
class Tool_Load(Menu):              #loads paints
    def on_mouse_click(self,others):
        if self.on_mouse_hover():
            grid = [eval(x) for x in open('data.txt','r')] 
            pixel_grid.set_grid(int(sqrt(len(grid))))
            for i,v in enumerate(grid):
                pixel_grid.cells[i].color = v
                if v != WHITE:
                    pixel_grid.cells[i].border = 0
                else:
                    if drawing_grid: pixel_grid.cells[i].border = 1
                    else:
                        pixel_grid.cells[i].border = 0
                        pixel_grid.cells[i].color = BLACK
            
class Menu_Grid(Grid):              #a different version of grid that allows for drawing of a transparent BG & selection boxes
    def __init__(self,screen_size,rows,columns,class_type,options,x=0,y=0,gap=0,w=100,h=100,font = 50):
        self.options = options
        self.count = 0
        self.font = font
        self.w = w
        self.h = h
        super().__init__(screen_size,rows,columns,class_type,x,y)       
        self.surf = pygame.Surface((self.screen_size[0],self.screen_size[1]))
        self.surf.set_alpha(200)        #draws transparent BG
        self.surf.fill((100,100,100))
        
    def draw_cells(self):
        p = []
        for x in range(self.rows):
            for v in range(self.columns):
                p.append(self.class_type((self.screen_size[0] - (self.w * self.columns))/2 + (((self.w * v)) + self.x)
                                         ,(self.screen_size[1] - (self.h * self.rows))/2 + (((self.h * x)) + self.y)
                                         ,self.w,self.h
                                         ,self.color, self.options[self.count], self.font))
                if self.count == 0:     #first item in list is always selected
                    p[0].selected = True
                self.count +=1
        return p
                
    def draw(self,surface): 
        screen.blit(self.surf,(self.x,self.y))
        for x in self.cells:
            if x.selected: #if one of the buttons is selected,
                self.cells += [self.cells.pop(self.cells.index(x))] #will be placed at the last spot in table so boxes don't overlap
            x.draw(surface)

    def check_event(self,old=0):    #returns the value of the current selected cell
        for x in self.cells:
            if x.on_mouse_click(self.cells):
                return x.data
        return old

class Pixel(Cell):                  #cell object that can be brushed over
    def on_mouse_click(self,new_color,brush,grid,cells,brush_size):
        if self.on_mouse_hover():           
            if brush == 'BRUSH':    #if its brush, do color
                self.color = new_color
                self.border = 0
                if brush_size > 1:
                    draw_brush(self,cells,new_color,brush_size) #allows for different brush sizes
            elif brush == 'ERASE':  #erases pixel depending on if it has grid or not
                if grid:
                    self.color = WHITE
                    self.border = 1
                else:
                    self.color = BLACK
                    self.border = 0
            elif brush == 'FILL': #fill recursion algorithm
                fill(self,cells,self.color,new_color)
            
class Pallet(Menu_Grid):          #pallet class derived from grid (to allow red selection box)
    def draw_cells(self):
        p = []
        for x in range(self.rows):
            for v in range(self.columns):
                p.append(self.class_type((self.screen_size[0] - (self.w * self.columns))/2 + (((self.w * v)) + self.x)
                                         ,(self.screen_size[1] - (self.h * self.rows))/2 + (((self.h * x)) + self.y)
                                         ,self.w,self.h, self.options[self.count][1],self.options[self.count])) #the only difference is that this one allows color
                if self.count == 0:
                    p[0].selected = True
                self.count +=1
        return p
    
class PixelArt(Grid):           #the grid that you can draw on
    def draw_grid(self,grid):
        for x in self.cells:    #if you want grid or not
            if grid:
                x.color = (255,255,255)
            else:
                x.color = BLACK

    def set_grid(self,value):   #changes grid size through options
        self.rows = self.columns = value
        self.width = self.screen_size[0] / self.rows
        self.height = self.screen_size[1] / self.columns
        self.cells = self.draw_cells()
            
    def check_event(self,new_color,brush,grid,brush_size):
        for x in self.cells:
            x.on_mouse_click(new_color,brush,grid,self,brush_size)
                

#=====INITIALIZE PYGAME AND COLORS=====#
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([700,900]) #screensize

pygame.mouse.set_visible(False)
pygame.display.set_caption('DRAW V1.0')

WHITE =  (255, 255, 255)
TRUWHITE=(249, 249, 249)
BLACK =  (  0,   0,   0)
RED   =  (255,  66,  66)
BLUE  =  ( 91,  65, 255)
GREEN =  ( 87, 255,  65)
YELLOW=  (239, 255,  65)
PURPLE=  (178,  65, 255)
PINK  =  (255,  65, 239)
TURQ  =  ( 65, 255, 248)
ORANGE=  (244, 176,  66)

#=====OPTIONS FOR TOOLBAR AND BEFORE GAME STARTS=====#
colors = [(None,TRUWHITE,'WHITE'),(None,ORANGE,'ORANGE'),(None,RED,'RED')
          ,(None,BLUE,'BLUE'),(None,GREEN,'GREEN'),(None,YELLOW,'YELLOW')
          ,(None,PURPLE,'PURPLE'),(None,PINK,'PINK'),(None,TURQ,'TURQUOISE')]

options = [('SMALL',10,'10 x 10 squares')
           ,('MEDIUM',25,'25 x 25 squares')
           ,('LARGE',50,'50 x 50 squares')]

grid_options = [('YES',True,'YES'),('NO',False,'NO')]
start_options = [('START',False,'START PAINTING')]
toolbar_options = [('B','BRUSH'),('E','ERASE'),('F','FILL')]

save_options = [('SAVE',False,'SAVE PROG.')]
load_options = [('LOAD',False,'LOAD PREV.')]

brush_sizes = [('1',1,'1 SQUARE'),('2',2,'2 SQUARES'),('3',3,'3 SQUARES')
               ,('4',4,'4 SQUARES'),('5',5,'5 SQUARES')]

#=====VARIABLES FOR GAME=====#
tool = 'BRUSH'
brush_size = 1
brush = TRUWHITE
menu_displayed = True
drawing_grid = True
grid_size = 10

drawing_board = [700,600]
pallet_board = [170,170]


#=====MENU BEFORE GAME STARTS=====#
background = Text_Render([700,900],1,1)

select_size = Text_Render([700,50],0,15,'SELECT YOUR GRID SIZE',35)
visible_grid = Text_Render([700,50],0,485,'VISIBLE GRID?',35)
start_paint = Text_Render([700,50],0,695,'START PAINTING',35)

start = Menu_Grid([700,130],1,1,Menu,start_options,0,760,0,225,100)
size_window = Menu_Grid([700,390],3,1,Menu,options,0,80,150,190,100)
has_grid = Menu_Grid([700,130],1,2,Menu,grid_options,0,550,0)

#=====ACTUAL PAINT PROGRAM=====#
pallet_text = Text_Render([170,30],40,635,'COLOR PALLET',25)
credit_text = Text_Render([620,30],40,845,'PAINT PROGRAM BY: NICK TKACHOV',25)
toolbar_text = Text_Render([270,30],215,635,'TOOLBAR',25)
brush_text = Text_Render([270,30],215,740,'BRUSH SIZE (px)',25)
save_text = Text_Render([170,30],490,635,'SAVE',25)
load_text = Text_Render([170,30],490,740,'LOAD',25)

pixel_grid = PixelArt(drawing_board,grid_size,grid_size,Pixel)
draw_pallet = Pallet(pallet_board,3,3,Menu,colors,40,670,0,50,50)

toolbar = Menu_Grid([270,65],1,3,Menu,toolbar_options,215,670,10,50,50)

save = Menu_Grid([170,65],1,1,Tool_Save,save_options,490,670,10,130,50)
load = Menu_Grid([170,65],1,1,Tool_Load,load_options,490,775,10,130,50)

brushes = Menu_Grid([270,65],1,5,Menu,brush_sizes,215,775,10,50,50,40)

#=====LISTS THAT HAVE CLASSES TO DRAW IN LOOP=====#
menu_screen = [background,select_size,size_window
               ,visible_grid,has_grid,start_paint
               ,start]

drawing_screen = [pallet_text,toolbar_text,brush_text,save_text
                  ,load_text,credit_text,save,load,toolbar
                  ,brushes,pixel_grid,draw_pallet]


#=====MAIN LOOP=====#
while True:
    screen.fill(BLACK)
    if menu_displayed:
        for x in menu_screen: x.draw(screen)
    else:  
        for x in drawing_screen: x.draw(screen)
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0]:
            if not menu_displayed: #IF DRAWING
                pixel_grid.check_event(brush,tool,drawing_grid,brush_size)
                brush = draw_pallet.check_event(brush)
                tool = toolbar.check_event(tool)
                brush_size = brushes.check_event(brush_size)
                save.check_event()
                load.check_event()
            else:                   #IF IN MENU
                grid_size = size_window.check_event(grid_size)
                drawing_grid = has_grid.check_event(drawing_grid)
                menu_displayed = start.check_event(menu_displayed)
                pixel_grid.set_grid(grid_size)
                pixel_grid.draw_grid(drawing_grid)
    
    set_cursor(screen,brush,tool) #CHANGES CURSOR
    clock.tick(0)
    pygame.display.flip()
pygame.quit()
