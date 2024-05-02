import os.path
import datetime
import cv2
from PIL import Image
import subprocess
import streamlit as st
from mainapp import show_menu

class App:
    def __init__(self):
        #st.set_page_config(page_title="LogIn Page", layout="wide")
        self.capture = cv2.VideoCapture(0)
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        self.log_path = './log.txt'

    def process_webcam(self):
        ret, frame = self.capture.read()
        if not ret:
           st.error('Failed to capture image from webcam.')
           return
        frame = cv2.flip(frame, 1)
        most_recent_capture_arr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(most_recent_capture_arr, channels="RGB", width=800, use_column_width=True)

    def login(self):
        unknown_img_path = './.tmp.jpg'
        ret, frame = self.capture.read()
        cv2.imwrite(unknown_img_path, frame)
        try:
            output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]).decode('utf-8')
            name = output.split(',')[1][:-3]

            if name in ['unknown_person', 'no_persons_found']:
                st.error('Unknown user. Please register a new user or try again.')
            else:
                st.success('Welcome, {}!'.format(name))
                
                with open(self.log_path, 'a') as f:
                    f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                    #show_menu()
                st.success("Login successful!")
                st.session_state.logged_in = True
        except subprocess.CalledProcessError:
            st.error('Error occurred during face recognition.')
        os.remove(unknown_img_path)

    def register_new_user(self):
        st.sidebar.header('Register New User')
        name = st.sidebar.text_input('Enter username:')
        if st.sidebar.button('Register'):
            ret, frame = self.capture.read()
            if ret:
                new_user_image_path = os.path.join(self.db_dir, f"{name}.jpg")
                cv2.imwrite(new_user_image_path, frame)
                st.success('User was registered successfully!')
                st.sidebar.text("Image saved to: " + new_user_image_path)
                

            else:
                st.error('Failed to capture image. Please try again.')
   # def show_success_message(self):
       # st.write("User was registered successfully!")

    def run(self):
        st.title("LogIn Page")
        col1, col2 = st.columns([3, 2])

        with col1:
            self.process_webcam()

        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            login_icon = Image.open(r'Final_Project\images\login.png')
            st.image(login_icon, width=100)
            if st.button('Login', key='login'):
                self.login()

            register_icon = Image.open(r'Final_Project\images\new-registration-icon.webp')
            st.image(register_icon, width=100)
            if st.button('Register', key='register'):
                self.register_new_user()

if __name__ == "__main__":
    app = App()
    app.run()
    #app.register_new_user()
