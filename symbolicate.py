# how to use?
# copy your app, dsym file and log file ideally int the same folder
# call "python3 symbolicate.py -l <log_filename> -n <app_name>" to get symbolicated output
# you do not need to provide directory nor architecure if you are ok with default values

import sys
import getopt
import os
import subprocess


def main(argv):
    # defaults
    app_name = ""
    log_filename = ""
    directory = "./"
    architecture = "arm64"

    info = 'symbolicate.py -l <log_filename> -d <base_directory> -n <app_name> -a <architecture>'
    try:
        opts, args = getopt.getopt(argv, "hd:l:n:", [])
    except getopt.GetoptError:
        print(info)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(info)
            sys.exit()
        elif opt == '-l':
            log_filename = arg
        elif opt == '-d':
            directory = arg
        elif opt == '-n':
            app_name = arg
        elif opt == '-a':
            architecture = arg
    symbolicate_file(log_filename, directory, app_name, architecture)


def symbolicate_file(log_filename, directory, app_name, architecture):
    log_path = os.path.join(directory, log_filename)
    dsym_path = os.path.join(directory, app_name + ".app.dSYM")

    with open(log_path) as logfile:
        for line in logfile:
            matches = [app_name, "0x", "+"]
            if all(x in line for x in matches):
                words = line.split()
                method_address = ""
                relative_address_index = -1
                relative_address = ""
                line_number = ""
                for index, word in enumerate(words):
                    if index == 0:
                        if word.isdigit():
                            line_number = word + " "
                    if word.startswith("0x"):
                        method_address = word
                    elif word == "+":
                        relative_address_index = index + 1
                    elif relative_address_index == index:
                        relative_address = word

                if method_address != "" and relative_address != "":
                    symbolicate(directory, app_name, architecture, method_address, relative_address, line_number)
                else:
                    print(line, end='')
            else:
                print(line, end='')


def symbolicate(directory, app_name, architecture, method_address, relative_address, line_number):
    dsym_path = os.path.join(directory, app_name + ".app.dSYM")

    load_address = int(method_address, base=16) - int(relative_address)
    load_address_str = "{0:x}".format(load_address)

    cmd = 'atos -o ' + app_name + '.app/' + app_name + ' -l ' + load_address_str + ' ' + method_address + ' -arch ' + architecture
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output_bytes, error = process.communicate()

    atos_output = output_bytes.decode("utf-8")
    print(line_number + atos_output, end='')


if __name__ == "__main__":
    main(sys.argv[1:])
