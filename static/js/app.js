/* ============================================================
   TravelBot — Frontend JavaScript
   Handles chat UI, API calls, and markdown rendering
   ============================================================ */

const API_BASE = "";  // Same origin

// DOM References
const messagesEl = document.getElementById("messages");
const userInputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");
const resetBtn = document.getElementById("resetBtn");
const quickPromptsEl = document.getElementById("quickPrompts");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const planTripBtn = document.getElementById("planTripBtn");

// ---- INITIALISATION ----
window.addEventListener("DOMContentLoaded", async () => {
  await checkHealth();
  await loadQuickPrompts();
  addWelcomeMessage();
  autoResizeTextarea();
});

// ---- HEALTH CHECK ----
async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    const data = await res.json();
    const dot = statusDot.querySelector(".dot");
    if (data.status === "ok") {
      dot.className = "dot dot--ok";
      statusText.textContent = data.ibm_configured
        ? `IBM Granite Connected`
        : `Demo Mode (add credentials)`;
    }
  } catch {
    const dot = statusDot.querySelector(".dot");
    dot.className = "dot dot--error";
    statusText.textContent = "Disconnected";
  }
}

// ---- QUICK PROMPTS ----
async function loadQuickPrompts() {
  try {
    const res = await fetch(`${API_BASE}/api/quick-prompts`);
    const data = await res.json();
    quickPromptsEl.innerHTML = "";
    data.prompts.forEach(prompt => {
      const btn = document.createElement("button");
      btn.className = "quick-prompt-btn";
      btn.textContent = prompt.label;
      btn.title = prompt.text;
      btn.addEventListener("click", () => {
        userInputEl.value = prompt.text;
        userInputEl.focus();
        sendMessage();
      });
      quickPromptsEl.appendChild(btn);
    });
  } catch {
    quickPromptsEl.innerHTML = "<span style='color:var(--muted);font-size:12px'>Could not load prompts</span>";
  }
}

// ---- WELCOME MESSAGE ----
function addWelcomeMessage() {
  const welcome = `👋 **Welcome to TravelBot!**

I'm your AI Travel Planner powered by **IBM Granite** (IBM watsonx.ai).

Here's what I can do for you:

✈️ **Suggest Destinations** — based on your interests & budget
🗺️ **Build Itineraries** — detailed day-by-day travel plans
🌤️ **Check Weather** — real-time forecasts & packing tips
🚆 **Plan Transport** — flights, trains, buses compared
🏨 **Find Accommodation** — from hostels to luxury resorts
📋 **Manage Bookings** — confirm & track your trips

---
Try asking: *"Suggest beach destinations under $50/day"* or use the **Quick Prompts** on the left to get started!`;

  addMessage("bot", welcome);
}

// ---- SEND MESSAGE ----
async function sendMessage() {
  const text = userInputEl.value.trim();
  if (!text) return;

  addMessage("user", text);
  userInputEl.value = "";
  resizeTextarea();
  sendBtn.disabled = true;
  showTyping(true);

  let attempt = 0;
  const maxRetries = 3;
  const retryDelays = [3000, 6000, 12000];

  while (attempt <= maxRetries) {
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();

      if (res.status === 429 || (data.error && data.error.includes("429"))) {
        // IBM rate limit — show retry message and wait
        document.querySelector(".typing-text").textContent =
          `IBM rate limit hit — retrying in ${retryDelays[attempt]/1000}s… (attempt ${attempt+1}/${maxRetries})`;
        await new Promise(r => setTimeout(r, retryDelays[attempt]));
        attempt++;
        continue;
      }

      if (data.response) {
        addMessage("bot", data.response);
      } else if (data.error) {
        if (data.error.includes("rate limit") || data.error.includes("429") || data.error.includes("consumption_limit")) {
          addMessage("bot",
            "⏳ **IBM Granite is busy right now** (free tier concurrent limit reached).\n\n" +
            "This is a limitation of the IBM Cloud Lite free plan — it allows only a limited number of simultaneous requests.\n\n" +
            "✅ **Just wait 10–15 seconds and send your message again** — it will work!"
          );
        } else {
          addMessage("bot", `⚠️ **Error:** ${data.error}`);
        }
      }
      break;
    } catch (err) {
      if (attempt < maxRetries) {
        await new Promise(r => setTimeout(r, retryDelays[attempt]));
        attempt++;
      } else {
        addMessage("bot", `⚠️ **Connection Error:** Could not reach the server.\n\`\`\`\n${err.message}\n\`\`\``);
        break;
      }
    }
  }

  document.querySelector(".typing-text").textContent = "TravelBot is thinking…";
  showTyping(false);
  sendBtn.disabled = false;
}

