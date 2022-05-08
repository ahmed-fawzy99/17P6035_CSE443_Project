import os
import subprocess
import time

clear = lambda: os.system('clear')


def separate_paths(file_paths):
    return file_paths.split("\n")[:-1]  # Last split will be an empty path, so we need to remove it


def find_inode_of_file():
    while True:
        clear()
        filename = input("Please enter the file name you are looking for (example: 'test.txt'):\n> ")
        print("")
        file_path = subprocess.run(f'find {search_dir} -name {filename} -print 2>/dev/null | grep .', shell=True,
                                   capture_output=True)
        find_path_status = file_path.returncode

        if not find_path_status:  # if the return code is 0 i.e. success
            file_paths = separate_paths(file_path.stdout.decode())
            print(f"{len(file_paths)} file(s) under that name were found:")
            for i in range(len(file_paths)):
                print(f"\nFile_#{i + 1}: File is found at: {file_paths[i]}")
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
                            subprocess.run(f'stat {file_paths[id - 1]}', shell=True)
                else:
                    subprocess.run(f'stat {file_paths[0]}', shell=True)

            time.sleep(1)
            choice = input("\n\nWould you like to check the inode of another file? [Y/N]\n> ").upper()
            if choice == 'N':
                return
        else:
            input("File is not found, please recheck the input filename if you are sure it's on the system.")


