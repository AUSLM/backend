function revoke_access_function(obj) {

    var machine_address = obj.getAttribute('machine_address')
    var user_email = obj.getAttribute('user_email')

    button_text = obj.querySelector('#button_text')

    row_link = obj.parentNode.parentNode.querySelector('#row_link')

    obj.disabled = true

    fetch(
        '/api/revoke_access',
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
                button.disabled = true
                return response.json().then(
                    data => Promise.reject(data['error'])
                )
            }
            return response.json()
        }
    ).then(
        body => {
            button_text.innerHTML = 'Revoked'
            obj.parentNode.parentNode.className += " text-light bg-secondary"

            row_link.className += " text-light"
            row_link.removeAttribute("href")
        }
    ).catch(
        error => {
            button_text.innerHTML = error
            setTimeout(
                () => {
                    obj.disabled = false
                    button_text.innerHTML = 'Revoke'
                },
                750
            )
        }
    )
}