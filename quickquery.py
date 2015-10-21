__author__ = "Kerstin Frailey, Cornell University Department of Statistics"
__credits__ = ["Kerstin Frailey", "Nicholas Santantonio"]
__email__ = "frailey@gmail.com"

"""This module was developed to provide quick querying of structured
    files in which finding a substring in one line then requires the
    copying of that line and nearby lines to be saved to a new file.

    This was particularly designed for genetic sequencing data of the
    of the format:

        Tag line
        Genetic sequencing
        +
        Bar Code

    in which the second line (place = 2) is the line of interest, and all four line
    (n_line = 4) must be written to the new file.

    Other than the default values, there is no reason the structured data must
    conform.  Alterations can be made by adjusting line and n_line appropriately.

    This module assumes that the strings of interest (queries) that are sought
    to be found in the specified line (as substrings) are in a .txt file
    in which each line is one query:

        geneticSubsequence1
        geneticSubsequence2

    Currently, this module assumes this .txt file can be held in memory.

    Found substrings can be written into one file (tally=tally_all) or into 
    separate files (tally=tally_each).

    TODO: Add zip and unzip capabilities.
    TODO: Add auto execution on files in directory and subdirectories.

"""

import argparse
import os
import copy

def sort_queries(queries_file):
    """Makes an intermediate list of queries, sorted, and a list
    of the number of pops that will be required from the stack.
    The number of pops is calculated between the (sorted) ith and
    (i+1)th string 
    """
    queries = []
    with open(queries_file, 'r') as q:
        for line in q:
            trimmed_line = line.replace('\n', "").replace('\r', "")
            queries += [trimmed_line]
    queries.sort()
    pops = [0]
    for i in range(1,len(queries)):
        pops.append(pop_count(queries[i-1],queries[i]))
    return queries, pops

def pop_count(old_string, new_string):
    """
    Counts the number of remaining characters in the old_string
    after and including the first character mismatch occurs
    between the old_string and the new_string.
    """
    
    i = 0 #the numbe of known matches
    smaller = min(len(old_string), len(new_string))
    while i < smaller:
        if old_string[i] == new_string[i]:
            i += 1
        else:
            break
    return len(old_string) - i 

def tally_all(lines_to_write, queries, file_name):
    """
    Writes each item with a found query to one file, in the order 
    as originally appeared.
    """

    with open(file_name + ".txt","a") as a:
        for line in lines_to_write:
            a.write(line)

def tally_each(lines_to_write, queries,  file_name):
    """
    Writes an item to the appropriate file (file_name_query.txt)
    for each query found in it.
    """

    for query in queries:
        with open( file_name + "_" + query + ".txt", "a") as f:
            for line in lines_to_write:
                f.write(line)

def cqnc(seq_file,queries_file, file_name="sequenced",n_lines=4,
             place=2, tally=tally_all ):
    """Reads from items of length n_lines in seq_file and checks to see if any
    query from the queries_file appears in the place line.  If so, it writes the item
    to file(s) according to the tally function specified."""

    queries, pops = sort_queries(queries_file)
    place = place - 1
    line_max = n_lines - 1
    with open(seq_file, 'r') as f:
        i = 0
        current_lines = []
        for line in f:
            if i < line_max:
                current_lines.append(line)
                i+=1
            elif i == line_max:
                current_lines.append(line)
                string = current_lines[place].replace('\n', "").replace('\r', "")
                matches = match_queries(string,copy.copy(queries), pops)
                if bool(matches):
                    tally(current_lines, matches, file_name)
                i = 0
                current_lines = []
            else:
                # TODO: throw an error
                print "Oh Nos!"


def match_queries(string, queries, pops):
    """
    Efficiently checks a string for each query in queries by employing
    *sorted* queries and a stack.

    Any subsequence beginning at the
    first character of a query is only checked once.  This is
    is accomplished by employing a stack structure to store 
    the last indices of matching subsequences and capitalizing
    on the sorted query list.
    """
    
    def match_next(string, letter, indices):
        """
        Given the last indices matching the previous substring, 
        checks the subsequent indices against the next character in
        the substring.
        """

        return [index + 1 for index in indices if (index + 1) < len(string) and string[index+1] == letter ]
    
    def match_string(string, query, stack):
        """
        Checks if a query is contained within a string
        and returns a stack of lists, such that list at position i
        is the list of indices of the string such that
        query[0:i] == string[index-i:index] .

        This is sped up by the passing of stacks between
        queries that share initial substrings.
        """
        
        for i in range(max(0,len(stack)-1), len(query)):
            if i == 0:
                stack.append(match_next(string, query[i], range(-1,len(string)-1)))
            else:
                stack.append(match_next(string, query[i], stack[-1]))
        return bool(stack[-1]), stack

    matches = []
    stack = []
    for query, pop in zip(queries, pops):
        for each in range(pop):
            stack.pop(-1)
        matched, stack = match_string(string, query, stack)
        if matched:
            matches.append(query)
    return matches

def main():
    parser = argparse.ArgumentParser(description="Do something.")
    parser.add_argument('-sf','--seq_file', type=str, required=True)
    parser.add_argument('-qf','--queries_file', type=str, required=True)
    parser.add_argument('-df','--dest_file', type=str, required=False)
    parser.add_argument('-nl','--n_lines', type=int)
    parser.add_argument('-pl','--place', type=int)
    parser.add_argument('-ty','--tally', type=int)
    args = parser.parse_args()
    args_dict = args.__dict__
    for key, arg in args_dict.items():
        if not arg:
            del args_dict[key]
    cqnc(**args_dict)

if __name__ == '__main__':
    main()