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

	def __init__(self, *signals_to_send):
		self.listeners = []
		self.signals = signals_to_send
		
		
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
		
	def recieve_signal(signal):
		if signal not in self.signals_to_listen_for:
			raise Exception('class doesnt accept signal '+ signal.name )
			

class TimerManager(SignalSender):
	def __init__(self,interval):
		self.interval = interval
		self.timer = simplegui.create_timer(interval, self.tic)
		self.step = 1
		self.tic_signal = Signal("tic")
		SignalSender.__init__(self,self.tic_signal)
		print('TimerManager __init__ done')
		
	def tic(self):
		self.step += 1
		
		if len(self.listeners) == 0:
			self.timer.stop()
		else:
			SignalSender.send(self,self.tic_signal)
			print('TimerManager  tic sent')


url2 = 'https://raw.githubusercontent.com/semisided1/cousera-iip/dd4fd7d10d260c01fc106b093d43a4f3e7bf6c4d/SVG-cards-2.0.1/svg-cards.png'

row0x = 1
colw = 82
col0x = 1
rowh = 118
image_source_centers = []
for l in range(52):
	row = l % 4
	col = l % 13
	tlx = col0x + colw * col
	tly = row0x + rowh * row
	centerx = tlx + colw / 2
	centery = tly + rowh / 2
	image_source_centers.append( (tlx,tly) )


class CardImage():
			
	def __init__(self):
		print(image_source_centers)
			
		
	
class Deck():
	
	def __init__(self):
		cards = []
		for c in range(52):
			pass

class BlackJack(SignalListener):

	def draw_handler(self, c):
		c.draw_image(self.deck_image, (1089 / 2, 608/ 2), (1089, 608), (1089 / 2, 608/ 2), (1089, 608))
    
	def __init__(self):
		self.tic_tm = TimerManager(1000)
		self.tic_tm.listeners.append(self, Signal("tic"))
		self.deck_image = simplegui.load_image(url2)
		self.frame = simplegui.create_frame('BlackJack',1090, 610,100)	
		self.frame.set_draw_handler(self.draw_handler)
		self.frame.start()
		
		
	def recieve_signal(signal):
		if signal.name == "tic":
			print(self.tic_tm.step)
				
random.seed()
BlackJack()					
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
