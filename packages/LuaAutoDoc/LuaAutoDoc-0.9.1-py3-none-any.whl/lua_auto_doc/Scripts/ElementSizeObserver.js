// Make the navbar and main-center dynamic in width
function main_center_nav_bar_offset() {
    let navbar = document.querySelector('#nav-bar');
    let content = document.querySelector('#main-center');
    let observer = new ResizeObserver(function (entries) {
        for (let entry of entries) {
            content.style.marginLeft = `calc(${entry.contentRect.width}px + 2em)`;
        }
    });
    observer.observe(navbar);
}


// Make the bottom of main-container have a margin at the bottom equal to the height of the footer
function main_center_footer_margin() {
    let footer = document.querySelector('#footer');
    let mainContainer = document.querySelector('#main-center');
    let observer = new ResizeObserver(function (entries) {
        for (let entry of entries) {
            mainContainer.style.marginBottom = `calc(${entry.contentRect.height}px + 1em)`;
        }
    });
    observer.observe(footer);
}


// Give the nav-list a margin at the bottom equal to the height of the footer
function nav_list_footer_margin() {
    let footer = document.querySelector('#footer');
    let navBar = document.querySelector('#nav-list');
    let observer = new ResizeObserver(function (entries) {
        for (let entry of entries) {
            navBar.style.marginBottom = `calc(${entry.contentRect.height}px + 1em)`;
        }
    });
    observer.observe(footer);
}


// Set up resize listeners
window.addEventListener('load', function () {
    main_center_nav_bar_offset();
    main_center_footer_margin();
    nav_list_footer_margin();
});
