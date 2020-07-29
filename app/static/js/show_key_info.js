function show_key_info_function(u_email, k_id) {

    var key_name_modal = document.getElementById('key_name_modal')
    var key_data_modal = document.getElementById('key_data_modal')
    var key_time_modal = document.getElementById('key_time_modal')

    fetch(
        '/api/key_info',
        {
            method: 'POST',
            body: JSON.stringify(
                {
                    u_email: u_email,
                    k_id: k_id
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
            key_name_modal.innerHTML = body['name']
            key_data_modal.innerHTML = body['key']
            key_time_modal.innerHTML = body['update_time']
        }
    ).catch(
        error => {
            key_name_modal.innerHTML = error
        }
    )
}