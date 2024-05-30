function toggleDarkmode(){
    var body = document.body;
    var blocks = document.querySelectorAll('#block');

    body.classList.toggle("darkmodebody");
    for (var i=0;i<blocks.length;i++){
        blocks[i].classList.toggle("darkmodeblock");
    }

    if (body.classList.contains("darkmodebody")) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

function handle(input){
    if (input.keyCode === 13){
        input.preventDefault();
        window.location.href = "dashboard";
    }
}

function closeMenu(){
    document.getElementById('menu').checked = false;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('darkmodebody');
        var blocks = document.querySelectorAll('#block');
        for (var i = 0; i < blocks.length; i++) {
            blocks[i].classList.add('darkmodeblock');
        }
    }  
}); 