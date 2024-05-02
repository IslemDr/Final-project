from streamlit_chat import message 
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st
from faker import Faker
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st
import json
import speech_recognition as sr
import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

nltk.download('stopwords')
nltk.download('wordnet')

def get_nearest_store_location():
    
    fake = Faker()

    cities = ['Los Angeles', 'New York', 'Houston', 'Chicago', 'Miami', 'San Francisco']

    addresses = {}
    for city in cities:
        addresses[city] = fake.address()

    with open('addresses.json', 'w') as f:
      json.dump(addresses, f, indent=4)
    with open('addresses.json', 'r') as f:
        addresses = json.load(f)

        return addresses

def get_discount_availability():
    # Add your code here to check for available discounts
    # Placeholder response for demonstration
    return "We currently offer discounts! Feel free to visit our website to explore them."

def get_membership_types():
    # Add your code here to fetch available membership types
    # Placeholder response for demonstration
    return ["Gold Membership", "Silver Membership", "Bronze Membership"]

# Function to handle user queries
def handle_query(query):

   
    if "closest store location" in query:
        return get_nearest_store_location()
  
    elif "membership type" in query:
        return ", ".join(get_membership_types())
    elif "discount" in query:
        return get_discount_availability()
    else:
        return "I'm sorry, I couldn't understand your question. Please ask about store locations, discounts, or membership types."
    
def main():
    def load_lottiefile(filepath: str):
     with open(filepath, "r", encoding="utf-8") as f:
       return json.load(f)

    def load_lottieurl(url: str):
      r = requests.get(url)
      if r.status_code != 200:
        return None
      return r.json()

# Load the Lottie animation file
    lottie_coding = load_lottiefile(r"Final_Project\animation\chatbot.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
      st.header("Customer Habit Chatbot")
    with col2:
# Display the Lottie animation using Streamlit
     st_lottie(
      lottie_coding,
      speed=1,
      reverse=False,
      loop=True,
      quality="low",  # Options: low, medium, high
      height=250,
      width=250,
      key=None,
      )

    #st.header("Customer Habit Chatbot")
    st.write("# <span style='color: lightblue;'> Hi there! :wave:</span>", unsafe_allow_html=True)
    #st.write("## How can I help you today?")     
    message('How can I help you today?')
    message('Hi there! This is a bot speaking. I’m here to answer your questions, but you’ll always have the option to talk to our team.')
    message("Are any of these related to your question?")


    #with st.chat_message(name="assistant"):
        #st.write("Hi there! This is a bot speaking. I’m here to answer your questions, but you’ll always have the option to talk to our team.")
        #st.write("So what brings you here today?")
        #st.markdown("<span style='color: grey; font-style: italic;'>Are any of these related to your question?</span>", unsafe_allow_html=True)
    
    option = st.radio("Select an option", ["What is the closest store location to my current position?", "Are there any current discounts available?", "What types of memberships are available?", "Rate our products"])

    #with st.chat_message("user"):
        #if option:
            #st.write(option)
    if option:
     message(option, is_user=True)


    if option == "What is the closest store location to my current position?":
       city_input = st.text_input("Please enter your city:")
       if city_input:
        city = city_input.strip().title()
        addresses = get_nearest_store_location()
        if city in addresses:
            message(f"The closest store location in {city} is: {addresses[city]}", is_user=False)
        else:
            message("Sorry, I don't have an address for that city. Please try another one", is_user=False)
    elif option == "Are there any current discounts available?":
            message(handle_query("discount"), is_user=False)
    elif option == "What types of memberships are available?":
            message(handle_query("membership type"), is_user=False)
    elif option == "Rate our products":
            rating = st.slider("Please rate our products", min_value=1, max_value=5)
            if rating > 3:
              message("Thank you for your confidence in our products!", is_user=False)
            else:
              issue = st.text_input("We're sorry to hear that. Can you please specify the issue or how we can improve?")
              if issue:
                 message(f"We appreciate your feedback. We will work on resolving the issue or meeting your expectations regarding {issue}.", is_user=False)
              else:
                  message("Your feedback is valuable to us. Please let us know how we can improve.", is_user=False)


if __name__ == "__main__":
    main()
