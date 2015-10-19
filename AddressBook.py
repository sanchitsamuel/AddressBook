__author__ = 'Sanchit Samuel'
__license__ = "GPL v2"
__email__ = "sanchit.samuel@live.com"
__status__ = "beta"
__version__ = "2.0.0"
__date__ = "19 Oct' 2015"

#global start

first_name_cache = []
name_index_cache = {}
name_index_sorted_cache = {}

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
        read_file_object = open('contact.ab', 'r')
        for line in read_file_object:
            count += count
            temp_split_list = line.split('|')
            first_name_cache.append(temp_split_list[0])
            name_index_cache[temp_split_list[0]] = count
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

#end

run = True
build_cache(False)

print 'Welcome to Address Book \nversion {} {}'.format(__version__, __status__)

while run:
    command = str(raw_input('cmd > '))

    if command == 'exit':
        print
        print 'Thank you for using address book.'
        exit(0)

    elif not command:
        pass






    else:
        print 'Unrecognized command'