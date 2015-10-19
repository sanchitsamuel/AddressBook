from collections import OrderedDict
import linecache

__author__ = 'Sanchit Samuel'
__license__ = "GPL v2"
__email__ = "sanchit.samuel@live.com"
__status__ = "beta"
__version__ = "2.0.0"
__date__ = "19 Oct' 2015"

#global start

first_name_cache = []
name_index_cache = OrderedDict()
name_index_sorted_cache = OrderedDict()

#end

#fuction start

def build_cache(verbose = False):
    global first_name_cache
    global name_index_cache
    global name_index_sorted_cache
    count = 0

    first_name_cache[:] = []
    name_index_cache.clear()
    name_index_sorted_cache.clear()

    try:
        read_file_object = open('contacts.ab', 'r')
        for line in read_file_object:
            count += count
            temp_split_list = line.split('|')
            temp_split_field_list = temp_split_list[0].split('@')
            first_name_cache.append(temp_split_field_list[1])
            name_index_cache[temp_split_field_list[1]] = count
        read_file_object.close()
        #sort the index cache
    except IOError:
        if verbose:
            print 'Contact database not found'
        else:
            pass

def sort_index_cache():
    global name_index_cache
    global name_index_sorted_cache

    name_index_sorted_cache = sorted(name_index_cache.items(), key = lambda t: t[0])

def input_line_spliter(input_line):
    temp_dict = OrderedDict()
    temp_list = input_line.split('|')
    for counter in range(0, len(temp_list) - 1):
        temp_split_category_list = temp_list[counter].split('@')
        temp_dict[temp_split_category_list[0]] = temp_split_category_list[1]
    return temp_dict

def get_fields():
    try:
        fields = linecache.getline('category', 1)
        fields_list = fields.split('|')
        fields_dict = OrderedDict()
        fields_dict = input_line_spliter(fields)
        return fields_dict
    except IOError:
        return input_line_spliter('first@First Name|second@Second Name|phone@Phone Number|address@Address')

def print_line(input_line, number = 0):
    temp_dict = input_line_spliter(input_line)
    fields_dict = get_fields()
    fields_print = []
    fields_core = []
    for key, value in fields_dict.items():
        fields_core.append(key)
        fields_print.append(value)

    if number == 0:
        for counter in range(0, len(fields_dict)):
            print '{:^14}'.format(fields_print[counter]),
        else:
            print

    for size in range(0, len(fields_core)):
        if fields_core[size] in temp_dict:
            print '{:^14}'.format(temp_dict[fields_core[size]]),
        else:
            print '{:^14}'.format(''),
    else:
        print
    #for line in temp_dict.items():
    #    print

def new_field():
    try:
        read_file_object = open('category', 'r')
        current = read_file_object.readline()
        read_file_object.close()
        write_file_object = open('category', 'w')
        current += '|'
        core_name = str(raw_input('Enter the core name: '))
        current += core_name
        current += '@'
        print_name = str(raw_input('Enter visible name: '))
        current += print_name
        write_file_object.write(current)
        write_file_object.close()
    except IOError:
        print 'No field config found. Create default(yes or no)? '

def new_contact():
    fields_dict = get_fields()
    fields_print = []
    fields_core = []
    input_line = ''
    for key, value in fields_dict.items():
        fields_core.append(key)
        fields_print.append(value)

    for size in range(0, len(fields_print)):
        input_line += fields_core[size]
        input_line += '@'
        input_line += str(raw_input('\tEnter {}: '.format(fields_print[size])))
        input_line += '|'
    input_line += '\n'

    write_file_object = open('contacts.ab', 'a')
    write_file_object.writelines(input_line)
    write_file_object.close()
    build_cache()

    #print input_line


def read_contacts():
    count = 0
    try:
        read_file_object = open('contacts.ab', 'r')
        for line in read_file_object:
            print_line(line, count)
            count += 1
        read_file_object.close()
    except IOError:
        print 'Contact DB not found'


#end

run = True
build_cache(False)

print 'Welcome to Address Book \nversion {} {}'.format(__version__, __status__)

while run:
    command = str(raw_input('cmd > '))

    if command == 'exit':
        print 'Thank you for using address book.'
        exit(0)

    elif not command:
        pass

    elif command == 'print':
        read_contacts()

    elif command == 'test':
        #print_line('first@Sanchit|second@Samuel|phone@123456|address@23 Railway')
        #new_field()
        #read_contacts()
        new_contact()


    else:
        print 'Unrecognized command'