def find_file_by_inode():
    while True:
        clear()
        inode_number = int(input("Please enter the inode number you are looking for (example: '791910'):\n> "))
        print("")
        file_path = subprocess.run(f'find {search_dir} -inum {inode_number} -print 2>/dev/null | grep .', shell=True,
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
                        print(f"\nFile {i + 1} details:")
                        subprocess.run(f'stat {file_paths[i]}', shell=True)
                else:
                    subprocess.run(f'stat {file_paths[0]}', shell=True)

            time.sleep(1)
            choice = input("\n\nWould you like to search for another inode? [Y/n]\n> ").upper()
            if choice == 'N':
                return
        else:
            input("inode number is not found, please recheck the input inode if you are sure it's on the system.")


def packet_capture():
    print("\nNotes:\n1- This service requires tcpdump package to be installed.\n2- This tool requires sudo "
          "privileges. You will be asked for sudo password in the procedure")
    protocol_checked = False
    # subprocess.run(command, shell=True)

    while True:
        command = ""
        clear()
        print("A new capture is about to start...")
        time.sleep(1)
        print(
            "\nEnter 'q' to quit. \nPlease enter the name of interface to capture with. Choose 'any' if you are "
            "unsure:\n")
        subprocess.run("tcpdump -D", shell=True)
        interface = input("> ").lower()
        if interface == 'q':
            return
        command = f"sudo -S tcpdump -i {interface} -nn -w webserver.pcap"
        filter_op = input("\nEnter 'q' to quit and return to the main menu.\nWould you like to filter the traffic ["
                          "port-src-dst-protocol]? [Y/n/q]\n> ").upper()
        if filter_op == 'Q':
            return
        elif filter_op == 'Y':
            while True:
                filters = input("\nChoose filter options (choose a number): \n>1. Filter by Port Number\n>2. Filter by "
                                "Protocol\n>3. Filter by Destination\n>4. Filter by Source\nEnter 'r' return to "
                                "previous menu\n> ")
                if filters == '1':
                    port = input("\nEnter the port number to filter with [example: 80]:\n> ")
                    if not port.isnumeric():
                        print("you entered a non-integer value. Please try again.")
                    else:
                        command += f" port {port}"
                        print("Port filter is added.")

                elif filters == '2':
                    protocol = input("\nEnter the Protocol you want to filter with [example: tcp, udp, etc]:\n> ")
                    command += f" {protocol}"
                    protocol_checked = True
                    print("Protocol filter is added.")

                elif filters == '3':
                    dst = input("\nEnter the destination you want to filter traffic to [example: 192.168.1.251]:\n> ")
                    if protocol_checked:
                        command += f" and dst {dst}"
                    else:
                        command += f" dst {dst}"
                    print("Destination filter is added.")

                elif filters == '4':
                    src = input("\nEnter the source you want to filter traffic from [example: 192.168.1.2]:\n> ")
                    if protocol_checked:
                        command += f" and src {src}"
                    else:
                        command += f" src {src}"
                    print("Source filter is added.")

                elif filters == 'r':
                    break

        capture_termination_choice = input("\nWhen would you like to terminate the capturing?\n"
                                           "1. After N seconds\n"
                                           "2. After N packet captures\nChoose 1 or 2. Enter '-1' to return to main "
                                           "menu\n> ")
        if capture_termination_choice == '1':

            sec_count = int(input("\nAfter how many seconds should the program terminate?\n> "))
            cmd_index = command.find('tcpdump')
            command = command[:cmd_index] + f"timeout {sec_count} " + command[cmd_index:]
            subprocess.run(command, shell=True)
            open_option = input("\nSuccess. a PCAP capture is saved to the current directory as this python "
                                "code's directory.\nWould you like to read this file now? [Y/N]\n> ").upper()
            if open_option == 'Y':
                subprocess.run(f'tcpdump -r webserver.pcap', shell=True)
                time.sleep(1)
                input("\nEnter any key to continue..")


        elif capture_termination_choice == '2':
            packet_count = int(input("\nAfter how many packets should the program terminate?\n> "))
            command += f" -c{packet_count}"
            subprocess.run(command, shell=True)
            open_option = input("Success. a PCAP capture is saved to the current directory as this python "
                                "code's directory.\nWould you like to read this file now? [Y/N]\n> ").upper()
            if open_option == 'Y':
                subprocess.run(f'tcpdump -r webserver.pcap', shell=True)
                time.sleep(1)
                input("\nEnter any key to continue..")
        elif capture_termination_choice == "-1":
            return


def bit_by_bit_image():
    while True:
        clear()
        print("\nNote: This tool requires sudo "
              "privileges. You will be asked for sudo password in the procedure")
        time.sleep(1)
        print(f"\nHere's a list of all devices mounted currently on the system:\n")
        subprocess.run(f'lsblk -e7 -o NAME,SIZE', shell=True)
        input_disk = "/dev/"
        input_disk += input("\nWARNING: Please be extremly careful at choosing input and output disks. Enter 'q' or "
                            "quit to exit "
                            "\nPlease enter the name of the disk to be copied [example: sdd or sdc1]:\n> ").lower()
        if input_disk == "/dev/q" or input_disk == "/dev/quit":
            return
        output_disk = "/dev/"
        output_disk += input("Please enter the name of the target disk to save the copy at [example: sdb or sdc1]:\n> ")
        print("\nProcessing.. Please wait..")
        command = f"sudo dd if={input_disk} of={output_disk}"
        subprocess.run(command, shell=True)

        input("\nPress any key to continue..")

def read_trace_file():

    while True:
        file_choice = input("\nChoose an option (1 or 2 - Enter 'q' to quit):\n1. I will enter the file path manually (example: "
                            "~/Desktop/webserver.pcap).\n2. I will enter the file name and the tool should search for it "
                            "then open it.\n> ")
        if file_choice == '1':
            file_path = input("\nPlease Enter the path of the trace file (example: ~/Desktop/webserver.pcap)\n>")
            subprocess.run(f'tcpdump -r {file_path}', shell=True)
            input("\nPress any key to continue..")
        elif file_choice == '2':
            filename = input("Please enter the file name you are looking for (example: 'webserver.pcap'):\n> ")
            file_path = subprocess.run(f'find {search_dir} -name {filename} -print 2>/dev/null | grep .', shell=True,
                                       capture_output=True)
            find_path_status = file_path.returncode
            print("")

            if not find_path_status:  # if the return code is 0 i.e. success
                file_paths = separate_paths(file_path.stdout.decode())
                print(f"{len(file_paths)} file(s) under that name were found:")
                for i in range(len(file_paths)):
                    print(f"\nFile_#{i + 1}: File is found at: {file_paths[i]}")
                    inode_command = subprocess.run(f'ls -i {file_paths[i]}', shell=True,
                                                   capture_output=True)  # returns inode + path
                if len(file_paths) == 1:
                    print("")
                    subprocess.run(f'tcpdump -r {file_paths[0]}', shell=True)
                    input("\nPress any key to continue..")
                    break
                else:
                    while True:
                        id = int(input("\nEnter File_# of the file (1, 2, 3.. etc). Enter '-1' to quit:\n> "))
                        if id == -1:
                            break
                        if id > len(file_paths) or id <= 0:
                            print("Incorrect ID. Please Try Again...")
                            continue
                        else:
                            subprocess.run(f'tcpdump -r {file_paths[id - 1]}', shell=True)

                    time.sleep(1)
                    choice = input("\n\nWould you like to read another trace file? [Y/N]\n> ").upper()
                    if choice == 'N':
                        return
            else:
                print("\nFile is not found, please recheck the input filename if you are sure it's on the system.")
        elif file_choice == 'q' or file_choice == 'Q':
            return
        else:
            print("Incorrect choice entered. Please Try again.")

#######################################################################################################################

print("Welcome to Mini Forensics Tool!")

search_dir = "/home"

# The tool only performs search in the home directory (/home) for speed purposes. If you want the tool to search the
# Entire File system (i.e. the root directory /), please uncomment the next line.
# search_dir = "/"

while True:
    option = input("The tool has the following services:\n1. Find the inode number of a file.\n"
                       "2. Find the file that belongs to a specific inode.\n"
                       "3. Make a packet capture from network device.\n"
                       "4. Make a Take a bit-by-bit image for a drive.\n"
                       "5. Read a trace file.\n"
                       "6. Quit the Tool\n\nChoose an option (1, 2, 3, 4, 5 or 6):\n> ")
    if option == '1':
        find_inode_of_file()
    elif option == '2':
        find_file_by_inode()
    elif option == '3':
        packet_capture()
    elif option == '4':
        bit_by_bit_image()
    elif option == '5':
        read_trace_file()
    elif option == '6':
        break
    else:
        print("Incorrect option. Please Enter a valid number.")
        time.sleep(2)
    clear()
