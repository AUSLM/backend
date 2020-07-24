document.addEventListener('DOMContentLoaded', () => {

    var form = document.getElementById('grant_access_form')
    var button = document.getElementById('grant_access_button')

    form.addEventListener('submit', event => {

        var machine_address = button.getAttribute('machine_address')
        if (machine_address == null || machine_address == "") {
            machine_address = document.getElementById('grant_access_address').value
        }

        var user_email = button.getAttribute('user_email')
        if (user_email == null || user_email == "") {
            user_email = document.getElementById('grant_access_email').value
        }

        event.preventDefault()

        button.disabled = true

        fetch(
            '/api/grant_access',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        email: user_email,
                        address: machine_address
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
                        button.textContent = 'Grant'
                    },
                    750
                )
            }
        )
    })
})