import subprocess
from subprocess import Popen, PIPE
import time

def separate_paths(file_paths):
    return file_paths.split("\n")[:-1]  # Last split will be an empty path, so we need to remove it

def option_1():
    while True:

        print("######################################################### \n\n")
        filename = input("Please enter the file name you are looking for (example: 'test.txt'):\n> ")
        print("")
        file_path = subprocess.run(f'find /home -name {filename} -print 2>/dev/null | grep .', shell=True,
                                   capture_output=True)
        find_path_status = file_path.returncode

        if not find_path_status: # if the return code is 0 i.e. success
            file_paths = separate_paths(file_path.stdout.decode())
            print(f"{len(file_paths)} file(s) under that name were found:")
            for i in range(len(file_paths)):

                print(f"\nFile_#{i+1}: File is found at: {file_paths[i]}")
                inode_command = subprocess.run(f'ls -i {file_paths[i]}', shell=True,
                                               capture_output=True)  # returns inode + path
                print(f"\t\tinode number is: {inode_command.stdout.decode().split()[0]}")  # returns inode number only.

            choice = input("\nWould you like to see more details about this file / these files? [Y/N]\n> ").upper()
            if choice == 'Y':
                if len(file_paths) > 1:
                    while True:
                        id = int(input("\nEnter File_# of the file (1, 2, 3.. etc). Enter '-1' to quit:\n> "))
                        if id == -1:
                            break
                        if id > len(file_paths) or id <= 0:
                            print("Incorrect ID. Please Try Again...")
                            continue
                        else:
                            subprocess.run(f'stat {file_paths[id-1]}', shell=True)
                else:
                    subprocess.run(f'stat {file_paths[0]}', shell=True)

            time.sleep(1)
            choice = input("\n\nWould you like to check the inode of another file? [Y/N]\n> ").upper()
            if choice == 'N':
                return
        else:
            print("File is not found, please recheck the input filename if you are sure it's on the system.")

def option_2():
    while True:

        print("######################################################### \n\n")
        inode_number = int(input("Please enter the inode number you are looking for (example: '791910'):\n> "))
        print("")
        file_path = subprocess.run(f'find /home -inum {inode_number} -print 2>/dev/null | grep .', shell=True,
                                   capture_output=True)
        find_path_status = file_path.returncode

        if not find_path_status:  # if the return code is 0 i.e. success
            file_paths = separate_paths(file_path.stdout.decode())
            print(f"{len(file_paths)} file(s) under that inode were found:")
            for i in range(len(file_paths)):
                print(f"File_#{i + 1}: File is found at: {file_paths[i]}")
                inode_command = subprocess.run(f'ls -i {file_paths[i]}', shell=True,
                                               capture_output=True)  # returns inode + path
            if len(file_paths) > 1:
                note_string = "\nNote: \nFiles: "
                for i in range(len(file_paths)):
                    note_string += f"{file_paths[i]} and "
                note_string += note_string[-4]  # Remove last dangling 'and '
                note_string += " Are hard links."
                print(note_string)

            choice = input("\nWould you like to see more details about this inode? [Y/N]\n> ").upper()
            if choice == 'Y':
                if len(file_paths) > 1:
                    print("Hard Links details:")
                    for i in range(len(file_paths)):
                        print(f"\nFile {i+1} details:")
                        subprocess.run(f'stat {file_paths[i]}', shell=True)
                else:
                    subprocess.run(f'stat {file_paths[0]}', shell=True)

            time.sleep(1)
            choice = input("\n\nWould you like to search for another inode? [Y/N]\n> ").upper()
            if choice == 'N':
                return
        else:
            print("inode number is not found, please recheck the input inode if you are sure it's on the system.")

def option_3():
    print("\nNote: This service requires tcpdump package to be installed.")
    sudo_pass = input("\nThis service requires sudo privileges in order to proceed.\nPlease enter your "
                      "password (or Q to return to the main menu):\n> ")
    if sudo_pass == 'q' or sudo_pass == 'Q':
        return
    while True:
        print("\nA new capture is about to start...")
        filter_op = input("When would you like to terminate the capturing?\n"
                          "1. After N seconds\n"
                          "2. After N packet captures\nChoose 1 or 2. Enter '-1\ to return to main menu\n> ")
        if filter_op == '1':
            sec_count = int(input("After how many seconds should the program terminate?\n> "))
            subprocess.call('echo {} | sudo -S timeout {} tcpdump -i any -nn -w webserver.pcap'.format(sudo_pass, sec_count), shell=True)
            open_option = input("\nSuccess. a PCAB capture is saved to the current directory as this python "
                                "code's directory.\nWould you like to read this file now? [Y/N]\n> ").upper()
            if open_option == 'Y':
                subprocess.run(f'tcpdump -r webserver.pcap', shell=True)
                print("")
                time.sleep(2)

        elif filter_op == '2':
            packet_count = int(input("After how many packets should the program terminate?\n> "))
            subprocess.call(
                'echo {} | sudo -S tcpdump -i any -c{} -nn -w webserver.pcap'.format(sudo_pass, packet_count),
                shell=True)
            open_option = input("Success. a PCAB capture is saved to the current directory as this python "
                                "code's directory.\nWould you like to read this file now? [Y/N]\n> ").upper()
            if open_option == 'Y':
                subprocess.run(f'tcpdump -r webserver.pcap', shell=True)
                print("")
                time.sleep(2)
        elif filter_op == "-1":
            return





print("Welcome to Mini Forensics Tool!")
while True:
    option = int(input("\nThe tool has the following services:\n1. Find the inode number of a file.\n"
                       "2. Find the file that belongs to a specific inode.\n"
                       "3. Search for a keyword in a disk image.\n"
                       "4. Quit the Tool\n\nChoose an option (1, 2, 3, or 4):\n> "))
    if option == 1:
        option_1()
    elif option == 2:
        option_2()
    elif option == 3:
        option_3()
    elif option == 4:
        break
    else:
        print("Incorrect option. Please Enter a valid number.")
        time.sleep(1)














