from random import choice
import tkinter as tk
import tkinter.font 
from math import floor
sequence = ["0", "1"]
worst_situaion = '101'

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



def draw_graph(time_records, colour = 'black'):
	''' Creates a graph of the times used to process all 
	substrings using tkinter and other built-in python methods'''
	if sum(time_records)<=0.002:
		print("Podano dane dążące do zera!!!")
		return -1
	master = tk.Tk()

	width, height = 1000, 500
	legend_x, legend_y, title, post_graph_area = 100, 50, 50, 20
	density = 25

	graph_width = width - legend_x - post_graph_area
	graph_height = height - legend_y - title

	canv = tk.Canvas(master, 
	           width=width,
	           height=height)
	canv.pack()

	times12 = tkinter.font.Font(family='Times',
        size=12, weight='bold')
	times30 = tkinter.font.Font(family='Times',
        size=30, weight='bold')

	canv.create_line( legend_x+1, title+graph_height+1, width, title+graph_height+1, fill = "grey" )
	canv.create_line( legend_x+1, title-5, legend_x+1, title+graph_height+1, fill = "grey" )
	canv.create_text(width/2, title/2,  text = "Wykres", font = times30, anchor = tk.CENTER, fill="black")


	distance = graph_width/len(time_records)
	multiplicator = graph_height/sum(time_records)
	x1, y1= legend_x, graph_height+title
	iterator = 1
	for record in time_records:
		record =multiplicator*record
		x2 = x1+distance
		canv.create_line( x1, y1, x2, y1-record, fill = colour )
		canv.create_text(x2, graph_height+title,  text = str(iterator), font = times12, anchor = tk.N, fill="green")
		x1 = x2
		y1 -= record
		iterator+=1

	quantity_labels = floor(graph_height/density)
	Min, Max =min(time_records), max(time_records)
	step = (Max - Min) / quantity_labels

	for i in range(quantity_labels):
		canv.create_text(legend_x, i*density+title, text = str(round(Max-i*step, 3)), font = times12, anchor = tk.E, fill="red")
	tk.mainloop()