// ---- ADD MESSAGE TO CHAT ----
function addMessage(role, content) {
  const wrapper = document.createElement("div");
  wrapper.className = `message message--${role}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "bot" ? "🤖" : "👤";

  const inner = document.createElement("div");

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.innerHTML = renderMarkdown(content);

  const time = document.createElement("div");
  time.className = "message-time";
  time.textContent = formatTime(new Date());

  inner.appendChild(bubble);
  inner.appendChild(time);

  wrapper.appendChild(avatar);
  wrapper.appendChild(inner);
  messagesEl.appendChild(wrapper);
  scrollToBottom();
}

// ---- MARKDOWN-LIKE RENDERER ----
function renderMarkdown(text) {
  return text
    // Escape HTML first
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    // Code blocks
    .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
    // Inline code
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    // Bold
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    // Italic
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    // Horizontal rule
    .replace(/^---$/gm, "<hr/>")
    // Headers (## and ###)
    .replace(/^### (.+)$/gm, "<h4 style='color:var(--accent-light);margin:10px 0 4px'>$1</h4>")
    .replace(/^## (.+)$/gm, "<h3 style='color:var(--accent-light);margin:12px 0 6px'>$1</h3>")
    // Line breaks
    .replace(/\n/g, "<br/>");
}

// ---- UTILITIES ----
function showTyping(show) {
  typingIndicator.style.display = show ? "flex" : "none";
  if (show) scrollToBottom();
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  });
}

function formatTime(date) {
  return date.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
}

function autoResizeTextarea() {
  userInputEl.addEventListener("input", resizeTextarea);
}

function resizeTextarea() {
  userInputEl.style.height = "auto";
  userInputEl.style.height = Math.min(userInputEl.scrollHeight, 140) + "px";
}

// ---- PLAN TRIP BUTTON ----
planTripBtn.addEventListener("click", () => {
  const destination = document.getElementById("tripDestination").value.trim();
  const duration = document.getElementById("tripDuration").value;
  const budget = document.getElementById("tripBudget").value;
  const interest = document.getElementById("tripInterest").value;

  let parts = [];
  if (destination) parts.push(`to ${destination}`);
  if (duration) parts.push(`for ${duration} days`);
  if (budget) {
    const budgetLabels = { low: "on a budget", medium: "mid-range budget", high: "with a luxury budget" };
    parts.push(budgetLabels[budget] || "");
  }
  if (interest) {
    const interestLabels = { beach: "beach", cultural: "cultural", adventure: "adventure", city: "city", nature: "nature" };
    parts.push(`focused on ${interestLabels[interest] || interest} activities`);
  }

  if (!parts.length) {
    userInputEl.value = "Suggest some great travel destinations for me";
  } else if (destination) {
    userInputEl.value = `Plan a complete trip ${parts.join(", ")}`;
  } else {
    userInputEl.value = `Suggest travel destinations ${parts.join(", ")}`;
  }

  sendMessage();
});

// ---- RESET ----
resetBtn.addEventListener("click", async () => {
  try {
    await fetch(`${API_BASE}/api/reset`, { method: "POST" });
  } catch { /* ignore */ }
  messagesEl.innerHTML = "";
  addWelcomeMessage();
});

// ---- KEYBOARD SHORTCUTS ----
userInputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

sendBtn.addEventListener("click", sendMessage);
