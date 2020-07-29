document.addEventListener('DOMContentLoaded', () => {
    
    var form = document.getElementById('change_password_form')
    var button = document.getElementById('change_password_button')

    form.addEventListener('input', () => {

        var passwordInput = document.getElementById('change_password_new_password')
        var passwordInputConfirmation = document.getElementById('change_password_new_password_confirm')
        
        if (passwordInput.value != passwordInputConfirmation.value) {
            passwordInputConfirmation.setCustomValidity('Not the same passwords')
        } else {
            passwordInputConfirmation.setCustomValidity('')
        }
    })

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true;

        fetch(
            '/api/change_password',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        old_password: document.getElementById('change_password_old_password').value,
                        new_password: document.getElementById('change_password_new_password').value,
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
                        button.textContent = 'Change password'
                        form.reset()
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
                        button.textContent = 'Change password'
                    },
                    750
                )
            }
        )
    })
})