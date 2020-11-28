from time import *
from math import floor

try:
	import assistant_module	as assist	# Another part of my program where some cool functions are placed.
										# File assistant_module.py should be located in the same folder with following file: (podciagi.py)
except ModuleNotFoundError:
	print("Wystąpił błąd!\nUmieść pliki „assistant_module.py” i „podciagi.py” w tym samym folderze.")
	import sys, os
	os.system("pause")
	sys.exit()
except:
	print("Przepraszamy, coś poszło nie tak ... \nSprawdź, czy plik „assistant_module.py” nie posiada błedów.")
	import sys, os
	os.system("pause")
	sys.exit()



class binary_sequences:
	
	def __init__(self, path_in = 'input.txt', path_out = 'output.txt'):
		''' Initialization of the class and assigning default values to flags'''

		self.path_in = path_in
		self.path_out = path_out
		self.reading_file()
		self.enable_repeating_lists_before_output = False
		self.optimization_level = 3
		self.show_progress_bar = False



	def draw_separator(self):
		''' This function draws a "pretty" separator between tasks'''

		heading = " Nowe zadanie z pliku: \"{}\" ".format(self.path_in)
		separator = '-'*5 + heading + '-'*(115 - len(heading))
		print('\n\n\n\n' + separator + '\n')
		


	def solve_problem(self):
		''' The main function. Iterates the process of searching substrings for each sequence.
		After completing the task it writes out small conclusion to the console. '''

		global current_sequence
		self.iterator = 0							# If more than one input was given, then this variable will help to iterate the whole process
		self.number_of_sequences = len(self.all_sequences)	# Number of sequences given in the input file
		self.time_results = [] 						# List of records of the time used by algorithm function

		self.draw_separator()						# Drawing a "pretty" separator between tasks

		while self.iterator < self.number_of_sequences:
			current_sequence = self.all_sequences[self.iterator]

			if self.show_progress_bar:				# Updates the progress bar if the appropriate flag is enabled
				assist.update_progress(self.iterator/self.number_of_sequences, self.path_in)

			self.iterator += 1

			k = current_sequence.count(1)			# n, k - the quantity of digits "zero" & "one" respectively
			n = len(current_sequence)-k
			p = min(n,k)							# p - theoretical maximum of possible pairs (0,1)

			if n==k!=0:								# Checking for the easiest solutions when k=0, n=0 or n=k
				self.give_answer(1, [current_sequence])
				self.time_results.append(0.0)
			elif n==0 or k==0:
				self.give_answer(0)
				self.time_results.append(0.0)
			elif n>=1 and k>=1:
				start_time = time()					# Recording the time of the main algorithm start
				if self.optimization_level == 3:
					substring = self.main_algorithm_optimized(p)
				elif self.optimization_level == 2:
					substring = self.main_algorithm_better(p)
				elif self.optimization_level == 1:
					substring = self.main_algorithm_brute()
				else:
					print("\nNieprawidłowo określony poziom optymalizacji. Wybrano ustawienia domyślne.")
					self.optimization_level = 3
					substring = self.main_algorithm_optimized(p)
				end_time = time()					# Recording the time of the main algorithm end

				self.time_results.append(round(end_time - start_time,3))
				self.give_answer(len(substring), substring)

		else:										# Writing of the conclusion with respect to conjugation of polish numerals

			if self.input_file_exist and not self.reading_file_error and self.number_of_sequences>0:

				if self.show_progress_bar:
					assist.update_progress(self.iterator/self.number_of_sequences, self.path_in)
					print('')

				last_digit=list(str(self.number_of_sequences)).pop()
	
				teened = False
				if self.number_of_sequences >=10:
					if str(self.number_of_sequences)[-2:] in ['11', '12', '13', '14']:		# excluding -teen numbers
						teened = True
	
				if last_digit=='1' and not teened:
					insert_text = 'wejściowy ciąg'
				elif last_digit in ['2', '3', '4'] and not teened:
					insert_text = 'wejściowy ciągi'
				else:
					insert_text = 'wejściowych ciągów'

				time_used = round(sum(self.time_results),3)
				avarage_time_used = round(time_used/self.number_of_sequences, 5)

				print("Rozpoznano {0} {1} w pliku \"{2}\". ".format(self.number_of_sequences, insert_text, self.path_in)+
					"Wszystkie odpowiedzi zostały zapisane w pliku \"{}\". ".format(self.path_out) +
					"\nWybrany {} poziom optymalizacji.".format(self.optimization_level)+
					"\nCzas roboty algorytmu wynosi {} s.".format(time_used) + 
					"\nŚredni czas przetwarzania jednego ciągu wynosi {} s.\n".format(avarage_time_used))

			elif not self.input_file_exist and self.reading_file_error:
				print("\nNie znaleziono pliku według ścieżki \"{}\".\n".format(self.path_in))

			elif self.input_file_exist and self.reading_file_error:
				print("\n\nCoś poszło nie tak podczas odczytu pliku.\n")

			elif self.number_of_sequences==0:
				print("Nie rozpoznano wejściowych ciągów w pliku \"{}\". ".format(self.path_in))



	def reading_file(self):
		''' Reading of the file containing input data and creating a clean output file'''

		with open(self.path_out,'w', encoding='utf-8') as file:		# Cleaning the output file
			pass

		self.all_sequences, accepted_values = [], ['0', '1']
		try:
			with open(self.path_in,'r') as file:					# Opens the input file and reads it symbol by symbol
				for line in file:
					this_sequence = []
					for word in line.strip().split():
						for symbol in word:
							if symbol in accepted_values:			# Checks if the symbol is equal to '0' or '1', and if it is
								this_sequence.append(int(symbol))	# then adds that symbol to the sequence
					if this_sequence != []:
						self.all_sequences.append(this_sequence)
		except FileNotFoundError:
			self.input_file_exist = False
			self.reading_file_error = True
		except:
			self.input_file_exist = True
			self.reading_file_error = True
		else:
			self.input_file_exist = True
			self.reading_file_error = False



	def main_algorithm_optimized(self, max_substr_length):
		''' Takes a sequence and returns the subsequence so that it would have equal number 
		of digits "zero" & "one". More detailed explanation can be found in my report. '''

		global current_sequence
		substring =[]															# Defining the output array of found substrings
		found = False
		length_current_sequence = len(current_sequence)

		for substr_len in range(max_substr_length, 0, -1):
			starting_point, end_point = 0, substr_len*2
			while end_point<=length_current_sequence:
				one = current_sequence[starting_point:end_point].count(1)
				if one == substr_len:
					found = True
					if current_sequence[starting_point:end_point] not in substring:
						substring.append(current_sequence[starting_point:end_point])
					starting_point+=1
					end_point+=1
				else:
					difference = abs(substr_len-one)
					starting_point+=difference
					end_point+=difference
			if found:
				break
		return substring



	def main_algorithm_better(self, max_substr_length):
		''' Takes a sequence and returns the subsequence so that it would have equal number 
		of digits "zero" & "one". More detailed explanation can be found in my report. '''

		global current_sequence
		substring =[]															# Defining the output array of found substrings
		found = False
		length_current_sequence = len(current_sequence)

		for substr_len in range(max_substr_length, 0, -1):
			starting_point, end_point = 0, substr_len*2
			while end_point<=length_current_sequence:
				one = 0
				for element in current_sequence[starting_point:end_point]:		# Counts all digits "one" in the substring
					one += element												# Actually it's equal to the method "array.count(1)"
				if one == substr_len:
					found = True
					already_exist = self.check_if_exists(current_sequence[starting_point:end_point], substring)
					if not already_exist:
						substring.append(current_sequence[starting_point:end_point])
					starting_point+=1
					end_point+=1
				else:
					difference = abs(substr_len-one)
					starting_point+=difference
					end_point+=difference
			if found:
				break
		return substring



	def main_algorithm_brute(self):
		''' Takes a sequence and returns the subsequence so that it would have equal number 
		of digits "zero" & "one". More detailed explanation can be found in my report. '''
		
		global current_sequence
		substring =[]															# Defining the output array of found substrings
		found = False
		length_current_sequence = len(current_sequence)
		length = floor(length_current_sequence/2)								# Finding the starting number of searched pairs (0,1)

		for substr_len in range(length, 0, -1):									
			starting_point, end_point = 0, substr_len*2 						# Defining the size of the first subsequence (as a partition of an array)
			while end_point<=length_current_sequence:							# While we are within sequence edges - do the following 
				one = 0
				for element in current_sequence[starting_point:end_point]:		# Counts all digits "one" in the substring
					one += element												# It's equal to the function "array.count(1)"
				if one == substr_len:
					found = True
					already_exist = self.check_if_exists(current_sequence[starting_point:end_point], substring)
					if not already_exist: 										# Adding the found sequence to the array, if it isn't there already
						substring.append(current_sequence[starting_point:end_point])
				starting_point+=1												# Moving forward along the sequence
				end_point+=1
			if found:															# If the subsequence is found - stop searching
				break
		return substring 														# And return the result



	def check_if_exists(self, prey, sequence):
		''' Checks if the given prey exists in the array "sequence". In other words, it is 
		the equivalent to the native Python method "<object> in <object>".'''

		for element in sequence: 
			if element == prey:
				return True
		else:
			return False



	def sequence_to_string(self, sequence):
		''' Creates a beautiful string from the sequence with comas after each element except for the last one'''

		string = ''
		last_without_period = str(sequence.pop())
		for element in sequence:
			string += "{}, ".format(element)
		return string + last_without_period



	def give_answer(self, n_of_answ, answer = ''):
		'''Creates a file in the given path and adds an answer to it with respect to the amount of answers'''

		with open(self.path_out,'a', encoding='utf-8') as file:
			if self.iterator != 1:
				file.write('\n\n')

			file.write("Rozwiązanie dla ciągu №" + str(self.iterator))
			if self.enable_repeating_lists_before_output:
				file.write(' ({})'.format(self.sequence_to_string(current_sequence.copy())))
			file.write('\n')

			if n_of_answ==0:
				file.write("Dla takich danych wejściowych: {}\npodciąg zawierający równą".format(self.sequence_to_string(current_sequence)) + 
					" liczbę zer i jedynek nie istnieje.")

			elif n_of_answ==1:
				file.write('Najdłuższym podciągiem jest: ' + self.sequence_to_string(answer[0]))

			elif n_of_answ==2:
				file.write('Najdłuższymi podciągami są ' + self.sequence_to_string(answer[0]) + ' oraz ' + 
					self.sequence_to_string(answer[1]))

			elif n_of_answ>=3:
				file.write('Najdłuższymi podciągami są:\n')
				file.write(self.sequence_to_string(['('+self.sequence_to_string(ans)+')' for ans in answer]))



