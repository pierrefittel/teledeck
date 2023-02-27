async function login() {
    //POST request content formatting
    const username = document.getElementById('id_username').value;
    const password = document.getElementById('id_password').value;
    const content = `{"username": "${username}", "password": "${password}"}`;
    //POST request
    const CSRFToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const URL = '/dashboard/login';
    const response = await fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken,
            'origin': CSRFToken
        },
        body: content
    });
    if (response.status == 200) {
        window.open(response.url,"_self");
    } else if (response.status == 405) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerText = 'Authentication failed';
    }
}


document.getElementById('login').addEventListener('click', function() { login(); });
