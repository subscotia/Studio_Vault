### **Feature Context: Dark/Light Theme Toggle**

### **Version: 1.1**

#### **1\. Feature Description**

The goal is to implement a theme-switching functionality that allows the user to toggle between the existing light theme and a new dark theme. The user's preference should be saved so it persists between visits.

#### **2\. User Story**

As a user working in a dimly lit studio environment, I want to switch to a dark theme to reduce eye strain and create a more focused, less intrusive interface.

#### **3\. Core Requirements**

* A toggle button/icon must be added to the header area for easy access.  
* The theme switching will be handled by adding or removing a dark class to the root \<html\> element.  
* Tailwind's dark: variant will be used to apply different styles when the dark class is present (e.g., bg-white dark:bg-gray-800).  
* JavaScript will be used to manage the click event on the toggle button and to modify the class on the \<html\> element.  
* The user's theme choice (light or dark) must be saved in the browser's localStorage to ensure the selected theme is automatically applied on subsequent visits.

#### **4\. Vibe & Aesthetic**

* **Light Theme: "Classic Pearl"**  
  * **Vibe:** Clean, clear, professional, and utilitarian. It should feel glossy and well-defined.  
* **Dark Theme: "Subscotia Dark"**  
  * **Vibe:** "Atmospheric & Focused". The theme should feel professional and immersive, suitable for late-night work.  
  * **Analogy:** The color palette will be inspired by the Subscotia Sound brand, using a sophisticated palette of dark charcoal greys instead of pure black, with a clear but not overwhelming accent color for contrast.

#### **5\. Known Constraints**

* This implementation will focus on the core application layout (body, header, sidebar, cards). More granular elements added later may require specific dark mode styling.