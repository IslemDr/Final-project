import streamlit as st 
from streamlit_option_menu import option_menu
from dashboard import show_dashboard
from chatbot import main
from prediction import prediction

def show_menu():

#with st.sidebar:
   # selected = option_menu(
        #menu_title="main menu",
      #  options=["home", "Projects", "CONTACT"],
       # icons=["house", "book", "enveloppe"],
       # menu_icon="cast",
      #  default_index=0,
    #)
 selected = option_menu(
    menu_title=None,
    options=["dashbord","prediction","chatbot"],
    icons=["clipboard-data", "question", "robot"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={}
 )

 if selected == "dashbord":
    #st.title(f"you have selected {selected}")
    show_dashboard()  
 if selected == "prediction":
    #st.title(f"you have selected {selected}")
    prediction()
 if selected == "chatbot":
    #st.title(f"you have selected {selected}")
    main()



 st.title('')

if __name__ == "__main__":
    show_menu()
