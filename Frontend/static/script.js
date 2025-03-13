document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const languageBtn = document.getElementById("language-btn");
    const overlayText = document.getElementById("overlay-text");

    let currentLanguage = "en";

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") sendMessage();
    });

    languageBtn.addEventListener("click", toggleLanguage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;


        append_message("user", message);
        userInput.value = "";

        try {
            const response = await fetch("http://localhost:8000/chat/invoke", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    input: { question: message } 
                })
            });

            const data = await response.json();
            const botResponse = data.output || "I'm sorry, but I couldn't generate a response.";
            append_message("bot", botResponse);
        } catch (error) {
            console.error("Error fetching response:", error);
            append_message("bot", "An error occurred while processing your request. Please try again.");
        }
    }

    function append_message(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; 
    }

    function toggleLanguage() {
        currentLanguage = currentLanguage === "en" ? "es" : "en"; 
        updateUIText();
    }

    function updateUIText() {
        userInput.placeholder = translations[currentLanguage].placeholder;
        sendBtn.textContent = translations[currentLanguage].send_button;
        languageBtn.querySelector(".text").textContent = translations[currentLanguage].language_button;
        overlayText.innerHTML = translations[currentLanguage].overlay_text;
    }

    const translations = {
        "en": {
            "placeholder": "Write your message...",
            "send_button": "Send",
            "language_button": "English",
            "overlay_text": "Building Human-AI Collaboration <br> Any doubts? Ask us"
        },
        "es": {
            "placeholder": "Escribe tu mensaje...",
            "send_button": "Enviar",
            "language_button": "Español",
            "overlay_text": "Construyendo un puente entre los Humanos y la IA <br> ¿Alguna duda? Pregúntanos"
        }
    };
});