def porownanie_algorytmow():
	''' Here I would like to show instructions I used in
	the paragraph "Porównanie algorytmów" of my report'''

	# I HIGHLY RECOMMEND performing this function ONLY
	# after reading the description in the article, 
	# because in general it can take a long time to perform
	"""

	# Generating 20 random sequences of digits zero and one and writing them down to the file "report_rand_input.txt"
	# The following function is commented, because we already created this file before, 
	# so we don't need to create it one more time. Moreover, since the input data is the same, 
	# you can test this yourself and get similar results to one, shown in the report.
	# assist.random_sequence(path = ".\\tests\\report_rand_input.txt", lines = 20, start_length = 1000, increment = 0, multiplier = 1)

	# Creating an object of class binary_sequences
	test_1 = binary_sequences('.\\tests\\report_rand_input.txt', '.\\tests\\report_rand_output.txt')

	# Needed values have to be assigned to flags
	test_1.optimization_level = 1
	test_1.show_progress_bar = True

	# Now we can start our test
	test_1.solve_problem()

	# Since we are going to compare our algorithms, we need the time results information
	give_time(test_1)

	# Second algorithm test
	test_1.optimization_level = 2
	test_1.solve_problem()
	give_time(test_1)
	
	# Third algorithm test
	test(optimization_level = 3, path_in = '.\\tests\\report_rand_input.txt', path_out = '.\\tests\\report_rand_output.txt', 
		return_time = True, generate_new_data = False, show_progress_bar = True)
	
	# Creating a comparison of three algorithms using graph
	# Maybe we would like to comment all upper rows, since this function creates tests itself.
	algorithm_comparison(".\\tests\\report_rand_input.txt", ".\\tests\\report_rand_output.txt",generate_new_data = False, 
		show_progress_bar = True, width=1200, height=800, show_stats = False)
	
	assist.worst_sequence(path = ".\\tests\\report_worst_input.txt", lines = 20, start_repeats = 333, increment = 0, multiplier = 1)

	algorithm_comparison(".\\tests\\report_worst_input.txt", ".\\tests\\report_worst_output.txt",generate_new_data = False, 
		show_progress_bar = True, width=1200, height=800, show_stats = False)
	
	assist.worst_sequence(path = ".\\tests\\report_worst_increment_input.txt", lines = 20, start_repeats = 100, increment = 15, multiplier = 1)
	
	algorithm_comparison(".\\tests\\report_worst_increment_input.txt", ".\\tests\\report_worst_increment_output.txt",generate_new_data = False, 
		show_progress_bar = True, width=1200, height=800, show_stats = False)
	"""
	pass



