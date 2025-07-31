### **Feature Context: Main Application Layout**

### **Version: 1.1**

#### **1\. Feature Description**

The goal is to create the primary, top-level layout for the Subscotia Vault web application. This layout will be a persistent structure that contains all other components of the application.

#### **2\. User Story**

As a user, I want to see a clean, organized, and professional interface with a clear separation between the main content area and the filtering controls, so I can easily navigate and interact with the plugin database.

#### **3\. Core Requirements**

* The layout must consist of three main regions:  
  1. A **Header** at the top of the page.  
  2. A **Sidebar** on the left for filter controls.  
  3. A **Main Content Area** on the right where the plugin cards will be displayed.  
* The Header should be fixed and always visible.  
* The Sidebar and Main Content Area should occupy the remaining vertical space.  
* The Sidebar and Main Content Area should be scrollable independently if their content overflows the viewport height.  
* The layout must be responsive. On smaller screens (mobile), the sidebar may need to be hidden by default and toggled with a button.

#### **4\. Vibe & Aesthetic**

* **Overall Vibe:** The design should feel like a professional piece of studio software, not a generic website. It should be clean, utilitarian, and data-focused.  
* **Color Palette:** The initial build will use a neutral, muted color palette (e.g., shades of grey) to focus on structure.  
  * **Future Goal:** A dedicated "theming" task will be created later to implement the official Subscotia Sound brand colors across the application.  
* **Analogy:** The layout should have the clarity and no-nonsense feel of a well-designed hardware rack unit or a high-end mixing console's channel strip.

#### **5\. Known Constraints**

* This layout will initially be populated with placeholder text. The actual filter components and plugin cards will be built in subsequent tasks.  
* The initial build will focus on the "light mode" aesthetic. Dark mode will be implemented later.