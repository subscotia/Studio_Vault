### **Project Global Rules & Conventions**

### **Version: 1.0**

#### **1\. General Architecture**

* **Technology Stack:** The frontend will be built using HTML, CSS, and vanilla JavaScript (ES6+). The backend is a Python Flask application.  
* **Styling:** All styling must be implemented using the Tailwind CSS utility-first framework. No custom CSS files or inline styles are permitted, except where absolutely necessary for third-party library integration.  
* **Responsiveness:** All components and layouts must be fully responsive, ensuring optimal usability on mobile, tablet, and desktop viewports. A mobile-first approach is preferred.  
* **Font & Icons:** The primary font for all text is "Inter". Icons should be sourced from the "Lucide Icons" library to maintain visual consistency.

#### **2\. Code Conventions**

* **HTML:** Code must be semantic and well-structured. Use appropriate tags for their intended purpose (e.g., \<nav\>, \<aside\>, \<main\>). All attributes must be double-quoted.  
* **JavaScript:** Code must be clean, modular, and well-commented. Avoid global variables; encapsulate logic within functions or modules where appropriate. Use const for variables that are not reassigned and let for variables that are.  
* **Python (Backend):** Adherence to the PEP 8 style guide is mandatory.

#### **3\. Component Design**

* **Modularity:** Components should be designed to be as self-contained and reusable as possible.  
* **State Management:** For now, component state will be managed directly via JavaScript and DOM manipulation. As complexity increases, we will re-evaluate and potentially introduce a lightweight state management solution.

#### **4\. Testing**

* **Manual Testing:** All new features must be manually tested by the Product Director in the Bolt DIY playground across different screen sizes before being considered complete.  
* **Automated Testing:** (Future Goal) A framework for automated unit and integration tests will be established in a later project phase.