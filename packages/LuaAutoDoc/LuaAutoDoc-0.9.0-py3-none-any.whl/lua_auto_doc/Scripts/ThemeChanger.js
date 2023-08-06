// Requires: get_current_folder() from LuaAutoDoc.js

// This function is called when the page loads to initialise the theme
function initTheme() {
    // Get the current theme from localStorage
    let theme = localStorage.getItem('theme');

    // If the current theme is dark or not initialised, set the theme to theme to dark
    if (theme === 'dark' || theme === null) {
        // Invert the value since toggleTheme will change it to the opposite theme
        localStorage.setItem('theme', 'light');
        toggleTheme();
    }
    else {
        // Invert the value since toggleTheme will change it to the opposite theme
        localStorage.setItem('theme', 'dark');
        toggleTheme();
    }
}


// This function is called when the user clicks on the theme-toggle button
function toggleTheme() {
    // Get the current theme from localStorage
    let theme = localStorage.getItem('theme');
    // Get the theme-toggle button element
    let themeToggle = document.getElementById('theme-toggle');

    // If the current theme is dark, switch to light mode
    if (theme === 'dark') {
        // Set the CSS variables to their light mode values
        /* LuaAutoDoc css variables. */
        document.documentElement.style.setProperty('--background-colour', 'var(--background-colour-light-theme)');
        document.documentElement.style.setProperty('--default-text-colour', 'var(--default-text-colour-light-theme)');
        document.documentElement.style.setProperty('--nav-base-colour', 'var(--nav-base-colour-light-theme)');
        document.documentElement.style.setProperty('--nav-header-colour', 'var(--nav-header-colour-light-theme)');
        document.documentElement.style.setProperty('--nav-bar-text-colour', 'var(--nav-bar-text-colour-light-theme)');
        document.documentElement.style.setProperty('--footer-base-colour', 'var(--footer-base-colour-light-theme)');
        document.documentElement.style.setProperty('--footer-text-colour', 'var(--footer-text-colour-light-theme)');
        document.documentElement.style.setProperty('--default-link-colour', 'var(--default-link-colour-light-theme)');
        document.documentElement.style.setProperty('--default-link-colour-visited', 'var(--default-link-colour-visited-light-theme)');
        document.documentElement.style.setProperty('--smooth-link-highlight-colour', 'var(--smooth-link-highlight-colour-light-theme)');
        document.documentElement.style.setProperty('--highlight-link-colour', 'var(--highlight-link-colour-light-theme)');
        /* CodeObject css variables. */
        document.documentElement.style.setProperty('--code-object-list-background-colour', 'var(--code-object-list-background-colour-light-theme)');
        document.documentElement.style.setProperty('--keyword-colour', 'var(--keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-object-header-colour', 'var(--code-object-header-colour-light-theme)');
        document.documentElement.style.setProperty('--param-table-border-colour', 'var(--param-table-border-colour-light-theme)');
        document.documentElement.style.setProperty('--param-table-head-background-colour', 'var(--param-table-head-background-colour-light-theme)');
        document.documentElement.style.setProperty('--prop-table-border-colour', 'var(--prop-table-border-colour-light-theme)');
        document.documentElement.style.setProperty('--prop-table-head-background-colour', 'var(--prop-table-head-background-colour-light-theme)');
        document.documentElement.style.setProperty('--custom-type-colour', 'var(--custom-type-colour-light-theme)');
        document.documentElement.style.setProperty('--lua-type-colour', 'var(--lua-type-colour-light-theme)');
        document.documentElement.style.setProperty('--lua-param-colour', 'var(--lua-param-colour-light-theme)');
        document.documentElement.style.setProperty('--lua-function-colour', 'var(--lua-function-colour-light-theme)');
        document.documentElement.style.setProperty('--lua-unknown-colour', 'var(--lua-unknown-colour-light-theme)');
        document.documentElement.style.setProperty('--lua-number-colour', 'var(--lua-number-colour-light-theme)');
        document.documentElement.style.setProperty('--internal-use-warning-colour', 'var(--internal-use-warning-colour-light-theme)');
        document.documentElement.style.setProperty('--internal-use-background-colour', 'var(--internal-use-background-colour-light-theme)');
        document.documentElement.style.setProperty('--deprecated-warning-colour', 'var(--deprecated-warning-colour-light-theme)');
        document.documentElement.style.setProperty('--deprecated-background-colour', 'var(--deprecated-background-colour-light-theme)');
        /* SearchPage css variables. */
        document.documentElement.style.setProperty('--search-match-background-colour', 'var(--search-match-background-colour-light-theme)');
        document.documentElement.style.setProperty('--search-match-text-colour', 'var(--search-match-text-colour-light-theme)');
        document.documentElement.style.setProperty('--search-result-background-colour', 'var(--search-result-background-colour-light-theme)');
        /* SourceCode css variables. */
        document.documentElement.style.setProperty('--code-field-border-colour', 'var(--code-field-border-colour-light-theme)');
        document.documentElement.style.setProperty('--line-number-colour', 'var(--line-number-colour-light-theme)');
        document.documentElement.style.setProperty('--code-default-text-colour', 'var(--code-default-text-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-background', 'var(--code-field-background-light-theme)');
        document.documentElement.style.setProperty('--code-field-background-alt', 'var(--code-field-background-alt-light-theme)');
        document.documentElement.style.setProperty('--code-field-string-colour', 'var(--code-field-string-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-number-colour', 'var(--code-field-number-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-keyword-colour', 'var(--code-field-keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-nil-keyword-colour', 'var(--code-field-nil-keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-true-keyword-colour', 'var(--code-field-true-keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-false-keyword-colour', 'var(--code-field-false-keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-unique-keyword-background', 'var(--code-field-unique-keyword-background-light-theme)');
        document.documentElement.style.setProperty('--code-field-self-keyword-colour', 'var(--code-field-self-keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-token-colour', 'var(--code-field-token-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-rainbow-colour-1', 'var(--code-field-rainbow-colour-1-light-theme)');
        document.documentElement.style.setProperty('--code-field-rainbow-colour-2', 'var(--code-field-rainbow-colour-2-light-theme)');
        document.documentElement.style.setProperty('--code-field-rainbow-colour-3', 'var(--code-field-rainbow-colour-3-light-theme)');
        document.documentElement.style.setProperty('--code-field-rainbow-colour-4', 'var(--code-field-rainbow-colour-4-light-theme)');
        document.documentElement.style.setProperty('--code-field-rainbow-colour-5', 'var(--code-field-rainbow-colour-5-light-theme)');
        document.documentElement.style.setProperty('--code-field-comment-colour', 'var(--code-field-comment-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-text-colour', 'var(--code-field-documentation-text-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-tag-colour', 'var(--code-field-documentation-tag-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-type-colour', 'var(--code-field-documentation-type-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-param-name-colour', 'var(--code-field-documentation-param-name-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-name-colour', 'var(--code-field-documentation-name-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-keyword-colour', 'var(--code-field-documentation-keyword-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-documentation-optional-colour', 'var(--code-field-documentation-optional-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-built-in-colour', 'var(--code-field-built-in-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-metamethods-colour', 'var(--code-field-metamethods-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-environment-var-colour', 'var(--code-field-environment-var-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-fields-colour', 'var(--code-field-fields-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-global-var-colour', 'var(--code-field-global-var-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-local-var-colour', 'var(--code-field-local-var-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-param-var-colour', 'var(--code-field-param-var-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-global-function-colour', 'var(--code-field-global-function-colour-light-theme)');
        document.documentElement.style.setProperty('--code-field-local-function-colour', 'var(--code-field-local-function-colour-light-theme)');
        document.documentElement.style.setProperty('--code-instance-method-colour', 'var(--code-instance-method-colour-light-theme)');
        document.documentElement.style.setProperty('--code-static-method-colour', 'var(--code-static-method-colour-light-theme)');
        /* SourceCodeFolderMap css variables. */
        document.documentElement.style.setProperty('--source-code-map-background-colour', 'var(--source-code-map-background-colour-light-theme)');
        document.documentElement.style.setProperty('--source-code-folder-highlight-colour', 'var(--source-code-folder-highlight-colour-light-theme)');

        // Update the background image of the theme-toggle button
        let folder = get_current_folder();
        if (folder === 'html') {
            themeToggle.style.backgroundImage = "url('../assets/DarkModeButton.svg')";
        } else {
            themeToggle.style.backgroundImage = "url('assets/DarkModeButton.svg')";
        }

        // Set the current theme to light in localStorage
        localStorage.setItem('theme', 'light');
    }
    else {
        // Reset the CSS variables to their default values
        /* LuaAutoDoc css variables. */
        document.documentElement.style.removeProperty('--background-colour');
        document.documentElement.style.removeProperty('--default-text-colour');
        document.documentElement.style.removeProperty('--nav-base-colour');
        document.documentElement.style.removeProperty('--nav-header-colour');
        document.documentElement.style.removeProperty('--nav-bar-text-colour');
        document.documentElement.style.removeProperty('--footer-base-colour');
        document.documentElement.style.removeProperty('--footer-text-colour');
        document.documentElement.style.removeProperty('--default-link-colour');
        document.documentElement.style.removeProperty('--default-link-colour-visited');
        document.documentElement.style.removeProperty('--smooth-link-highlight-colour');
        document.documentElement.style.removeProperty('--highlight-link-colour');
        /* CodeObject css variables. */
        document.documentElement.style.removeProperty('--code-object-list-background-colour');
        document.documentElement.style.removeProperty('--keyword-colour');
        document.documentElement.style.removeProperty('--code-object-header-colour');
        document.documentElement.style.removeProperty('--param-table-border-colour');
        document.documentElement.style.removeProperty('--param-table-head-background-colour');
        document.documentElement.style.removeProperty('--prop-table-border-colour');
        document.documentElement.style.removeProperty('--prop-table-head-background-colour');
        document.documentElement.style.removeProperty('--custom-type-colour');
        document.documentElement.style.removeProperty('--lua-type-colour');
        document.documentElement.style.removeProperty('--lua-param-colour');
        document.documentElement.style.removeProperty('--lua-function-colour');
        document.documentElement.style.removeProperty('--lua-unknown-colour');
        document.documentElement.style.removeProperty('--lua-number-colour');
        document.documentElement.style.removeProperty('--internal-use-warning-colour');
        document.documentElement.style.removeProperty('--internal-use-background-colour');
        document.documentElement.style.removeProperty('--deprecated-warning-colour');
        document.documentElement.style.removeProperty('--deprecated-background-colour');
        /* SearchPage css variables. */
        document.documentElement.style.removeProperty('--search-match-background-colour');
        document.documentElement.style.removeProperty('--search-match-text-colour');
        document.documentElement.style.removeProperty('--search-result-background-colour');
        /* SourceCode css variables. */
        document.documentElement.style.removeProperty('--code-field-border-colour');
        document.documentElement.style.removeProperty('--line-number-colour');
        document.documentElement.style.removeProperty('--code-default-text-colour');
        document.documentElement.style.removeProperty('--code-field-background');
        document.documentElement.style.removeProperty('--code-field-background-alt');
        document.documentElement.style.removeProperty('--code-field-string-colour');
        document.documentElement.style.removeProperty('--code-field-number-colour');
        document.documentElement.style.removeProperty('--code-field-keyword-colour');
        document.documentElement.style.removeProperty('--code-field-nil-keyword-colour');
        document.documentElement.style.removeProperty('--code-field-true-keyword-colour');
        document.documentElement.style.removeProperty('--code-field-false-keyword-colour');
        document.documentElement.style.removeProperty('--code-field-unique-keyword-background');
        document.documentElement.style.removeProperty('--code-field-self-keyword-colour');
        document.documentElement.style.removeProperty('--code-field-token-colour');
        document.documentElement.style.removeProperty('--code-field-rainbow-colour-1');
        document.documentElement.style.removeProperty('--code-field-rainbow-colour-2');
        document.documentElement.style.removeProperty('--code-field-rainbow-colour-3');
        document.documentElement.style.removeProperty('--code-field-rainbow-colour-4');
        document.documentElement.style.removeProperty('--code-field-rainbow-colour-5');
        document.documentElement.style.removeProperty('--code-field-comment-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-text-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-tag-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-type-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-param-name-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-name-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-keyword-colour');
        document.documentElement.style.removeProperty('--code-field-documentation-optional-colour');
        document.documentElement.style.removeProperty('--code-field-built-in-colour');
        document.documentElement.style.removeProperty('--code-field-metamethods-colour');
        document.documentElement.style.removeProperty('--code-field-environment-var-colour');
        document.documentElement.style.removeProperty('--code-field-fields-colour');
        document.documentElement.style.removeProperty('--code-field-global-var-colour');
        document.documentElement.style.removeProperty('--code-field-local-var-colour');
        document.documentElement.style.removeProperty('--code-field-param-var-colour');
        document.documentElement.style.removeProperty('--code-field-global-function-colour');
        document.documentElement.style.removeProperty('--code-field-local-function-colour');
        document.documentElement.style.removeProperty('--code-instance-method-colour');
        document.documentElement.style.removeProperty('--code-static-method-colour');
        /*SourceCodeFolderMap.css variables. */
        document.documentElement.style.removeProperty('--source-code-map-background-colour');
        document.documentElement.style.removeProperty('--source-code-folder-highlight-colour');

        // Update the background image of the theme-toggle button
        let folder = get_current_folder();
        if (folder === 'html') {
            themeToggle.style.backgroundImage = "url('../assets/LightModeButton.svg')";
        }
        else {
            themeToggle.style.backgroundImage = "url('assets/LightModeButton.svg')";
        }

        // Set the current theme to dark in localStorage
        localStorage.setItem('theme', 'dark');
    }
}

// Set up the theme
window.addEventListener('load', function () {
    initTheme();
});
