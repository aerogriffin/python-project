let menuVisible = false;

function hideMenu(){
    if(menuVisible){
        document.getElementById("nav").classList ="";
        menuVisible = false;
    }else{
        document.getElementById("nav").classList ="responsive";
        menuVisible = true;
    }
}

function seleccionar(){
    document.getElementById("nav").classList = "";
    menuVisible = false;
}
function toggleUserOptions() {
    var userOptions = document.getElementById("userOptions");
    userOptions.style.display = (userOptions.style.display === "block") ? "none" : "block";
}

// Cerrar las opciones del usuario al hacer clic fuera de ellas
document.addEventListener("click", function(event) {
    var userSection = document.querySelector(".user-section");
    var userOptions = document.getElementById("userOptions");

    if (event.target !== userSection && !userSection.contains(event.target)) {
        userOptions.style.display = "none";
    }
});
