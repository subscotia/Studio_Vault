# **Dellin Server Reference Sheet (Subscotia Sound)**

Server Name: dellin  
Static IP Address: 192.168.2.50

### **1\. Connection Methods (from Windows 10\)**

|

| Method | Application | Address / Command | Purpose |  
| Web Management | Web Browser | https://192.168.2.50:9090 | Primary tool for server admin (storage, updates, logs). |  
| Full GUI | Remote Desktop Connection | 192.168.2.50 | Access the full XFCE graphical desktop (your "safety net"). |  
| Command Line (SSH) | PowerShell | ssh your\_username@192.168.2.50 | Quick, efficient command-line access. |  
*Remember to replace your\_username with the username you created for the server.*

### **2\. Essential Management Commands (via SSH or Cockpit Terminal)**

*Always use sudo before a command that needs administrator rights (e.g., sudo apt update).*

#### **System Information**

| Command | Description |  
| df \-h | Shows disk free space in a human-readable format. |  
| free \-h | Shows free and used memory (RAM) in a human-readable format. |  
| top or htop | Displays a live, updating list of running processes (like Task Manager). Press q to quit. |  
| ip a | Shows all network interfaces and their IP/MAC addresses. |  
| uname \-a | Displays detailed information about the Linux kernel. |

#### **Software Management (using apt)**

| Command | Description |  
| sudo apt update | Refreshes the list of available software packages. Run this first. |  
| sudo apt upgrade | Installs all available updates for your system. |  
| sudo apt install \[package\_name\] | Installs a new software package (e.g., sudo apt install samba). |  
| sudo apt remove \[package\_name\] | Uninstalls a software package. |  
| apt search \[search\_term\] | Searches for available packages. |

#### **File & Directory Management**

| Command | Description |  
| ls \-l | Lists files and directories in the current location with details. |  
| cd \[directory\_path\] | Changes your current directory (e.g., cd /var/www). |  
| pwd | Prints the full path of your current working directory. |  
| mkdir \[directory\_name\] | Creates a new directory. |  
| cp \[source\] \[destination\] | Copies a file or directory. |  
| mv \[source\] \[destination\] | Moves or renames a file or directory. |  
| rm \[file\_name\] | Deletes a file. Use with caution. |  
| rm \-r \[directory\_name\] | Deletes a directory and everything inside it. Use with extreme caution. |

#### **System Control & Services**

| Command | Description |  
| sudo reboot | Reboots the server immediately. |  
| sudo shutdown now | Shuts down the server immediately. |  
| sudo systemctl status \[service\_name\] | Checks the status of a service (e.g., sudo systemctl status xrdp). |  
| sudo systemctl restart \[service\_name\] | Restarts a service. |  
| sudo systemctl enable \[service\_name\] | Makes a service start automatically on boot. |  
| sudo systemctl disable \[service\_name\] | Stops a service from starting automatically on boot. |

### **3\. Specific Commands for Your Setup**

| Command | Description |  
| ssh your\_username@192.168.2.50 'sudo reboot' | (From PowerShell) Reboots the server remotely without a full login. |  
| sudo systemctl set-default multi-user.target | Sets the server to boot to the command line (the correct default). |  
| sudo systemctl set-default graphical.target | Sets the server to boot to the XFCE desktop (for troubleshooting). |  
| lsblk | Lists all connected block devices (your SSDs and external drives). |