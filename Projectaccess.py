import streamlit as st
from mainapp import show_menu
from loginFace import App

def login():
    # Check if the user is already logged in
    if st.session_state.get("logged_in"):
        return  # Exit the function to prevent the login page from being displayed

    # Display camera for face recognition
    app = App()
    app.run()

    if st.session_state.get("logged_in"):
        return  # Exit if logged in successfully

def main():
    login()

    # Sidebar navigation
    if st.session_state.get("logged_in"):

        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Menu", "Profile"])
        if page == "Menu":
            show_menu()
        elif page == "Profile":
            st.write("This is the profile page.")  # Example profile page

if __name__ == "__main__":
    main()