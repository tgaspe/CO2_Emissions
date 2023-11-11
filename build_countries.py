# Theodoro Gasperin Terra Camargo
# 260842764

# Build Countries

# Modules
import doctest
import copy

class Country:
    
    min_year_recorded = 2000
    max_year_recorded = 2000
    
    def __init__(self, iso_code, name, continents, year, co2_emission, pop):
        '''
        Instance attributes: iso_code (a string), name (a string), continents (a list of strings), co2_emissions
        (a dictionary mapping integers to floats), population (a dictionary mapping integers to integers).
        '''
        self.iso_code = iso_code
        self.name = name
        self.continents = continents[:]
        self.year = year
        if co2_emission != -1:
            self.co2_emissions = { year: co2_emission}
        else: self.co2_emissions = {}
        if pop != -1:
            self.population = { year: pop}
        else: self.population = {}
    
    def __str__(self):
        '''(self) -> str
        returns a string representation of a country containing the name, the
        continents (separated by a comma if more than one), and a string representation of both the
        co2_emissions dictionary and the population dictionary.
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> str(r)
        'Russia\\tASIA,EUROPE\\t{2007: 1604.778}\\t{2007: 14266000}'
        '''
        if len(self.continents) == 2:
            info = self.name + '\t' + str(self.continents[0] +','+ self.continents[1]) + '\t' + str(self.co2_emissions) + '\t' + str(self.population)
        else:
            info = self.name + '\t' + str(self.continents[0]) + '\t' + str(self.co2_emissions) + '\t' + str(self.population)
        # fix russia (two continents)
        return info
    
    def add_yearly_data(self, data):
        '''
        takes as input a string with the year, co2 emissions, and population, all separated by a tab. This method updates the appropriate attributes of
        the country. Note that if the co2 emission or the population data is an empty column, then no
        changes should be made to the corresponding attribute. 
        >>> a = Country("AFG", "Afghnistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> a.co2_emissions == {1949: 0.015, 2018: 9.439}
        True
        >>> a.population == {1949: 7663783, 2018: 37122000}
        True
        '''
        
        try:
            # Unpacking data, separating columns
            year, co2, pop = data.split('\t')
            # Adding keys to respective dict
            if co2 != '':
                self.co2_emissions[int(year)] = float(co2)
            if pop.strip('\n') != '':
                self.population[int(year)] = int(pop.strip('\n'))
            
            # Update class attributes
            if int(year) < Country.min_year_recorded:
                Country.min_year_recorded = int(year)
            if int(year) > Country.max_year_recorded:
                Country.max_year_recorded = int(year)
        
        except ValueError:
            print(data)
            year, column = data.split('\t')
            # if column is the pop
            if type(column) == int:
                pop = column
                co2 = -1
                # Adding keys to respective dict
                self.co2_emissions[int(year)] = float(co2)
                self.population[int(year)] = int(pop)
            # if column is the co2
            if type(column) == float:
                co2 = column
                pop = -1
                self.co2_emissions[int(year)] = float(co2)
                self.population[int(year)] = int(pop)
            
            # Update class attributes
            if int(year) < Country.min_year_recorded:
                Country.min_year_recorded = int(year)
            if int(year) > Country.max_year_recorded:
                Country.max_year_recorded = int(year)
            
    def get_co2_emissions_by_year(self, year):
        '''
        It returns the co2 emission of the country
        in the specified year if available. It returns 0.0 otherwise.
        >>> a = Country("AFG", "Afghnistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> a.get_co2_emissions_by_year(1949)
        0.015
        >>> a.get_co2_emissions_by_year(2000)
        0.0
        '''
        if year in self.co2_emissions:
            return self.co2_emissions[year]
        else:
            return 0.0
    
    def get_co2_per_capita_by_year(self, year):
        '''
        Return the co2 emission per capita in tonnes
        (note that the co2 emissions for a country are recorded in
        millions of tonnes) for the specified year if available. If either the co2 emissions or the population
        of the country are not available for the specified year, the method returns None.
        >>> a = Country("AFG", "Afghnistan", ["ASIA"], 1949, -1, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> round(a.get_co2_per_capita_by_year(2018), 5)
        0.25427
        >>> print(a.get_co2_per_capita_by_year(1949))
        None
        '''
        if year in self.population:
            
            co2_per_capita = (self.get_co2_emissions_by_year(year) * 1000000) / self.population[year]
            
            if co2_per_capita == 0.0:
                return None
            
            return co2_per_capita

    
    def get_historical_co2(self, year):
        '''
        It return the
        historical (total) co2 emission in millions of tonnes that the country has produced for all years up
        to and including the specified year
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> q.get_historical_co2(2000)
        45.277
        >>> q.get_historical_co2(2007)
        108.176

        '''
        total_emission = 0.0
        
        for years in sorted(self.co2_emissions):
            if years <= year:
                total_emission += self.get_co2_emissions_by_year(years)

        
        return total_emission
    
    @classmethod
    def get_country_from_data(cls, data):
        '''
        Return a new Country object created from the data in the input string.
        >>> a = Country.get_country_from_data("ALB\\tAlbania\\tEUROPE\\t1991\\t4.283\\t3280000")
        >>> a.__str__()
        'Albania\\tEUROPE\\t{1991: 4.283}\\t{1991: 3280000}'
        '''
        data1 = data.strip('\n')
        column = data1.split('\t')
        #print(column)
        
        if column[4] == "":
            column[4] = -1
        if column[5] == "":
            column[5] = -1
            
        return cls(column[0], column[1], [column[2]], int(column[3]), float(column[4]), int(column[5]))
        
            
    
    @staticmethod
    def get_countries_by_continent(list_countries):
        '''
        The method returns a dictionary mapping a string representing a continent to a list of countries (i.e., objects of type Country) which all belong to that continent. The
        order in which each country appears in the list should match the order in which they appeared in
        the input list.
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> d = Country.get_countries_by_continent(c)
        >>> str(d['ASIA'][1])
        'Russia\\tASIA,EUROPE\\t{2007: 1604.778}\\t{2007: 14266000}'
        '''
        continents_dict = {}
        
        for country in list_countries:
            continent_name = country.continents
            if type(continent_name) == list:
                for continent in continent_name:
                    if continent not in continents_dict:
                        continents_dict[continent] = list()
                    if continent in list(continents_dict):
                        continents_dict[continent].append(country)
                    
            else:   
                if continent_name not in continents_dict:
                    continents_dict[continent_name] = list()
                if continent_name in list(continents_dict):
                    continents_dict[continent_name].append(country)
        
        return continents_dict
    
    @staticmethod
    def get_total_historical_co2_emissions(list_countries, year):
        '''
        The method returns a float
        representing the total co2 emissions (in millions of tonnes) produced by all the countries in the
        input list for all years up to and including the specified year.
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> b.add_yearly_data("1991\\t4.283\\t3280000")
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = [b, r, q]
        >>> Country.get_total_historical_co2_emissions(c,2007)
        1721.161
        >>> Country.get_total_historical_co2_emissions(c,2000)
        49.56

        '''
        total_co2 = 0
        for country in list_countries:
            total_co2 += country.get_historical_co2(year)
        
        return total_co2
    
    @staticmethod
    def get_total_co2_emissions_per_capita_by_year(list_countries, year):
        '''
        The method returns
        the co2 emissions per capita in tonnes produced by the countries in the given list in the specified
        year.
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [b, r]
        >>> round(Country.get_total_co2_emissions_per_capita_by_year(c,2007), 5)
        92.98855

        '''
        try:
            total_co2 = 0
            total_pop = 0 
            for country in list_countries:
                # In case one of the data point is missing
                if year not in country.co2_emissions or year not in country.population:
                    continue
                #print(country, country.population, country.co2_emissions)
                total_co2 += country.get_co2_emissions_by_year(year)
               #print(country.population[year])
                total_pop += country.population[year]
                
            # In case one of the total values is 0
            if total_co2 == 0 or total_pop == 0:
                return 0.0
            else:
                return total_co2*1000000/total_pop
        
        except ZeroDivisionError:
            
            total_co2 = 0
            total_pop = 1 
            for country in list_countries:
                if year not in country.co2_emissions or year not in country.population:
                    continue
                #print(country, country.population, country.co2_emissions)
                total_co2 += country.get_co2_emissions_by_year(year)
               #print(country.population[year])
                total_pop += country.population[year]
                
            
            return total_co2*1000000/total_pop



    @staticmethod
    def get_co2_emissions_per_capita_by_year(list_countries, year):
        '''
        The method returns a
        dictionary mapping objects of type Country to floats representing the co2 emissions per capita in
        tonnes produced by the country in the specified year. Note that it is possible that some of the
        values in the output dictionary might be None. This could occur when the co2 per capita of that
        country for the specified year cannot be computed.
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> b.add_yearly_data("1991\\t4.283\\t3280000")
        >>> c = [b, r]
        >>> d1 = Country.get_co2_emissions_per_capita_by_year(c,2007)
        >>> len(d1)
        2
        >>> round(d1[r], 5)
        112.4897
        >>> d2 = Country.get_co2_emissions_per_capita_by_year(c, 1991)
        >>> print(d2[r])
        None
        >>> round(d2[b], 5)
        1.30579
        '''
        dict_country_co2_capita = {}
        
        for country in list_countries:
            dict_country_co2_capita[country] = country.get_co2_per_capita_by_year(year)
        
        return dict_country_co2_capita
    
    @staticmethod
    def get_historical_co2_emissions(list_countries, year):
        '''
        The method returns a dictionary
        mapping objects of type Country to floats representing the total co2 emissions (in millions of
        tonnes) produced by that country for all years up to and including the specified year
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> b.add_yearly_data("1991\\t4.283\\t3280000")
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = [b, r, q]
        >>> d1 = Country.get_historical_co2_emissions(c,2007)
        >>> len(d1)
        3
        >>> round(d1[q], 5)
        108.176
        >>> d2 = Country.get_historical_co2_emissions(c, 1991)
        >>> print(d2[r])
        0.0
        >>> round(d2[b], 5)
        4.283
        '''
        
        dict_country_co2_historical = {}
        
        for country in list_countries:
            dict_country_co2_historical[country] = float(country.get_historical_co2(year))
        
        return dict_country_co2_historical
    
    @staticmethod
    def get_top_n(dict_country, n):
        '''
        The method returns a list of tuples. Each tuple is made up by the
        iso code of a country and the number to which the country is mapped in the input dictionary. Only
        the countries that map to the top n values should appear in the list. The tuples in the list should
        appear sorted on the values in descending order. If there are countries that map to the same values,
        the countries should be compared based on the alphabetical order of their names. Please note that
        this function should NOT modify the input dictionary
        >>> a = Country("ALB", "Albania", [], 0, 0.0, 0)
        >>> b = Country("AUT", "Austria", [], 0, 0.0, 0)
        >>> c = Country("BEL", "Belgium", [], 0, 0.0, 0)
        >>> d = Country("BOL", "Bolivia", [], 0, 0.0, 0)
        >>> e = Country("BRA", "Brazil", [], 0, 0.0, 0)
        >>> f = Country("IRL", "Ireland", [], 0, 0.0, 0)
        >>> g = Country("MAR", "Marocco", [], 0, 0.0, 0)
        >>> h = Country("NZL", "New Zealand", [], 0, 0.0, 0)
        >>> i = Country("PRY", "Paraguay", [], 0, 0.0, 0)
        >>> j = Country("PER", "Peru", [], 0, 0.0, 0)
        >>> k = Country("SEN", "Senegal", [], 0, 0.0, 0)
        >>> l = Country("THA", "Thailand", [], 0, 0.0, 0)
        >>> d = {a: 5, b: 5, c: 3, d: 10, e: 3, f: 9, g: 7, h: 8, i: 7, j: 4, k: 6, l: 0}
        >>> t = Country.get_top_n(d, 10)
        >>> t[:5]
        [('BOL', 10), ('IRL', 9), ('NZL', 8), ('MAR', 7), ('PRY', 7)]
        >>> t[5:]
        [('SEN', 6), ('ALB', 5), ('AUT', 5), ('PER', 4), ('BEL', 3)]
        '''
    
        
        # Create list of tuples
        list_tuples = []
        for country in dict_country:
            t = (dict_country[country], country.iso_code)
            list_tuples.append(t)
            
        # Sort list and invert it
        a_list = sorted(list_tuples)
        new_list = a_list[::-1]
        
        # Make list in right order
        right_list = []
        for country in new_list:
            t1 = (country[1], country[0])
            right_list.append(t1)
            
        # In case of tie alphabetic order
        for i in range(len(right_list)):
            if i < (len(right_list)-1):
                if right_list[i][1] == right_list[i + 1][1]:
                    a, b =  right_list.index(right_list[i]),  right_list.index(right_list[i+1])
                    right_list[b], right_list[a] = right_list[a], right_list[b]
                  
        
        return right_list[:n]
            

def  get_countries_from_file(filename):
    '''
    This function takes as input a string representing a filename which has exactly the same format as
    the output file generated by the function add_continents_to_data. The function creates and return a
    dictionary mapping ISO country codes (strings) to objects of type Country based on the data in the file.
    >>> d1 = get_countries_from_file("small_co2_data.tsv")
    >>> len(d1)
    9
    >>> str(d1['ALB'])
    'Albania\\tEUROPE\\t{2002: 3.748}\\t{2002: 3126000}'
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> len(d2)
    193
    '''
    iso_dict = {}
    
    fobj = open(filename, "r", encoding="utf-8")
    
    for line in fobj:
        #print(line)
        a = Country.get_country_from_data(line)
        if a.iso_code not in iso_dict:
            iso_dict[a.iso_code] = a
        if a.iso_code in iso_dict:
            columns = line.strip('\n').split('\t')
            #print(columns)
            data = '\t'.join(columns[3:])
            iso_dict[a.iso_code].add_yearly_data(data)

    fobj.close()
    
    
    return iso_dict


if __name__ == "__main__":
    doctest.testmod()
