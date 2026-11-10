"""
TravelBot — AI Travel Planner Agent
Streamlit UI  |  IBM Granite (watsonx.ai)  |  AICTE Problem Statement #5
"""

import os
import sys
import time
import datetime
import streamlit as st
from dotenv import load_dotenv

# Ensure the aicte directory is on the path so agent/tools are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from agent import TravelPlannerAgent  # noqa: E402

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be the first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TravelBot — AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── global ── */
[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] { background: #1a1d27; border-right: 1px solid #2d3148; }
[data-testid="stSidebar"] * { color: #e8eaf6 !important; }
h1,h2,h3,h4 { color: #e8eaf6 !important; }

/* ── chat messages ── */
.chat-user {
    background: #1a3a6e; border-radius: 12px 12px 4px 12px;
    padding: 12px 16px; margin: 6px 0 6px 60px;
    color: #e8eaf6; font-size: 14px; line-height: 1.6;
}
.chat-bot {
    background: #1e2238; border: 1px solid #2d3148;
    border-radius: 4px 12px 12px 12px;
    padding: 12px 16px; margin: 6px 60px 6px 0;
    color: #e8eaf6; font-size: 14px; line-height: 1.6;
}
.chat-meta { font-size: 11px; color: #8b95b8; margin-bottom: 2px; }

/* ── IBM badge ── */
.ibm-badge {
    background: #23273a; border: 1px solid #2d3148;
    border-radius: 10px; padding: 10px 12px;
    font-size: 12px; color: #8b95b8; margin-top: 16px;
    text-align: center;
}
.ibm-badge strong { color: #7b9fff; display: block; font-size: 13px; }

/* ── status pill ── */
.status-ok   { color: #22c55e; font-weight: 600; }
.status-demo { color: #f59e0b; font-weight: 600; }
.status-err  { color: #ef4444; font-weight: 600; }

/* ── quick-prompt buttons ── */
div[data-testid="stButton"] button {
    background: #23273a; border: 1px solid #2d3148;
    color: #c9d1f0; border-radius: 8px;
    font-size: 12px; width: 100%; text-align: left;
    padding: 7px 10px; margin-bottom: 4px;
    transition: border-color .15s;
}
div[data-testid="stButton"] button:hover {
    border-color: #4f7cff; color: #7b9fff;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = TravelPlannerAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []          # list of {"role": "user"|"bot", "content": str, "time": str}

if "thinking" not in st.session_state:
    st.session_state.thinking = False


def _now() -> str:
    return datetime.datetime.now().strftime("%I:%M %p")


def _ibm_status() -> tuple[str, str]:
    """Return (label, css_class) for the IBM connection status badge."""
    agent: TravelPlannerAgent = st.session_state.agent
    if agent.llm.is_configured():
        return "● IBM Granite Connected", "status-ok"
    return "● Demo Mode — add IBM credentials", "status-demo"


# ─────────────────────────────────────────────
#  SEND MESSAGE HANDLER
# ─────────────────────────────────────────────
def send_message(text: str):
    text = text.strip()
    if not text:
        return
    st.session_state.messages.append({"role": "user", "content": text, "time": _now()})

    max_retries = 4
    retry_delays = [3, 6, 12, 20]
    last_err = None

    for attempt in range(max_retries):
        spinner_msg = (
            "TravelBot is thinking…"
            if attempt == 0
            else f"IBM rate limit — retrying… (attempt {attempt + 1}/{max_retries})"
        )
        with st.spinner(spinner_msg):
            try:
                reply = st.session_state.agent.chat(text)
                st.session_state.messages.append({"role": "bot", "content": reply, "time": _now()})
                return
            except Exception as e:
                last_err = str(e)
                if "429" in last_err or "consumption_limit" in last_err:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delays[attempt])
                        continue
                else:
                    # Non-rate-limit error — surface it directly
                    break

    # All retries done or non-429 error
    if last_err and ("429" in last_err or "consumption_limit" in last_err):
        friendly = (
            "⏳ **IBM Granite is busy** (free tier rate limit reached).\n\n"
            "The IBM Cloud Lite plan limits simultaneous requests across all users.\n\n"
            "✅ **Wait 15–20 seconds then send your message again** — it will work!"
        )
    else:
        friendly = (
            f"⚠️ **IBM Granite error:**\n\n{last_err}\n\n"
            "The travel tools are still working — try asking about destinations, "
            "weather, or hotels."
        )
    st.session_state.messages.append({"role": "bot", "content": friendly, "time": _now()})


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ TravelBot")
    st.markdown("*AI Travel Planner · IBM Granite*")

    # Status
    label, css = _ibm_status()
    st.markdown(f'<p class="{css}">{label}</p>', unsafe_allow_html=True)
    st.divider()

    # ── Trip Planner Form ──────────────────────
    st.markdown("### 🗺️ Plan a Trip")
    destination_input = st.text_input("Destination", placeholder="e.g. Goa, Bali, Paris", key="form_dest")
    duration_input = st.number_input("Duration (days)", min_value=1, max_value=30, value=7, key="form_days")
    budget_input = st.selectbox(
        "Budget",
        ["", "🎒 Budget / Backpacker", "💼 Mid-Range", "💎 Luxury"],
        key="form_budget",
    )
    interest_input = st.selectbox(
        "Interest",
        ["", "🏖️ Beach", "🏛️ Cultural", "🏔️ Adventure", "🏙️ City", "🌿 Nature"],
        key="form_interest",
    )

    if st.button("🗺️ Plan My Trip", use_container_width=True, key="plan_btn"):
        budget_map = {
            "🎒 Budget / Backpacker": "budget",
            "💼 Mid-Range": "mid-range",
            "💎 Luxury": "luxury",
        }
        interest_map = {
            "🏖️ Beach": "beach", "🏛️ Cultural": "cultural",
            "🏔️ Adventure": "adventure", "🏙️ City": "city", "🌿 Nature": "nature",
        }
        parts = []
        if destination_input:
            parts.append(f"to {destination_input}")
        parts.append(f"for {duration_input} days")
        if budget_input:
            parts.append(f"on a {budget_map.get(budget_input, 'medium')} budget")
        if interest_input:
            parts.append(f"with {interest_map.get(interest_input, '')} activities")

        if destination_input:
            query = f"Plan a complete trip {' '.join(parts)}"
        else:
            query = f"Suggest travel destinations {' '.join(parts)}"
        send_message(query)
        st.rerun()

    st.divider()

    # ── Quick Prompts ──────────────────────────
    st.markdown("### ⚡ Quick Prompts")
    quick_prompts = [
        ("🏖️ Beach Destinations", "Suggest budget-friendly beach destinations for 7 days"),
        ("🏔️ Adventure Trip", "Plan an adventure trip to Manali for 5 days"),
        ("🏛️ Cultural Tour", "Best cultural destinations in India for 2 people"),
        ("🌤️ Weather in Goa", "What is the weather like in Goa right now?"),
        ("🚆 How to reach Goa", "Transport options to reach Goa from Mumbai"),
        ("🏨 Hotels in Bali", "Recommend mid-range hotels in Bali for 6 nights"),
        ("🗺️ Bali Itinerary", "Create a 7-day itinerary for Bali for a couple"),
        ("📋 Book a Trip", "Book a trip to Rajasthan for 2 people"),
    ]
    for label, prompt_text in quick_prompts:
        if st.button(label, key=f"qp_{label}", use_container_width=True):
            send_message(prompt_text)
            st.rerun()

    st.divider()

    # ── Reset ──────────────────────────────────
    if st.button("🔄 New Conversation", use_container_width=True, key="reset_btn"):
        st.session_state.agent.reset_conversation()
        st.session_state.messages = []
        st.rerun()

    # ── IBM Badge ─────────────────────────────
    st.markdown("""
    <div class="ibm-badge">
        🤖 <strong>IBM Granite</strong>
        granite-13b-chat-v2<br/>
        <small>via IBM watsonx.ai (Cloud Lite)</small>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN CHAT AREA
# ─────────────────────────────────────────────
st.markdown("# ✈️ TravelBot — AI Travel Planner")
st.caption("Powered by **IBM Granite** · IBM watsonx.ai · AICTE Problem Statement #5")
st.divider()

# ── Welcome message on first load ─────────────
if not st.session_state.messages:
    st.markdown("""
> 👋 **Welcome to TravelBot!**
>
> I'm your AI Travel Planner powered by **IBM Granite** (IBM watsonx.ai).
>
> I can help you:
> - ✈️ **Suggest destinations** based on interests & budget
> - 🗺️ **Build itineraries** — day-by-day travel plans
> - 🌤️ **Check weather** — forecasts & packing tips
> - 🚆 **Plan transport** — flights, trains, buses
> - 🏨 **Find accommodation** — hostels to luxury resorts
> - 📋 **Manage bookings** — confirm & track trips
>
> Use the **sidebar** to plan a trip or try a **Quick Prompt** to get started!
    """)

# ── Render conversation history ───────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<p class="chat-meta">👤 You · {msg["time"]}</p>'
            f'<div class="chat-user">{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<p class="chat-meta">🤖 TravelBot · {msg["time"]}</p>'
            f'<div class="chat-bot">{msg["content"]}</div>',
            unsafe_allow_html=True,
        )

# ── Chat input (pinned at bottom by Streamlit) ─
user_input = st.chat_input("Ask me anything about your trip… e.g. 'Plan a 5-day beach vacation under $50/day'")
if user_input:
    send_message(user_input)
    st.rerun()
