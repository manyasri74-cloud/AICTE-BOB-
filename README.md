# 🌍 TravelBot — AI Travel Planner Agent
### Built with IBM Granite (watsonx.ai) | AICTE Problem Statement #5

---

## 📌 Project Overview

**TravelBot** is an intelligent, AI-powered Travel Planner Agent that helps users plan trips efficiently and effortlessly. It leverages **IBM Granite LLM via IBM watsonx.ai** (IBM Cloud Lite) for natural language understanding and uses modular tools to deliver personalized travel planning.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 🌍 **Destination Discovery** | Suggests destinations based on interests, budget, and duration |
| 🗺️ **Itinerary Builder** | Creates detailed day-by-day travel plans |
| 🌤️ **Weather & Packing** | Real-time weather + smart packing tips |
| 🚆 **Transport Planner** | Compares flights, trains, buses with booking links |
| 🏨 **Accommodation Finder** | Budget to luxury hotel recommendations |
| 📋 **Booking Manager** | Creates and tracks travel bookings with alerts |
| 🤖 **IBM Granite AI** | Natural conversation powered by IBM Granite LLM |

---

## 🏗️ Architecture

```
AICTE Travel Agent/
├── aicte/
│   ├── app.py              ← Flask web server + API routes
│   ├── agent.py            ← Core Travel Planner Agent (IBM Granite)
│   ├── ibm_client.py       ← IBM watsonx.ai + Weather API clients
│   ├── run.py              ← Quick setup & launch script
│   ├── requirements.txt    ← Python dependencies
│   ├── .env.example        ← Environment variables template
│   │
│   ├── tools/              ← Modular travel tools
│   │   ├── destinations.py ← Destination discovery & filtering
│   │   ├── itinerary.py    ← Day-by-day itinerary builder
│   │   ├── weather.py      ← Weather info & packing tips
│   │   ├── transport.py    ← Transport recommendations
│   │   ├── accommodation.py← Hotel & stay recommendations
│   │   └── bookings.py     ← Booking management
│   │
│   ├── templates/
│   │   └── index.html      ← Chat UI frontend
│   └── static/
│       ├── css/style.css   ← Dark theme UI styles
│       └── js/app.js       ← Frontend chat logic
```

---

## 🚀 Quick Start

### Step 1: Get IBM Cloud Credentials (Free)

1. Sign up at [IBM Cloud](https://cloud.ibm.com/registration) — **free Lite account**
2. Go to [IBM Cloud IAM](https://cloud.ibm.com/iam/apikeys) → Create an API Key
3. Go to [IBM watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home) → Create a Project → Copy the **Project ID**

### Step 2: Configure `.env`

```bash
# Copy the example file
cp .env.example .env

# Edit and add your credentials
WATSONX_API_KEY=your_actual_api_key_here
WATSONX_PROJECT_ID=your_actual_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
```

### Step 3: Install & Run

```bash
cd aicte
pip install -r requirements.txt

# ▶ Streamlit (recommended)
streamlit run streamlit_app.py

# ▶ Flask (alternative REST + HTML UI)
python app.py
```

### Step 4: Open in Browser

| Interface | URL |
|---|---|
| **Streamlit** (recommended) | `http://localhost:8501` |
| Flask | `http://localhost:5000` |

---

## 🤖 IBM Technologies Used

| Technology | Purpose | Plan |
|---|---|---|
| **IBM watsonx.ai** | Hosting IBM Granite LLM | Free Lite |
| **IBM Granite 13B Chat** | NLU & conversation | Free via watsonx.ai |
| **IBM Cloud IAM** | Authentication (API key) | Free |
| **IBM NLU** *(optional)* | Advanced entity extraction | Free Lite (30k chars/month) |
| **IBM Language Translator** *(optional)* | Multi-language support | Free Lite |

---

## 💬 Example Conversations

```
User: Suggest beach destinations under $50/day for 7 days

TravelBot: 🌍 Recommended Destinations:
1. Goa, India — $40/day, Best: Nov–Feb ✨ Beaches, Nightlife, Water Sports
2. Bali, Indonesia — $55/day, Best: Apr–Oct ✨ Temples, Surfing, Nightlife
3. Phuket, Thailand — $60/day, Best: Nov–Apr ✨ Islands, Diving, Thai cuisine
...
```

```
User: Plan a 5-day itinerary for Goa

TravelBot: 🗺️ 5-Day Itinerary for Goa
Day 1 – Arrival: Check in, orientation walk, welcome seafood dinner
Day 2 – Exploration: Sunrise beach walk, island hopping, sunset cruise
Day 3 – Deep Dive: Scuba diving, local market, beachside bonfire
...
```

---

## 📁 Environment Variables Reference

| Variable | Description | Required |
|---|---|---|
| `WATSONX_API_KEY` | IBM Cloud API Key | ✅ Yes |
| `WATSONX_PROJECT_ID` | watsonx.ai Project ID | ✅ Yes |
| `WATSONX_URL` | watsonx.ai endpoint URL | ✅ Yes |
| `GRANITE_MODEL_ID` | IBM Granite model ID | ✅ Yes |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | ⚡ Optional (real weather) |
| `IBM_NLU_API_KEY` | IBM NLU API key | ⚡ Optional |
| `SECRET_KEY` | Flask session secret | 🔒 Change in production |
| `PORT` | Server port (default: 5000) | ⚙️ Optional |

---

## 🔗 Useful Links

- [IBM Cloud Registration (Free)](https://cloud.ibm.com/registration)
- [IBM watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
- [IBM Granite Models](https://www.ibm.com/granite)
- [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
- [OpenWeatherMap Free API](https://openweathermap.org/api)

---

## 📄 License

MIT License — Built for AICTE Student Innovation Project, Problem Statement #5: Travel Planner Agent
