
import simplegui
import random


class CardManager:
    
    def __init__(self):
        self.cards = []
        self.wait_for_callback = False
        self.match_delay_timer = simplegui.create_timer(1500, self.flip_unmatched)
        self.game_over_timer = simplegui.create_timer(3000, self.reset)
       
        self.turns = 0                
 
    def append(self,i):
        self.cards.append(i)
    
    def click(self,xy):
        if self.wait_for_callback:
            return
        for i in self.cards:            
            if i.hit_test(xy):
                i.click()
                if i.flipped:
                    return
                nfu = self.n_flipped_unmatched()
                if nfu == 0:
                    i.flip()
                    return
                if nfu == 1:
                   
                    i.flip()
                    self.turns += 1
                    
                    if self.check_for_match():
                        self.match_matched()
                        if self.check_for_win():
                           
                            self.wait_for_callback = True
                            self.game_over_timer.start()
                        
                    else:
                        self.wait_for_callback = True
                        self.match_delay_timer.start()

    def reset(self):
        self.game_over_timer.stop()
        self.match_delay_timer.stop()
        self.wait_for_callback = False
        self.shuffle()
        self.turns = 0
        for i in self.cards:
            if i.flipped:
                i.unflip()
            i.matched = False
     
    def shuffle(self):
        #return
        for i in range(5):
            rand1 = random.randrange(0,len(self.cards))
            rand2 = rand1
            while (rand1 == rand2):
                rand2 = random.randrange(0,len(self.cards))
            print(rand1,rand2)
            tl = self.cards[rand1].tl
            br = self.cards[rand1].br
            self.cards[rand1].tl = self.cards[rand2].tl
            self.cards[rand1].br = self.cards[rand2].br
            self.cards[rand2].tl = tl
            self.cards[rand2].br = br
                    
    def check_for_match(self): 
        twoc = []
        for i in self.cards:
            if i.flipped and not i.matched:
                twoc.append(i)
        if len(twoc) == 2:
            return twoc[0].url == twoc[1].url
      
    def match_matched(self):
        twoc = []
        for i in self.cards:
            if i.flipped and not i.matched:
                twoc.append(i)
        if len(twoc) == 2:
            twoc[0].matched = True
            twoc[1].matched = True
    
    def n_flipped(self):
        n = 0
        for i in self.cards:
            if i.flipped:
                n += 1
        return n
    
    def n_matched(self):
        n = 0
        for i in self.cards:
            if i.matched:
                n += 1
        return n
    
    def check_for_win(self):
        return self.n_matched() ==  len(self.cards)
    
    def n_flipped_unmatched(self):
        n = 0
        for i in self.cards:
            if i.flipped and not i.matched:
                n += 1
        return n
    
    def flip_unmatched(self):
        n = 0
        for i in self.cards:
            if not i.matched:
                i.unflip()
        self.match_delay_timer.stop()
        self.wait_for_callback = False
        
        

