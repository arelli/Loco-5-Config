'''
Script created to automate/simplify the task of uploading new settings to remote NanoStations.
Requirements: installed OpenSSH client and sshpass
The script uses a config file that we provide inits working directory as "system_base.cfg"
Then it asks for the username(hoostname), the associated base station ssid(wpa psk,ssid,wpasupplicant etc.)
and the IP of the nanostation(given by AdminTool Database).
***This version works for Nanostation Loco 5 only!***
'''

import os  # in order to be able to execute shell commands
import sys  # to pass arguments along from the call of the script
import getpass  # library to get username of local computer(used in hosts file deletion)

# User Interaction
print("\nNanostation Loco 5 Automatic Config File Uploader \n")

# the help menu
try:
    user_choice = sys.argv[1]
except:
    print("Error:No arguments.Use option \"help\" ")
    exit()

# present help menu
if (str(user_choice) == "help"):
    print("~Use as: python3.6 auto_setter.py <username for SSH> <IP to SSH>\n")
    print("~sshpass and openssh client are required to run this script ")
    print("~If you are connected via cable to the NanoStation, enter the word local in the position of the IP") 
    print("~You can enter \"dummy\" as the second argument to make the configuration file but do not upload it.")
    print("~IMPORTANT: before you execute the program you need two files:")
    print("->a file named \"password\"(no suffix) containing the ssh password in plain text, at the first line.")
    print("->a file named \"additional_config\" with the additional settings you want to temporarily change in the config file")
    print("format of additional_config: <string_to_be_replaced1> <string_to_replace1> ")
    print("~Built and Tested on XS5.ar2313.v4.0.4.5074.150724.1344 firmware of NanoStation5 L")
    exit()

try:
    targetIP = sys.argv[2]  # get the ssh username
except:
    print("script:No second argument...See \"help\" option.Exiting...")
    exit()
          
username=user_choice  # user_choice = sys.srgv[1]

# ping nanostation to see if it is online
print("script:Pinging nanostation at " +str(targetIP) + "...")
is_online = os.system("ping -c 1 -W 2 " + str(targetIP) + " >> pinglog")  # checks for 2 seconds(-W), and returns 0 if nanostation is online(256 if ofline)
if (is_online == 0):
    print("script:Nanostation responded.Continuing...")
else:
    print("script:Nanostation unreachable!Check your target IP!Exiting...")
    sys.exit(1)  # exits the script to save time(no need for ssh connect tries)
    exit()


# before any ssh connections are made, the hosts file is cleared of the old rsa keys
# if this is not done, a message pops up about security, and can block the script until manual user input is given
print("script: running ssh-keygen for " + str(targetIP) )
os.system("ssh-keygen -f \"/home/" + str(getpass.getuser()) + "/.ssh/known_hosts\" -R " + str(targetIP))  # removes annoying message about RSA Keys



#check model of the antenna because database is not always up to date
try:
    os.remove("boardinfo")  # if an old boardinfo exists, the text is appended to it and it is not valid
    print("script:Deleted old boardinfo file")
except:
    print("script:No old boardinfo file found to delete...")
    
print("script:Checking model of antenna...")
got_board_info = os.system("./get_board_info " + str(targetIP) + " diffie-hellman-group1-sha1 aes128-cbc " + str(username) + " >> boardinfo ")  # if succesfull, saves the board.info file as boardinfo
if got_board_info != 0:
    print("script:Could not get board info..Aborting..")
    sys.exit(1)
    exit()

# get the model of antenna by reading boardinfo file
boardinfo = open("boardinfo").read()  # boardinfo is now a string 
boardinfo_lines = boardinfo.splitlines()  # boardinfo_lines is a list that each element is a line of the board.info file
namestring = "board.name="  # the key-word to locate the line where the name of the NanoStation is
model = [model_line for model_line in boardinfo_lines if namestring in model_line]  # searches boardinfo_lines for lines *containing* nmestring
if len(model)!=0:  # if model[] list is empty, it means that no instance of namestring was found in it.
    model = model[0]

if model != "board.name=NanoStation5 L":
    print("script:his is not a NanoStation5 L, exiting...")
    sys.exit(2)  # returns 512 as exit value
    exit()
else:
    print("script:" +str(model))
    print("script:Model verified, continue")

try:
    os.remove("boardinfo")  # deletes the old boardinfo file, because the shell script appends text
except:  # it is not advised that more than one instances of the script run together, as they will cross-over each others temporary files!
    print("script:Something weird happened with the boardinfo file and it was deleted.Is another instance of the script running simultaneusly?")

# get board's configuration file from the NanoStation
try:
    os.remove("system_base.cfg")
except:
    print("script:No old system_base.cfg file to delete.Proceeding...")

# "download" configuration file from nanostation
# by downloading and changing only where we like to, we ensure to keep all the rest of the configuration the same for each user
got_config = os.system("./get_board_config " + str(targetIP) + " diffie-hellman-group1-sha1 aes128-cbc " + str(username) + " >>system_base.cfg" )
try:
    config_string = open("system_base.cfg").read()  # pass the whole file to a string(_base because it does not change)
except:
    print("script:Could not open system_base.cfg! Is another instance of the script running simultaneously?Exiting...")
    exit()

config_string_split = config_string.splitlines()  # now config_string is a set of strings, one for each line of the config file

