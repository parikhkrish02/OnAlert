let LoginBtn = document.getElementById("signup_login")
let LoginForm = document.getElementById("login-form")
let MainContent = document.querySelector(".hi")

LoginBtn.addEventListener('click', () => {
    if (MainContent.style.display != "none") {
        document.querySelector("body").style.backgroundColor = "black";
        LoginForm.style.marginTop = "150px";
        LoginForm.style.marginBottom = "50px";
        LoginForm.style.display = "flex";
        MainContent.style.display = "none";
    } else {
        document.querySelector("body").style.backgroundColor = "#eee";
        LoginForm.style.display = "none";
        MainContent.style.display = "inline";
    }
})

console.clear();

const loginBtn = document.getElementById("login");
const signupBtn = document.getElementById("signup");

loginBtn.addEventListener("click", (e) => {
    let parent = e.target.parentNode.parentNode;
    Array.from(e.target.parentNode.parentNode.classList).find((element) => {
        if (element !== "slide-up") {
            parent.classList.add("slide-up");
        } else {
            signupBtn.parentNode.classList.add("slide-up");
            parent.classList.remove("slide-up");
        }
    });
});

signupBtn.addEventListener("click", (e) => {
    let parent = e.target.parentNode;
    Array.from(e.target.parentNode.classList).find((element) => {
        if (element !== "slide-up") {
            parent.classList.add("slide-up");
        } else {
            loginBtn.parentNode.parentNode.classList.add("slide-up");
            parent.classList.remove("slide-up");
        }
    });
});