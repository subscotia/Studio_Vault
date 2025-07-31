### **Subscotia Vault: Daily Workflow Glance Sheet**

### **▶️ STARTING WORK ("Dev Mode")**

This checklist outlines the two applications and three processes that need to be running for the full development environment.

**1\. Start the Backend (Flask API)**

* **Application:** PyCharm  
* **Action:**  
  1. Open the vault\_project in PyCharm.  
  2. Select the app run configuration from the dropdown at the top-right.  
  3. Click the green **Play (▶️)** button.  
* **Verification:** The "Run" window shows \* Running on http://127.0.0.1:5000.

**2\. Start the Frontend Tool (Bolt DIY)**

* **Application:** PowerShell  
* **Action:**  
  1. Open a new PowerShell terminal.  
  2. Navigate to the Bolt DIY directory with the command:  
     cd F:\Tools\bolt.diy

  3. Start the Bolt DIY server with the command:  
     pnpm dev

* **Verification:** The terminal shows ➜ Local: http://localhost:5173/ and the command prompt does not return.


### **⏹️ STOPPING WORK ("Music Mode")**

This checklist ensures all development processes are terminated, freeing up system resources for Reaper.

**1\. Stop the Bolt DIY Server**

* **Location:** The PowerShell window running pnpm dev.  
* **Action:** Click on the window and press **Ctrl \+ C**.

**2\. Stop the Flask Backend**

* **Location:** The PyCharm "Run" window.  
* **Action:** Click the red **Stop (⏹️)** button next to the app process.


**3\. (Recommended) Close PyCharm**

* **Action:** File \> Exit to free up all associated memory.