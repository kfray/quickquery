import os
import copy

def sort_queries(queries_file):
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
    # this wants the input file in the form A AG AGC AGT AGTC CA CAC CC CCA ie alphabetized, with shortest prefernce 
    i = 0 #the numbe of known matches
    smaller = min(len(old_string), len(new_string))
    while i < smaller:
        if old_string[i] == new_string[i]:
            i += 1
        else:
            break
    return len(old_string) - i 

def tally_all(lines_to_write, queries, file_name):
    with open(file_name + ".txt","a") as a:
        for line in lines_to_write:
            a.write(line)

def tally_each(lines_to_write, queries,  file_name):
    for query in queries:
        with open( file_name + "_" + query + ".txt", "a") as f:
            for line in lines_to_write:
                f.write(line)

def cqnc(seq_file,queries_file, file_name="sequenced",n_lines=4, place=1, tally=tally_all ):
    """reads into a list a file that executes query on n_lines sets"""
    queries, pops = sort_queries(queries_file)
    line_max = n_lines - 1
    with open(seq_file, 'r') as f:
        i = 0
        current_lines = []
        for line in f:
            if i < line_max:
                # append four lines at a time for 0,1,2
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
    """ takes a string and finds all matches for sequnce up to an index, so the stacj is a list of lists, which at i is the list
    of indices of sthe string that are found in the current querry"""
    def match_next(string, letter, indices):
        return [index + 1 for index in indices if (index + 1) < len(string) and string[index+1] == letter ]
    def match_string(string, query, stack):
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

