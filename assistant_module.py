from random import choice
import tkinter as tk
import tkinter.font 
from math import floor, ceil
sequence = ["0", "1"]
worst_situaion = '101'

class Graph:
	''' Creates a graph of the times used to process all 
	substrings using tkinter and other built-in python methods'''
	def __init__(self):
		self.time_records = []
		master = tk.Tk()
	
		self.width, self.height = 1200, 500
		self.legend_x, self.legend_y, self.title, self.post_graph_area = 100, 50, 50, 20
		self.density = 25
	
		self.graph_width = self.width - self.legend_x - self.post_graph_area
		self.graph_height = self.height - self.legend_y - self.title
	
		self.canv = tk.Canvas(master, width=self.width, height=self.height)
		self.canv.pack()
	
		self.times12 = tkinter.font.Font(family='Times',
	        size=12, weight='bold')
		self.times30 = tkinter.font.Font(family='Times',
	        size=30, weight='bold')
	
		self.canv.create_line( self.legend_x+1, self.title+self.graph_height+1, self.width, self.title+self.graph_height+1, fill = "grey" )
		self.canv.create_line( self.legend_x+1, self.title-5, self.legend_x+1, self.title+self.graph_height+1, fill = "grey" )
		self.canv.create_text(self.width/2, self.title/2,  text = "Wykres", font = self.times30, anchor = tk.CENTER, fill="black")


	def save_new_data(self, data):
		self.time_records.append(data)


	def paint_graph(self):
		all_len, all_max, all_min, all_sum = [], [], [], []
		for data_set in self.time_records:
			if sum(data_set)<=0.002:
				print("Podano dane dążące do zera!!!")
				return -1
			else:
				all_len.append(len(data_set))
				all_max.append(max(data_set))
				all_min.append(min(data_set))
				all_sum.append(sum(data_set))

		self.distance = self.graph_width/max(all_len)
		self.multiplicator = self.graph_height/max(all_sum)

		quantity_labels = floor(self.graph_height/self.density)
		Min, Max =min(all_min), max(all_max)
		step = (Max - Min) / quantity_labels

		for i in range(quantity_labels):
			self.canv.create_text(self.legend_x, i*self.density+self.title, text = str(round(Max-i*step, 3)), 
				font = self.times12, anchor = tk.E, fill="red")

		quantity_labels = floor(self.graph_width/self.density)
		step =   floor(max(all_len) / quantity_labels)
		if step == 0:
			step = 1
		for i in range(0, max(all_len)+1, step):
			self.canv.create_text(i*self.distance+self.legend_x, self.graph_height+self.title,  text = str(i), 
				font = self.times12, anchor = tk.N, fill="green")

		for data_set in self.time_records:
			self.graph_painter(data_set)
		tk.mainloop()


	def graph_painter(self, data, colour="black"):
		x1, y1= self.legend_x, self.graph_height+self.title
		for record in data:
			record =self.multiplicator*record
			x2 = x1+self.distance
			self.canv.create_line( x1, y1, x2, y1-record, fill = colour )
			x1 = x2
			y1 -= record



def random_sequence(path = "input_rand.txt", lines = 10, start_length = 50, increment = 0, multiplier = 1):
	with open(path,'w', encoding='utf-8') as file:
		for i in range(lines):
			line = ''
			for j in range(start_length):
				line+=choice(sequence)
			file.write(line+'\n')
			start_length+= increment
			start_length*= multiplier


	
def worst_sequence(path = "input_worst.txt", lines = 10, start_repeats = 30, increment = 0, multiplier = 1):
	with open(path,'w', encoding='utf-8') as file:
		for i in range(lines):
			line = worst_situaion * start_repeats
			file.write(line+'\n')
			start_repeats+= increment
			start_repeats*= multiplier