import time
import argparse
import os
import datetime
import shutil

#error codes:
#   1 -d directory does not exist


def main():

    #init parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required=True, action="store", help="directory to backup from")
    parser.add_argument("-b", "--backup-dir", required=False, action="store", default=None, help="directory to backup to")

    #parse arguments
    args = parser.parse_args()

    #get backup dir if none was specified
    backup_dir = args.backup_dir
    if args.backup_dir == None:
        backup_dir = os.path.expanduser("~/backup")
    else:
        backup_dir = os.path.expanduser(args.backup_dir)

    #get backup from dir
    backup_from = os.path.expanduser(args.directory)

    #remove / at end
    if backup_dir[-1] == "/":
        backup_dir = backup_dir[:-1]
    if backup_from[-1] == "/":
        backup_from = backup_from[:-1]

    #backup dir
    backup_files(backup_from, backup_dir)


def backup_files(backup_from, backup_to):

    #check args are correct
    is_directory = check_backup_paths(backup_from, backup_to)

    #create new backup directory
    new_backup = backup_to + "/" + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    os.mkdir(new_backup)

    #get list of files to backup
    new_file_list = get_backup_file_list(backup_from, new_backup, is_directory)

    #compare/link files
    if os.path.exists(backup_to + "/latest"):
        compare_files(new_file_list, backup_from, backup_to, new_backup)

    #copy files
    copy_files(new_file_list, new_backup)

    #link latest to current
    if os.path.exists(backup_to + "/latest"):
        os.unlink(backup_to + "/latest")
    time.sleep(1)

    try:
        os.symlink(new_backup, backup_to + "/latest")
    except OSError as e:
        print("COULD NOT LINK " + backup_to + "/latest" + " TO " + new_backup)

def check_backup_paths(backup_from, backup_to):
    #check that to exists
    if not os.path.isdir(backup_to):
        #attempt to create backup dir
        os.mkdir(backup_to, 0o700)

    #check that from exists
    is_directory = False
    if os.path.isfile(backup_from):
        is_directory = False
    elif os.path.isdir(backup_from):
        is_directory = True
    else:
        print("link_backup:  " + backup_from + " does not exist")
        exit(1)

    return is_directory

def get_backup_file_list(backup_from, backup_to, is_directory):
    #if file just put file in list and return
    if not is_directory:
        return [backup_from]

    #now recursively generate a list of files
    return get_backup_files(backup_from, backup_from, backup_to)

def get_backup_files(directory, backup_from, backup_to):
    #init list
    current_list = []

    #check if file
    if os.path.isfile(directory):
        return [directory]

    #check if is the backup dir
    if directory == backup_to:
        return []

    #mkdir the new backup dir
    print("backup_to: " + backup_to)
    print("directory: " + directory)
    print(backup_to + directory)
    os.makedirs(backup_to + directory)

    #get list of files/dirs in directory
    list_objects = os.listdir(directory)

    #loop
    for obj in list_objects:
        current_list = current_list + get_backup_files(directory + "/" + obj, backup_from, backup_to)

    #return list
    return current_list


def compare_files(new_file_list, backup_from, backup_to, backup_dir):
    #compare current with last backup, if the same hard link to last backup
    #this is to save space instead of copying multiple times
    i = 0
    while i < len(new_file_list):
        new_file = new_file_list[i]
        backup_file = backup_dir + "/" + new_file
        latest_file = backup_to + "/latest" + new_file
        mod_time_new = -1
        mod_time_old = 1
        try:
            mod_time_old = int(os.path.getmtime(new_file))
            mod_time_new = int(os.path.getmtime(latest_file))
        except OSError as e:
            print("NOLINK:  " + latest_file + " not found!")
        if mod_time_new == mod_time_old:
            print("LINK: " + new_file)
            os.link(latest_file, backup_file)
            new_file_list.pop(i)
        else:
            print("NOLINK:  " + str(mod_time_old) + " <> " + str(mod_time_new))
            i = i + 1
    return

def copy_files(new_file_list, new_backup):
    #copy every file left in new_file_list
    for new_file in new_file_list:
        print("COPY:  " + new_file)
        shutil.copyfile(new_file, new_backup + "/" + new_file)
        mod_time = os.path.getmtime(new_file)
        acc_time = os.path.getatime(new_file)
        #set mod time to be the same
        os.utime(new_backup + "/" + new_file, (acc_time, mod_time))

if __name__ == "__main__":
    main()