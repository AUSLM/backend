document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('grant_access_form')
    var button = document.getElementById('grant_access_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/grant_access',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        email: document.getElementById('grant_access_email').value,
                        address: document.getElementById('grant_access_address').value
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
                        button.textContent = 'Grant'
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
                        button.textContent = 'Grant'
                    },
                    750
                )
            }
        )
    })
})