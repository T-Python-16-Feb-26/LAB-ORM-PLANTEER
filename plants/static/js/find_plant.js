function fillPlantMessage(text) {
    const input = document.querySelector('.plant-chat-form input[name="message"]');
    if (input) {
        input.value = text;
        input.focus();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const chatBody = document.getElementById("plantChatBody");
    if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight;
    }
});