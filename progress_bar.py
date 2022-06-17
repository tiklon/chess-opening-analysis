import time as t
import math

class ProgressBar:
	
	i = 0
	i_max = 100
	decimals = 2
	length = 100
	fill = "█"
	prefix = ""
	suffix = ""
	times = []
	average_time_per_iteration = -1
	
	AVERAGE_TIME_OVER_LAST_N_ELEMENTS = 10 # how many iterations are considered when calculating average time
	
	def __init__(self, i=0, i_max=100, decimals=2, length=100, fill="█", prefix="", suffix=""):
		self.i = i
		self.i_max = i_max
		self.decimals = decimals
		self.length = length
		self.fill = fill
		self.prefix = prefix
		self.suffix = suffix
	
	def draw(self, i):
		self.i = i
		
		# Credits for the concept of this function to Greenstick on Stackoverflow: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
		percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.i / float(self.i_max)))
		filledLength = int(self.length * self.i // self.i_max)
		bar = self.fill * filledLength + '-' * (self.length - filledLength)
		
		if self.average_time_per_iteration == -1:
			time_left = "~??h ??m ??s"
		else:
			time_left_seconds = (self.i_max - self.i) * self.average_time_per_iteration
			hours = str(math.floor(time_left_seconds / (60*60)))
			minutes = "{:02d}".format(math.floor(time_left_seconds / (60)) % 60)
			seconds = "{:02d}".format(math.floor(time_left_seconds) % 60)
			
			time_left = "~"+hours+"h "+minutes+"m "+seconds+"s"			
		
		print(f"\r{self.prefix}[{self.i}/{self.i_max}] |{bar}| {percent}% [{time_left} remaining]{self.suffix}", end = "\r")
		
		# Print New Line on Complete
		if self.i == self.i_max: 
			print()
	
	def time(self):
		self.times.append(t.time())
		
		# no calculation when too few timestamps
		if len(self.times)<2:
			self.average_time_per_iteration = -1
			return
			
		# culling when too many elements, defined by constant
		if len(self.times)<self.AVERAGE_TIME_OVER_LAST_N_ELEMENTS: 
			self.times = self.times[len(self.times)-self.AVERAGE_TIME_OVER_LAST_N_ELEMENTS:len(self.times)] # last n elements are preserved
		
		sum = 0
		for i in range(len(self.times)-1):
			sum = sum + (self.times[i+1] - self.times[i])
		self.average_time_per_iteration = sum / (len(self.times)-1)
		