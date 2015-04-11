#!/usr/bin/env python2

import random

try:
    import simplegui
    url2 = 'https://raw.githubusercontent.com/semisided1/cousera-iip/master/SVG-cards-2.0.1/svg-cards.png'

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    simplegui.Frame._hide_status = True
    url2 = 'http://localhost:8000/SVG-cards-2.0.1/svg-cards.png'

class Signal():

    def __init__(self,signal_name):
        self.name = signal_name
                
class SignalSender():

    def __init__(self):
        self.listeners = []
        self.signals = []
        
    def add_listener(self, listener, signal):
        self.listeners.append(listener)
        self.signals.append(signal)
        
    def send_all_signals(self):
        for l in self.listeners:
            for s in self.signals:
                l.recieve_signal(s)
                
    def	send(self,sig):
        for l in self.listeners:
            l.recieve_signal(sig)
        
class SignalListener():

    def __init__(self,*signals):
        self.signals_to_listen_for = signals
        
    def recieve_signal(self,signal):
        if signal not in self.signals_to_listen_for:
            raise Exception('class doesnt accept signal '+ signal.name )
            

class TimerManager(SignalSender):
    def __init__(self,interval):
        self.interval = interval
        self.timer = simplegui.create_timer(interval, self.tic)
        self.step = 1
        self.tic_signal = Signal("tic")
        SignalSender.__init__(self)
        print('TimerManager __init__ done')
    
    def add_listener(self, listener, signal):
        SignalSender.add_listener(self,listener,signal)
        self.timer.start()
        
    def tic(self):
        
        self.step += 1
        
        if len(self.listeners) == 0:
            #self.timer.stop()
            pass
        else:
            SignalSender.send(self,self.tic_signal)
            print('TimerManager  tic sent')



