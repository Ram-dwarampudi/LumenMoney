# 💰 LumenMoney

## 📌 Overview
**LumenMoney** is a multi-page personal finance dashboard built with **Streamlit**. It gives users a single place to track income and expenses, monitor budgets, set savings goals, and visualize spending patterns through interactive charts — all wrapped in a custom dark-themed, modern UI.

---

## 🚀 Features
- 🔐 **User authentication** — session-based signup/login with SHA-256 password hashing
- 📊 **Dashboard** — at-a-glance summary of income, expenses, and overall balance
- 🧾 **Transactions** — categorized income/expense records (Food, Transport, Utilities, Rent, Health, Shopping, etc.)
- 🎯 **Goals** — track savings goals with target amounts, deadlines, and progress visualization
- 💰 **Budget** — set category-wise budgets and monitor spent vs. remaining amounts, with over-budget alerts
- 📈 **Investment & Analytics pages** — additional views for portfolio and spending insights
- ⚙️ **Settings** — customizable theme, accent color, chart style, currency (INR), date format, time zone, and notification preferences
- 👤 **Profile** — user profile with editable details and preference toggles
- 📉 **Interactive charts** — built with Plotly (bar charts, trend lines) for budgets, goals, and monthly spending

---

## 🛠️ Tech Stack
- **Framework:** Streamlit (Python)
- **Visualization:** Plotly (`plotly.graph_objects`, `plotly.express`)
- **Data Handling:** Pandas, NumPy
- **Auth:** Session-based login/signup with `hashlib` (SHA-256) password hashing
- **Styling:** Custom CSS injected via Streamlit for a dark, glassmorphism-style UI

---

## 📂 Project Structure
```
LumenMoney/
│── dashboard.py           # Main Streamlit app (pages, auth, styling, charts)
│── dashboard_backup.py    # Backup/previous version of the app
│── requirements.txt       # Python dependencies
```

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Ram-dwarampudi/LumenMoney.git
   cd LumenMoney
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run dashboard.py
   ```

4. Sign up / log in with a new account, and start exploring the Dashboard, Transactions, Budget, and Goals pages.

---

## 📚 Concepts Used
- Multi-page app routing using Streamlit session state
- Session-based authentication and password hashing
- Data visualization with Plotly (bar charts, comparative charts)
- Custom CSS theming inside a Streamlit app
- State management for user preferences (theme, currency, notifications)

---

## ⚠️ Current Limitations
- Data (transactions, goals, budgets) is currently held in session state / sample data rather than a persistent database
- No real bank/payment integration — figures are illustrative
- Single-session auth (no persistent user database yet)

## 🔮 Future Improvements
- 💾 Persist user data with a database (SQLite/PostgreSQL) instead of session state
- 🔗 Real transaction import (bank statement/CSV upload)
- 📧 Email alerts for budget warnings and goal milestones
- 📱 Improve mobile responsiveness

---

## 🎯 Purpose
This project was built to:
- Practice building multi-page, stateful applications with Streamlit
- Work with data visualization libraries (Plotly) for real-world dashboards
- Design and implement a polished, custom UI within Streamlit's constraints
- Build a strong, functional portfolio project

---

## 👤 Author
**Ram Dwarampudi**
🔗 GitHub: https://github.com/Ram-dwarampudi
🔗 LinkedIn: https://www.linkedin.com/in/ram-dwarampudi-7a7a12316/

---

## ⭐ Support
If you find this project useful, consider giving it a star ⭐ on GitHub!
