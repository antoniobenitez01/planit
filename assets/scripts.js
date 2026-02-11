function showSnackbar(message, type = 'info') {
    const snackbar = document.getElementById('snackbar');
    snackbar.textContent = message;
    snackbar.className = 'snackbar ' + type;
    snackbar.classList.add('show');
    
    setTimeout(function() {
        snackbar.classList.remove('show');
    }, 4000);
}

document.addEventListener('DOMContentLoaded', function() {
    const snackbar = document.getElementById('snackbar');
    const messagesData = snackbar.getAttribute('data-messages');
    
    if (messagesData && messagesData.trim() !== '[]') {
        try {
            const messages = JSON.parse(messagesData);
            messages.forEach(function(msg) {
                showSnackbar(msg.message, msg.tags);
            });
        } catch (e) {
            console.error('Error parsing messages:', e);
        }
    }
});