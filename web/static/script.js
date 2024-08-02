document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    document.getElementById('NoMoreLeaks').classList.remove("good")
    document.getElementById('NoMoreLeaks').classList.remove("bad")

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();

    document.getElementById('NoMoreLeaks').textContent = result.NoMoreLeaks;
     
    if ( result.NoMoreLeaks ) {
        document.getElementById('NoMoreLeaks').classList.add("bad")
    } else {
        document.getElementById('NoMoreLeaks').classList.add("good")
    }
    
});