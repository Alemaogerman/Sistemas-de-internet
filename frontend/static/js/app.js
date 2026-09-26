/* trocar modo de tela */ 
const iconeDark = document.getElementById("modo-dark");

iconeDark.addEventListener("click", function(){
    document.body.classList.toggle("dark");
});
