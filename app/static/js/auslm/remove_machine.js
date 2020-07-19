document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('remove_form')
    var button = document.getElementById('remove_machine_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/remove_machine',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        address: 
                            document
                                .getElementById('remove_machine_address')
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
                        button.textContent = 'Remove'
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
                        button.textContent = 'Remove'
                    },
                    750
                )
            }
        )

    })

})