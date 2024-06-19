async function signup() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const responseElement = document.getElementById('response');

    const response = await fetch('/user/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
        }),
    });

    const result = await response.json();

    if (response.ok) {
        responseElement.innerText = 'User created successfully!';
        responseElement.style.color = 'green';
    } else {
        responseElement.innerText = `Error: ${result.detail}`;
        responseElement.style.color = 'red';
    }
}
