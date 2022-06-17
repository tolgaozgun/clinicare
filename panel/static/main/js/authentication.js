let current = 0;
let input = document.getElementById("id_role")
input.value = current;
function switchForm(value){
    if(value !== current){
        // Array.from(document.forms).forEach((input) => {
        //     input.classList.toggle("active")
        //     input.classList.toggle("inactive")
        // })

        input.value = value;
        Array.from(document.getElementsByClassName("form-selector")).forEach((input) => {
            input.classList.toggle("active")
            input.classList.toggle("inactive")
        })
    }
    current = value;
}
