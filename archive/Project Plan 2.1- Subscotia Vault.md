### **Part 1: The Work Plan**

#### **1\. Core Philosophy & Roles**

This project will be executed using a professional, AI-assisted development model. Our collaboration will be structured into the following roles to maximize efficiency and creativity:

* **Product Director (Drew):** You define the high-level goals, features, and desired outcomes for the application. You are the final arbiter of the project's direction.  
* **Project Manager & IDE (Bolt DIY):** This tool will manage our workflow. It will take your high-level prompts, orchestrate the interaction with me, handle the creation of the multi-file project structure, and provide a local development playground for immediate testing.  
* **Code Engine (Gemini 2.5 Pro):** My role is to act as the lead developer. I will generate high-quality, complete codebases based on the structured requests from Bolt DIY, and I will assist with advanced refactoring, debugging, and strategic technical advice.

#### **2\. The Development Workflow**

Each new feature will be developed using the following three-step process:

1. **Strategy & Ideation (S\&I):** This happens in our chat. We discuss the feature, brainstorm creative approaches, explore technical possibilities, and decide on a final plan. My creative and advisory input is centered here.  
2. **Execution:** You provide the high-level goal from our S\&I session to Bolt DIY. Bolt DIY manages the prompting process, and I generate the necessary code and file structure.  
3. **Testing & Refinement:** You test the generated feature in the Bolt DIY playground. We can then return to the S\&I phase to discuss and implement any necessary refinements or improvements.

#### **3\. Project Phases (Updated)**

* **Phase 1: Backend Foundation & API**  
  * **Status:** ✅ Complete.  
* **Phase 2: Frontend UI/UX \- The "Tasty" Interface**  
  * **Status:** 🟡 Complete.  
  * **Tasks:**  
    * 2.1: Integrate Tailwind CSS & Inter Font. (✅ Complete)  
    * 2.2: Build Main Application Layout. (Next Step, to be done via Bolt DIY)  
    * 2.3: Implement Plugin "Card" Layout.  
    * 2.4: Implement Dark/Light Theme.  
    * 2.5: Ensure Full Responsiveness.  
* **Phase 3: Advanced Functionality & Interactivity**  
  * **Status:** ⚪ Complete.  
  * **Tasks:** Live Search, Multi-Select Filtering, Detail View Modals.  
* **Phase 4: Data Management Interface**  
  * **Status:** ⚪ In Progress.  
  * **Tasks:** 
 * 4.1 "Add New Plugin" Form
 * 4.2 Backend API for data submission.  
 * 4.3: Implement the Python logic to safely add the new entry to the master vault.json file and create a backup.
 * 4.4 Frontend will automatically refresh to show the new plugin
* **Phase 5: Production Deployment**  
  * **Status:** ⚪ Not Started.  
  * **Tasks:** Configure Nginx & Gunicorn on dellin, deploy the application, set up as a service.

### **Part 2: Getting Started with Bolt DIY**

This section outlines the one-time setup required on your subwin machine.

#### **1\. Installation**

Bolt DIY is a free and open-source application that runs locally. The main dependencies are Node.js and the pnpm package manager.

1. **Install Node.js:** Download and install the latest LTS (Long-Term Support) version of Node.js from the official website: https://nodejs.org/.  
2. **Install pnpm:** Node.js comes with a tool called npm. Open a new PowerShell or Terminal window and run the following command to install pnpm:  
   npm install \-g pnpm

3. **Install Bolt DIY:** Follow the official installation instructions on the Bolt DIY GitHub page. This will likely involve using a pnpm command to download and set up the application.

#### **2\. Acquiring Your Google AI API Key**

To allow Bolt DIY to use me (Gemini 2.5 Pro), you need to provide it with a Google AI API key.

* **Crucial Clarification on Cost:** The API key for developers operates on a **pay-as-you-go** model and is **not connected to any existing consumer subscription** like Google One. However, Google provides a **generous free tier** for the API which is typically more than enough for development-level usage. You will only incur costs if your usage exceeds this free tier.  
* **Steps to get your key:**  
  1. Go to **Google AI Studio**: https://aistudio.google.com/  
  2. Sign in with your Google account.  
  3. On the left-hand menu, click **"Get API key"**.  
  4. Click **"Create API key in new project"**.  
  5. Copy the generated key and save it somewhere secure. **Do not share this key publicly.**

#### **3\. Configuration**

Once installed, you will need to configure Bolt DIY to use your new API key. The application will have a settings area where you can select the AI model (Gemini 2.5 Pro) and paste your API key to authenticate your requests.