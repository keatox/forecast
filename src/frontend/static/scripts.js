// function handle(input){
//     if (input.keyCode === 13){
//         input.preventDefault();

//         data = {
//             'ticker': document.getElementById('landingsearch').value
//         }
//         jsonData = JSON.stringify(data);
//         fetch('food_summary', {
//             method: "POST",
//             headers: {
//                 'Content-type': 'application/json'
//             },
//             body: jsonData
//         })
//     }
// }

// closes dropdown everytime a new page is loaded
// so that if one backtracks pages it is closed
function closeMenu(){
    document.getElementById('menu').checked = false;
}

// toggles all necessary items 
function toggleDarkmode(){
    var body = document.body;
    var blocks = document.querySelectorAll('#block');
    var border = document.getElementById('linebreak');

    try{
        border.classList.toggle("darklinebreak");
    } catch(error){
    }
    body.classList.toggle("darkmodebody");
    for (var i=0;i<blocks.length;i++){
        blocks[i].classList.toggle("darkmodeblock");
    }

    // saves toggle state
    if (body.classList.contains("darkmodebody")) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

// checks toggle state upon loading new page to keep light/dark mode
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