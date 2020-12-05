# **Zero A Jeden**  
*By Vitalii Morskyi*  

***

This project is a part of the curriculum in "Algorytmy i Struktury danych"
of the Polytechnic University of Rzeszów, Poland.  
  
## The task that was needed to be solved  
  
*For a string (in the form of an array) containing only the values of 0 or 1, find a substring that contains an equal number of ones and zeros whose length is the greatest.* [*original task*][1]  

Example:  
	Input file: `0, 0, 1, 0, 1, 0, 0`  
	Output file: `Najdłuższymi podciągami są 0, 1, 0, 1 oraz 1, 0, 1, 0`.  
  
## Navigation through files and folders  
  
A detailed explanation of my thoughts and decisions made to optimize the algorithm can be found in the file `"Sprawozdanie.docx"`.  

The main file of the program is named `"podciagi.py"`.  
There also exists an assistant program in the file `"assistant_module.py"`, where some necessary functions are held.  
  
In the file `"Block diagram.drawio"` you can find the block diagrams of the following functions:
 * `reading_file()`
 * `solve_problem()`
 * `main_algorithm_brute()`
 * `main_algorithm_better()`
 * `main_algorithm_optimized()`
 * `check_if_exists()`
  
The folder `tests` is used to keep input and output files.  
In the folder `Pictures`, all pictures used in the project are saved.  
  
## Recommendations regarding file executing  

1. Due to special polish symbols used in the file `"podciagi.py"`, sometimes it can not be executed from the Bash (maybe from some other terminals as well). I found two ways to solve this problem:  
	 - use another python file `"polish_to_eng.py"`, which creates exact copy of the file `"podciagi.py"`, but with all special characters replaced by the Latin letters.  
	 - or rewrite each `print("Some text")` method as `print("Some text".encode("utf-8"))`.  
	The second solution helps to avoid the throwing of the error too, but won't look as good as the first one, because encoded characters will appear in the text.  
2. If the progress bar in your environment looks like this:  
	`Przetwarzanie pliku ".\tests\input_worst_scenario.txt" : [----------] 0.0%  
	Przetwarzanie pliku ".\tests\input_worst_scenario.txt" : [----------] 5.0%  
	Przetwarzanie pliku ".\tests\input_worst_scenario.txt" : [#---------] 10.0%  
	Przetwarzanie pliku ".\tests\input_worst_scenario.txt" : [##--------] 15.0% `  
	(repeats instead of changing in one line),  
	than probably you would like to turn off the progress bar at all. In order to do this, please set flag `show_progress_bar` in the file `"podciagi.py"` to `false`.  
  
## Conclusions  
  
A program, that finds all the longest substrings of an input string that have the same number of ones and zeros, has been developed. In order for every file creation method to work with my program, an advanced file reader feature has been created accepting any input file. In order not to create the data manually each time, several assistant functions have been written which can generate input depending on the given settings. The algorithm was optimized three times and all three versions were compared with each other. In order to more clearly demonstrate the optimization of the algorithms, another program has been created that draws graphs of the dependence of the algorithm execution time on each substring. All the optimizations and improvements are clearly presented in graphical diagrams of the main algorithm. Block diagrams and pseudocodes have been created for the functions of reading files, rejecting the simplest cases, and main algorithms.  

***

  
![Project logo](/Pictures/logo.png)
  
[1]: https://i.imgur.com/Y6qv6ld.png "Link to the original task screen shot"