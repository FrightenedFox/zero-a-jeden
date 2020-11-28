from time import *

try:
	import assistant_module	as assist	# Another part of my program where some cool functions are placed.
										# File assistant_module.py should be located in the same folder with this file (podciagi.py)
except ModuleNotFoundError:
	print("Wystąpił błąd!\nUmieść pliki „assistant_module.py” i „podciagi.py” w tym samym folderze.")
	import sys, os
	os.system("pause")
	sys.exit()
except:
	print("Przepraszamy, coś poszło nie tak ... \nSprawdź, czy pliki „assistant_module.py” i „podciagi.py” znajdują się w tym samym folderze.")
	import sys, os
	os.system("pause")
	sys.exit()



class binary_sequences:
	
	def __init__(self, path_in = 'input.txt', path_out = 'output.txt', path_stats = 'statistics.txt'):
		''' Initialization of the class and assigning default values to flags'''
		self.path_in = path_in
		self.path_out = path_out
		self.path_stats = path_stats
		self.reading_file()
		self.enable_repeating_lists_before_output = False
		self.optimization_level = 3



	def solve_problem(self):
		''' The main function. Iterates the process of searching substrings for each sequence.
		After completing the task it writes out small conclusion to the console. '''

		global current_sequence
		self.iterator = 0								# If more than one input was given, then this variable will help to iterate the whole process
		self.number_of_sequences = len(self.all_sequences)	# Number of sequences given in the input file
		self.time_results = [] 							# List of records of the time used by algorithm function

		while self.iterator < self.number_of_sequences:
			current_sequence = self.all_sequences[self.iterator]
			self.iterator += 1

			k = current_sequence.count(1)	 # n, k - the quantity of digits "zero" & "one" respectively
			n = len(current_sequence)-k
			p = min(n,k)			# p - theoretical maximum of possible pairs (0,1)

			if n==k!=0:				# Checking for the easiest solutions when k=0, n=0 or n=k
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
					print("|\nNieprawidłowo określony poziom optymalizacji. Wybrano ustawienia domyślne.")
					self.optimization_level = 3
					substring = self.main_algorithm_optimized(p)
				end_time = time()					# Recording the time of the main algorithm end

				self.time_results.append(round(end_time - start_time,3))
				self.give_answer(len(substring), substring)

		else:		# Writing of the conclusion with respect to conjugation of polish numerals

			if self.input_file_exist and not self.reading_file_error:
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

				print("|\nRozpoznano {0} {1} w pliku \"{2}\". ".format(self.number_of_sequences, insert_text, self.path_in)+
					"Wszystkie odpowiedzi zostały zapisane w pliku \"{}\". ".format(self.path_out) +
					"\nWybrany {} poziom optymalizacji.".format(self.optimization_level)+
					"\nCzas roboty algorytmu wynosi {} s.".format(time_used) + 
					"\nŚredni czas przetwarzania jednego ciągu wynosi {} s.\n|".format(avarage_time_used))

			elif not self.input_file_exist and self.reading_file_error:
				print("|\nNie znaleziono pliku według ścieżki \"{}\".\n| ".format(self.path_in))
			elif self.input_file_exist and self.reading_file_error:
				print("|\n|\nCoś poszło nie tak.\n|")



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
		substring =[]
		found = False
		for substr_len in range(max_substr_length, 0, -1):
			starting_point, end_point = 0, substr_len*2
			while end_point<=len(current_sequence):
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
		substring =[]
		found = False
		for substr_len in range(max_substr_length, 0, -1):
			starting_point, end_point = 0, substr_len*2
			while end_point<=len(current_sequence):
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
		
		import math
		global current_sequence
		substring =[]
		length = math.floor(len(current_sequence)/2)
		found = False
		for substr_len in range(length, 0, -1):
			starting_point, end_point = 0, substr_len*2
			while end_point<=len(current_sequence):
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
			if found:
				break
		return substring



	def check_if_exists(self, prey, sequence):
		''' Checks if the given prey exists in the array "sequence". In other words it is 
		an equiwalent to the native Python method "<object> in <object>".'''

		for element in sequence: 
			if element == prey:
				return True
		else:
			return False



	def sequence_to_string(self, sequence):
		''' Creates a beautiful string from the sequence with comas after each element except of the last one'''
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



def test(optimization_level = 3, path_in = '', path_out = '', return_time = True, worst_scenario = False,
	lines = 10, start_repeats = 30, start_length = 50, increment = 0, multiplier = 1):
	''' Creates the test with the random or worst possible input data. 
	Be careful with the input and output files you are giving: they will be 
	replaced with the new automatically generated files. '''

	from random import randrange as rand 												# Generation the file names
	rand_koef = rand(1000)
	if path_in == '':
		path_in = "input_opt_{0}_rand{1}.txt".format(optimization_level, rand_koef)
	if path_out == '':
		path_out = "output_opt_{0}_rand{1}.txt".format(optimization_level, rand_koef)

	try:
		if worst_scenario:																	# Generation an input file
			assist.worst_sequence(path_in, lines, start_repeats, increment, multiplier)
		else:
			assist.random_sequence(path_in, lines, start_length, increment, multiplier)
	except FileNotFoundError as error:
		print("Wystąpił błąd: ", error)
	except:
		print("Przepraszamy, coś poszło nie tak ...")
	else:
		test_object = binary_sequences(path_in, path_out)									# Solving the problem if file is created
		test_object.optimization_level = optimization_level
		test_object.solve_problem()
		if return_time:
			give_time(test_object)
			assist.draw_graph(test_object.time_results)
		del test_object



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


	example_object.enable_repeating_lists_before_output = True 		# When you are going to read the results it looks prettier, but while working 
																	# with large amounts of data it is likely to mess up the look of the output file
																	# As I would appreciate you to read the file 'output.txt', I am going to enable this flag

	# Launching of the main function of the class 'binary_sequences'
	example_object.solve_problem()	


	# If you need to know how much time was needed to process each 
	# sequence you can use one of the next methods:
	print(example_object.time_results)								# Only prints the array of time records
	give_time(example_object)										# Do the same and also adds some pretty text


	test(															# You can also create tests using test() function, where:
		optimization_level = 2, 									# - level of algorithm optimisation, accepted values: 1, 2, 3;
		path_in = '.\\tests\\input_worst_scenario.txt', 			# - path, where new input file will be generated;
		path_out = '.\\tests\\output_worst_scenario.txt', 			# - path, where new output file will be created;
		return_time = True, 										# - flag, which asks if you would like to see used time results in console;
		worst_scenario = True, 										# - flag, which asks if the input file have to be filled with random strings or worst strings; 
		lines = 40, 												# - number of strings (lines) in generated file;
		start_repeats = 10, 										# - number of repeats of the sequence '101' in the first line, if worst scenario is chosen;
		start_length = 50, 											# - length of the first string (line), if random scenario is chosen;
		increment = 10, 											# - increment of (repeats / length) of the (sequence '101' / line) after each line;
		multiplier = 1)												# - multiplication of (repeats / length) of the (sequence '101' / line) after each line.

	# import os
	# os.system("pause")

if __name__ == "__main__":
    main()
