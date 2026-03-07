// ----------------------------------------------
// Grab DOM elements
// ----------------------------------------------
const messagesDiv = document.getElementById("messages");
const userInput   = document.getElementById("userInput");
const toneSelect  = document.getElementById("tone");
const sendBtn     = document.getElementById("sendBtn");
const loadingDiv  = document.getElementById("loading");
const errorDiv    = document.getElementById("error");

// Debug sanity log: comment out in production
console.log({ messagesDiv, userInput, toneSelect, sendBtn, loadingDiv, errorDiv });

// Maintain session across messages (in-memory for this tab)
let sessionId = null;

// ----------------------------------------------
// Helper: Append a message bubble to chat window
// ----------------------------------------------
function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = role === "user" ? "msg-user" : "msg-ai";
  div.textContent = text;
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ----------------------------------------------
// Main: Send user message to backend → show reply
// ----------------------------------------------
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  // Reset error banner
  if (errorDiv) errorDiv.classList.add("hidden");

  // Show user's message
  addMessage("user", text);

  // UI loading state
  if (loadingDiv) loadingDiv.classList.remove("hidden");
  sendBtn.disabled = true;

  // IMPORTANT: backend expects snake_case; we use camelCase variable
  const payload = {
    session_id: sessionId,           // send current session id (or null)
    tone: toneSelect.value,
    message: text
  };

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    // Parse body
    const data = await response.json();

    // Check HTTP status
    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}`);
    }

    // Show AI reply
    addMessage("ai", data.reply);

    // Save session id for follow-ups (backend returns camelCase)
    sessionId = data.sessionId;

    // Clear input for next message
    userInput.value = "";

  } catch (err) {
    console.error("Frontend error:", err);
    if (errorDiv) {
      errorDiv.textContent = err.message || "Something went wrong.";
      errorDiv.classList.remove("hidden");
    }
  } finally {
    // Reset UI loading state
    if (loadingDiv) loadingDiv.classList.add("hidden");
    sendBtn.disabled = false;
  }
}

// Click handler
sendBtn.addEventListener("click", sendMessage);

// Ctrl+Enter to send (nice UX)
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.ctrlKey) {
    sendMessage();
  }
});