let current = 0;
function switchForm(value){
    if(value !== current){
        // Array.from(document.forms).forEach((input) => {
        //     input.classList.toggle("active")
        //     input.classList.toggle("inactive")
        // })

        Array.from(document.getElementsByClassName("form-selector")).forEach((input) => {
            input.classList.toggle("active")
            input.classList.toggle("inactive")
        })
    }
    current = value;
}
