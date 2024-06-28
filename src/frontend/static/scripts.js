// closes dropdown everytime a new page is loaded so if user backtracks pages it is closed
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

// initiates cleanup function upon exiting window
window.addEventListener('beforeunload', function (event) {
    navigator.sendBeacon("/cleanup");
});

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

// queries db and lists top suggestions
document.addEventListener('DOMContentLoaded', () => {
    const landing = document.getElementById('landingsearch');
    const dash = document.getElementById('dashsearch');
    const resultsContainer = document.getElementById('results');
    const searchForm = document.getElementById('searchForm');

    navigator.sendBeacon("/create_conn");

    if (landing){
        var searchInput = landing;
    } else{
        var searchInput = dash;
    }

    // submits top autocomplete results on enter
    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && resultsContainer.innerHTML != '') {
            searchInput.value = resultsContainer.firstChild.innerText;
            clearSuggestions();
            searchForm.submit();
        }
    });
    
    // generates new queries on each input
    searchInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length > 0) {
            fetchSuggestions(query);
        } else {
            clearSuggestions();
        }
    });

    // fetches top suggestions from autocomplete
    function fetchSuggestions(query) {
        fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data);
            })
            .catch(error => {
                console.error('Error fetching autocomplete suggestions:', error);
            });
    }

    // creates new li tags for each suggestion
    function displaySuggestions(suggestions) {
        clearSuggestions();
        if (suggestions.length > 0) {
            resultsContainer.classList.remove('hidden');
            suggestions.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                li.addEventListener('click', () => {
                    searchInput.value = item;
                    clearSuggestions();
                    searchForm.submit();
                });
                resultsContainer.appendChild(li);
            });
        } else {
            resultsContainer.classList.add('hidden');
        }
    }

    // clears and hides dropdown as needed 
    function clearSuggestions() {
        resultsContainer.innerHTML = '';
        resultsContainer.classList.add('hidden');
    }
});