# **PowerShell: The Basics**

### **Purpose**

PowerShell is a command-line shell and scripting language designed for task automation and system management. It's more powerful and flexible than the older Command Prompt (CMD).

* **Object-based**: PowerShell works with objects, which are collections of data and methods. This allows for more complex operations and manipulation of information.  
* **Cmdlets**: PowerShell uses cmdlets (pronounced "command-lets"), which are specialized commands that perform specific actions. Cmdlet names follow a Verb-Noun format (e.g., Get-ChildItem, Set-Location).  
* **Pipeline**: You can chain cmdlets together using the pipeline symbol (|). This passes the output of one cmdlet as input to the next.  
* **Scripting**: PowerShell includes a full scripting language, enabling you to write scripts to automate tasks and manage configurations.

### **Basic Glossary**

* **Get-Help**: Displays help information about cmdlets.  
  * *Example*: Get-Help Get-ChildItem  
* **Get-ChildItem**: Lists the files and directories in the current location (similar to dir in CMD).  
* **Set-Location**: Changes the current directory (similar to cd in CMD).  
  * *Example*: Set-Location C:\\Users  
* **Get-Content**: Displays the contents of a file.  
  * *Example*: Get-Content myfile.txt  
* **Set-Content**: Writes content to a file.  
  * *Example*: Set-Content myfile.txt "Hello, world\!"  
* **Get-Process**: Lists the currently running processes.  
* **Stop-Process**: Stops a running process.  
  * *Example*: Stop-Process \-Name notepad  
* **Get-Service**: Lists the services installed on the computer.  
* **Start-Service**: Starts a service.  
  * *Example*: Start-Service \-Name Spooler  
* **Where-Object**: Filters objects based on specified conditions.  
  * *Example*: Get-ChildItem | Where-Object {$\_.Length \-gt 10KB} (gets files larger than 10KB)  
* **ForEach-Object**: Performs an operation on each object in a collection.  
  * *Example*: Get-ChildItem | ForEach-Object {$\_.FullName} (gets the full path of each file)

### **Basic Rules**

* **Case-insensitive**: PowerShell commands and parameters are not case-sensitive.  
* **Parameters**: Cmdlets accept parameters to modify their behavior, specified with a hyphen (-).  
* **Quotes**: Use quotes around file paths or strings that contain spaces.  
* **Pipeline**: Use the pipe symbol (|) to chain cmdlets together.  
* **Help**: Use Get-Help to get information about any cmdlet or concept.

## **Interrogate the OS**

### **1\. System Information**

* **Get basic OS details:**  
  Get-CimInstance Win32\_OperatingSystem

* **Find out your computer's name:**  
  $env:COMPUTERNAME

* **See how long your system has been running:**  
  (Get-CimInstance Win32\_OperatingSystem).LastBootUpTime

### **2\. Hardware Information**

* **Get details about your CPU:**  
  Get-CimInstance Win32\_Processor

* **Find out how much RAM you have (in GB):**  
  (Get-CimInstance Win32\_PhysicalMemory | Measure-Object \-Property Capacity \-Sum).Sum / 1GB

* **List all your disk drives:**  
  Get-CimInstance Win32\_DiskDrive

### **3\. Network Information**

* **Get your IP address:**  
  (Get-NetIPAddress | Where-Object {$\_.InterfaceAlias \-like "Ethernet\*" \-or $\_.InterfaceAlias \-like "Wi-Fi\*"}) | Select-Object IPAddress

* **See your network connections:**  
  Get-NetAdapter

* **List all open network ports:**  
  Get-NetTCPConnection \-State Listen

### **4\. Processes and Services**

* **See what processes are running:**  
  Get-Process

* **Find a specific process:**  
  Get-Process \-Name chrome

* **List all services:**  
  Get-Service

### **5\. File System**

* **List files in a directory:**  
  Get-ChildItem \-Path C:\\Users\\YourName\\Documents

* **Find files with a specific extension (recursively):**  
  Get-ChildItem \-Path C:\\ \-Filter "\*.txt" \-Recurse

* **Check the size of a file:**  
  (Get-Item "C:\\path\\to\\your\\file.txt").Length

### **6\. Control Wi-Fi Adapter**

* **Turning Wi-Fi Off:**  
  Disable-NetAdapter \-Name "Wi-Fi" \-Confirm:$false

  *(Note: The name "Wi-Fi" might vary. Use Get-NetAdapter to find the correct name.)*  
* **Turning Wi-Fi On:**  
  Enable-NetAdapter \-Name "Wi-Fi" \-Confirm:$false  
