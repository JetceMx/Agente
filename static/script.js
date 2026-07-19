const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    if (typeof content === 'string') {
        messageContent.innerHTML = formatText(content);
    } else {
        messageContent.innerHTML = content;
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatText(text) {
    text = text.replace(/\n\n/g, '</p><p>');
    text = text.replace(/\n/g, '<br>');
    text = text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    return `<p>${text}</p>`;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const indicator = document.createElement('div');
    indicator.className = 'message-content';
    indicator.innerHTML = `
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    typingDiv.appendChild(avatar);
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

async function askQuestion(question) {
    sendBtn.disabled = true;
    questionInput.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        removeTypingIndicator();

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al procesar la pregunta');
        }

        const data = await response.json();
        let answerHtml = formatText(data.answer);

        if (data.sources && data.sources.length > 0) {
            answerHtml += `
                <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0;">
                    <small style="color: #94a3b8;">📚 Fuentes consultadas: ${data.sources.length} fragmento(s) del documento</small>
                </div>
            `;
        }

        addMessage(answerHtml, false);
    } catch (error) {
        removeTypingIndicator();
        addMessage(`Lo siento, hubo un error: ${error.message}. Por favor, intenta de nuevo.`, false);
    } finally {
        sendBtn.disabled = false;
        questionInput.disabled = false;
        questionInput.focus();
    }
}

async function resetConversation() {
    try {
        await fetch('/api/reset', { method: 'POST' });
        chatMessages.innerHTML = '';

        addMessage(`
            ¡Hola! Soy tu asistente de Calculo Diferencial. Puedo responder preguntas sobre el Capítulo 1: Precision, Error y Aproximaciones.
            <p class="examples">Ejemplos de preguntas que puedes hacer:</p>
            <ul>
                <li>"¿Qué es el error absoluto?"</li>
                <li>"¿Cómo se calcula el error relativo?"</li>
                <li>"Explica la propagación de errores"</li>
                <li>"¿Qué diferencia hay entre precisión y exactitud?"</li>
            </ul>
        `, false);
    } catch (error) {
        console.error('Error resetting conversation:', error);
    }
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    addMessage(question, true);
    questionInput.value = '';
    questionInput.style.height = 'auto';

    await askQuestion(question);
});

questionInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

questionInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

resetBtn.addEventListener('click', resetConversation);

questionInput.focus();
