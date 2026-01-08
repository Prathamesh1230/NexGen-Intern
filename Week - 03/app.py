import streamlit as st
from database import create_user, verify_user, update_user, delete_user
from utils import validate_username, validate_password, passwords_match

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = 'login'

def show_login():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username and password:
            success, msg = verify_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = 'welcome'
                st.rerun()
            else:
                st.error(msg)
        else:
            st.error("Enter username and password")
    
    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = 'signup'
        st.rerun()

def show_signup():
    st.title("Sign Up")
    
    username = st.text_input("Username (min 5 characters)")
    password = st.text_input("Password (min 8 characters)", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        valid, msg = validate_username(username)
        if not valid:
            st.error(msg)
            return
        
        valid, msg = validate_password(password)
        if not valid:
            st.error(msg)
            return
        
        valid, msg = passwords_match(password, confirm)
        if not valid:
            st.error(msg)
            return
        
        success, msg = create_user(username, password)
        if success:
            st.success(msg + " - Please login")
        else:
            st.error(msg)
    
    if st.button("Already have an account? Login"):
        st.session_state.page = 'login'
        st.rerun()

def show_welcome():
    st.title(f"👋 Welcome, {st.session_state.username}!")
    st.success("You are logged in")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Update Account"):
            st.session_state.page = 'update'
            st.rerun()
    
    with col2:
        if st.button("Delete Account"):
            st.session_state.page = 'delete'
            st.rerun()
    
    with col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.page = 'login'
            st.rerun()

def show_update():
    st.title("Update Account")
    st.info(f"Current username: {st.session_state.username}")
    
    option = st.radio("Update", ["Username", "Password", "Both"])
    
    new_username = None
    new_password = None
    
    if option in ["Username", "Both"]:
        new_username = st.text_input("New Username")
    
    if option in ["Password", "Both"]:
        new_password = st.text_input("New Password", type="password")
        confirm = st.text_input("Confirm New Password", type="password")
    
    if st.button("Update"):
        if new_username:
            valid, msg = validate_username(new_username)
            if not valid:
                st.error(msg)
                return
        
        if new_password:
            valid, msg = validate_password(new_password)
            if not valid:
                st.error(msg)
                return
            valid, msg = passwords_match(new_password, confirm)
            if not valid:
                st.error(msg)
                return
        
        success, msg = update_user(st.session_state.username, new_username, new_password)
        if success:
            st.success(msg)
            if new_username:
                st.session_state.username = new_username
        else:
            st.error(msg)
    
    if st.button("← Back"):
        st.session_state.page = 'welcome'
        st.rerun()

def show_delete():
    st.title("Delete Account")
    st.warning(f"Delete account: {st.session_state.username}?")
    st.error("This cannot be undone!")
    
    confirm = st.checkbox("I understand")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Delete", disabled=not confirm):
            success, msg = delete_user(st.session_state.username)
            if success:
                st.success(msg)
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.page = 'login'
                st.rerun()
            else:
                st.error(msg)
    
    with col2:
        if st.button("Cancel"):
            st.session_state.page = 'welcome'
            st.rerun()

st.set_page_config(page_title="User Management", page_icon="🔐")

with st.sidebar:
    st.title("User Management")
    st.markdown("---")
    if st.session_state.logged_in:
        st.success(f"Logged in as:\n**{st.session_state.username}**")
    else:
        st.info("Please login or sign up")

if not st.session_state.logged_in:
    if st.session_state.page == 'signup':
        show_signup()
    else:
        show_login()
else:
    if st.session_state.page == 'update':
        show_update()
    elif st.session_state.page == 'delete':
        show_delete()
    else:
        show_welcome()