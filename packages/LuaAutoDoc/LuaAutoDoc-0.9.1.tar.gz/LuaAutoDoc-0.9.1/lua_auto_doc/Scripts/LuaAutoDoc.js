// Returns the current folder of the page
function get_current_folder() {
    let segments = window.location.pathname.split('/');
    let toDelete = [];
    for (let i = 0; i < segments.length; i++) {
        if (segments[i].length < 1) {
            toDelete.push(i);
        }
    }
    for (let i = 0; i < toDelete.length; i++) {
        segments.splice(i, 1);
    }
    return segments[segments.length - 2];
}

// Return current page name
function get_current_file() {
    let segments = window.location.pathname.split('/');
    let toDelete = [];
    for (let i = 0; i < segments.length; i++) {
        if (segments[i].length < 1) {
            toDelete.push(i);
        }
    }
    for (let i = 0; i < toDelete.length; i++) {
        segments.splice(i, 1);
    }
    return segments[segments.length - 1];
}
