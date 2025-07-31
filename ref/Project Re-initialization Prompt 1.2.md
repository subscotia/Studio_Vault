### **Project Re-initialization Prompt: Subscotia Vault**

### **Version: 1.0**

### **Date: 25 July 2025**

#### **1\. Project Overview**

* **Project:** Subscotia Vault Web Application.  
* **Goal:** To build a local-first, professional-grade web application to manage the Subscotia Sound audio plugin database. The application will run on a local server (dellin) and be accessed from the main studio workstation (subwin).  
* **Personnel:**  
  * **Product Director / Context Engineer:** Drew Campbell  
  * **Code Engine:** Gemini

#### **2\. Technology Stack**

* **Backend:** Python with the Flask framework.  
* **Data:** vault\_master.json file (long-term goal to migrate to PostgreSQL).  
* **Frontend:** HTML, CSS, vanilla JavaScript (ES6+).  
* **Styling:** Tailwind CSS. **Critical Note:** The local build toolchain for Tailwind failed. The project now uses the official **Tailwind Play CDN** for all styling. This is a permanent decision for the development phase.

#### **3\. Current Status & Next Steps**

The project is in **Phase 2: Frontend UI/UX**.

* **Task 2.1: Integrate Tailwind CSS & Inter Font:** ✅ Complete (via CDN).  
* **Task 2.2: Build Main Application Layout:** ✅ Complete.  
* **Task 2.3: Implement Plugin "Card" Layout:** ✅ Complete.  
* **Task 2.4: Implement Dark/Light Theme Toggle:** ✅ Complete.  
* **Current Task:** We are ready to begin **Task 2.5: Ensure Full Responsiveness**.

The application architecture has been pivoted to a **server-side data injection model**. The Flask backend now reads the JSON file and injects the data directly into the index.html template, eliminating the need for client-side fetch calls and associated CORS issues.

#### **4\. Development Workflow**

The project operates under the **"Context Engineering Framework" (v3.0)**. All new features are developed using the following four-step process:

1. **Define Global Context (rules.md):** Establish project-wide standards.  
2. **Describe Feature Context (feature.md):** Provide detailed requirements for the specific feature.  
3. **Generate Execution Plan (PRP):** The Code Engine generates a detailed Product Requirements Prompt for approval.  
4. **Execute the Plan:** Upon approval, the Code Engine generates the final code.

#### **5\. Key Active Documents**

* Project Plan v2.1 (High-level strategy)  
* Project Workflow v3.0: Context Engineering Framework (Tactical methodology)  
* DEVELOPMENT\_GUIDE.md v1.1 (Technical best practices)  
* VAULT\_GUIDE.md (Data schema rules)