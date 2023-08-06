// Requires: get_current_folder() from LuaAutoDoc.js

// Set up the listener for the search bar
function searchBarListener() {
    let searchBar = document.getElementById('nav-bar-search');
    searchBar.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
            event.preventDefault();
            let query = searchBar.value;
            searchIndex(query);
        }
    });
}


// Search the index for the query and redirect to the search page
function searchIndex(query) {
    // Check the current folder to determine the path to the search page
    let folder = get_current_folder();
    // If we are in the html folder, directly link to the search page
    if (folder === 'html') {
        window.location.href = `search_page.html?q=${encodeURIComponent(query)}`;
    }
    else {
        window.location.href = `html/search_page.html?q=${encodeURIComponent(query)}`;
    }
}


// Set up the search bar listener
window.addEventListener('load', function () {
    searchBarListener();
});