class Rectangle():
          
    def __init__(self,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.color = "#003300"
        self.nhits = 0

    def draw(self,c):
        c.draw_polygon([[self.tl[0], self.tl[1]], [self.br[0], self.tl[1]], 
                        [self.br[0],self.br[1]], [self.tl[0],self.br[1]]], 
                       1, "Black",self.color)
    
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
    
    @property
    def xy(self):
        return self.tl
     
    

class Card(Rectangle):

    def __init__(self,app_parent,top_left,width,height,url):
        self.tl = top_left
        self.flipped = False
        self.matched = False
        self.color = "#003300"
        self.nhits = 0
        self.parent = app_parent
        self.image = simplegui.load_image(url)
        self.url = url
        self.br = ( self.tl[0] + width, self.tl[1] + height )
        
        
        self.atimer = simplegui.create_timer(10, self.tic)
        self.stage = 0
        self.direction = 1
        # 0 is unflipped
        # 19 is totally flipped
    def click(self):
        #print('card clicked ')
       
        pass
    
    def tic(self):
        self.stage += self.direction
        if ( self.stage == 19 and self.direction == 1):
            self.atimer.stop()
        if ( self.stage <= 0 and self.direction == -1):
            self.stage = 0
            self.atimer.stop()
           
    
    
    def unflip(self): 
        if self.flipped:
            self.atimer.start()
            self.direction = -1
            self.flipped = False
        
    
    def flip(self):  
        if not self.flipped:
            self.atimer.start()
            self.direction = 1
            self.flipped = True
        
        
    
    def draw(self,c):
        if self.image.get_width() == 0 or self.image.get_height() == 0:
            #print('self.image.get_width() ' + str(self.image.get_width()))
            #print('self.image.get_height() ' + str(self.image.get_height()))
            
            return
            
        if self.stage == 19 :
            c.draw_image(self.image, ( self.image.get_width() / 2, self.image.get_height() / 2), 
                     (self.image.get_width(), self.image.get_height()), 
                     (self.tl[0] + self.image.get_width()/2, self.tl[1] + self.image.get_height() / 2),
                     (self.image.get_width(),self.image.get_height()) )
                
           
            
        if self.stage == 0:
            Rectangle.draw(self,c)  
           
        if self.stage > 0 and self.stage < 10:
            # draw rectangle turning over
            xoffpertic = float(self.width()) / 10.0
            xoff = xoffpertic * self.stage
            new_width = int(self.width() - xoff)
            tlx = self.tl[0] + int ( xoff / 2.0 )
            brx = self.br[0] - int ( xoff / 2.0 )
            
            
            r = Rectangle((tlx,self.tl[1]),(brx,self.br[1]))
            r.draw(c)              
            
        if self.stage >= 10 and self.stage < 19:
            xoffpertic = float(self.width()) / 10.0
            xoff = int( (xoffpertic * ( 19.0 - self.stage )))
            c.draw_image(self.image, ( self.image.get_width() / 2, self.image.get_height() / 2), 
                     (self.image.get_width(), self.image.get_height()), 
                     (self.tl[0] + self.image.get_width()/2, self.tl[1] + self.image.get_height() / 2),
                     (self.image.get_width() - xoff,self.image.get_height()) )
              
            #print(str(self.stage))

class DrawManager:
    
    def __init__(self):
        self.draw_items = []
  
    def append(self,i):
        self.draw_items.append(i)
    
    def remove(self,i) :
        self.draw_items.remove(i)
    
    def draw(self,c):
        for i in self.draw_items:
            i.draw(c)

            
class ResetButton(Rectangle):
    
    def __init__(self,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.leftpad = 60
        self.bottompad = 18
        self.font = "monospace"
        self.text_color = "Black"
        self.color = "White"
        self.text = "Reset"
        
    
    def draw(self,c):
        Rectangle.draw(self,c)
        bl = ( self.tl[0] + self.leftpad , self.br[1] - self.bottompad)
        c.draw_text(str(self.text), bl, 18, self.text_color, self.font)    

class MessageBox(Rectangle):
    
    def __init__(self,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.leftpad = 60
        self.bottompad = 18
        self.font = "monospace"
        self.text_color = "Black"
        self.color = "White"
        self.text = "Message Box"
        
    
    def draw(self,c):
        Rectangle.draw(self,c)
        bl = ( self.tl[0] + self.leftpad , self.br[1] - self.bottompad)
        c.draw_text(str(self.text), bl, 18, self.text_color, self.font)    

class Background:
    def __init__(self):
        url2 = 'https://raw.githubusercontent.com/semisided1/cousera-iip/master/background.png'

        #url2 = 'https://raw.githubusercontent.com/semisided1/cousera-iip/master/background.svg'
        self.bg = simplegui.load_image(url2)
    def draw(self,c):
        c.draw_image(self.bg,(1120 / 2, 500 / 2), (1120, 500), (1120 / 2, 500 / 2), (1120, 500))                             
        
class App:
    
    def draw(self,c):
        self.draw_manager.draw(c)
            
    def mouse_click_handler(self,xy):
        self.card_manager.click(xy)
        if self.card_manager.check_for_win():
            self.msgbox.text = "You win - Turns - " + str(self.card_manager.turns)
        else:
            self.msgbox.text = "Turns - " + str(self.card_manager.turns)
        if self.reset_btn.hit_test(xy):
            self.card_manager.reset()
            self.msgbox.text = "Turns - " + str(self.card_manager.turns)
             
    def __init__(self):
        
        self.card_manager = CardManager()
        self.draw_manager = DrawManager()
        self.bg = Background()
        self.draw_manager.append(self.bg)
        self.reset_btn = ResetButton((10,440),(210,490))
        self.draw_manager.append(self.reset_btn)
        
        self.msgbox = MessageBox((250,440),(800,490))
        self.draw_manager.append(self.msgbox)
        
        count = 0
        column = 130
        row = 180
        pad = 10
        left = -column
        top = 50
        #self.cards = []
        image_base_url = 'https://raw.githubusercontent.com/semisided1/pydoit/master/src/lists/feelings/'
        img_files = ['boss/boss.png','doh/doh.png','freezing/freezing.png','hot/hot.png',
            'party/party.png','relaxed/relaxed.png','scared/scared.png','whatever/whatever.png']
        for i in img_files:
            left += column + pad
            for y in range(2):
                newcard = Card(self,( left , top + (y * row)),120,170,image_base_url+i)
                #count += 1
                
            #self.cards.append(newcard)
                self.draw_manager.append(newcard)
                self.card_manager.append(newcard)
        
        self.card_manager.shuffle()
        self.frame = simplegui.create_frame('memory',1120, 500,100)
       
        self.frame.set_draw_handler(self.draw)
        self.frame.set_mouseclick_handler(self.mouse_click_handler)
        #self.frame.set_mousedrag_handler(self.mouse_drag_handler)
       
        self.frame.start()
        
random.seed()        
a = App()

