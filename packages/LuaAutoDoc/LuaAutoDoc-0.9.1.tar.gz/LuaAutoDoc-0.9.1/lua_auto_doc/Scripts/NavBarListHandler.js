//Remembers which lists are open using local storage.
function rememberOpenLists() {
    // Select all elements with the nav-bar-list-div class
    let dropdowns = document.getElementsByClassName("nav-bar-list-div");
    for (let i = 0; i < dropdowns.length; i++) {
        // Check if the dropdown element has at least two children
        if (dropdowns[i].children.length >= 2) {
            // Get the dropdown content and button elements
            let dropdownContent = dropdowns[i].children[1];
            let dropbtn = dropdowns[i].children[0];
            // If the button text is stored in local storage, show the dropdown content and set the data-prefix attribute to "-"
            if (localStorage.getItem(dropbtn.textContent)) {
                dropdownContent.style.display = "block";
                dropbtn.setAttribute("data-prefix", "-");
            }
        }
    }
}


//Opens and closes the lists when clicked.
function setupListToggle() {
    // Select all elements with the nav-bar-list-div class
    let dropdowns = document.getElementsByClassName("nav-bar-list-div");
    for (let i = 0; i < dropdowns.length; i++) {
        // Check if the dropdown element has at least two children
        if (dropdowns[i].children.length >= 2) {
            // Get the dropdown content and button elements
            let dropdownContent = dropdowns[i].children[1];
            let dropbtn = dropdowns[i].children[0];
            // If the dropdown content has no children, set the data-prefix attribute to two non-breaking space characters
            if (dropdownContent.children.length === 0) {
                dropbtn.setAttribute("data-prefix", "\u00A0\u00A0");
            }
            // Add a click event listener to the dropdown element
            dropdowns[i].addEventListener("click", function (event) {
                // Stop the event from propagating to parent elements
                event.stopPropagation();
                // Check if the clicked element is an <a> tag or a <span> tag inside an <a> tag
                if (event.target.tagName === "A" || (event.target.tagName === "SPAN" && event.target.parentNode.tagName === "A")) {
                    return;
                }
                // Toggle the active class on the dropdown element
                this.classList.toggle("active");
                // If the dropdown content is visible, hide it and remove the button text from local storage
                if (dropdownContent.style.display === "block") {
                    dropdownContent.style.display = "none";
                    localStorage.removeItem(dropbtn.textContent);
                    // If the dropdown content has children, set the data-prefix attribute to "+"
                    if (dropdownContent.children.length > 0) {
                        dropbtn.setAttribute("data-prefix", "+");
                    }
                }
                else {
                    // If the dropdown content is not visible, show it and store the button text in local storage
                    dropdownContent.style.display = "block";
                    localStorage.setItem(dropbtn.textContent, 'true');
                    // If the dropdown content has children, set the data-prefix attribute to "-"
                    if (dropdownContent.children.length > 0) {
                        dropbtn.setAttribute("data-prefix", "-");
                    }
                }
            });
        }
    }
}


// Add load event listeners to the window
window.addEventListener('load', function () {
    // Set up the list listeners
    rememberOpenLists();
    setupListToggle();
});
