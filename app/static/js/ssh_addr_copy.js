function ssh_addr_copy(obj) {

    var ssh_addr = obj.getAttribute('ssh_addr')
    navigator.clipboard.writeText(ssh_addr)
}