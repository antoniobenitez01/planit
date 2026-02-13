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

document.getElementById('id_images').addEventListener('change', function(e) {
    const files = e.target.files;
    const captionContainer = document.getElementById('caption-inputs');
    const captionSection = document.getElementById('image-captions');
    
    captionContainer.innerHTML = '';
    
    if (files.length > 0) {
        captionSection.style.display = 'block';
        
        for (let i = 0; i < files.length; i++) {
            const captionDiv = document.createElement('div');
            captionDiv.className = 'mb-3';
            captionDiv.innerHTML = `
                <label class="form-label">Caption for ${files[i].name}</label>
                <input 
                    type="text" 
                    name="caption_${i}" 
                    maxlength="200" 
                    class="form-control" 
                    placeholder="Optional caption"
                >
            `;
            captionContainer.appendChild(captionDiv);
        }
    } else {
        captionSection.style.display = 'none';
    }
});