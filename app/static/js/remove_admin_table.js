function remove_admin_table_function(obj) {

    var admin_email = obj.getAttribute('admin_email')

    button_text = obj.querySelector('#button_text')

    row_link = obj.parentNode.parentNode.querySelector('#row_link')

    obj.disabled = true

    fetch(
        '/api/remove_admin',
        {
            method: 'POST',
            body: JSON.stringify(
                {
                    email: admin_email
                }
            ),
            headers: {
                'Content-Type': 'application/json'
            }
        }
    ).then(
        response => {
            if (response.status < 200 || response.status >= 300) {
                obj.disabled = true
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