async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const userText = input.value.trim();
    if (!userText) return;

    chatBox.innerHTML += `<div><strong>You:</strong> ${userText}</div>`;
    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userText })
    });

    const data = await response.json();
    chatBox.innerHTML += `<div><strong>AI:</strong> ${data.response}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
