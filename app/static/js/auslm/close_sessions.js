document.addEventListener('DOMContentLoaded', () => {
    
    var form = document.getElementById('close_sessions_form')
    var button = document.getElementById('close_sessions_button')

    form.addEventListener('submit', event => {

        event.preventDefault()

        button.disabled = true;

        fetch(
            '/api/close_all_sessions',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        password: document.getElementById('close_sessions_password').value,
                    }
                )
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
                        button.textContent = 'Close other sessions'
                        form.reset()
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
                        button.textContent = 'Close other sessions'
                    },
                    750
                )
            }
        )
    })
})