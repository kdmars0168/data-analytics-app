let timeoutId;

document.addEventListener("DOMContentLoaded", function () {
    const messageBox = document.getElementById('personalized-message');
    if (!messageBox) return;

    messageBox.addEventListener('input', function () {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            const message = messageBox.value;

            fetch("/save_message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('meta[name=csrf-token]').content
                },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Message saved:", data);
            });
        }, 1000);
    });
});
