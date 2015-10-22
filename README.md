# quickquery
Designed to quickly and memory-efficiently query structured files, particularly genetics, for a set of substrings

The ```quickquery.py``` module  was created as a memory-efficient and speedy way to pull sections of text from a text file that has known structure.  The structure of the file must be such that `n_lines` correspond to one item and the  `place` line (within the n_lines) contains the string which will be searched for a query.

For example: n_lines = 3 , place = 3

The first few lines of the file to be searched for the queries "Marco" and "Polo" might be:

```
Malcom Reynolds
Serenity
Wash plays Marco Polo with reavers.
Spock
The needs of the many outweigh the needs of the few. 
Those are actually the Polo shirts of the future.
Obi-Wan Kenobi
These are not the lines you are looking for.
This is where you should check to make sure though!
```
The first six lines would be written to a new file, because the third and sixth line contain "Marco" and/or "Polo".

##Usage

###Command line
Command line ussage can be executed by

```
python quickquery.py -sf your_squence_file.txt -qf your_queries_file.txt
```
The arguments, all others of which are optional, are:

```
'-sf','--seq_file',
'-qf','--queries_file',
'-df','--dest_file',
'-nl','--n_lines',
'-pl','--place',
'-ty','--tally',
```
which refer, respectively, to
```
seq_file,queries_file, file_name="sequenced",n_lines=4, place=2, tally=tally_all
```

###As a module

The main worker function is:
> ```cqnc(seq_file,queries_file, file_name="sequenced",n_lines=4, place=2, tally=tally_all )```

where ```fille_name``` is the prefix of the destination file.

The module's docstring provides further details.


##Sample Input and Output:

```seq_file``` should be a .txt file of the form

Structured File: Genetic Sequencing

```
@HWI-ST397:233:D0E0LACXX
NGACAGTGCAGTCCAAGTACTCGCCTAAGTT
+
#4BDFFFFHHHHHJJJJIJJJJJJJJJJJJJ
@HWI-ST397:1186:2036 1:Y:0:
NGCANCAATTTGGCGGTTCAGCAGGAATGCCGAGACCGATCTCGT
+
#4;@#2@@@@@@??????>??==<<<:65888:8:5:<<8
```

```queries_file``` should be a .txt file of the form

Query File:  Genetic Sequences
```
AAAGTCGGTTCAGCAGG
CGGTTCAGTCAGCAGG
```
>Sample Output will be in the same form as in the Structured File

##TODO
Add auto unzip and zip functionality

Add auto execution on files in directories and their subdirectories

Potential future work:  partial string matching


##Contact
Kerstin Frailey, Department of Statistical Science, Cornell University

Nicholas Santantonio, Plant Breeding and Genetics, Cornell University