class Rectangle():
          
    def __init__(self,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.color = "Silver"
        self.nhits = 0

    def draw(self,c):
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
               
    
class Label(Rectangle):
    def __init__(self,app_parent,text,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.text = text
        self.color = "white"
        self.text_color = "black"
        self.font = 'monospace'
        self.font_size = 14
        self.nhits = 0
        self.leftpad = 2
        self.bottompad = 4
        self.parent = app_parent
        self.enabled = True
        self.disable_text_color = 'grey'
    
    def draw(self,c):
        Rectangle.draw(self,c)
        bl = ( self.tl[0] + self.leftpad , self.br[1] - self.bottompad)
        if self.enabled:
            c.draw_text(str(self.text), bl, self.font_size, self.text_color, self.font)    
        else:
            c.draw_text(str(self.text), bl, self.font_size, self.disable_text_color, self.font)
                
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
            
class ButtonManager:
    
    def __init__(self):
        self.buttons = []
 
    def add_button(self,i):
        self.buttons.append(i)
    
    def click(self,xy):
        for i in self.buttons:
            if i.enabled:            
                if i.hit_test(xy):
                    i.click()
                
class Button(Label):
        
    def click(self):
        pass
        
class DealButton(Button):

    def click(self):

        self.parent.deck.pick_up( self.parent.player_hand )
        self.parent.deck.pick_up( self.parent.dealer_hand )

        if self.parent.stand_button.enabled:
            self.parent.result_label.text = "Player 1 Looses"
            self.parent.losses += 1
            self.parent.losses_label.text = "Losses - " + str(self.parent.losses)

        random.shuffle( self.parent.deck.cards )

        self.parent.dealer_hand.add_card( self.parent.deck.cards.pop() )
        self.parent.player_hand.add_card( self.parent.deck.cards.pop() )
        holecard = self.parent.deck.cards.pop()
        holecard.isflipped = False
        self.parent.dealer_hand.add_card( holecard  )
        self.parent.player_hand.add_card( self.parent.deck.cards.pop() )
        
        #print(self.parent.player_hand)
        #print(self.parent.dealer_hand)
        
        self.parent.stand_button.enabled = True
        self.parent.hit_button.enabled = True
        self.enabled = True
        
        if self.parent.player_hand.count() == 21:
            self.parent.stand_button.click() 
  

class HitButton(Button):
    def click(self):
        self.parent.player_hand.add_card( self.parent.deck.cards.pop() )	
        if self.parent.player_hand.count() > 21 :
            self.parent.stand_button.click()
            self.parent.stand_button.enabled = False
        elif self.parent.player_hand.count() == 21:
            self.parent.stand_button.click()
        else:    
            self.parent.stand_button.enabled = True

class StandButton(Button):
    def click(self):
        
        for c in self.parent.dealer_hand.cards :
            c.isflipped = True
        
        while ( self.parent.dealer_hand.count() < 14 ):
            self.parent.dealer_hand.add_card( self.parent.deck.cards.pop() )
        
        self.parent.dealer_hand.update()
        
        if self.parent.player_hand.count() > 21:
            self.parent.result_label.text = "Player 1 Bust"
            self.parent.losses += 1
            self.parent.losses_label.text = "Losses - " + str(self.parent.losses)
       
        elif self.parent.player_hand.count() == 21 and len(self.parent.player_hand.cards) == 2:
            self.parent.result_label.text = "BlackJack!"
            self.parent.wins += 1
            self.parent.wins_label.text = "Wins - " + str(self.parent.wins)
            
        elif self.parent.dealer_hand.count() > 21:
            self.parent.result_label.text = "Dealer Bust"
            self.parent.wins += 1
            self.parent.wins_label.text = "Wins - " + str(self.parent.wins)
            
        elif  self.parent.player_hand.count() > self.parent.dealer_hand.count():
            self.parent.result_label.text = "Player 1 Wins"
            self.parent.wins += 1
            self.parent.wins_label.text = "Wins - " + str(self.parent.wins)
        else:
            self.parent.result_label.text = "Player 1 Looses"
            self.parent.losses += 1
            self.parent.losses_label.text = "Losses - " + str(self.parent.losses)
        
        self.parent.stand_button.enabled = False
        self.parent.hit_button.enabled = False
        self.parent.deal_button.enabled = True

row0x = 0
colw = 82
col0x = 0
rowh = 120
padx = 2
pady = 2

image_source_tls = []
for l in range(52):
    row = l // 13
    col = l % 13
    tlx = col0x + colw * col + padx * col
    tly = row0x + rowh * row + pady * row
    
    image_source_tls.append( (tlx,tly) )
    
suits = ['clubs','diamonds','hearts','spades']
ranks = ['ace','2','3','4','5','6','7','8','9','10','jack','queen','king']
rank_values = [11,2,3,4,5,6,7,8,9,10,10,10,10]

deck_image = simplegui.load_image(url2)


class Card():
            
    def __init__(self,source_top_left,canvas_top_left,rank,suit):
        self.stl = source_top_left
        self.tl = canvas_top_left
        self.br = ( self.tl[0] + colw, self.tl[1] + rowh )
        self.center = ( source_top_left[0] + colw / 2, 
            source_top_left[1] + rowh / 2 )
        self.sbr =  ( source_top_left[0] + colw, 
            source_top_left[1] + rowh )
        self.rank = rank
        self.suit = suit
        self.isflipped = True
        self.value = rank_values[ ranks.index(rank) ]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit + ' stl: ' + str(self.stl) + ' sbr: ' + str(self.sbr) + ' tl: ' + str(self.tl)	+ ' br: ' + str(self.br) + ' center: ' + str(self.center) 
    
    def draw(self,c):
        if self.isflipped:
            c.draw_image(deck_image, self.center, (colw,rowh), (self.tl[0] + colw / 2,self.tl[1] + rowh / 2), (colw,rowh) ) 
        else :
            c.draw_image(deck_image, (208,547), (colw,rowh), (self.tl[0] + colw / 2,self.tl[1] + rowh / 2), (colw,rowh) ) 

    
class Deck():
    
    def __init__(self):
        self.cards = []
        for c in range(52):
            row = c // 13
            col = c % 13
            self.cards.append( Card( 
                source_top_left=image_source_tls[c],
                canvas_top_left = (10,10),
                suit = suits[row],
                rank = ranks[col]			
                ) )
                
    def __str__(self):
        toret = ''
        for i in self.cards:
            toret +=  str(i) + '\n' 
        return toret
            
    def shuffle(self):
        random.shuffle(self.cards)
        
    def pick_up(self,hand):
        while len(hand.cards) > 0:
            c =  hand.cards.pop()
            c.isflipped = True
            self.cards.append(c)
                                
class Hand():
    def __init__(self,tl,player_name):
        self.tl = tl
        self.cards = []
        self.name = player_name
        self.label = Label(self,player_name,tl,(tl[0]+200,tl[1]+20))
        
    def draw(self,canvas):
        for c in self.cards:
            c.draw(canvas)
        self.label.draw(canvas)
        
    def __str__(self):
        toret = ''
        for i in self.cards:
            toret +=  str(i) + '\n' 
        return toret
        
    def update(self) :
        self.label.text = self.name + ' - ' + str(self.count())	
    
    def add_card(self, card) :
        self.cards.append(card)
        card.tl = (self.tl[0] +  ( colw + 5 ) * ( len(self.cards) - 1 ), self.tl[1] + 25 )
        self.label.text = self.name + ' - ' + str(self.count())
        
    def count(self):
        n_aces = 0
        max_total = 0
        for c in self.cards:
            if c.isflipped == True:
                if c.value == 11:
                    n_aces += 1
                max_total += c.value
            
        while ( n_aces > 0 and max_total > 21 ) :
            n_aces -= 1
            max_total -= 10
                
        return max_total

class BlackJack(SignalListener):
    
    def __init__(self):
        
        self.wins = 0
        self.losses = -1
        
        self.deck = Deck()
        random.shuffle(self.deck.cards)
        #print(str(self.deck))
        
        self.dealer_hand = Hand(( 10, 50),"Dealer")
        self.player_hand = Hand((100,210),"Player 1")
        
        self.draw_manager = DrawManager()
        self.button_manager = ButtonManager()
        
        self.game_label = Label(self,"BlackJack",(200,20), (400,35))
        self.game_label.color = "Black"
        self.game_label.text_color = "Green"
        self.game_label.font_size = 36
        
        self.deal_button = DealButton(self,"Deal",(20,400),(100,440))
        self.deal_button.color = 'Green'
        self.button_manager.add_button(self.deal_button)
        self.draw_manager.add_draw_item(self.deal_button)

        self.hit_button = HitButton(self,"Hit",(110,400),(190,440))
        self.hit_button.color = 'Gold'
        self.button_manager.add_button(self.hit_button)
        self.draw_manager.add_draw_item(self.hit_button)
        
        self.stand_button = StandButton(self,"Stand",(200,400),(280,440))
        self.stand_button.color = 'Red'
        self.button_manager.add_button(self.stand_button)
        self.draw_manager.add_draw_item(self.stand_button)
        
        self.result_label = Label(self,"Good Luck", (350,400),(500,440) )
        self.draw_manager.add_draw_item(self.result_label)
        
        self.wins_label = Label(self,"Wins - 0", (510,400),(600,420) )
        self.draw_manager.add_draw_item(self.wins_label)
        
        self.losses_label = Label(self,"Losses - 0", (510,420),(600,440) )
        self.draw_manager.add_draw_item(self.losses_label)
    
        self.deal_button.click()
        self.result_label.text = "Good Luck"	
         
        
        
        self.draw_manager.add_draw_item(self.game_label)
        self.draw_manager.add_draw_item(self.player_hand)
        self.draw_manager.add_draw_item(self.dealer_hand)
            
        self.tic_tm = TimerManager(1000)
        #self.tic_tm.add_listener(self, Signal("tic"))
        self.frame = simplegui.create_frame('BlackJack',630, 500,100)	
        self.frame.set_draw_handler(self.draw_handler)
        self.frame.set_mouseclick_handler(self.mouse_click_handler)
        self.frame.start()
        
    def mouse_click_handler(self,xy):
        self.button_manager.click(xy)

    def draw_handler(self, c):
        self.draw_manager.draw(c)
        
    def recieve_signal(self,signal):
        print('black jack tic')
        if signal.name == "tic":
            print(self.tic_tm.step)
                
random.seed()
BlackJack()					
