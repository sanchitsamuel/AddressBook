from collections import OrderedDict
import linecache
import time
import os

__author__ = 'Sanchit Samuel'
__license__ = "GPL v2"
__email__ = "sanchit.samuel@live.com"
__status__ = "beta"
__version__ = "2.0.0"
__date__ = "19 Oct' 2015"

# global start

first_name_cache = []
name_index_cache = OrderedDict()
name_index_sorted_cache = []
field_cache = OrderedDict()

# end

# function start

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
        linecache.updatecache('contacts.ab')
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
        return input_line_spliter('first@First Name|second@Second Name|phone@Phone Number|address@Address|')

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

def new_field():
    try:
        read_file_object = open('category', 'r')
        current = read_file_object.readline()
        read_file_object.close()
        write_file_object = open('category', 'w')
        core_name = str(raw_input('Enter the core name: '))
        current += core_name
        current += '@'
        print_name = str(raw_input('Enter visible name: '))
        current += print_name
        current += '|'
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
    try:
        write_file_object = open('contacts.ab', 'a')
        write_file_object.writelines(input_line)
        write_file_object.close()
    except IOError:
        write_file_object = open('contacts.ab', 'w')
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

def edit_contact(name):
    if name in name_index_cache:
        read_file_object = open('contacts.ab', 'r')
        all_contact_lines = read_file_object.readlines()
        read_file_object.close()
        contact_line = all_contact_lines[name_index_cache[name] - 1]
        contact_field_list = contact_line.split('|')
        fields_core = []
        fields_print = []
        fields_dict = get_fields()
        for key, value in fields_dict.items():
            fields_core.append(key)
            fields_print.append(value)
        new_line = ''
        for counter in range(0, len(fields_print)):
            new_line += fields_core[counter]
            new_line += '@'
            new_line += str(raw_input("Edit '{}', current '{}': ".format(fields_print[counter], contact_field_list[counter])))
            new_line += '|'
        else:
            new_line += '\n'

        all_contact_lines[name_index_cache[name] - 1] = new_line

        write_file_object = open('contacts.ab', 'w')
        write_file_object.writelines(all_contact_lines)
        write_file_object.close()
        build_cache()

    else:
        print "No contact found with the name '{}'".format(name)

def delete_contact(name):
    if name in name_index_cache:
        read_file_object = open('contacts.ab', 'r')
        all_contact_lines = read_file_object.readlines()
        read_file_object.close()
        del all_contact_lines[name_index_cache[name] - 1]
        write_file_object = open('contacts.ab', 'w')
        write_file_object.writelines(all_contact_lines)
        write_file_object.close()
        build_cache()
    else:
        print "No contact found with the name '{}'".format(name)

def print_help():
    print \
    '''usage: command -option [required_input]
|---command: 'print': prints the first name of all contacts in the order added
|   options:
|     -l   : prints all the fields of all the contacts in the order added
|     -l []: prints all the contacts with the specified field format in the order added
|     -o   : prints all the fields of all the contacts in the lexical order
|     -o []: prints all the contacts with the specified field format in the lexical order
|     -s []: searches and prints the contact info of the input name
|---command: 'new': creates a new contact entry
|---command: 'edit []': edits the given contact
|---command: 'delete []': deletes the given contact
|---command: 'field': lists all the fields with their core names to their visible names
|   options:
|     -n   : adds new field to the database
|---command: 'refresh': refreshes the cache, you don't really need to use this, but if the app displays
|            old or deleted data then this might help
|---command: 'about': displays information about the software, version authors and other stuff'''

# end

run = True
build_cache(False)

print 'Welcome to Address Book \nversion {} {}'.format(__version__, __status__)
if __status__ == 'beta':
    print '\tThe program is still in beta, please look in the issue list before using at, \n ' \
          '\thttps://github.com/sanchitsamuel/AddressBook/issues'

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
                start_time = time.time()
                line_from_name(command_split[2])
                print '\nTime taken {}s'.format(time.time() - start_time)

        else:
            print "Unrecognized parameter for 'print'"

    elif command.startswith('edit'):
        command_split = command.split(' ')
        if len(command_split) == 1:
            print "Invalid entry. Run 'help' for assistance."
        else:
            start_time = time.time()
            edit_contact(command_split[1])
            print '\nTime taken {}s'.format(time.time() - start_time)

    elif command.startswith('delete') or command.startswith('del'):
        command_split = command.split(' ')
        if len(command_split) == 1:
            print "Invalid entry. Run 'help' for assistance."
        else:
            start_time = time.time()
            delete_contact(command_split[1])
            print '\nTime taken {}s'.format(time.time() - start_time)

    elif command.startswith('fields'):
        if command == 'fields' or command == 'fields ':
            fields_dict = get_fields()
            for key, value in fields_dict.items():
                print '{:^15} for {:^15}'.format(key, value)
        else:
            if command == 'fields -n' or command == 'fields -n ':
                xnew_field()

    elif command == 'refresh ' or command == 'refresh':
        build_cache(True)

    elif command == 'test':
        pass
        # print_line('first@Sanchit|second@Samuel|phone@123456|address@23 Railway')
        # new_field()
        # read_contacts()
    elif command == 'clear' or command == 'clear ':
        os.system('cls')

    elif command == 'help' or command == 'help ':
        print_help()

    elif command == 'about' or command == 'about ':
        print '''Address book, {} {}
  In development since, {}
  Written by {} <{}>
  Licenced under {}'''.format(__version__, __status__, __date__, __author__, __email__, __license__)

    elif command == 'license':
        read_file_object = open('LICENSE', 'r')
        license = read_file_object.read()
        print license
        read_file_object.close()

    else:
        print 'Unrecognized command'