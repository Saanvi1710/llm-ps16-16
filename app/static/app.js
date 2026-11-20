const conversationId = crypto.randomUUID();
const form = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message");
const figureInput = document.querySelector("#figure");
const messages = document.querySelector("#messages");
const error = document.querySelector("#error");
const button = form.querySelector("button");

function appendMessage(role, text) {
  const item = document.createElement("article");
  item.className = `message ${role}`;
  const label = role === "assistant" ? "AI role-play" : "You";
  item.innerHTML = `<span>${label}</span><p></p>`;
  item.querySelector("p").textContent = text;
  messages.append(item);
  messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  error.textContent = "";
  appendMessage("user", message);
  messageInput.value = "";
  button.disabled = true;
  button.textContent = "Thinking...";

  try {
    const response = await fetch("/api/v1/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ figure: figureInput.value, message, conversation_id: conversationId }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Unable to get a response.");
    appendMessage("assistant", data.reply);
  } catch (requestError) {
    error.textContent = requestError.message;
  } finally {
    button.disabled = false;
    button.textContent = "Send";
    messageInput.focus();
  }
});
