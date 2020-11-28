from random import choice
import time, sys
import tkinter as tk
import tkinter.font 
from math import floor
sequence = ["0", "1"]															# Possible values in the test sequence
worst_situaion = '101'															# In my opinion, it is the worst possible input sequence, if repeated

class Graph:
	''' Creates a graph of the times used to process all 
	substrings using "tkinter" and other built-in python methods'''

	def __init__(self, show_stats = False, worst_scenario=False, increment=0, multiplier=1, width=1200, height=400, text_density=25):
		self.time_records = []
		self.optimalization_level = []

		master = tk.Tk()														# Creating a window for the graph
		master.title("Wykres porównania algorytmów")
		
		if height < 200:
			height = 200
		if width < 650:
			width = 650

		self.width, self.height = width, height 								# Defining some basic distances
		self.legend_x, self.legend_y, self.title, self.post_graph_area = 100, 120, 50, 20
		self.density = text_density	
		self.graph_width = self.width - self.legend_x - self.post_graph_area
		self.graph_height = self.height - self.legend_y - self.title

		
		self.canv = tk.Canvas(master, width=self.width, height=self.height)		# Creating a canvas to write on
		self.canv.pack()
	
		self.times12 = tkinter.font.Font(family='Times',						# Defining some fonts and colours, which will be used later
	        size=12, weight='bold')
		self.times30 = tkinter.font.Font(family='Times',
	        size=30, weight='bold')
		self.times20 = tkinter.font.Font(family='Times',
	        size=20, weight='bold')
		self.colors = ['darkgreen', 'crimson', 'mediumblue', 'indigo', 'maroon', 'saddlebrown', 'darkgoldenrod', 'black']

																				# Creating a plot

		self.canv.create_line( self.legend_x+1, self.title+self.graph_height+1, self.width, 
			self.title+self.graph_height+1, fill = "grey", width = 3, arrow = tk.LAST )
		self.canv.create_line( self.legend_x+1, self.title+self.graph_height, self.legend_x+1, 
			self.title*0.5, fill = "grey", width = 3, arrow = tk.LAST)
		self.canv.create_text(self.width/2, self.title/2,  text = "Porównania algorytmów", font = self.times30, anchor = tk.CENTER, fill="black")
		self.canv.create_text(self.legend_x/2, self.title/2,  text = "Czas, s", font = self.times20, anchor = tk.CENTER, fill="black")
		self.canv.create_text(self.width, self.title+self.graph_height+self.legend_y/3,  
			text = "Numer ciągu", font = self.times20, anchor = tk.E, fill="black")

		if worst_scenario and show_stats:
			self.canv.create_text(self.width/2, self.title/2 + 18,  text = "najgorsze dane wejściowe", font = self.times20, anchor = tk.N, fill="black")
			self.canv.create_text(self.width/2, self.title+self.graph_height+self.legend_y/4,  
			text = "length increment: {}  multiplier: {}".format(increment*3, multiplier), font = self.times12, anchor = tk.N, fill="black")
		elif not worst_scenario and show_stats:
			self.canv.create_text(self.width/2, self.title/2 + 18,  text = "przypadkowe dane wejściowe", font = self.times20, anchor = tk.N, fill="black")
			self.canv.create_text(self.width/2, self.title+self.graph_height+self.legend_y/4,  
			text = "length increment: {}  multiplier: {}".format(increment, multiplier), font = self.times12, anchor = tk.N, fill="black")



	def save_new_data(self, times_info, optimalization_level):
		''' This function takes data and writes it down'''

		if sum(times_info)<=0.001:
			print("\nPODANO DANE DĄŻĄCE DO ZERA!!!\nWYKRES TEJ FUNKCJI NIE ZOSTANIE NARYSOWANY!")
		else:
			self.time_records.append(times_info)
			self.optimalization_level.append(optimalization_level)



	def paint_graph(self):
		''' This function creates a graph after all data is collected.'''

		if self.time_records == []:												# Checking if data exist at all
			print("Za mało danych, aby narysować wykres!")
			return -1

		all_len, all_max, all_min, all_sum = [], [], [], []						# Defining the common scale for all data
		for data_set in self.time_records:
			all_len.append(len(data_set))
			all_max.append(max(data_set))
			all_min.append(min(data_set))
		self.distance = self.graph_width/max(all_len)
		self.multiplicator = self.graph_height/max(all_max)


		quantity_labels = floor(self.graph_height/self.density)					# Defining values on Y axis
		Min, Max =min(all_min), max(all_max)
		step = (Max - Min) / quantity_labels
		for i in range(quantity_labels):
			self.canv.create_text(self.legend_x-8, i*self.density+self.title, text = str(round(Max-i*step, 3)), 
				font = self.times12, anchor = tk.E, fill="red")

		quantity_labels = floor(self.graph_width/self.density)					# Defining values on X axis
		step =   floor(max(all_len) / quantity_labels)
		if step == 0:
			step = 1
		for i in range(0, max(all_len)+1, step):
			self.canv.create_text(i*self.distance+self.legend_x, self.graph_height+self.title+8,  text = str(i), 
				font = self.times12, anchor = tk.N, fill="green")


		numb_of_records = len(self.time_records)								# Drawing all graphs and writing down the legend under the plot
		for i in range(numb_of_records):
			self.graph_painter(self.time_records[i], i+1)
			self.canv.create_text(self.graph_width/numb_of_records*(i)+self.post_graph_area, self.height - 10,  
				text = "Test {0} - wykres funkcji zależności czasu od\nciągu algorytmu z poziomem optymalizacji {1}".format(i+1, self.optimalization_level[i]), 
				font = self.times12, anchor = tk.SW, fill=self.colors[(i+1)%len(self.colors)])
		tk.mainloop()


	def graph_painter(self, times_info, number):
		''' This function draws a graph of values given in the array times_info'''

		color = self.colors[number%len(self.colors)]
		x1, y1= self.legend_x, self.graph_height+self.title
		previous = 0
		for record in times_info:												# Drawing a line from the previous record to the current record.
			shift = record - previous											# Null record defined as (0,0)
			previous = record
			shift =self.multiplicator*shift
			x2 = x1+self.distance
			self.canv.create_line( x1, y1, x2, y1-shift, fill = color, width = 1 )
			x1 = x2
			y1 -= shift
		self.canv.create_text(x2, y1,  text = "Test "+str(number), 				# Creating a caption of the graph
				font = self.times12, anchor = tk.SE, fill=color)



