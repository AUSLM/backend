function jwt_token_reissue_function() {

    var button = document.getElementById('jwt_token_reissue_button')

    button.disabled = true

    fetch(
        '/api/issue_token'
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
            document.getElementById('token_text').innerHTML = body['description']
            button.textContent = "(Re)issued"
            setTimeout(
                () => {
                    button.disabled = false
                    button.textContent = '(Re)issue token'
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
                    button.textContent = '(Re)issue token'
                },
                750
            )
        }
    )
}