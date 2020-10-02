document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('delete_user_form')
    var button = document.getElementById('delete_user_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/delete_user',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        email: document.getElementById('delete_user_email').value
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
                        button.disabled = false
                        button.textContent = 'Delete'
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
                        button.textContent = 'Delete'
                    },
                    750
                )
            }
        )
    })
})