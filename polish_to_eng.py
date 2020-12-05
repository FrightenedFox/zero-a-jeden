def remove_special_symbols(special_symbols, path_in="input.txt", path_out="output.txt"):
	''' This function replaces all elements with the respect to dictionary special_symbols'''

	with open(path_in,'r', encoding='utf-8') as file_in:
		with open(path_out,'w', encoding='utf-8') as file_out:
			for line in file_in:
				for symbol in line:
					if symbol in special_symbols:
						file_out.write(special_symbols[symbol])
					else:
						file_out.write(symbol)



def dictionary_creator(dict_path="new_dict.txt"):
	''' You can create new dictionary faster using this function '''

	with open(dict_path,'w', encoding='utf-8') as dictionary:
		dictionary.write('new_dict = {\n')
		print("\nIf you want to stop the proces of dictionary creation then input '0'.")
		while True:
			key = input("\nPlease input the key: ")
			if key != '0':
				replacer = input("Please input the replacer: ")
				dictionary.write('"{}" : "{}",\n'.format(key, replacer))
			else:
				break
		dictionary.write('}')

polish_letters = {
"Ą" : "A",
"Ć" : "C",
"Ę" : "E",
"Ł" : "L",
"Ń" : "N",
"Ó" : "O",
"Ś" : "S",
"Ż" : "Z",
"Ź" : "Z",
"ą" : "a",
"ć" : "c",
"ę" : "e",
"ł" : "l",
"ń" : "n",
"ó" : "o",
"ś" : "s",
"ź" : "z",
"ż" : "z"}

remove_special_symbols(polish_letters, path_in ="podciagi.py", path_out ="podciagi_utf_8.py")

#dictionary_creator()