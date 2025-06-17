// displayRegister & displayLogin logic

const loginForm = document.querySelector(".input-form");
const loginWelcome = document.querySelector(".welcome");
const registerForm =  document.querySelector(".input-form-register");
const registerWelcome = document.querySelector(".welcome-register");

let isLoginDisplayed = false;

window.onload = () => {
    loginForm.style.display = "none";
    loginWelcome.style.display = "none";
    isLoginDisplayed = false;
};


//apply fade 

function applyFade(){
    const formContainers = [
        document.querySelector(".input-form-register"),
        document.querySelector(".welcome-register"),
        document.querySelector(".input-form"),
        document.querySelector(".welcome")
    ];
    
    formContainers.forEach(container => {
        const children = container.children;
        Array.from(children).forEach(child => {
            child.style.animation = 'fadeAnim 0.1s ease'; 
        });
    });
    
}

function displayLogin() {
    if (!isLoginDisplayed) {
        registerForm.classList.add("active");
        registerWelcome.classList.add("active");

        setTimeout(() => {

            registerForm.style.display = "none";
            registerWelcome.style.display = "none";

            loginForm.style.display = "flex";
            loginWelcome.style.display = "flex";

           
            isLoginDisplayed = true;
        }, 500); 

        

        setTimeout(() => {
            registerForm.classList.remove("active");
            registerWelcome.classList.remove("active");

        }, 600);
        applyFade()
    }
}

function displayRegister() {
    if (isLoginDisplayed) {
        
        loginForm.classList.add("active");
        loginWelcome.classList.add("active");
        

        setTimeout(() => {
            loginForm.style.display = "none";
            loginWelcome.style.display = "none";

            registerForm.style.display = "flex";
            registerWelcome.style.display = "flex";

            isLoginDisplayed = false;
        }, 500);


        setTimeout(() => {
            loginForm.classList.remove("active");
            loginWelcome.classList.remove("active");
        }, 600);
        applyFade()
    }
}



// confirm password logic
document.addEventListener("DOMContentLoaded", () => {
    const passwordField = document.getElementById("passwordRegister");
    const confirmPasswordField = document.getElementById("confirmpass");
    const divConfirm = document.querySelector(".fieldConfirm");
    const labelCF = document.getElementById("labelCF");

    //initial check 
    if (passwordField.value === "") {
        divConfirm.style.display = "none";
    }

    function validatePassword() {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;

        console.log("password:", password);
        console.log("confirmPassword:", confirmPassword);

        // Show/hide div 
        if (password === "") {
            divConfirm.style.display = "none";
        } else {
            divConfirm.style.display = "flex";
        }

        // Label validation 
        if (confirmPassword !== "" && confirmPassword !== password) {
            labelCF.innerHTML = "Password is not the same";
            labelCF.style.color = "red";
        } else {
            labelCF.innerHTML = "<h4>Confirm Password</h4>";
            labelCF.style.color = "rgba(0, 0, 0, 0.32)"; 
        }
    }

    
    passwordField.addEventListener("input", validatePassword);
    confirmPasswordField.addEventListener("input", validatePassword);

});






    
