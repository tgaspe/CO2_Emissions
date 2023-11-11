# Theodoro Gasperin Terra Camargo
# 260842764

# Data Clean Up

# Modules
import doctest

def find_delim(column):
    '''(str) -> str
    Find and returns the delimiter of the column.
    Delimiters accounted for:
    tabs ('\t'), commas (','), spaces (' '), or dashes ('-').
    >>> find_delim("0 1 2 3,4")
    ' '
    >>> find_delim("cat\\tdog bat\\tcrab-cod")
    '\\t'
    '''
    delimeter = ['\t', ',', ' ', '-', '    ', '\\t']
    occurences_delim = {}
    
    for delim in delimeter:
        if delim in column:
            # count number of occurences of delim and add to dict
            occurences_delim[delim]= column.count(delim)
   
    #print(occurences_delim)
    
    # Raise exception
    if occurences_delim == {}:
        raise AssertionError('No delimeter found')
    
    max_key = max(occurences_delim, key = occurences_delim.get)
    return max_key


def clean_one(input_filename, output_filename):
    '''
    (str, str) -> int
    Takes two filenames as input.
    Creates a new file where it replaces the old delimeter for a tab delimeter. 
    >>> clean_one('small_raw_co2_data.txt', 'small_tab_sep_co2_data.tsv')
    10
    >>> clean_one('large_raw_co2_data.txt', 'large_tab_sep_co2_data.tsv')
    17452
    '''
    
    num_lines = 0
    
    fobj = open(input_filename, "r", encoding="utf-8")
    fobj2 = open(output_filename, "w", encoding="utf-8")
    
    for line in fobj:
        delim = find_delim(line)
        new_line = line.replace(delim, "\t")
        fobj2.write(new_line)
        num_lines += 1
        #print(new_line)
    
    fobj2.close()    
    fobj.close()   
    
    return num_lines



def final_clean(input_filename, output_filename):
    '''
    (str, str) -> int
    Takes a inputfile and creates a new one with the final editions to the columns.
    >>> final_clean('small_tab_sep_co2_data.tsv', 'small_clean_co2_data.tsv')
    10
    >>> final_clean('large_tab_sep_co2_data.tsv', 'large_clean_co2_data.tsv')
    17452
    '''
    
    num_lines = 0
    list_lines = []
    
    fobj = open(input_filename, "r", encoding="utf-8")
    fobj2 = open(output_filename, "w", encoding="utf-8")
    
    # Creating list to store columns
    for line in fobj:
        list_columns = line.split('\t')
        list_lines.append(list_columns)
            
            
    for line in list_lines:
        
        i = 0
        while i < len(line):
            # Conditions needed to fix
            # Large country names
            if line[2].isnumeric() == False:
                new_column = ' '.join(line[1:3])
                line.remove(line[2])
                line.remove(line[1])
                line.insert(1, new_column)
            # Comma in co2 and delimeter = comma
            if line[3].isnumeric() == True and '.' not in line[3] and len(line) > 5:
                if int(line[3]) < 1000:
                    new_column = '.'.join(line[3:5])
                    line.remove(line[4])
                    line.remove(line[3])
                    line.insert(3, new_column)
                
            if ',' in line[3]:
                new_column = line[3].replace(',', '.')
                line.remove(line[3])
                line.insert(3, new_column)
            i += 1
        new_line = '\t'.join(line)
        num_lines += 1
        #print(new_line)
        fobj2.write(new_line)
    
    fobj2.close()    
    fobj.close()   
    
    return num_lines



if __name__ == "__main__":
    doctest.testmod()