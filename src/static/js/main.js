/**
 * $(document).ready() in pure javascript.
 * @param {*} fn 
 */
function ready(fn) {
    if (document.readyState !== 'loading') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}


ready(function(){
    const openMenu = document.getElementById("openMenu");
    const closeMenu = document.getElementById("closeMenu");
    const hiddenMenu = document.getElementById("hiddenMenu");

    const toggleMenu = function(){
        console.log("aquiiii")
        let isOpen = hiddenMenu.classList.contains("translate-x-0");

        if (isOpen){
            hiddenMenu.classList.add("translate-x-full")
            hiddenMenu.classList.remove("translate-x-0")
        }else{
            hiddenMenu.classList.add("translate-x-0")
            hiddenMenu.classList.remove("translate-x-full")            
        }
    }

    openMenu.addEventListener("click", toggleMenu);
    closeMenu.addEventListener("click", toggleMenu);
});
