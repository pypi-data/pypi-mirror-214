// Save the names of all open folders to localStorage
function saveOpenFolders() {
    // Get all the open folders
    let openFolders = document.querySelectorAll(".source-code-open-folder");
    // Create an array to store the names of the open folders
    let openFolderNames = [];
    // Loop through all the open folders and add their names to the array
    for (let i = 0; i < openFolders.length; i++) {
        let folderName = openFolders[i].previousElementSibling.textContent;
        openFolderNames.push(folderName);
    }
    // Save the array of open folder names to localStorage
    localStorage.setItem("openFolders", JSON.stringify(openFolderNames));
}


// Used to remember which folders are between sessions
function restoreOpenFolders() {
    // Check if there is saved data in localStorage
    if (localStorage.getItem("openFolders")) {
        // Get the saved array of open folder names from localStorage
        let openFolderNames = JSON.parse(localStorage.getItem("openFolders"));
        // Loop through all the open folder names
        for (let i = 0; i < openFolderNames.length; i++) {
            let folderName = openFolderNames[i];
            // Find all folder elements
            let folderElements = document.querySelectorAll(".source-code-tree-icon-prefix");
            for (let j = 0; j < folderElements.length; j++) {
                let folderElement = folderElements[j];
                // Check if the folder element has a matching name
                if (folderElement.textContent === folderName) {
                    // Open the matching folder
                    let nestedList = folderElement.nextElementSibling;
                    nestedList.classList.add("source-code-open-folder");
                    let img = nestedList.parentElement.querySelector(".source-code-file-icon");
                    img.src = "../assets/FolderOpen.svg";
                }
            }
        }
    }
}


// Used to toggle the visibility of the contents of folders in the source code tree and change file icon prefixes
function toggleSourceCodeFolderContents() {
    let toggler = document.getElementsByClassName("source-code-tree-icon-prefix");
    for (let i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function () {
            // Find the nested list element representing the contents of the clicked folder
            let nestedList = this.parentElement.querySelector(".source-code-tree-nested-list");

            // Toggle the "source-code-open-folder" class to show or hide the contents of the clicked folder
            nestedList.classList.toggle("source-code-open-folder");

            // Find the img element representing the prefixed image for the clicked folder
            let img = this.parentElement.querySelector(".source-code-file-icon");

            // Check if the nested list element has the "source-code-open-folder" class
            if (nestedList.classList.contains("source-code-open-folder")) {
                // If the nested list element has the "source-code-open-folder" class, it means the folder is open,
                // so set the src attribute of the img element to "LuaAutoDoc/Assets/FolderOpen.svg"
                img.src = "../assets/FolderOpen.svg";
            } else {
                // If the nested list element does not have the "source-code-open-folder" class, it means the folder is closed,
                // so set the src attribute of the img element to "LuaAutoDoc/Assets/FolderClosed.svg"
                img.src = "../assets/FolderClosed.svg";
            }
            // Save the state of open folders
            saveOpenFolders();
        });
    }
}


// Set up the folder map listeners
window.addEventListener('load', function () {
    toggleSourceCodeFolderContents();
    restoreOpenFolders();
});
