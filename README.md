# **Zero A Jeden**  
*By Vitalii Morskyi*  

***

This project is a part of the curriculum in "Algorytmy i Struktury danych"
of the Polytechnic University of Rzeszów, Poland.  
  
## The task that was needed to be solved  
  
*For a string (in the form of an array) containing only the values 0 or 1, find a substring that contains an equal number of ones and zeros whose length is the greatest.* [*original task*][1]  
  
## Navigation through files and folders  
  
A detailed explanation of my thoughts and decisions made to optimize the algorithm can be found in file `"Sprawozdanie.docx"`.  

The main file of the program is named `"podciagi.py"`.  
There is also exists an assistant program in the file `"assistant_module.py"`, where some necessary functions are held.  
  
In the file `"Block diagram.drawio"` you can find the block diagrams of the following functions:
 * `reading_file()`
 * `solve_problem()`
 * `main_algorithm_brute()`
 * `main_algorithm_better()`
 * `main_algorithm_optimized()`
 * `check_if_exists()`
  
The folder `tests` is used to keep input and output files.  
In the folder `Pictures` are saved all pictures used in the project.  
  
## Conclusions  
  
A program, that finds all the longest substrings of an input string that have the same number of ones and zeros, has been developed. In order for every file creation method to work with my program, an advanced file reader feature has been created that accepts almost any file. In order not to create the data manually each time, several helper functions have been written that can generate input depending to the given settings. The algorithm was optimized three times and all three versions were compared with each other. In order to more clearly demonstrate the optimization of the algorithms, another program was created that draws graphs of the dependence of the algorithm execution time on each substring. All the optimizations and improvements are clearly presented in graphical diagrams of the main algorithm. Block diagrams and pseudocodes were created for the functions of reading files, rejecting the simplest cases, and main algorithms.  

***

  
![Project logo](/Pictures/logo.png)
  
[1]: https://i.imgur.com/Y6qv6ld.png "Link to the original task screen shot"