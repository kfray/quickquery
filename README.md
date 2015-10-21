# quickquery
Designed to quickly and memory-efficiently query structured files, particularly genetics, for a set of substrings

The ```quickquery.py``` module  was created as a memory-efficient and speedy way to pull sections of text from a text file that has known structure.  A file follow the form of `n_lines` correspond to one item, and the substring to be searched for occurs on the `place` line in each item.

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
