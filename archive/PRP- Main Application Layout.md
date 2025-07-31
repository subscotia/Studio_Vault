### **Product Requirements Prompt (PRP)**

### **Feature: Main Application Layout**

### **Version: 1.0**

#### **Objective**

To generate the complete HTML and JavaScript structure for the main application layout of the Subscotia Vault project. The final output will be a single index.html file that adheres to all global rules and feature requirements.

### **Execution Plan**

#### **Phase 1: HTML Structure (index.html)**

1. **Document Boilerplate:**  
   * Generate a standard HTML5 document structure with \<\!DOCTYPE html\>, \<html\>, \<head\>, and \<body\> tags.  
   * Set the language to en.  
   * In the \<head\>:  
     * Set charset to UTF-8.  
     * Set viewport for responsive design: \<meta name="viewport" content="width=device-width, initial-scale=1.0"\>.  
     * Set the title to "Subscotia Vault".  
     * Link the "Inter" font from Google Fonts.  
     * Link the output.css stylesheet using Flask's url\_for syntax: \<link href="{{ url\_for('static', filename='output.css') }}" rel="stylesheet"\>.  
2. **Body & Main Container:**  
   * Apply base styling to the \<body\> tag: a neutral background color (bg-gray-100), default text color (text-gray-800), and the "Inter" font (font-sans).  
   * Create a main container \<div\> that will hold the entire application. This \<div\> will use Flexbox to manage its children in a column layout (flex flex-col) and will be constrained to the full height of the viewport (h-screen).  
3. **Header Component:**  
   * Create a \<header\> element.  
   * Style it with a white background (bg-white), a subtle shadow (shadow-md), and padding (p-4).  
   * Inside the header, add an \<h1\> element with the text "Subscotia Vault". Style it with a larger font size (text-2xl), bold weight (font-bold), and dark text color (text-gray-900).  
4. **Main Content Wrapper:**  
   * Below the header, create a \<div\> that will wrap the Sidebar and Main Content areas.  
   * This wrapper will use Flexbox (flex) and be set to take up the remaining available space (flex-1).  
   * To prevent the entire page from scrolling, add overflow-y-hidden.  
5. **Sidebar Component:**  
   * Inside the content wrapper, create an \<aside\> element for the sidebar.  
   * Set its width to a fraction of the parent, e.g., one-quarter (w-1/4).  
   * Style it with a slightly different background to distinguish it (bg-gray-200), padding (p-6), and enable vertical scrolling only for its own content (overflow-y-auto).  
   * Add placeholder content: an \<h2\> with "Filters" and a \<p\> with "(Filter controls will go here)".  
6. **Main Content Area Component:**  
   * Next to the sidebar, create a \<main\> element for the primary content.  
   * Set its width to the remaining fraction, e.g., three-quarters (w-3/4).  
   * Style it with padding (p-6) and enable independent vertical scrolling (overflow-y-auto).  
   * Add placeholder content: an \<h2\> with "Plugins" and a \<div\> with id="json-container" that will hold our data for now.

#### **Phase 2: JavaScript Logic (index.html)**

1. **Data Fetching:**  
   * Create a \<script\> tag at the end of the \<body\>.  
   * Implement a fetch call to the /api/vault endpoint.  
   * Use .then() promises to handle the response. First, parse the response as JSON (response.json()).  
   * In the second .then(), take the parsed data and display it inside the \#json-container element. Use JSON.stringify(data, null, 2\) to format it neatly.  
   * Implement a .catch() block to log any errors to the console and display a failure message in the container.

#### **Final Review**

* Confirm all class names are valid Tailwind CSS utilities.  
* Verify the HTML structure is semantic and correctly nested.  
* Ensure the layout is responsive by design due to the use of fractional widths and flexbox.  
* Confirm the final output adheres to all constraints defined in rules.md and feature.md.

**Approval Request:** The Product Director is requested to review this PRP. Upon approval, the Code Engine will proceed with the execution phase via Bolt DIY.