def random_sequence(path = "input_rand.txt", lines = 10, start_length = 50, increment = 0, multiplier = 1):
	''' This function creates a file filled with random sequence of digits "zero" and "one". 
	More detailed explanation is given below the function'''

	with open(path,'w', encoding='utf-8') as file:
		for i in range(lines):
			line = ''
			for j in range(start_length):
				line+=choice(sequence)
			file.write(line+'\n')
			start_length+= increment
			start_length*= multiplier
""" Example:
path_in = '', 		- path, where a new input file will be generated;
lines = 20, 		- number of strings (lines) in the generated file;
start_length = 50, 	- length of the first string (line);
increment = 5,		- increment of the length of the line after each line;
multiplier = 1		- multiplication of the length of the line after each line.
"""

	
def worst_sequence(path = "input_worst.txt", lines = 10, start_repeats = 30, increment = 0, multiplier = 1):
	''' This function creates file filled with worst sequence of digit "zero" and "one". 
	More detailed explanation is given below the function'''

	with open(path,'w', encoding='utf-8') as file:
		for i in range(lines):
			line = worst_situaion * start_repeats
			file.write(line+'\n')
			start_repeats+= increment
			start_repeats*= multiplier
""" Example:
path_in = '', 		- path, where a new input file will be generated;
lines = 20, 		- number of strings (lines) in the generated file;
start_repeats = 10, - number of repeats of the sequence '101' in the first line;
increment = 5,		- increment of repeats of the sequence '101' after each line;
multiplier = 1		- multiplication of repeats of the sequence '101' after each line.
"""


# The next function is not written by Vitalii Morskyi (just modified)
# Source: https://stackoverflow.com/questions/3160699/python-progress-bar
def update_progress(progress, path_in):
	''' Displays or updates a console progress bar. WORKS ONLY WITH CONSOLE
	Accepts a float between 0 and 1. Any int will be converted to a float.
	A value under 0 represents a 'halt'.
	A value at 1 or bigger represents 100%.'''

	barLength = 10 # Modify this to change the length of the progress bar
	status = ""
	if isinstance(progress, int):
		progress = float(progress)
	if not isinstance(progress, float):
		progress = 0
		status = "error: progress var must be float\r\n"
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		status = "Gotowy...\r\n"
	block = int(round(barLength*progress))
	text = "\rPrzetwarzanie pliku \"{3}\" : [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100,1), status, path_in)
	sys.stdout.write(text)
	sys.stdout.flush()