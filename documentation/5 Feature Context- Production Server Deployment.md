### **Feature Context: Production Server Deployment**

### **Version: 1.0**

#### **1\. Feature Description**

The goal is to deploy the Subscotia Vault web application to the dedicated Linux server (dellin). This involves installing all necessary system software, configuring a production-grade application server (Gunicorn) and web server (Nginx), and setting up the application to run as a persistent background service.

#### **2\. User Story**

As the system administrator, I want to deploy the Vault application to the dellin server, so that it is always running and can be accessed reliably from the main studio workstation (subwin) by simply navigating to a local network address (e.g., http://dellin.local).

#### **3\. Core Requirements**

This task will be performed entirely on the dellin (Ubuntu) server via the command line.

* **Environment Setup:**  
  * Install necessary system packages: python3-venv, python3-pip, and nginx.  
  * Clone the latest version of the vault\_project repository from Git onto the server.  
  * Create a dedicated Python virtual environment for the application on the server.  
  * Install all required Python packages (Flask, Gunicorn, etc.) into this virtual environment using the requirements.txt file.  
* **Application Server (Gunicorn):**  
  * A systemd service file will be created for Gunicorn. This will ensure that our Flask application is managed by the operating system.  
  * The service will be configured to run the application automatically on server boot and to restart it if it ever crashes.  
* **Web Server (Nginx):**  
  * A new Nginx "server block" (virtual host) file will be created.  
  * Nginx will be configured to act as a **reverse proxy**. It will listen for incoming network requests on port 80 and forward them internally to the Gunicorn process, which is running our Flask application.  
  * Nginx will also be configured to directly and efficiently serve our static files (CSS, and in the future, JavaScript and images).

#### **4\. Vibe & Aesthetic**

* **Vibe:** "Robust & Automated". The final deployment should be a "set it and forget it" configuration. The application should run reliably as a background service without requiring manual intervention.