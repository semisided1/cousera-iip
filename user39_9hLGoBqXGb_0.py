#!/usr/bin/env python2

import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    simplegui.Frame._hide_status = True
    

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
    







url3 = 'https://raw.githubusercontent.com/semisided1/cousera-iip/dd4fd7d10d260c01fc106b093d43a4f3e7bf6c4d/SVG-cards-2.0.1/svg-cards.png'

url2= 'http://localhost:8000/SVG-cards-2.0.1/svg-cards.png'

row0x = 0
colw = 82
col0x = 0
rowh = 119
padx = 2
pady = 3

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
		self.isflipped = False
		self.value = rank_values[ ranks.index(rank) ]
		#ectangle.__init__(self,self.tl,self.br)			
	
	def __str__(self):
		return self.rank + ' of ' + self.suit + ' stl: ' + str(self.stl) + ' sbr: ' + str(self.sbr) + ' tl: ' + str(self.tl)	+ ' br: ' + str(self.br) + ' center: ' + str(self.center) 
	
	def draw(self,c):
		c.draw_image(deck_image, self.center, (colw,rowh), (self.tl[0] + colw / 2,self.tl[1] + rowh / 2), (colw,rowh) ) 
		
		
		#
		#	( self.tl[0] + colw / 2  , self.tl[1] + rowh / 2 ),
		#	self.br)
		#c.draw_image(deck_image, (1089 / 2, 608/ 2), (1089, 608), (1089 / 2, 608/ 2), (1089, 608))	
	
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
	
	def add_card(self, card) :
		self.cards.append(card)
		card.tl = (self.tl[0] +  ( colw + 5 ) * ( len(self.cards) - 1 ), self.tl[1] + 25 )
		self.label.text = self.name + ' - ' + str(self.count())
		
	def count(self):
		n_aces = 0
		max_total = 0
		for c in self.cards:
			if c.value == 11:
				n_aces += 1
			max_total += c.value
			
		while ( n_aces > 0 and max_total > 21 ) :
			n_aces -= 1
			max_total -= 10
				
		return max_total
		
			
	
#row0x = 1
#colw = 82
#col0x = 1
#rowh = 118

class BlackJack(SignalListener):

	
    
	def __init__(self):
		
		self.deck = Deck()
		random.shuffle(self.deck.cards)
		#print(str(self.deck))
		
		self.dealer_hand = Hand(( 10, 50),"Dealer")
		self.player_hand = Hand((100,200),"Player 1")
		
		self.dealer_hand.add_card( self.deck.cards.pop() )
		self.dealer_hand.add_card( self.deck.cards.pop() )
		self.player_hand.add_card( self.deck.cards.pop() )
		self.player_hand.add_card( self.deck.cards.pop() )
		self.dealer_hand.add_card( self.deck.cards.pop() )
		self.dealer_hand.add_card( self.deck.cards.pop() )
		self.player_hand.add_card( self.deck.cards.pop() )
		self.player_hand.add_card( self.deck.cards.pop() )
		
		self.game_label = Label(self,"BlackJack",(200,10), (270,30))
		
		self.tic_tm = TimerManager(1000)
		#self.tic_tm.add_listener(self, Signal("tic"))
		self.frame = simplegui.create_frame('BlackJack',1090, 610,100)	
		self.frame.set_draw_handler(self.draw_handler)
		self.frame.start()
		
	def draw_handler(self, c):
		self.dealer_hand.draw(c)
		self.player_hand.draw(c)
		self.game_label.draw(c)
    	#self.player_hand.draw(c)
		#c.draw_image(deck_image, (1089 / 2, 608/ 2), (1089, 608), (1089 / 2, 608/ 2), (1089, 608))
		#self.deck.cards[51].draw(c)
		#c.draw_image( deck_image, (82+41,118/2) , (82 + 39 ,rowh),  (10 + ( colw/2 ),10 +(rowh/2)), (92,128) )
    	
		
	def recieve_signal(self,signal):
		print('black jack tic')
		if signal.name == "tic":
			print(self.tic_tm.step)
				
random.seed()
BlackJack()					
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
