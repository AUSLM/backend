document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('grant_form')
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
                        email:
                            document
                                .getElementById('grant_email')
                                    .value,
                        address: 
                            document
                                .getElementById('grant_address')
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
                        button.textContent = 'Grant'
                        form.reset()
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
                        button.textContent = 'Grant'
                    },
                    750
                )
            }
        )

    })

})