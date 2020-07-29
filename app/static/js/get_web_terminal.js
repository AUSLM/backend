function get_web_terminal_function(obj) {
    var machine_address = obj.getAttribute('machine_address')
    button_text = obj.querySelector('#button_text')

    obj.disabled = true

    fetch(
        '/api/web_terminal',
        {
            method: 'POST',
            body: JSON.stringify(
                {
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
            obj.disabled = false
            alert("Use current password: " + body["password"])
            window.location.href = body["url"]
        }
    ).catch(
        error => {
            button_text.innerHTML = error
            setTimeout(
                () => {
                    obj.disabled = false
                    button_text.innerHTML = 'Remove'
                },
                750
            )
        }
    )
}