def test(optimization_level = 3, path_in = '', path_out = '', return_time = True, worst_scenario = False,
	lines = 10, start_repeats = 30, start_length = 50, increment = 0, multiplier = 1, send_to_class = False,
	receiver_object = '', generate_new_data = True, show_progress_bar = False):
	''' Creates the test with random or the worst possible input data. 
	Be careful with the input and output files you are providing: they will be 
	replaced with the new automatically generated files, if generate_new_data flag is set to True'''

	from random import randrange as rand 													# Generation of the file names
	rand_koef = rand(1000)
	if path_in == '':
		path_in = ".\\tests\\input_opt_{0}_rand{1}.txt".format(optimization_level, rand_koef)
	if path_out == '':
		path_out = ".\\tests\\output_opt_{0}_rand{1}.txt".format(optimization_level, rand_koef)

	try:
		if worst_scenario and generate_new_data:											# Generation of an input file
			assist.worst_sequence(path_in, lines, start_repeats, increment, multiplier)
		elif generate_new_data:
			assist.random_sequence(path_in, lines, start_length, increment, multiplier)
	except FileNotFoundError as error:
		print("Wystąpił błąd: ", error)
	except:
		print("Przepraszamy, coś poszło nie tak ...")
	else:
		test_object = binary_sequences(path_in, path_out)									# Solving the problem if a file is created
		test_object.optimization_level = optimization_level
		test_object.show_progress_bar = show_progress_bar
		test_object.solve_problem()
		if return_time:
			give_time(test_object)
			if send_to_class:
				receiver_object.save_new_data(test_object.time_results, optimization_level)
		del test_object	



