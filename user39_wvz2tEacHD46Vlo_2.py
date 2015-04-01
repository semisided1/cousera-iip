'''
2d lab
darrell dupas
dirtslayer@gmail.com

fridge poetry - click the 'add word' button to add words to the fridge


use the mouse to drag the words on the fridge to make a poem

(you can also drag the 'add word' button )

if you dont like a word just drag it off the fridge

you can stack the words and drag them together

todo: wordy.add_common_verb() wordy.add_common_adjective()
        wordy.add_common_noun() wordsy.add_commom_python()

post a screenshot of your poem!
'''


import simplegui
import user39_vodaCIpISu_1 as wordy


class DragManager:
    
    def __init__(self, app_parent, garbage):
        self.parent = app_parent
        self.dragitems_waiting = []
        self.dragitems_being_dragged = []
        self.currently_dragging = False
        self.start_of_drag = (0,0)
        self.garbage = garbage     
    
    def add_dragable_item(self,i):
        self.dragitems_waiting.append(i)
        
    def remove_dragable_item(self,i):
        self.dragitems_waiting.remove(i)
    
    def check_for_hit(self,xy):
        
        #print("check for hit")
        for i in self.dragitems_waiting:
            
            if i.hit_test(xy):
                self.currently_dragging = True
                i.isdragging = True
                self.dragitems_being_dragged.append(i) 
                self.start_of_drag = xy
                i.set_drag_shift(xy)
                
    def drag_hit_items(self,xy):
        #print("drag")
        #print(str(self.dragitems_being_draged))
        for i in self.dragitems_being_dragged:
            i.move_to(xy)
       
    def release_at(self,xy):
        #print('release at')
        for i in self.dragitems_being_dragged:
            i.isdragging = False
            i.do_release(xy)
            if self.garbage.hit_test(xy) and i != self.garbage :
                self.parent.kill_word(i)
        self.dragitems_being_dragged = []
  
        self.currently_dragging = False
        
class Dragable:

    def __init__(self,xy):
        self.xy = xy
        self.isdragging = False
        self.enabled = True
        
     # virtual functions
    def move_to(self,xy):
        pass
        #self.xy = xy
     
    def set_drag_shift(self,xy):
        pass
    
    def hit_test(self,xy):        
        pass
    
    def do_release(self,xy):
        pass
    
class ButtonManager:
    
    def __init__(self):
        self.buttons = []
 
    def add_button(self,i):
        self.buttons.append(i)
    
    def click(self,xy):
        for i in self.buttons:            
            if i.hit_test(xy):
                i.click()

