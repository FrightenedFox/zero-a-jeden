from time import time
start_time = time()		# Recording the time of the program start.

class binary_sequences:
	
	def __init__(self, path_in, path_out):
		''' Initialization of the class '''

		self.iterator = 0			# If more than one input was given, then this variable will help to iterate the whole process
		self.path_in = path_in
		self.path_out = path_out
		self.reading_file()
		self.enable_repeating_lists_before_output = False
		self.number_of_sequences = len(self.numbers)	# Number of sequences given in the input file



	def main(self):
		''' The main function. Iterates the process of searching substrings for each sequence.
		After completing the task it writes out small conclusion to the console. '''

		global current_sequence
		while self.iterator < self.number_of_sequences:
			current_sequence = self.numbers[self.iterator]
			self.iterator += 1
			n, k = current_sequence.count(0), current_sequence.count(1)	 # n, k - the quantity of digits "zero" & "one" respectively
			p = min(n,k)			# p - theoretical maximum of possible pairs (0,1)
			if n==k!=0:			# Checking for the easiest solutions when k=0, n=0 or n=k
				self.give_answer(1, [current_sequence])
			elif n==0 or k==0:
				self.give_answer(0, '')
			elif n>=1 and k>=1:
				self.algorithm(p)

		else:		# Writing of the conclusion with respect to conjugation of polish numerals
			last_digit=list(str(self.number_of_sequences)).pop()

			teened = False
			if self.number_of_sequences >=10:
				if str(self.number_of_sequences)[-2:] in ['11', '12', '13', '14']:		#excluding -teen numbers
					teened = True

			if last_digit=='1' and not teened:
				insert_text = 'wejściowy ciąg'
			elif last_digit in ['2', '3', '4'] and not teened:
				insert_text = 'wejściowy ciągi'
			else:
				insert_text = 'wejściowych ciągów'

			print("\n\nRozpoznano {0} {1} w pliku {2}. ".format(self.number_of_sequences, insert_text, self.path_in)+
				"Wszystkie odpowiedzi zostały zapisane w pliku {}. ".format(self.path_out) +
				"\nCzas roboty programu wynosi ", end='')



	def reading_file(self):
		''' Reading of the file containing input data and creating a clean output file'''

		with open(self.path_out,'w', encoding='utf-8') as file:		# Cleaning the output file
			pass

		self.numbers, accepted_values = [], ['0', '1']
		with open(self.path_in,'r', encoding='utf-8') as file:
			for line in file:
				this_sequence = []
				for word in line.strip().split():
					for i in word:
						if i in accepted_values:
							this_sequence.append(int(i))
				self.numbers.append(this_sequence)



	def algorithm(self, max_substr_length):
		''' Takes a sequence and returns the subsequence so that it would have equal number 
		of digits "zero" & "one". More detailed explanation can be found in my report. '''

		global current_sequence
		found, substring = False, []
		zero, one = self.zo_count(current_sequence)

		for substr_len in range(max_substr_length, 0, -1):
			starting_point = 0
			for i in range(1, len(current_sequence)+1):
				zero, one = self.zo_count(current_sequence[starting_point:i])
				while zero > substr_len or one > substr_len:
					starting_point+=1
					zero, one = self.zo_count(current_sequence[starting_point:i])
				if zero == substr_len and one == substr_len:
					found = True
					if current_sequence[starting_point:i] not in substring:
						substring.append(current_sequence[starting_point:i])
			if found:
				break
		self.give_answer(len(substring), substring)


	
	def zo_count(self, list_):
		'''Counts the number of digits "zero" & "one" in the given list'''
		return list_.count(0), list_.count(1)



	def sequence_to_string(self, sequence):
		''' Creates a beautiful string from the sequence with comas after each element except of the last one'''
		string = ''
		last_without_period = str(sequence.pop())
		for element in sequence:
			string += "{}, ".format(element)
		return string + last_without_period



	def give_answer(self, n_of_answ, answer):
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



'''
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
Io_oI = binary_sequences('input.txt', 'output.txt')

Io_oI.enable_repeating_lists_before_output = True

Io_oI.main()

print(time()-start_time, 's.\n\n')