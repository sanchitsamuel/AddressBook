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
name_index_sorted_cache = []
field_cache = OrderedDict()

#end

#fuction start

def build_cache(verbose = False):
    global first_name_cache
    global name_index_cache
    global name_index_sorted_cache
    global field_cache
    count = 0

    first_name_cache[:] = []
    name_index_cache.clear()
    name_index_sorted_cache[:] = []
    field_cache.clear()

    try:
        read_file_object = open('contacts.ab', 'r')
        for line in read_file_object:
            count += 1
            temp_split_list = line.split('|')
            temp_split_field_list = temp_split_list[0].split('@')
            first_name_cache.append(temp_split_field_list[1])
            name_index_cache[temp_split_field_list[1]] = count
        read_file_object.close()
        sort_index_cache()
        field_cache = get_fields()
    except IOError:
        if verbose:
            print 'Contact database not found'
        else:
            pass

def sort_index_cache():
    global name_index_cache
    global name_index_sorted_cache

    name_index_sorted_cache = sorted(name_index_cache.items(), key=lambda t: t[0])

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

def line_from_name(name, format = 'default'):
    global name_index_cache
    if name in name_index_cache:
        index = name_index_cache[name]
        line = linecache.getline('contacts.ab', int(index))
        if format == 'default':
            print_line(line)
    else:
        print 'No contact by the name {} found in the database'.format(name)

def print_line(input_line, number = 0, format = 'null'):
    temp_dict = input_line_spliter(input_line)
    fields_dict = get_fields()
    fields_print = []
    fields_core = []
    for key, value in fields_dict.items():
        fields_core.append(key)
        fields_print.append(value)

    custom_field_list = format.split(',')

    if number == 0 and format == 'null':
        for counter in range(0, len(fields_dict)):
            print '{:^14}'.format(fields_print[counter]),
        else:
            print
    elif not format == 'null' and number == 0:
        for counter in range(0, len(custom_field_list)):
            print '{:^14}'.format(field_cache[custom_field_list[counter]]),
        else:
            print

    if format == 'null':
        for size in range(0, len(fields_core)):
            if fields_core[size] in temp_dict:
                print '{:^14}'.format(temp_dict[fields_core[size]]),
            else:
                print '{:^14}'.format(''),
        else:
            print
    else:
        for size in range(0, len(custom_field_list)):
            if custom_field_list[size] in temp_dict:
                print '{:^14}'.format(temp_dict[custom_field_list[size]]),
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
        build_cache()
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

def print_all_contacts(format = 'default'):
    count = 0
    try:
        read_file_object = open('contacts.ab', 'r')
        for line in read_file_object:
            if format == 'default':
                print_line(line, count)
            else:
                print_line(line, count, format)
            count += 1
        read_file_object.close()
    except IOError:
        print 'Contact DB not found'

def print_first_contact_name():
    global first_name_cache
    serial = 1
    print 'Listing all contacts'
    for item in first_name_cache:
        print '\t{}. '.format(serial),
        print item
        serial += 1

def print_ordered_all_contacts(format = 'default'):
    global name_index_sorted_cache
    count = 0
    for key, value in name_index_sorted_cache:
        line = linecache.getline('contacts.ab', value)
        if format == 'default':
            print_line(line, count)
        else:
            print_line(line, count, format)
        count += 1

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

    elif command == 'new' or command == 'new ':
        new_contact()

    elif command.startswith('print'):
        if command == 'print ' or command == 'print':
            print_first_contact_name()

        elif command.startswith('print -l'):
            command_split = command.split(' ')
            if len(command_split) == 2:
                print_all_contacts()
            else:
                format = command_split[2]
                check_field_list = format.split(',')
                if set(check_field_list) < set(field_cache.keys()):
                    print_all_contacts(format)
                else:
                    print "Invalid field format. Run 'help' for assistance."

        elif command.startswith('print -o'):
            command_split = command.split(' ')
            if len(command_split) == 2:
                print_ordered_all_contacts()
            else:
                format = command_split[2]
                check_field_list = format.split(',')
                if set(check_field_list) < set(field_cache.keys()):
                    print_ordered_all_contacts(format)
                else:
                    print "Invalid field format. Run 'help' for assistance."

        elif command.startswith('print -s'):
            command_split = command.split(' ')
            if len(command_split) == 2:
                print "Invalid entry. Run 'help' for assistance."
            else:
                line_from_name(command_split[2])

        else:
            print "Unrecognized parameter for 'print'"

    elif command == 'refresh ' or command == 'refresh':
        build_cache(True)

    elif command == 'test':
        # print_line('first@Sanchit|second@Samuel|phone@123456|address@23 Railway')
        # new_field()
        # read_contacts()
        pass

    elif command == 'license':
        read_file_object = open('LICENSE', 'r')
        license = read_file_object.read()
        print license
        read_file_object.close()


    else:
        print 'Unrecognized command'