class DelayedImage(SignalSender, SignalListener):
	def __init__(self, url):
		self.image = simplegui.load_image(url)
		if self.is_ready():
			print(url)
		self.ready_signal = Signal("ready")
		self.tic_signal = Signal("tic")
		SignalSender.__init__(self,self.ready_signal)
		SignalListener.__init__(self,self.tic_signal)
		print('DelayedImage __init__ done')
		
	def is_ready(self):
		return self.image.get_width() > 0
	
	def recieve_signal(self,signal):
		print('DelayedImage recieve_signal')
		if signal.name == "tic":
			if self.is_ready():
				SignalSender.send(self, self.ready_signal)
