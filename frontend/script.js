document.addEventListener('DOMContentLoaded', function() {
    
    const textInput = document.getElementById('email_text');
    const charCounter = document.getElementById('char-counter');
    const MAX_CHARS = 15000;
    const fileInput = document.getElementById('email_file');
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const groupText = document.getElementById('group-text');
    const groupFile = document.getElementById('group-file');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const form = document.getElementById('analysisForm');
    const loadingDiv = document.getElementById('loadingState');


    if (textInput && charCounter) {
        textInput.addEventListener('input', function() {
            const count = this.value.length;
            charCounter.textContent = `${count} / ${MAX_CHARS}`;
            
            // Adiciona aviso visual perto do limite
            if (count > MAX_CHARS * 0.9) {
                charCounter.classList.add('limit-warning');
            } else {
                charCounter.classList.remove('limit-warning');
            }
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileNameDisplay = document.getElementById('file-name-display');
            
            if (this.files.length > 0) {
                const file = this.files[0];
                const nomeArquivo = file.name;

                // 1. VERIFICA O TAMANHO
                if (file.size > MAX_FILE_SIZE) {
                    alert(`Arquivo muito grande!\n\nO arquivo "${nomeArquivo}" tem ${(file.size / 1024 / 1024).toFixed(1)}MB.\nO limite é 10MB.`);
                    
                    // Limpa o input
                    this.value = ''; 
                    fileNameDisplay.textContent = "Clique para selecionar arquivo";
                    fileNameDisplay.classList.remove('file-selected');
                    checkSubmit(); // Re-checa o botão (vai desabilitar)
                    return; // Para a execução
                }

                // 2. Se o tamanho for OK, continua
                fileNameDisplay.textContent = nomeArquivo;
                fileNameDisplay.classList.add('file-selected');

                textInput.disabled = true;
                textInput.placeholder = "Arquivo selecionado...";
                if (groupText) groupText.classList.add('disabled-area');

            } else {

            }
            checkSubmit();
        });
    }

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
            // Seleciona o elemento de texto que criamos no HTML
            const fileNameDisplay = document.getElementById('file-name-display');

            if (this.files.length > 0) {
                // ATUALIZAÇÃO: Exibe o nome do arquivo ao lado do botão
                fileNameDisplay.textContent = this.files[0].name;

                textInput.disabled = true;
                textInput.placeholder = "Arquivo selecionado. Remova o arquivo para digitar.";
                groupText.classList.add('disabled-area');
            } else {
                // Se o usuário cancelar a seleção, limpa o texto
                fileNameDisplay.textContent = '';

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
            
            // ATUALIZAÇÃO: Limpa o nome do arquivo visualmente
            const fileNameDisplay = document.getElementById('file-name-display');
            if (fileNameDisplay) fileNameDisplay.textContent = '';

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
    }
}