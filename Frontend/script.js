document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") sendMessage();
    });

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;


        append_message("user", message);
        userInput.value = "";

        try {
            // enviar mensaje a la API
            const response = await fetch("http://localhost:8000/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: message, language: "en" })
            });

            const data = await response.json();
            append_message("bot", data.response.content);
        } catch (error) {
            console.error("error", error);
            //TODO: rewrite error message
            append_message("bot", "error.");
        }
    }

    function append_message(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; 
    }
});


// TODO: add translate behavior