document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('reset_password_form')
    var button = document.getElementById('reset_password_submit_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/reset_password',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        password: document.getElementById('reset_password_email').value
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
                        window.location = '/login'
                    },
                    750
                )
            }
        ).catch(
            error => {
                button.textContent = error.message
                setTimeout(
                    () => {
                        button.disabled = false
                        button.textContent = 'Reset'
                    },
                    750
                )
            }
        )
    })
})