def algorithm_comparison(path_in='', path_out='', worst_scenario = False, generate_new_data = True, show_progress_bar = False,
	lines = 10, start_repeats = 10, start_length = 100, increment = 0, multiplier = 1, width=1200, height=800, show_stats = False):
	''' Creates the algorithm comparison with random or the worst possible input data. 
	Be careful with the input and output files you are providing: they will be 
	replaced with the new automatically generated files, if generate_new_data flag is set to True'''

	if worst_scenario and generate_new_data:
		assist.worst_sequence(path_in, lines = lines, start_repeats = start_repeats, increment = increment, multiplier = multiplier)
	elif generate_new_data:
		assist.random_sequence(path_in,  lines = lines, start_length = start_length, increment = increment, multiplier = multiplier)
																							# Defining the object of the class  assist.Graph
	graph_object = assist.Graph(worst_scenario=worst_scenario, increment=increment, 
		multiplier=multiplier, width=width, height=height, show_stats = show_stats)	
																							# Creating some tests with different optimization level
	test(path_in=path_in, path_out=path_out, show_progress_bar = show_progress_bar,
		optimization_level = 1, send_to_class=True, receiver_object=graph_object, return_time = True, generate_new_data = False)
	test(path_in=path_in, path_out=path_out, show_progress_bar = show_progress_bar,
		optimization_level = 2, send_to_class=True, receiver_object=graph_object, return_time = True, generate_new_data = False)
	test(path_in=path_in, path_out=path_out, show_progress_bar = show_progress_bar,
		optimization_level = 3, send_to_class=True, receiver_object=graph_object, return_time = True, generate_new_data = False)
	graph_object.paint_graph()																# Drawing the graph
	del graph_object



def give_time(object_):
	''' Returns time needed for each input sequence to be processed '''
	print("Czas przetwarzania każdego podciągu: ", object_.time_results)