# additional configuration changes through the additional_config file
try:
    strings_to_replace = open("additional_config").read()  # read the auto_setter's configuration file
except:
    print("script:Could not open additional_config! It must be created before running the script to indicate configuration changes!")
    print("script:Generating additional_config file...")
    try:
        additional_config = open("additional_config","w")  # create additional_config file
        additional_config.write("<setting_to_be_replaced> <setting_to_replace_it>")  # write this string to the additional_config file
    except:
        print("script:Cannot create additional_config file! Do you have enough privileges in this directory?Exiting....")
        exit()

strings_to_replace = strings_to_replace.split()  # splits the text into seperate strings,and puts them in a list
'''
# comment recognition
for x in len(strings_to_replace):
    if strings_to_replace[x][0] == "#":
        strings_to_replace.pop(x)  # delete(ignore) the x'th element of the list if it starts with a "#" (its a comment)
'''
how_many_strings_to_replace = len(strings_to_replace)
i = 0  # counter for the loop
while i<how_many_strings_to_replace:  # the altered config is stored temporarily in the system.cfg file
    setting_string = str(strings_to_replace[i])
    # the command below finds an occurence of settings_string(a part of a setting) and assigns the *whole* line in the "setting" variable,
    # to be replaced *whole* from the new setting.
    setting = [setting_line for setting_line in config_string_split if setting_string in setting_line]  # searches in the config string for setting's (whole) line
    if len(setting) > 0:  # if the setting was not found, setting[] is empty.
        setting = setting[0]
        try:
            config_string = config_string.replace(setting,strings_to_replace[i+1])  # replaces the whole line( not just the setting until "=")
        except:
            print("script:WARNING:the format of the additional_config file is not correct!Exiting...")
            exit()
    else:  # if the string(setting) was not found inside the config file:  (WARNING: DANGEROUS IF USED FOR OTHER NANOSTATION MODELS SCRIPT!)
        config_string = config_string +"\n" + str(strings_to_replace[i+1])  # i+1 because its the second word in the additional_conofig file(or fourth, or sixth etc)
        # some commands to sort the config file in alphabetical order
    i = i + 2 #increment by 2 because each time the 1st word is replace by the second, the 3rd by the 4rth etc

config_string_split = config_string.splitlines()  # split the config to lines
config_string_split.sort()  # sorts the list of strings in alphabetical order
config_string = "\n".join(config_string_split)  # "/n" splits each setting with a new line! very importand to produce valid configuratioon files

# write tha changes to the cfg file
try:
    config_file = open("system.cfg",'w')  # opens  the file to write to it
    config_file.write(config_string)
    config_file.close()
except:
    print("script:Can't open/create system.cfg! Do you have enough privileges in this directory?Exiting...")
    exit()




#DUMMY MODE
try:
    if sys.argv[2] == "dummy":
        print("script:The configuration is saved in system.cfg and it will NOT be uploaded.Exiting...")
    exit()
except:
    print("script:Normal Upload Mode")
# the command that uploads the config file
# WARNING needs target ip and config filename specification
config_filename = "system.cfg"
upload_config_command = "sshpass -f password scp -o KexAlgorithms=diffie-hellman-group1-sha1 -o StrictHostKeyChecking=no -c aes128-cbc " + str(config_filename) + " " + str(username) + "@" + str(targetIP) +":/tmp/"

'''
Some words for the above command:
    sshpass = program that non-interactively enters the password for the ssh connection
    "-f password" = -f is the option to specify a text file containing the password
    "scp" = stands for secure copy(copy file via ssh)
    "-v" stands for verbose mode
    "-o" represents an ssh option following
    "KexAlgorithms" = the key exchange algorithm used(had to modify it due to old ssh in nanostations)
    "-c" = the cipher used(had to modify it for the same reasons)
'''

# passes the settings and aplies them
print("script:Entering SCP  Shell...")
scp_upload_status = os.system(upload_config_command)  # executes the scp command
print("script:Exiting SCP Shell...")


# the command that saves the config(via ssh)
save_config_command = "sshpass -f password ssh -o KexAlgorithms=diffie-hellman-group1-sha1 -c aes128-cbc  " + str(username) + "@" + str(targetIP) 
save_command_ssh = "save && exit"  # executes "save" command inside the ssh shell and then exits

print("script:Entering ssh to execute command")
# executes the shell script that saves the configuration
# IMPORTANT: "ssh_save" must have execution permission(chmod u+x ssh_save)
ssh_save_status = os.system("./ssh_save "+ str(targetIP) + " " + str(username)) # targetIP is passed as first argument($1) in the ssh_save script
if ssh_save_status == 0:
    print("script:Done saving via ssh..")
else:
    print("script:Saving via SSH was impossible!")

if (scp_upload_status != 0):  # os.system returns a non-zero value for unsuccessful tasks
    print("script:The SCP SSH upload command did not finish succesfully!Exit value=" + str(scp_upload_status))
    sys.exit(1)  # returns exit code 1 to the system to inform the caller script that there has been a problem
    exit()

if (ssh_save_status != 0):
    print("script:The SSH save command did not finish succesfully!Exit value= " + str(ssh_save_status))
    sys.exit(1)
    exit()

if (scp_upload_status !=0) and (ssh_save_status != 0):
    print("script:Done.Exiting...")
    sys.exit(0)
    exit()
