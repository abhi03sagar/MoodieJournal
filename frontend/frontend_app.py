import streamlit as st
import requests

# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------
API_BASE_URL = "http://localhost:5000/api"

# -------------------------------------------------------------------
# AUTH FUNCTIONS
# -------------------------------------------------------------------
def login(username, password):
    try:
        res = requests.post(f"{API_BASE_URL}/auth/login", json={"username": username, "password": password})
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Login failed: {res.json().get('message', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def register(username, password):
    try:
        res = requests.post(f"{API_BASE_URL}/auth/register", json={"username": username, "password": password})
        if res.status_code == 201:
            st.success("Registration successful! Please login.")
            return True
        else:
            st.error(f"Registration failed: {res.json().get('message')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

# -------------------------------------------------------------------
# ENTRY FUNCTIONS (REQUIRE TOKEN)
# -------------------------------------------------------------------
def get_auth_headers():
    return {"Authorization": f"Bearer {st.session_state['token']}"}

def create_entry(text):
    res = requests.post(
        f"{API_BASE_URL}/entries/", 
        json={"text": text}, 
        headers=get_auth_headers()
    )
    if res.status_code == 201:
        st.success("Entry saved!")
        st.rerun() # Refresh the page to show new entry
    else:
        st.error("Failed to save entry.")

def get_entries():
    res = requests.get(f"{API_BASE_URL}/entries/", headers=get_auth_headers())
    if res.status_code == 200:
        return res.json()
    return []

def delete_entry(entry_id):
    res = requests.delete(f"{API_BASE_URL}/entries/{entry_id}", headers=get_auth_headers())
    if res.status_code == 200:
        st.success("Deleted!")
        st.rerun()

def update_entry(entry_id, new_text):
    res = requests.put(
        f"{API_BASE_URL}/entries/{entry_id}", 
        json={"text": new_text}, 
        headers=get_auth_headers()
    )
    if res.status_code == 200:
        st.success("Updated!")
        return True
    else:
        st.error("Failed to update entry.")
        return False

def download_pdf(entry_id):
    res = requests.get(f"{API_BASE_URL}/entries/{entry_id}/download", headers=get_auth_headers())
    if res.status_code == 200:
        return res.content # Returns the PDF binary data
    return None

# -------------------------------------------------------------------
# MAIN APP UI
# -------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Moodie Journal", page_icon="📓")
    st.title("📓 Virtual Moodie Diary")

    # Initialize Session State (This replaces LocalStorage in React)
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    # ------------------ LOGGED OUT VIEW ------------------
    if st.session_state['token'] is None:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Log In"):
                data = login(username, password)
                if data:
                    st.session_state['token'] = data['accessToken']
                    st.session_state['username'] = data['username']
                    st.rerun()

        with tab2:
            st.subheader("Create an Account")
            new_user = st.text_input("Username", key="reg_user")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            if st.button("Register"):
                register(new_user, new_pass)

    # ------------------ LOGGED IN VIEW ------------------
    else:
        # Sidebar with user info and Logout
        with st.sidebar:
            st.write(f"Logged in as: **{st.session_state['username']}**")
            if st.button("Logout"):
                st.session_state['token'] = None
                st.session_state['username'] = None
                st.rerun()

        # Main Dashboard
        st.subheader("How are you feeling today?")
        
        # 1. Create Entry Form
        with st.form("new_entry_form"):
            text_input = st.text_area("Dear Diary...", height=150)
            submitted = st.form_submit_button("Save Entry")
            if submitted and text_input:
                create_entry(text_input)

        st.divider()

        # 2. View Entries
        st.subheader("Your Past Entries")
        entries = get_entries()

        if not entries:
            st.info("No entries yet. Write your first one above!")
        
        for entry in entries:
            # Fix: Convert date to string before slicing to prevent crash if it's a dictionary
            date_str = str(entry.get('date', 'Unknown'))
            entry_id = entry['_id']
            
            with st.expander(f"{date_str[:10]} - Sentiment: {entry.get('sentiment', 'Unknown')}"):
                
                # Initialize edit mode state for this specific entry if not exists
                edit_key = f"edit_mode_{entry_id}"
                if edit_key not in st.session_state:
                    st.session_state[edit_key] = False

                if st.session_state[edit_key]:
                    # --- EDIT MODE ---
                    new_text = st.text_area("Edit your entry", value=entry['text'], key=f"text_{entry_id}")
                    col_save, col_cancel = st.columns([1, 1])
                    
                    with col_save:
                        if st.button("Save Update", key=f"save_{entry_id}"):
                            if update_entry(entry_id, new_text):
                                st.session_state[edit_key] = False
                                st.rerun()
                    
                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_{entry_id}"):
                            st.session_state[edit_key] = False
                            st.rerun()
                else:
                    # --- VIEW MODE ---
                    st.write(entry['text'])
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    # Edit Button
                    with col1:
                        if st.button("Edit", key=f"edit_{entry_id}"):
                            st.session_state[edit_key] = True
                            st.rerun()

                    # Delete Button
                    with col2:
                        if st.button("Delete", key=f"del_{entry_id}"):
                            delete_entry(entry_id)
                    
                    # Download Button
                    with col3:
                        pdf_data = download_pdf(entry_id)
                        if pdf_data:
                            st.download_button(
                                label="Download PDF",
                                data=pdf_data,
                                file_name=f"diary_{entry_id}.pdf",
                                mime="application/pdf",
                                key=f"pdf_{entry_id}"
                            )

if __name__ == "__main__":
    main()