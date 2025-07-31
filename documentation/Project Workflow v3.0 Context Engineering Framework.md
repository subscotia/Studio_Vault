### **Document Version: 3.0**

### **Date: 21 July 2025**

### **1\. Core Philosophy: From Vibe to Vector**

This document formalizes the project's evolution from an intuitive "Vibe Coding" methodology to a rigorous **"Context Engineering"** framework. The core philosophy is to maximize the quality and efficiency of AI-driven development by providing the Code Engine with clear, comprehensive, and unambiguous context *before* code generation begins.

This structured approach minimizes ambiguity and reduces the need for iterative refinement, allowing us to build more complex features correctly on the first attempt.

### **2\. The Context Engineering Workflow**

All new features will be developed using the following four-step, document-driven process. This process now constitutes the main activity within our **Strategy & Ideation (S\&I)** phase.

#### **Step 1: Define Global Context (rules.md)**

* **Purpose:** To establish a single source of truth for project-wide standards that the Code Engine must adhere to at all times.  
* **Content:** This document will contain:  
  * **Coding Conventions:** Language-specific style guides (e.g., PEP 8 for Python).  
  * **Architectural Principles:** Key design patterns to be used (e.g., "separation of concerns," "modular components").  
  * **Testing Requirements:** Mandates for unit tests, integration tests, etc.  
  * **Dependencies:** A list of approved libraries and frameworks.  
* **Process:** This is a living document, reviewed and updated during S\&I sessions as the project evolves.

#### **Step 2: Describe Feature Context (feature.md)**

* **Purpose:** For each new feature, a dedicated context document will be created to provide all necessary information for its implementation.  
* **Content:** This document will include:  
  * **Feature Description:** A clear, concise explanation of the feature and its goals.  
  * **User Stories:** Descriptions of how a user will interact with the feature.  
  * **Code Examples:** Relevant snippets of existing code that the new feature will interact with.  
  * **RAG Inputs:** Links to external documentation for libraries or APIs that will be used.  
  * **Known Constraints & Pitfalls:** A list of potential issues or limitations to be aware of.

#### **Step 3: Generate Execution Plan (PRP)**

* **Purpose:** To create a highly detailed, AI-generated plan for building the feature. This is the **Product Requirements Prompt (PRP)**.  
* **Process:**  
  1. The Code Engine analyzes the rules.md and the specific feature.md.  
  2. Based on this context, the Code Engine generates the PRP, which outlines the proposed file structure, function signatures, component hierarchy, and implementation logic.  
  3. The Product Director reviews and approves this PRP. This is the final quality gate before code is written.

#### **Step 4: Execute the Plan**

* **Purpose:** To generate the complete, production-ready code for the feature.  
* **Process:**  
  1. The Product Director instructs the Code Engine to execute the approved PRP.  
  2. The Code Engine, using Bolt DIY as the execution environment, follows its own detailed plan to write all necessary code, create tests, and assemble the final feature.

### **3\. Updated Roles & Responsibilities**

* **Product Director (Drew Campbell):** The primary Context Engineer. Responsible for authoring the feature.md for each new task and for providing final review and approval of the AI-generated PRP.  
* **Code Engine (Gemini 2.5 Pro):** Analyzes all provided context to generate the detailed PRP. Upon approval, executes the PRP to produce the final code. Also responsible for explaining the "why" behind any architectural decisions to reinforce the Product Director's technical knowledge.  
* **Project Manager (Bolt DIY):** Remains the tool for execution, providing the local playground for scaffolding, testing, and verifying the final output.