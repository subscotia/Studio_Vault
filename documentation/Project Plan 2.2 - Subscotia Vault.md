Here is the updated project plan, version 2.2.

---

### **Project Plan 2.2 \- Subscotia Vault**

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
  * **Status:** ✅ Complete  
* **Phase 2: Frontend UI/UX \- The "Tasty" Interface**  
  * **Status:** ✅ Complete  
* **Phase 3: Advanced Functionality & Interactivity**  
  * **Status:** ✅ Complete  
* **Phase 4: Data Management Interface**  
  * **Status:** ✅ Complete  
* **Phase 5: UI/UX Refinement**  
  * **Status:** 🟡 In Progress (Next Step)  
  * **Tasks:**  
    * 5.1: Redesign filter layout into a compact format (e.g., multi-column or collapsible sections).  
    * 5.2: Implement "Smart" Search within each filter category to quickly narrow down options.  
* **Phase 6: Production Deployment**  
  * **Status:** ⚪ Not Started  
  * **Tasks:** Configure Nginx & Gunicorn on the server, deploy the application, and set it up as a service.

### **Part 2: Getting Started with Bolt DIY**

This section outlines the one-time setup required on your subwin machine.

#### **1\. Installation**

Bolt DIY is a free and open-source application that runs locally. The main dependencies are Node.js and the pnpm package manager.

1. **Install Node.js:** Download and install the latest LTS (Long-Term Support) version of Node.js from the official website.  
2. **Install pnpm:** Open a new PowerShell or Terminal window and run the command: npm install \-g pnpm.  
3. **Install Bolt DIY:** Follow the official installation instructions on the Bolt DIY GitHub page.

#### **2\. Acquiring Your Google AI API Key**

To allow Bolt DIY to use me (Gemini 2.5 Pro), you need to provide it with a Google AI API key. This operates on a pay-as-you-go model with a generous free tier for development.

* **Steps to get your key:**  
  1. Go to **Google AI Studio**.  
  2. Sign in with your Google account.  
  3. Click **"Get API key"** and then **"Create API key in new project"**.  
  4. Copy the generated key and save it securely.

#### **3\. Configuration**

Once installed, configure Bolt DIY in its settings area to use the Gemini 2.5 Pro model and paste in your API key to authenticate requests.