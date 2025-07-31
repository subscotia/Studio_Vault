### **Product Requirements Prompt (PRP)**

### **Feature: Production Server Deployment**

### **Version: 1.0**

#### **Objective**

To execute a complete deployment of the Subscotia Vault application to the dellin (Ubuntu) server. This involves setting up the system environment, configuring Gunicorn to run the Flask application as a persistent service, and configuring Nginx as a reverse proxy to handle incoming traffic.

### **Execution Plan**

This plan outlines the sequence of commands to be executed on the dellin server's terminal.

#### **Phase 1: Prerequisite (on subwin workstation)**

1. **Generate requirements.txt:** Before proceeding, a requirements.txt file must be generated from the local development environment to ensure the server installs the exact same Python package versions.  
   * In the PyCharm terminal on subwin (with the (venv) active), run:  
     pip freeze \> requirements.txt

   * Commit and push this new file to the Git repository.

#### **Phase 2: Server Environment Setup (on dellin)**

1. **Update System Packages:**  
   sudo apt update  
   sudo apt upgrade \-y

2. **Install Dependencies:** Install Python tools, Nginx, and Git.  
   sudo apt install python3-venv python3-pip nginx git \-y

3. **Clone Project Repository:** Clone the project into the user's home directory. (Replace \<your-repo-url\> with the actual URL).  
   cd \~  
   git clone \<your-repo-url\> vault\_project

4. **Create Python Virtual Environment:**  
   cd \~/vault\_project  
   python3 \-m venv venv

5. **Install Python Packages:** Activate the new environment and install packages from requirements.txt.  
   source venv/bin/activate  
   pip install \-r requirements.txt  
   pip install gunicorn \# Install gunicorn separately  
   deactivate

#### **Phase 3: Gunicorn systemd Service Configuration (on dellin)**

1. **Create Service File:** Use a text editor like nano to create a new service file.  
   sudo nano /etc/systemd/system/vault.service

2. **Populate Service File:** Paste the following content into the editor. **Crucially, replace \<your\_username\> with your actual username on the dellin server.**  
   \[Unit\]  
   Description=Gunicorn instance to serve Subscotia Vault  
   After=network.target

   \[Service\]  
   User=\<your\_username\>  
   Group=www-data  
   WorkingDirectory=/home/\<your\_username\>/vault\_project/webapp  
   Environment="PATH=/home/\<your\_username\>/vault\_project/venv/bin"  
   ExecStart=/home/\<your\_username\>/vault\_project/venv/bin/gunicorn \--workers 3 \--bind unix:vault.sock \-m 007 app:app

   \[Install\]  
   WantedBy=multi-user.target

3. **Start and Enable the Service:**  
   sudo systemctl start vault  
   sudo systemctl enable vault

#### **Phase 4: Nginx Reverse Proxy Configuration (on dellin)**

1. **Create Nginx Server Block File:**  
   sudo nano /etc/nginx/sites-available/vault

2. **Populate Server Block File:** Paste the following configuration. This tells Nginx to listen for requests and pass them to the Gunicorn service. **Replace \<your\_username\> with your actual username.**  
   server {  
       listen 80;  
       server\_name dellin.local www.dellin.local; \# Or the server's IP address

       location / {  
           include proxy\_params;  
           proxy\_pass http://unix:/home/\<your\_username\>/vault\_project/webapp/vault.sock;  
       }  
   }

3. **Enable the New Server Block:** Create a symbolic link from sites-available to sites-enabled.  
   sudo ln \-s /etc/nginx/sites-available/vault /etc/nginx/sites-enabled

4. **Test Nginx Configuration:**  
   sudo nginx \-t

   If the test is successful, it will report syntax is ok and test is successful.  
5. **Restart Nginx:** Apply the new configuration.  
   sudo systemctl restart nginx

#### **Final Review**

* Check the status of both services to ensure they are active and running without errors:  
  sudo systemctl status vault  
  sudo systemctl status nginx

* From the subwin workstation, open a web browser and navigate to the dellin server's IP address or local hostname. The Subscotia Vault application should load and be fully functional.

**Approval Request:** The Product Director is requested to review this PRP. Upon approval, this plan will be executed.