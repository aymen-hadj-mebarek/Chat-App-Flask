const viewportHeight = window.innerHeight;
const viewportWidth = window.innerWidth;
const main = document.querySelector("#main")
main.style.height = viewportHeight+"px"
try {
    const header = document.querySelector("#header")
    header.style.height = viewportHeight+"px"
} catch (error) {
    console.log("no header")
}

let showed = "login"
try {
    let value = document.querySelector("#value")
    if (viewportWidth >= 915){    
        if (value.innerHTML == "login"){
            showed = "login"
            header.style.left = "-50%";
        }else if (value.innerHTML == "signup"){
            showed = "signup"
            header.style.left = "50%";
        }
    }else{
        if (value.innerHTML == "login"){
            showed = "login"
            header.style.top = "-50%";
        }else if (value.innerHTML == "signup"){
            showed = "signup"
            header.style.top = "50%";
        }   
    }
} catch (error) {
    console.log("no header")
}

function changepage(){
    let header = document.querySelector("#header");
    console.log("pressed");
    if (viewportWidth >= 915){    
        if (showed == "login"){
            header.style.left = "50%";
            showed = "signup";
        }else if (showed == "signup"){
            header.style.left = "-50%";
            showed = "login"
        }
    }else{
        if (showed == "login"){
            header.style.top = "50%";
            showed = "signup";
        }else if (showed == "signup"){
            header.style.top = "-50%";
            showed = "login"
        }
    }
}

function showmessage(){
    let message = document.querySelector("#message");
    console.log(message.value)
}

