### **Product Requirements Prompt (PRP)**

### **Feature: Dark/Light Theme Toggle**

### **Version: 1.0**

#### **Objective**

To modify the index.html file to include a theme-switching mechanism. This involves adding a toggle button, implementing the necessary JavaScript logic to handle theme changes and persistence, and adding Tailwind CSS dark: variant classes to style the application for the "Subscotia Dark" theme.

### **Execution Plan**

#### **Phase 1: HTML Structure Modification (index.html)**

1. **Add Theme Toggle Button:**  
   * Locate the \<header\> element.  
   * Inside the header, after the \<h1\>, add a \<button\> element with id="theme-toggle-button".  
   * The button will contain two SVG icons (one for "sun" representing light mode, one for "moon" representing dark mode) sourced from Lucide Icons. The visibility of these icons will be controlled by the dark class on the \<html\> element.  
   * Apply appropriate styling to the button to position it correctly (e.g., in the top-right corner).  
2. **Enable Tailwind Dark Mode:**  
   * Open the tailwind.config.js file.  
   * Modify the module.exports object to enable class-based dark mode by adding darkMode: 'class'.

#### **Phase 2: CSS Styling (index.html via Tailwind Classes)**

1. **Apply dark: Variants:**  
   * Go through the existing layout elements (body, header, aside, main, and the plugin cards).  
   * For each element, add the corresponding dark: variant classes to define its appearance in the "Subscotia Dark" theme.  
   * **Example:** \<body class="bg-gray-100 dark:bg-gray-900 ..."\>  
   * **Example:** \<div class="bg-white dark:bg-gray-800 ..."\> (for cards and header)  
   * Text colors will also be updated using dark: variants (e.g., text-gray-800 dark:text-gray-200).

#### **Phase 3: JavaScript Logic (index.html)**

A new, self-contained script block will be added to manage all theme-related logic. It will be placed just before the closing \</body\> tag.

1. **Define Elements:** Get references to the theme toggle button and the two icons (sun/moon) within it.  
2. **Initial Theme Check (On Page Load):**  
   * Create a script that runs immediately on page load.  
   * This script will check for a theme preference stored in localStorage (localStorage.getItem('theme')).  
   * It will also check the user's OS-level preference via window.matchMedia('(prefers-color-scheme: dark)').matches.  
   * **Logic:**  
     * If localStorage has 'dark', apply the dark class to \<html\>.  
     * Else if localStorage has 'light', remove the dark class.  
     * Else if the OS prefers dark, apply the dark class.  
   * This ensures the correct theme is applied instantly, preventing a "flash" of the wrong theme.  
3. **Event Listener:**  
   * Attach a click event listener to the theme-toggle-button.  
   * **On Click:**  
     * Check if the \<html\> element currently has the dark class.  
     * If it does, remove the dark class and save 'light' to localStorage.  
     * If it does not, add the dark class and save 'dark' to localStorage.  
     * Update the visibility of the sun/moon icons accordingly.

#### **Final Review**

* Confirm the theme toggle button is correctly placed and functional.  
* Verify that all major UI elements have appropriate dark: variant styles.  
* Test the localStorage persistence by toggling the theme, refreshing the page, and ensuring the choice is remembered.  
* Test the initial OS-level preference detection by clearing localStorage and refreshing.

**Approval Request:** The Product Director is requested to review this PRP. Upon approval, the Code Engine will proceed with the execution phase.