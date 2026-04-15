from io import BytesIO

import requests
import streamlit as st


st.set_page_config(
    page_title="Moodie Journal",
    page_icon="📔",
    layout="wide",
)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Serif:wght@500;600&display=swap');

        :root {
            --bg-a: #fdf6ec;
            --bg-b: #e8f7f0;
            --ink: #1f2937;
            --muted: #4b5563;
            --brand: #0b7a75;
            --brand-dark: #065f5b;
            --card: #ffffff;
            --line: rgba(15, 23, 42, 0.1);
        }

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Space Grotesk', sans-serif;
            background: radial-gradient(circle at 10% 10%, var(--bg-a) 0%, #ffffff 45%),
                        radial-gradient(circle at 90% 90%, var(--bg-b) 0%, #ffffff 55%);
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            font-family: 'IBM Plex Serif', serif;
            color: var(--ink);
        }

        .hero {
            padding: 1.4rem 1.6rem;
            border-radius: 1.1rem;
            background: linear-gradient(125deg, #0f172a 0%, #0b7a75 100%);
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.25);
        }

        .card {
            padding: 1rem 1.2rem;
            border-radius: 0.85rem;
            background: var(--card);
            border: 1px solid var(--line);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }

        .metric-box {
            padding: 0.9rem 1rem;
            border-radius: 0.8rem;
            border: 1px solid var(--line);
            background: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state():
    defaults = {
        "base_url": "http://localhost:5000",
        "auth_user": None,
        "auth_token": None,
        "auth_view": "landing",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def api_url(path):
    return f"{st.session_state['base_url']}{path}"


def safe_response_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw": response.text}


def post_json(path, payload):
    headers = {}
    if st.session_state.get("auth_token"):
        headers["Authorization"] = f"Bearer {st.session_state['auth_token']}"
    try:
        return requests.post(api_url(path), json=payload, headers=headers, timeout=30), None
    except requests.RequestException as exc:
        return None, str(exc)


def get_json(path, params=None):
    headers = {}
    if st.session_state.get("auth_token"):
        headers["Authorization"] = f"Bearer {st.session_state['auth_token']}"
    try:
        return requests.get(api_url(path), params=params, headers=headers, timeout=30), None
    except requests.RequestException as exc:
        return None, str(exc)


def render_landing():
    st.markdown(
        """
        <div class="hero">
            <h1 style="margin-bottom: 0.25rem;">Moodie Journal</h1>
            <p style="margin: 0; opacity: 0.92;">
                Reflect daily, understand your emotional trends, and keep your own private mood archive.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_left, cta_right = st.columns(2)
    with cta_left:
        if st.button("Login", type="primary", use_container_width=True):
            st.session_state["auth_view"] = "login"
            st.rerun()
    with cta_right:
        if st.button("Create Account", use_container_width=True):
            st.session_state["auth_view"] = "register"
            st.rerun()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Why this flow feels like a real app")
    st.write("- New visitors start on a clear landing page.")
    st.write("- Authentication gates personal data and account actions.")
    st.write("- Logged-in users only see their own entries and analytics.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_register():
    st.title("Create your account")
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        register_submit = st.form_submit_button("Register", type="primary")

    if register_submit:
        payload = {"username": username, "email": email, "password": password}
        response, error = post_json("/api/users/register", payload)
        if error:
            st.error("Registration request failed.")
            st.code(error)
        else:
            data = safe_response_json(response)
            if response.ok:
                st.success(data.get("message", "Account created successfully."))
                st.info("You can now log in.")
                st.session_state["auth_view"] = "login"
            else:
                st.error(data.get("message", "Registration failed."))

    if st.button("Back to landing"):
        st.session_state["auth_view"] = "landing"
        st.rerun()


def render_login():
    st.title("Welcome back")
    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login", type="primary")

    if login_submit:
        login_payload = {"password": password}
        if "@" in username_or_email:
            login_payload["email"] = username_or_email
            login_payload["username"] = ""
        else:
            login_payload["username"] = username_or_email
            login_payload["email"] = ""

        response, error = post_json("/api/users/login", login_payload)
        if error:
            st.error("Login request failed.")
            st.code(error)
        else:
            data = safe_response_json(response)
            if response.ok:
                st.session_state["auth_user"] = data.get("user")
                st.session_state["auth_token"] = data.get("access_token")
                st.session_state["auth_view"] = "dashboard"
                st.success(data.get("message", "Login successful."))
                st.rerun()
            else:
                st.error(data.get("message", "Login failed."))

    if st.button("Back to landing"):
        st.session_state["auth_view"] = "landing"
        st.rerun()


def render_dashboard(user):
    with st.sidebar:
        st.subheader("Session")
        st.write(f"Signed in as **{user.get('username', 'User')}**")
        st.caption(user.get("email", ""))

        base_url = st.text_input("API base URL", value=st.session_state["base_url"])
        st.session_state["base_url"] = base_url.rstrip("/")

        page = st.radio("Navigate", ["Home", "New Entry", "My Entries", "Account", "API Status"], index=0)

        if st.button("Logout", use_container_width=True):
            st.session_state["auth_user"] = None
            st.session_state["auth_token"] = None
            st.session_state["auth_view"] = "landing"
            st.rerun()

    st.markdown(
        f"""
        <div class="hero">
            <h1 style="margin-bottom: 0.3rem;">Hello, {user.get('username', 'User')}</h1>
            <p style="margin: 0; opacity: 0.92;">Your personal mood dashboard is ready.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page == "Home":
        response, error = get_json("/api/history")
        if error:
            st.error("Could not load your dashboard data.")
            st.code(error)
            return

        entries = []
        if response.ok:
            entries = safe_response_json(response)
        else:
            st.error("Could not load your entries.")
            st.code(response.text)
            return

        total_entries = len(entries)
        positive_count = len([entry for entry in entries if str(entry.get("sentiment", "")).lower() == "positive"])
        negative_count = len([entry for entry in entries if str(entry.get("sentiment", "")).lower() == "negative"])

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Total Entries", total_entries)
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Positive Entries", positive_count)
            st.markdown("</div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Negative Entries", negative_count)
            st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Recent entries")
        if not entries:
            st.info("You have not added any entries yet.")
        else:
            for entry in entries[:5]:
                with st.container(border=True):
                    st.write(entry.get("date_pretty", "Unknown date"))
                    st.write(entry.get("text", ""))
                    st.caption(
                        f"Sentiment: {entry.get('sentiment', 'Unknown')} | Confidence: {entry.get('confidence', 'N/A')}"
                    )

    elif page == "New Entry":
        st.subheader("Write a new entry")
        entry_text = st.text_area(
            "Your journal entry",
            height=220,
            placeholder="Write about your day, thoughts, or moments worth remembering...",
        )
        analyze_only = st.checkbox("Analyze only (skip PDF)", value=False)

        if st.button("Submit entry", type="primary"):
            text = entry_text.strip()
            if not text:
                st.warning("Please enter your journal text first.")
            else:
                with st.spinner("Analyzing sentiment..."):
                    response, error = post_json("/api/sentiment/analyse", {"text": text})

                if error:
                    st.error("Sentiment analysis request failed.")
                    st.code(error)
                elif response.ok:
                    data = safe_response_json(response).get("data", {})
                    st.success("Sentiment analysis complete.")
                    st.metric("Sentiment", data.get("sentiment", "Unknown"))
                    st.metric("Confidence", f"{data.get('confidence', 0.0)}")

                    if not analyze_only:
                        complete_payload = {"text": text}
                        with st.spinner("Saving entry and generating PDF..."):
                            pdf_response, pdf_error = post_json("/api/complete-entry", complete_payload)

                        if pdf_error:
                            st.error("PDF generation request failed.")
                            st.code(pdf_error)
                        elif pdf_response.ok and pdf_response.headers.get("content-type", "").startswith("application/pdf"):
                            st.success("Entry saved and PDF generated.")
                            st.download_button(
                                "Download journal PDF",
                                data=BytesIO(pdf_response.content),
                                file_name="moodie_journal_entry.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                            )
                        else:
                            st.error("Entry save/PDF generation failed.")
                            st.code(pdf_response.text)
                else:
                    st.error("Sentiment analysis failed.")
                    st.code(response.text)

    elif page == "My Entries":
        st.subheader("My journal history")
        if st.button("Refresh"):
            st.rerun()

        response, error = get_json("/api/history")
        if error:
            st.error("Could not reach the API.")
            st.code(error)
            return

        if not response.ok:
            st.error("Failed to load your entries.")
            st.code(response.text)
            return

        entries = safe_response_json(response)
        if not entries:
            st.info("No entries found for your account yet.")
        else:
            for entry in entries:
                with st.container(border=True):
                    st.write(entry.get("date_pretty", "Unknown date"))
                    st.write(entry.get("text", ""))
                    st.caption(
                        f"Sentiment: {entry.get('sentiment', 'Unknown')} | Confidence: {entry.get('confidence', 'N/A')}"
                    )

    elif page == "Account":
        st.subheader("Account")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write(f"Username: **{user.get('username', '-') }**")
        st.write(f"Email: **{user.get('email', '-') }**")
        st.write(f"User ID: **{user.get('id', '-') }**")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.subheader("API Status")
        endpoints = [
            ("Home", "/"),
            ("My History", "/api/history"),
            ("Sentiment", "/api/sentiment/analyse"),
            ("Users", "/api/users/login"),
        ]

        for label, path in endpoints:
            try:
                if label in ["Sentiment", "Users"]:
                    response = requests.options(api_url(path), timeout=10)
                else:
                    response = requests.get(api_url(path), timeout=10)
                st.write(f"{label}: {response.status_code}")
            except requests.RequestException as exc:
                st.write(f"{label}: unavailable")
                st.caption(str(exc))


if st.session_state["auth_user"]:
    render_dashboard(st.session_state["auth_user"])
else:
    base_url = st.sidebar.text_input("API base URL", value=st.session_state["base_url"])
    st.session_state["base_url"] = base_url.rstrip("/")

    view = st.session_state.get("auth_view", "landing")
    if view == "register":
        render_register()
    elif view == "login":
        render_login()
    else:
        render_landing()