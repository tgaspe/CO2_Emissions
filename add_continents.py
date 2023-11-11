# Theodoro Gasperin Terra Camargo
# 260842764

# Add Continents

# Modules
import doctest

def get_iso_codes_by_continent(filename):
    '''
    (str) -> dict
    takes as input a string representing a
    filename of a file that has the same format as iso_codes_by_continent.tsv. The function returns a
    dictionary mapping continents’ names (all upper case) to a list of ISO codes (strings) of countries
    that belongs to that continent. The order in which the ISO codes appear in the list should be the
    same in which they appear in the input file
    >>> d = get_iso_codes_by_continent("iso_codes_by_continent.tsv")
    >>> len(d['ASIA'])
    50
    >>> len(d['NORTH AMERICA'])
    23
    >>> d['AFRICA'][0]
    'NGA'
    >>> d['EUROPE'][2]
    'BLR'
    '''
    
    continents_dict = {}
    list_countries = []
    
    fobj = open(filename, "r", encoding="utf-8")
    
    for line in fobj:
        country = line.split("\t")
        list_countries.append(country)
    
    fobj.close()
    
    for country in list_countries:
        continent_name = country[1].strip("\n").upper()
        if continent_name not in continents_dict:
            continents_dict[continent_name] = list()
        if continent_name in list(continents_dict):
            continents_dict[continent_name].append(country[0])           
                
    return continents_dict

#d = get_iso_codes_by_continent("iso_codes_by_continent.tsv")
#print(d)

def dict_countries_in_two_continents(filename):
    ''' (str) -> dict
    Helper function; creates a dict where the iso is the key and the value is a list with the continent(s).
    Return a dict with only the iso with two continents
    
    '''
    
    list_countries = []
    iso_dict = {}
    
    fobj = open(filename, "r", encoding="utf-8")
    
    for line in fobj:
        country = line.split("\t")
        list_countries.append(country)
    
    fobj.close()
    
    for country, continents in list_countries:
        # Countries in two continents
        continent = continents.strip("\n").upper()
        if country not in iso_dict:
            iso_dict[country] = list()
        if country in iso_dict:
            iso_dict[country].append(continent)
   
    iso_dict1 = dict(iso_dict)
    for key in iso_dict: 
        if len(iso_dict[key]) == 1:
            del iso_dict1[key]

            
    return iso_dict1

#print(dict_countries_in_two_continents("iso_codes_by_continent.tsv"))

def add_continents_to_data(input_filename, continents_filename, output_filename):
    ''' (str, str, str) -> int
    The only change that should happen to the data is that in the output file a column should be added
    with the continent to which each country belongs. This should be the third column in the file, the
    one right after the name of the country. Note that there are some countries that are considered to
    be part of two continents. For these countries, write both continents separated by a comma.
    >>> add_continents_to_data("small_clean_co2_data.tsv", "iso_codes_by_continent.tsv", "small_co2_data.tsv")
    10
    >>> add_continents_to_data("large_clean_co2_data.tsv", "iso_codes_by_continent.tsv", "large_co2_data.tsv")
    17452
    '''
    num_lines = 0
    cont_dict = get_iso_codes_by_continent(continents_filename)
    list_lines = []
    iso_dict = dict_countries_in_two_continents(continents_filename)
    
    # Opening files
    fobj = open(input_filename, "r", encoding="utf-8")
    fobj2 = open(output_filename, "w", encoding="utf-8")
    
    # Creating list to store columns
    for line in fobj:
        list_columns = line.split('\t')
        list_lines.append(list_columns)
        num_lines += 1
    
    # Check country and insert continent column
    #Abacaxi_count = 0
    for line in list_lines:
        # Fixing BUG
        if line[0] in iso_dict and ',' not in line[2] and len(line) == 6:  
            co2_column = ".".join(line[3:5])
            line.remove(line[4])
            line.remove(line[3])
            line.insert(3, co2_column)
            #print(line)
        
        for continent in list(cont_dict):
            
            if line[0] in iso_dict and len(line) <= 5:
            
                two_continents = ','.join(iso_dict[line[0]])
                line.insert(2, two_continents)
                new_line = '\t'.join(line)
                #print(new_line)
                fobj2.write(new_line)
                #Abacaxi_count +=1
            
            elif line[0] in cont_dict[continent] and len(line) <= 5:
                line.insert(2, continent)
                #print(line)
                new_line = '\t'.join(line)
                #print(new_line)
                fobj2.write(new_line)
                #Abacaxi_count +=1
                
            # Fixing bug! Went crazy because of this shit. 
            elif line[0] in cont_dict[continent] and line[0] not in iso_dict and len(line) == 6:
                co2_column = ".".join(line[3:5])
                new_line = line[:]
                new_line.remove(line[4])
                new_line.remove(line[3])
                new_line.insert(3, co2_column)
                new_line.insert(2, continent)
                new_new_line = '\t'.join(new_line)
                fobj2.write(new_new_line)
                #Abacaxi_count += 1
                
    #print(Abacaxi_count)
                
    
    # Closing files
    fobj.close()
    fobj2.close()
    
    return num_lines
      
#print(add_continents_to_data("testing_final_large_data.tsv", "iso_codes_by_continent.tsv", "TheLARGE_data.tsv"))
    
if __name__ == "__main__":
    doctest.testmod()