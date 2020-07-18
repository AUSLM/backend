document.addEventListener('DOMContentLoaded', () => {
    
    var form = document.getElementById('registration_form')
    var button = document.getElementById('registration_form_submit_button')

    form.addEventListener('input', () => {

        var passwordInput = document.getElementById('register_user_password')
        var passwordInputConfirmation =
            document
                .getElementById('register_user_password_confirmation')
        
        if (passwordInput.value != passwordInputConfirmation.value) {
            passwordInputConfirmation.setCustomValidity('Not the same answers')
        } else {
            passwordInputConfirmation.setCustomValidity('')
        }
        

    })

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true;

        fetch(
            '/api/register',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        email:
                            document
                                .getElementById('register_user_email')
                                    .value,
                        password:
                            document
                                .getElementById('register_user_password')
                                    .value,
                        name:
                            document
                                .getElementById('register_user_name')
                                    .value,
                        surname: 
                            document
                                .getElementById('register_user_surname')
                                    .value
                    }
                )
            }
        ).then(
            response => {
                if (response.status < 200 || response.status >= 300) {
                    button.disabled = true
                    return response.json().then(
                        data => Promise.reject(data['error'])
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
                        button.textContent = 'Register'
                        window.location = '/login'
                    },
                    750
                )
            }
        ).catch(
            error => {
                button.textContent = error
                setTimeout(
                    () => {
                        button.disabled = false
                        button.textContent = 'Register'
                    },
                    750
                )
            }
        )

    })
})