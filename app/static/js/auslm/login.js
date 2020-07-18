document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('login_form')
    var button = document.getElementById('login_submit_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/login',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        email:
                            document
                                .getElementById('login_user_email')
                                    .value,
                        password: 
                            document
                                .getElementById('login_user_password')
                                    .value
                    }
                ),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then(
            response => {
                if (response.status < 200 || response.status >= 300) {
                    return response.json().then(
                        data => Promise.reject(
                            {
                                code: response.status,
                                message: data['error']
                            }
                        )
                    )
                }
                return response.json()
            }
        ).then(
            body => {
                button.textContent = body['description']
                setTimeout(
                    () => {
                        button.disabled = false
                        button.textContent = 'Login'
                        const urlParams = 
                            new URLSearchParams(window.location.search);
                        const location = urlParams.get('next');
                        if (location != null) {
                            window.location = location
                        } else {
                            window.location = '/'
                        }
                    },
                    750
                )
            }
        )
        .catch(
            error => {
                button.textContent = error.message
                setTimeout(
                    () => {
                        button.disabled = false
                        button.textContent = 'Send'
                        if (error.code == 409) {
                            window.location = '/'
                        }
                    },
                    750
                )
            }
        )

    })

})