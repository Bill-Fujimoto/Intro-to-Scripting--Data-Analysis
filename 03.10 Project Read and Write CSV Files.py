"""
Project for Week 3 of "Python Data Analysis".
Read and write CSV files using a dictionary of dictionaries.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv

def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Ouput:
      A list of strings corresponding to the field names in
      the given CSV file.
    """
    with open(filename, "r", newline = '') as csv_file:
        csvreader = csv.DictReader(csv_file, \
                                   delimiter=separator, quotechar=quote) #skipinitialspace=True
        return csvreader.fieldnames

##print(read_csv_fieldnames("table1.csv", ",","'"))
##print(read_csv_fieldnames("table2.csv", ",",'"'))
##print(read_csv_fieldnames("table3.csv", ",", "'"))
##print(read_csv_fieldnames("table4.csv", ",", "'"))
##print(read_csv_fieldnames("table5.csv", ",",'"'))
##print(read_csv_fieldnames("table6.csv", ",", "'"))
##print(read_csv_fieldnames("table7.csv", ",", "'"))

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    with open(filename, "r", newline = '') as csv_file:
        list_dict=[]
        csvreader = csv.DictReader(csv_file, \
                                   delimiter=separator, quotechar=quote) #skipinitialspace=True
        for row in csvreader:
            list_dict.append(row)
        
        return list_dict

##print(read_csv_as_list_dict("table1.csv", ",","'"))
##print(read_csv_as_list_dict("table2.csv", ",",'"'))
##print(read_csv_as_list_dict("table3.csv", ",", "'"))
##print(read_csv_as_list_dict("table4.csv", ",", "'"))
##print(read_csv_as_list_dict("table5.csv", ",",'"'))
##print(read_csv_as_list_dict("table6.csv", ",", "'"))
##print(read_csv_as_list_dict("table7.csv", ",", "'"))

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    with open(filename, "r", newline = '') as csv_file:
        dict_of_dict={}
        csvreader = csv.DictReader(csv_file, \
                                   delimiter=separator, quotechar=quote) #skipinitialspace=True
        for row in csvreader:
            dict_of_dict[row[keyfield]] = row
            
        return dict_of_dict

##print(read_csv_as_nested_dict("table1.csv", "Field1", ",", "'"))
##print(read_csv_as_nested_dict("table2.csv", "Field1", ",", '"'))
##print(read_csv_as_nested_dict("table3.csv", "Field1", ",", "'"))
##print(read_csv_as_nested_dict("table4.csv", '"Field', ",", "'"))
##print(read_csv_as_nested_dict("table5.csv", "Field, 1;'Field 2'", ",",'"'))
##print(read_csv_as_nested_dict("table6.csv", "FD;1", ",", "'"))
##print(read_csv_as_nested_dict("table7.csv", "3bcd;", ",", "'"))

def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames.  The CSV file should use the given separator and
      quote characters.  All non-numeric fields will be quoted.
    """
##    for row in table:
##        print(row)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,\
                                fieldnames, quoting=csv.QUOTE_NONNUMERIC, \
                                delimiter=separator, quotechar=quote)
        writer.writeheader()
        for row in table:
##            print(row)
            writer.writerow(row)


fields = read_csv_fieldnames("table2.csv", ",", "'")
print(fields)
table = read_csv_as_list_dict("table2.csv", ",", "'")
print(table)

write_csv_from_list_dict("table2_new.csv", table, fields, ",", "'")
##print(read_csv_as_nested_dict("table1.csv", "Field1", ",", "'"))
##print(read_csv_as_nested_dict("table2.csv", "Field1", ",", '"'))
##print(read_csv_as_nested_dict("table3.csv", "Field1", ",", "'"))
##print(read_csv_as_nested_dict("table4.csv", '"Field', ",", "'"))
##print(read_csv_as_nested_dict("table5.csv", "Field, 1;'Field 2'", ",",'"'))
##print(read_csv_as_nested_dict("table6.csv", "FD;1", ",", "'"))
##print(read_csv_as_nested_dict("table7.csv", "3bcd;", ",", "'"))