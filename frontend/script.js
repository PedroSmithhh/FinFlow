document.addEventListener('DOMContentLoaded', function() {
    
    const textInput = document.getElementById('email_text');
    const fileInput = document.getElementById('email_file');
    const groupText = document.getElementById('group-text');
    const groupFile = document.getElementById('group-file');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const form = document.getElementById('analysisForm');
    const loadingDiv = document.getElementById('loadingState');

    // Função para verificar se pode enviar
    function checkSubmit() {
        const hasText = textInput.value.trim().length > 0;
        const hasFile = fileInput.files.length > 0;
        
        // Habilita o botão se tiver um OU outro
        if (hasText || hasFile) {
            submitBtn.removeAttribute('disabled');
            submitBtn.classList.add('active');
        } else {
            submitBtn.setAttribute('disabled', 'true');
            submitBtn.classList.remove('active');
        }
    }

    // Lógica de Exclusão Mútua (Se digitar, trava arquivo. Se anexar, trava texto)
    if (textInput) {
        textInput.addEventListener('input', function() {
            if (this.value.length > 0) {
                fileInput.disabled = true;
                groupFile.classList.add('disabled-area');
            } else {
                fileInput.disabled = false;
                groupFile.classList.remove('disabled-area');
            }
            checkSubmit();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                textInput.disabled = true;
                textInput.placeholder = "Arquivo selecionado. Remova o arquivo para digitar.";
                groupText.classList.add('disabled-area');
            } else {
                textInput.disabled = false;
                textInput.placeholder = "Cole o corpo do e-mail aqui...";
                groupText.classList.remove('disabled-area');
            }
            checkSubmit();
        });
    }

    // Botão Limpar
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            textInput.value = '';
            fileInput.value = '';
            textInput.disabled = false;
            fileInput.disabled = false;
            groupText.classList.remove('disabled-area');
            groupFile.classList.remove('disabled-area');
            textInput.placeholder = "Cole o corpo do e-mail aqui...";
            checkSubmit();
        });
    }

    // Feedback de Loading ao enviar
    if (form) {
        form.addEventListener('submit', function() {
            loadingDiv.classList.remove('hidden');
            submitBtn.classList.add('hidden'); // Esconde o botão para evitar duplo clique
        });
    }
});

// Função global para ser chamada pelo onclick do HTML
function copiarTexto() {
    const responseBox = document.querySelector('.response-box');
    if (responseBox) {
        const texto = responseBox.innerText;
        navigator.clipboard.writeText(texto);
        alert('Resposta copiada para a área de transferência!');
    }
}