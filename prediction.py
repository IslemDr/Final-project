import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie



def prediction():
    df = pd.read_excel("Final_Project\E-commerceCustomerBehavior.xlsx")

    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    numerical_imputer = SimpleImputer(strategy='mean')
    df[numerical_columns] = numerical_imputer.fit_transform(df[numerical_columns])

    categorical_imputer = SimpleImputer(strategy='most_frequent')
    df[categorical_columns] = categorical_imputer.fit_transform(df[categorical_columns])

    data_encoded = pd.get_dummies(df, columns=['Gender', 'City', 'Membership Type', 'Discount Applied'])

    X = data_encoded.drop('Satisfaction Level', axis=1)  
    y = data_encoded['Satisfaction Level']  

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    rf_classifier.fit(X_train, y_train)
    def load_lottiefile(filepath: str):
     with open(filepath, "r", encoding="utf-8") as f:
       return json.load(f)

    def load_lottieurl(url: str):
      r = requests.get(url)
      if r.status_code != 200:
        return None
      return r.json()

# Load the Lottie animation file
    lottie_coding = load_lottiefile(r"Final_Project\animation\satisfaction.json")
    
    col1, col2 = st.columns([2, 1])
    with col1:
      st.title('E-commerce Customer Satisfaction Prediction')
    with col2:
# Display the Lottie animation using Streamlit
     st_lottie(
      lottie_coding,
      speed=1,
      reverse=False,
      loop=True,
      quality="low",  # Options: low, medium, high
      height=250,
      width=200,
      key=None,
      )

    

    st.sidebar.title('Enter Customer Information')

    customer_id = st.sidebar.text_input('Customer ID')
    gender = st.sidebar.selectbox('Gender', ['Male', 'Female'])
    age = st.sidebar.number_input('Age', min_value=0)
    city = st.sidebar.selectbox('City', df['City'].unique())
    membership_type = st.sidebar.selectbox('Membership Type', df['Membership Type'].unique())
    total_spend = st.sidebar.number_input('Total Spend', min_value=0.0)
    items_purchased = st.sidebar.number_input('Items Purchased', min_value=0)
    average_rating = st.sidebar.number_input('Average Rating', min_value=0.0, max_value=5.0)
    discount_applied = st.sidebar.selectbox('Discount Applied', df['Discount Applied'].unique())
    days_since_last_purchase = st.sidebar.number_input('Days Since Last Purchase', min_value=0)

    if st.sidebar.button('Predict Satisfaction Level'):
        input_data = pd.DataFrame({
            'Customer ID': [customer_id],
            'Gender': [gender],
            'Age': [age],
            'City': [city],
            'Membership Type': [membership_type],
            'Total Spend': [total_spend],
            'Items Purchased': [items_purchased],
            'Average Rating': [average_rating],
            'Discount Applied': [discount_applied],
            'Days Since Last Purchase': [days_since_last_purchase]
        })

        input_data_encoded = pd.get_dummies(input_data, columns=['Gender', 'City', 'Membership Type', 'Discount Applied'])

        missing_cols = set(X.columns) - set(input_data_encoded.columns)
        for col in missing_cols:
            input_data_encoded[col] = 0

        input_data_encoded = input_data_encoded[X.columns]

        prediction = rf_classifier.predict(input_data_encoded)

        st.write(f'Predicted Satisfaction Level: {prediction[0]}')

        if prediction[0] == 'Satisfied':
            st.image(r"Final_Project\images\high_satisfaction_image.jpg", caption='High Satisfaction')
        elif prediction[0] == 'Neutral':
            st.image(r'Final_Project\images\medium_satisfaction_image.png', caption='Medium Satisfaction')
        else:
            st.image(r'Final_Project\images\low_satisfaction_image.png', caption='Low Satisfaction')

if __name__ == "__main__":
    prediction()