def main():
	'''
	Main function of the whole program.

	Almost any possible format of input is accepted. For example:
	"1, 0, 1, 0"; "1,0,1,0"; "1 0 1 0"; " 1*0*1*0 "; "1, qwe0  e1 *0"; "1010".
	Every single of those inputs declares the following sequence: [1, 0, 1, 0]
	
	For more than one input, please separate them using a new line. For example this input:
	1111010111
	1101011010
	1011101010
	1111010101
	will be understood as 4 sequences. 
	[1, 1, 1, 1, 0, 1, 0, 1, 1, 1], [1, 1, 0, 1, 0, 1, 1, 0, 1, 0], 
	[1, 0, 1, 1, 1, 0, 1, 0, 1, 0], [1, 1, 1, 1, 0, 1, 0, 1, 0, 1]
	'''

	example_object = binary_sequences('input.txt', 'output.txt')	# Input the object of the class binary_sequences with two
																	# parameters: the path to the input & output files

	# Default values of the flags:
	example_object.enable_repeating_lists_before_output = False		# Enable to add the repetition of the input data in the output file	
	example_object.optimization_level = 3							# Level of algorithm optimisation. Accepted values: 1, 2, 3 (bigger is better).
	example_object.show_progress_bar = False						# Enable to see the progress bar. WORKS WELL ONLY IN CONSOLE. In python Shelf it looks ugly.


	example_object.enable_repeating_lists_before_output = True 		# When you are going to read the results it looks prettier, but while working 
																	# with large amounts of data it is likely to mess up the look of the output file.
																	# Since I would appreciate you to read the file 'output.txt', I am going to enable this flag

	# Launching the main function of the class 'binary_sequences'
	example_object.solve_problem()	


	# If you need to know how much time was needed to process each 
	# sequence you can use one of the next methods:
	print(example_object.time_results)								# Only prints the array of time records
	give_time(example_object)										# Does the same and also adds some pretty text

	# If you finished working with some object 
	# it is better to delete it than not, because
	# in that case it won't use any RAM
	del example_object


	test(															# You can also create tests using test() function, where:
		optimization_level = 1, 									# - level of algorithm optimisation, accepted values: 1, 2, 3;
		path_in = '.\\tests\\input_worst_scenario.txt', 			# - path, where new input file will be generated or existing file opened;
		path_out = '.\\tests\\output_worst_scenario.txt', 			# - path, where new output file will be created;
		return_time = True, 										# - flag, which asks if you would like to see used time results in console;
		generate_new_data = True,									# - flag, which asks if you would like to create a new input file or use an existing one;
		show_progress_bar = True, 									# - flag, which asks if you would like to see the progress bar (WORKS WELL ONLY IN CONSOLE);

		# Next options make changes only if generate_new_data flag is set to True:
		worst_scenario = True,										# - flag, which asks if the input file has to be filled with
																	#   the worst possible (True) strings or random (False) strings; 
		lines = 20, 												# - number of strings (lines) in a generated file;
		start_repeats = 10, 										# - number of repeats of the sequence '101' in the first line, if the worst scenario is chosen;
		start_length = 500, 										# - length of the first string (line), if random scenario is chosen;
		increment = 5,												# - increment of (repeats / length) of the (sequence '101' / line) after each line;
		multiplier = 1												# - multiplication of (repeats / length) of the (sequence '101' / line) after each line.
		)

	
	algorithm_comparison(											# You can also create algorithm comparison using algorithm_comparison() function, where:
		path_in = '.\\tests\\inp_comparison.txt', 					# - path, where new input file will be generated;
		path_out = '.\\tests\\out_comparison.txt', 					# - path, where new output file will be created;
		generate_new_data = True,									# - flag, which asks if you would like to create a new input file or use an existing one;
		show_progress_bar = True, 									# - flag, which asks if you would like to see the progress bar (WORKS WELL ONLY IN CONSOLE);
		height = 800,												# - height of the created graph (minimum 200, recommended 800);
		width = 1200,												# - width of the created graph (minimum 650, recommended 1200);
		show_stats = True,											# - shows the information about the increment and multiplier on the plot;

		# Next options make changes only if generate_new_data flag is set to True:
		worst_scenario = True,										# - flag, which asks if the input file has to be filled with 
																	#   the worst possible (True) strings or random (False) strings; 
		lines = 15, 												# - number of strings (lines) in a generated file;
		start_repeats = 50, 										# - number of repeats of the sequence '101' in the first line, if the worst scenario is chosen;
		start_length = 500,		 									# - length of the first string (line), if random scenario is chosen;
		increment = 5,												# - increment of (repeats / length) of the (sequence '101' / line) after each line;
		multiplier = 1												# - multiplication of (repeats / length) of the (sequence '101' / line) after each line.
		)


	# I HIGHLY RECOMMEND performing this function ONLY
	# after reading the description in the article, 
	# because in general it can take a long time to perform
	porownanie_algorytmow()
	
	# If you need the console not to close immediately after
	# finishing your task, then please uncomment the following two rows. 
	# import os 							
	# os.system("pause")



if __name__ == "__main__":
    main()