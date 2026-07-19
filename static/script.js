const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const resetBtn = document.getElementById("resetBtn");
const documentList = document.getElementById("documentList");
const documentCount = document.getElementById("documentCount");
const indexStatus = document.getElementById("indexStatus");
const systemState = document.getElementById("systemState");
const welcomeMarkup = chatMessages.innerHTML;

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function formatText(value) {
    const codeBlocks = [];
    let text = escapeHtml(value).replace(/```([\s\S]*?)```/g, (_, code) => {
        const token = `%%MARVIN_CODE_${codeBlocks.length}%%`;
        codeBlocks.push(`<pre><code>${code.trim()}</code></pre>`);
        return token;
    });

    text = text
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n\n/g, "</p><p>")
        .replace(/\n/g, "<br>");

    codeBlocks.forEach((block, index) => {
        text = text.replace(`%%MARVIN_CODE_${index}%%`, block);
    });
    return `<p>${text}</p>`;
}

function nowLabel() {
    return new Intl.DateTimeFormat("es-MX", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
    }).format(new Date());
}

function setSystemState(mode, label) {
    systemState.classList.remove("processing", "error");
    if (mode) {
        systemState.classList.add(mode);
    }
    systemState.lastElementChild.textContent = label;
}

function createSources(sources) {
    if (!Array.isArray(sources) || sources.length === 0) {
        return null;
    }

    const strip = document.createElement("div");
    strip.className = "source-strip";

    const label = document.createElement("span");
    label.className = "source-label";
    label.textContent = "INTEL RECUPERADA";
    strip.appendChild(label);

    sources.forEach((source) => {
        const chip = document.createElement("span");
        chip.className = "source-chip";
        const file = source.metadata?.source || "Documento";
        const page = source.metadata?.page;
        chip.textContent = page ? `${file} // P.${page}` : file;
        chip.title = source.content || file;
        strip.appendChild(chip);
    });

    return strip;
}

function addMessage(content, isUser = false, sources = []) {
    const article = document.createElement("article");
    article.className = `message ${isUser ? "user-message" : "bot-message"}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.innerHTML = `<span>${isUser ? "P" : "M"}</span>`;

    const body = document.createElement("div");
    body.className = "message-body";

    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.innerHTML = `
        <span>${isUser ? "PILOTO" : "M.A.R.V.I.N."}</span>
        <time>${nowLabel()}</time>
    `;

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";
    messageContent.innerHTML = formatText(content);

    const sourceStrip = createSources(sources);
    body.appendChild(meta);
    body.appendChild(messageContent);
    if (sourceStrip) {
        body.appendChild(sourceStrip);
    }

    article.appendChild(avatar);
    article.appendChild(body);
    chatMessages.appendChild(article);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const article = document.createElement("article");
    article.className = "message bot-message";
    article.id = "typingIndicator";
    article.innerHTML = `
        <div class="message-avatar" aria-hidden="true"><span>M</span></div>
        <div class="message-body">
            <div class="message-meta">
                <span>M.A.R.V.I.N.</span>
                <time>RASTREANDO ARCHIVOS</time>
            </div>
            <div class="message-content typing-content">
                <div class="typing-indicator" aria-label="Procesando consulta">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(article);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    document.getElementById("typingIndicator")?.remove();
}

function formatBytes(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) {
        return "0 KB";
    }
    const units = ["B", "KB", "MB", "GB"];
    const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), 3);
    return `${(bytes / 1024 ** index).toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}

async function loadCatalog() {
    try {
        const response = await fetch("/api/documents");
        if (!response.ok) {
            throw new Error("No fue posible leer la biblioteca");
        }
        const data = await response.json();
        documentCount.textContent = String(data.count).padStart(2, "0");
        indexStatus.textContent = data.indexed ? "INDEXADO" : "LISTO";
        indexStatus.classList.toggle("ready", data.count > 0);

        if (!data.documents.length) {
            documentList.innerHTML = `
                <div class="document-empty">Añade archivos PDF a la biblioteca</div>
            `;
            return;
        }

        documentList.innerHTML = "";
        data.documents.forEach((file, index) => {
            const item = document.createElement("div");
            item.className = "document-item";
            item.innerHTML = `
                <span class="document-index">${String(index + 1).padStart(2, "0")}</span>
                <div>
                    <div class="document-name" title="${escapeHtml(file.name)}">
                        ${escapeHtml(file.name)}
                    </div>
                    <span class="document-size">${formatBytes(file.size)}</span>
                </div>
            `;
            documentList.appendChild(item);
        });
    } catch (error) {
        documentCount.textContent = "ERR";
        indexStatus.textContent = "OFFLINE";
        indexStatus.classList.remove("ready");
        documentList.innerHTML = `
            <div class="document-empty">${escapeHtml(error.message)}</div>
        `;
    }
}

async function askQuestion(question) {
    sendBtn.disabled = true;
    questionInput.disabled = true;
    setSystemState("processing", "RECUPERANDO INTEL");
    showTypingIndicator();

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Error al procesar la consulta");
        }

        addMessage(data.answer, false, data.sources);
        indexStatus.textContent = "INDEXADO";
        indexStatus.classList.add("ready");
        setSystemState("", "ENLACE ESTABLE");
    } catch (error) {
        addMessage(
            `Protocolo interrumpido: ${error.message} Intenta nuevamente.`,
            false,
        );
        setSystemState("error", "ENLACE INESTABLE");
    } finally {
        removeTypingIndicator();
        sendBtn.disabled = false;
        questionInput.disabled = false;
        questionInput.focus();
    }
}

async function submitQuestion(question) {
    const normalized = question.trim();
    if (!normalized || sendBtn.disabled) {
        return;
    }
    addMessage(normalized, true);
    questionInput.value = "";
    questionInput.style.height = "auto";
    await askQuestion(normalized);
}

async function resetConversation() {
    resetBtn.disabled = true;
    try {
        const response = await fetch("/api/reset", { method: "POST" });
        if (!response.ok) {
            throw new Error("No se pudo reiniciar la sesión");
        }
        chatMessages.innerHTML = welcomeMarkup;
        setSystemState("", "ENLACE ESTABLE");
    } catch (error) {
        setSystemState("error", "RESET FALLIDO");
    } finally {
        resetBtn.disabled = false;
        questionInput.focus();
    }
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await submitQuestion(questionInput.value);
});

questionInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = `${Math.min(this.scrollHeight, 132)}px`;
});

questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});

chatMessages.addEventListener("click", async (event) => {
    const prompt = event.target.closest("[data-question]");
    if (prompt) {
        await submitQuestion(prompt.dataset.question);
    }
});

resetBtn.addEventListener("click", resetConversation);

loadCatalog();
questionInput.focus();
