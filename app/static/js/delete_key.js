function delete_key_function(obj) {

    var ssh_key_id = obj.getAttribute('ssh_key_id')
    var user_email = obj.getAttribute('user_email')

    button_text = obj.querySelector('#button_text')

    obj.disabled = true

    fetch(
        '/api/remove_key',
        {
            method: 'POST',
            body: JSON.stringify(
                {
                    u_email: user_email,
                    k_id: ssh_key_id
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
            button_text.innerHTML = 'Deleted'
            obj.parentNode.parentNode.className += " text-light bg-secondary"
        }
    ).catch(
        error => {
            button_text.innerHTML = error
            setTimeout(
                () => {
                    obj.disabled = false
                    button_text.innerHTML = 'Delete'
                },
                750
            )
        }
    )
}