
import os
print("~~Installing script.~~")
os.system("sudo apt-get update")
os.system("sudo apt-get install ssh")
os.system("sudo apt-get install sshpass")
os.system("sudo apt-get install python3.6")
#os.system("pip install openpyxl")
os.system("touch additional_config")
try:
  os.system("sudo chmod u+x ssh_save")
  print("installation: Making \"ssh_save\" executable....")
except:
  print("installation:Could not make file ssh_save executable!Do it manually with sudo chmod u+x ssh_save")
try:
  os.system("sudo chmod u+x get_board_info")
  print("installation: Making \"get_board_info\" executable....")
except:
  print("installation:Could not make file get_board_info executable!Do it manually with sudo chmod u+x get_board_info")
try:
  os.system("sudo chmod u+x get_board_config")
  print("installation: Making \"get_board_config\" executable....")
except:
  print("installation:Could not make file get_board_config executable!Do it manually with sudo chmod u+x get_board_config")
print("installation:Now edit the password file with your password")
print("installation:Done.Exiting...")
