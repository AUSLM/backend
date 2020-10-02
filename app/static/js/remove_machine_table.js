function remove_machine_function(obj) {

    var machine_address = obj.getAttribute('machine_address')

    button_text = obj.querySelector('#button_text')

    machine_link = obj.parentNode.parentNode.querySelector('#machine_link')
    web_terminal_button = obj.parentNode.parentNode.querySelector('#web_terminal_button')
    ssh_addr_copy_button = obj.parentNode.parentNode.querySelector('#ssh_addr_copy_button')

    obj.disabled = true

    fetch(
        '/api/remove_machine',
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
                obj.disabled = true
                return response.json().then(
                    data => Promise.reject(data['error'])
                )
            }
            return response.json()
        }
    ).then(
        body => {
            button_text.innerHTML = 'Removed'
            obj.parentNode.parentNode.className += " text-light bg-secondary"

            machine_link.className += " text-light"
            machine_link.removeAttribute("href")

            web_terminal_button.disabled = true
            ssh_addr_copy_button.disabled = true
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