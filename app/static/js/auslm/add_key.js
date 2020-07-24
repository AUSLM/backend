document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('add_key_form')
    var button = document.getElementById('add_key_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/add_key',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        name: document.getElementById('add_key_name').value,
                        key: document.getElementById('add_key_data').value
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
                        button.textContent = 'Add'
                        form.reset()
                        document.location.reload(true)
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
                        button.textContent = 'Add'
                    },
                    750
                )
            }
        )
    })
})