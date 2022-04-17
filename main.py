import subprocess
import time

while True:

    print("######################################################### \n\n")
    filename = input("Please enter the file name you are looking for (example: 'test.txt'):\n> ")
    file_path = subprocess.run(f'find /home -name {filename} -print 2>/dev/null | grep .', shell=True, capture_output=True)
    find_path_status = file_path.returncode

    if not find_path_status:
        print(f"File is found at: {file_path.stdout.decode()}")
        inode_command = subprocess.run(f'ls -i {file_path.stdout.decode()}', shell=True, capture_output=True) # returns inode + path
        print(f"inode number is: {inode_command.stdout.decode().split()[0]}") # returns inode number only.
        time.sleep(2)
        choice = input("Would you like to see more details about this file? [Y/N]\n> ").upper()
        if choice == 'Y':
            file_path = subprocess.run(f'stat {file_path.stdout.decode()}', shell=True)

    else:
        print("File is not found, please recheck the filename if you are sure it's on the system.")