class Rectangle(Dragable):
          
    def __init__(self,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.color = "Silver"
        self.nhits = 0

    def draw(self,c):
        '''
        this is the ugliest line of code i have ever written it makes me want to barf
        '''
        c.draw_polygon([[self.tl[0], self.tl[1]], [self.br[0], self.tl[1]], 
                        [self.br[0],self.br[1]], [self.tl[0],self.br[1]]], 
                       1, self.color, self.color)
    
    def hit_test(self,xy):
        #print('rectangle hit test implementation')
        if self.tl[0] > xy[0]:
            #print('left of')
            return False
        if self.br[0] < xy[0]:
            #print('right of')
            return False
        if self.tl[1] > xy[1]:
            #print('above')
            return False
        if self.br[1] < xy[1]:
            #print('below')
            return False
        #print('rect hit')
        #self.nhits += 1
        return True
        
    def width(self):
        return self.br[0] - self.tl[0]
   
    def height(self):
        return self.br[1] - self.tl[1]
    
    def move_to(self,xy):
        h = self.height()
        w = self.width()
        self.tl = (xy[0] + self.drag_shift[0], xy[1] + self.drag_shift[1]) 
        self.br = ( self.tl[0] + w, self.tl[1] + h )
     
    def do_release(self,xy):
        pass
    
    @property
    def xy(self):
        return self.tl
    
    def set_drag_shift(self,xy):
        self.drag_shift = (self.tl[0]-xy[0] ,self.tl[1] - xy[1]) 
        #print('drag shift : ',self.drag_shift)
    
    
class Label(Rectangle):
    def __init__(self,app_parent,text,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.text = text
        self.color = "white"
        self.text_color = "black"
        self.font = 'monospace'
        self.nhits = 0
        self.leftpad = 2
        self.bottompad = 2
        self.parent = app_parent
        
    def draw(self,c):
        #super(Label,self).draw(c)
        Rectangle.draw(self,c)
        bl = ( self.tl[0] + self.leftpad , self.br[1] - self.bottompad)
        c.draw_text(str(self.text), bl, 12, self.text_color, self.font)    
    
class Button(Label):

    def click(self):
        pass
        #print( self.text, wordy.pick_word())

class AddWordButton(Button):
    def click(self):
       
        self.nhits += 1
        if ( self.nhits % 3 == 0 ):
            word = wordy.pick_more_likely_word()
        if ( self.nhits % 3 == 1 ):
            word = wordy.pick_from_first(100)
        if ( self.nhits % 3 == 2 ):
            word = wordy.pick_word()
        label_width = len(word) * 8
        # label height is 12
        label = Label(self.parent,word,( self.tl[0] , 30 + self.tl[1] + 12 * ( self.nhits % 20 ) ),
                                        ( self.tl[0] + label_width, 30 +  self.tl[1] + 12 * ( self.nhits % 20 ) + 12))
        
       
        self.parent.draw_manager.add_draw_item(label)
        self.parent.drag_manager.add_dragable_item(label)
        
        
class Fridge:
    def __init__(self):
        url2 = 'https://lh4.googleusercontent.com/-3BgmPnrJX6A/VQpo3k8fm3I/AAAAAAAAHv4/3gX6QMGeTH0/w400-h770-no/fridge800.png'
        self.fridge = simplegui.load_image(url2)
    def draw(self,c):
        c.draw_image(self.fridge,(400 / 2, 770 / 2), (400, 770), (400 / 2, 770 / 2), (400, 770))                             
    
    # tl = (0,0)
    # br = (400,770)
    
    
class Garbage(Rectangle):
    # 150, 182
    def __init__(self):

        self.tl = ( 400, 770 - 182 )
        self.br = ( 400 + 150 , 770 )
        #Rectangle.__init__(self,tl,br)
        url3 = 'https://lh3.googleusercontent.com/-ISPY4T0J2Kw/VQuHOqIHB9I/AAAAAAAAHw8/p-8OF-7fayc/w150-h182-no/waste.png'
        self.garbage = simplegui.load_image(url3)
        
    def draw(self,c):
        #c.draw_image(self.garbage, (150 / 2, 182 / 2), (150, 182), (400 + 150/2, 770-182/2), (150,182))
        c.draw_image(self.garbage, ( self.width() / 2, self.height() / 2), 
                     (self.width(), self.height()), 
                     (self.tl[0] + self.width()/2, self.br[1] - self.height() / 2),
                     (self.width(),self.height()) )
       
        
class DrawManager:
    
    def __init__(self):
        self.draw_items = []
  
    def add_draw_item(self,i):
        self.draw_items.append(i)
    
    def remove_draw_item(self,i) :
        self.draw_items.remove(i)
    
    def draw(self,c):
        for i in self.draw_items:
            i.draw(c)
    
class App:
    
    def draw(self,c):
        # canvas.draw_text('A', (20, 20), 12, 'Red')
        self.draw_manager.draw(c)
            
    def mouse_click_handler(self,xy):
        #print('mouse click handler')
        if self.drag_manager.currently_dragging:
            #print('calling release')
            self.drag_manager.release_at(xy)
            self.drag_manager.currently_dragging = False
        else:
            self.button_manager.click(xy)
             
    def mouse_drag_handler(self,xy):
        if not self.drag_manager.currently_dragging:
            self.drag_manager.check_for_hit(xy)
        else:
            self.drag_manager.drag_hit_items(xy)
    
    def kill_word(self,word):
        self.draw_manager.remove_draw_item(word)
        self.drag_manager.remove_dragable_item(word)        
 
    def __init__(self):
       
        self.button_manager = ButtonManager()
        self.draw_manager = DrawManager()
        
        self.garbage = Garbage()
        self.draw_manager.add_draw_item(self.garbage)
        
        self.drag_manager = DragManager(self, self.garbage)
        self.drag_manager.add_dragable_item(self.garbage)
        
        self.fridge = Fridge()
        self.draw_manager.add_draw_item(self.fridge)
        
        self.add_word_button = AddWordButton(self,"add word",(390,20),(450,40))
        self.button_manager.add_button(self.add_word_button)
        self.draw_manager.add_draw_item(self.add_word_button)
        self.drag_manager.add_dragable_item(self.add_word_button)
        
   
        self.frame = simplegui.create_frame('fridge poetry',600, 780,0)
       
        self.frame.set_draw_handler(self.draw)
        self.frame.set_mouseclick_handler(self.mouse_click_handler)
        self.frame.set_mousedrag_handler(self.mouse_drag_handler)
       
        self.frame.start()
        
   
        
a = App()

