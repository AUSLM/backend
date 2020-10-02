function grant_admin_function() {

    var form = document.getElementById('admins_form')
    var button = document.getElementById('grant_admin_button')

    button.disabled = true

    fetch(
        '/api/grant_admin',
        {
            method: 'POST',
            body: JSON.stringify(
                {
                    email: document.getElementById('admin_email').value
                }
            ),
            headers: {
                'Content-Type': 'application/json'
            }
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
}