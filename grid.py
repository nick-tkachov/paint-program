import pygame
WHITE = (255,255,255)
BLACK = (0,0,0)

#CELL OBJECT 
class Cell(object):             #ABSTRACT CLASS, USED AS A BASE FOR ALL OTHER CLASSES IN GAME
    def __init__(self,x,y,width,height,color=BLACK,grid_location = (0,0)):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = color
        self.border = 1
        self.row = grid_location[0]
        self.column = grid_location[1]
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        
    def draw(self,surface):     #DRAWS CELL
        pygame.draw.rect(surface,self.color,self.rect,self.border)

    def on_mouse_hover(self):   #DETERMINES IF USER HOVERED OVER CELL
        return self.rect.collidepoint(pygame.mouse.get_pos())

#GRID OBJECT
class Grid(object):             #ABSTRACT CLASS USED AS A BASE FOR MAIN GRID CLASSES
    def __init__(self,screen_size,rows,columns,class_type,x=0,y=0,gap=0):
        self.color = BLACK
        self.screen_size = screen_size
        self.rows = rows
        self.columns = columns
        self.class_type = class_type
        self.x = x
        self.y = y
        self.gap = gap
        self.width = self.screen_size[0] / self.rows        #DETERMINES WIDTH OF EACH CELL
        self.height = self.screen_size[1]  / self.columns   #DETERMINES HEIGHT OF EACH CELL (DEPENDING ON SCREEN SIZE)
        self.cells = self.draw_cells()
        self.count = 0      

    def draw_cells(self): #CREATES CELL OBJECTS (USING CLASS)
        p = []
        for x in range(self.rows):
            for v in range(self.columns):  #CENTERS THEM
                p.append(self.class_type(self.width * (v + self.x) + self.gap
                                         ,self.height * (x + self.y)+ self.gap
                                         ,self.width,self.height,self.color,(x,v)))
        return p
                
    def draw(self,surface): #DRAWS SCREEN
        for x in self.cells:
            x.draw(surface)
        pygame.draw.rect(surface,WHITE,pygame.Rect(self.width * (self.x)
                                                   ,self.height * (self.y)
                                                   ,self.screen_size[0],self.screen_size[1]),2)

    def find_cell(self,row,column): #USED FOR FILL ALGORITHM TO DETERMINE POSITION OF CELLS
        for x in self.cells:
            if x.row is row and x.column is column:
                return x
