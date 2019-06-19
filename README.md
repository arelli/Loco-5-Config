# Ubiquiti NanoStation Loco 5 Auto Config Uploader
Developed for Networks Operation Center of Technological University Of Crete this is a script
written in python that uploads a config file to a [NanoStation](https://www.ui.com/) without the need for http 
logging-in or typing passowrds.It is designed for large networks administrated by one authority, with certain
administrator ssh credentials, and runs in Linux boxes(now tested on Ubuntu). It allows the administrators to uninteractively upload settings through the config files of the antennas via ssh.

## Installation

Run installation.py as root to install the script(if you dont run it as root, you will be probably prompted to enter your sudo password during the process).
```bash
 sudo python installation.py
```
Then, you need to edit the <u>password</u> file according to your needs.</br>
The above should have installed [Python](https://www.python.org/), [sshpass](https://linux.die.net/man/1/sshpass), 
[openssh](https://www.openssh.com/) client and the [openpyxl](https://openpyxl.readthedocs.io/en/stable/) Python library.

To access the help menu through the terminal:
```bash
python auto_setter.py help
```
## Usage
Place the scripts in a dedicated working directory, alongside with(included in repository):</br> </br>
<b>"password"</b></br>
A text file containing the ssh session password for all the nanostations in plain text(the file has no suffix)</br></br>
<b>"users.xlsx"</b></br>
The file that contains all the user info and it is downloaded through the Admin Tool database(be aware that the configuration of the file can be different than yours.Our current configuration is in the form of comment in the excel_reader.py</br></br>
<b>"additional_config"</b></br>
This file contains the additional configuration changes you want to make, in the format <string_to_be_replaced> <string_to_replace_it>.See example in the additional_config file above.It can also be empty</br>
To use the script with remote antennas of your network, you use the form:
```bash
python auto_setter.py <ip_of_nanostation> <ssh_username>
```
for example:
```bash
python auto_setter.py 192.168.56.77 linuxadmin
```
<b>Inside Info</b></br>
Inside the script <i>ssh</i> and <i>sshpass</i> are used. Each of these had its own complications with the antenna.
The Loco 5, being old, supports mainly old security protocols.This is why the preferred [Key Exchange Algorithm](https://en.wikipedia.org/wiki/Key_exchange) is 
[diffie-hellman-group1-sha1](https://www.openssh.com/legacy.html) and the cipher used is aes128-cbc in the form of custom options.SSHpass is used to avoid entering manually 
the password for each ssh and scp(secure copy, part of ssh suite) connection.Having a key stored in each device was not an 
option in my case.Also, sshpass needs the -f option to read the password from a (unencrypted for now) text file named 
"password" to avoid entering it manually. </br></br>
Problems with SSH connection: the newer models ask for other key exchange algorithms and ciphers than the Loco 5,so a new script must be constructed(based on this one) that supports their protocols.

## Contributing
Currently tested and approved at remote and LAN NanoStations Loco 5 with the firmware version XS5.ar2313.v4.0.4.5074.150724.1344 in Ubuntu 18.04 LTS x86_64 enviroment.
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[Mozilla Public License 2.0](https://choosealicense.com/licenses/mpl-2.0/)
