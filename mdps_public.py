# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 10:11:11 2024

@author: M S I
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Firebase initialization
cred = credentials.Certificate('C:/Users/M S I/Downloads/multiple-disease-detecti-d13a4-d495337dba87.json')
# Check if the Firebase app is already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Load saved models
diabetes_model = pickle.load(open("C:/Users/M S I/Downloads/diabetes_trained_model2.sav", 'rb'))
heart_model = pickle.load(open("C:/Users/M S I/Downloads/heart_trained_model.sav", 'rb'))
parkinsons_model = pickle.load(open("C:/Users/M S I/Downloads/parkinsons_trained_model.sav", 'rb'))


# Inject CSS to fix the sidebar width
st.markdown("""
    <style>
    .blur-background {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        z-index: -1;
        background: linear-gradient(135deg, #b5f0ff 80%, #b6b5ff 0%);
        filter: blur(15px);
    }

    .stApp {
        background-color: rgba(202, 240, 255, 0.6);
        background-clip: padding-box;
        border-radius: 15px;
        padding: 20px;
    }

    /* Optional: Fixing the sidebar width */
    .css-1d391kg {
        width: 250px;
    }
    </style>
    <div class="blur-background"></div>
""", unsafe_allow_html=True)


# Initialize session state to track login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar to navigate
with st.sidebar:
    selected = option_menu('Multiple Diseases Prediction Web',
                           ['Homepage',
                            'Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           icons=['house', 'capsule', 'heart-pulse-fill', 'person-wheelchair'])

# Homepage
if selected == 'Homepage':
    st.title('Welcome to Multiple Diseases Prediction Web 🤩')
    
    choice = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'])
    
    def login():
        try:
            user = auth.get_user_by_email(email)
            st.session_state.logged_in = True
            st.write('Login Success!')
        except:
            st.warning('Login Failed')

    if choice == 'Login':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.button('Login', on_click=login)
        
    else:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input('Enter your unique username')
        
        if st.button('Create new account'):
            try:
                auth.create_user(email=email, password=password, uid=username)
                st.success('Account created successfully🙌')
                st.markdown('Please Login using your email and password')
                st.balloons()
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")

# Function to check login status
def check_login():
    if not st.session_state.logged_in:
        st.warning("You need to log in to use this feature.")
        return False
    return True

# Diabetes prediction page
if selected == 'Diabetes Prediction':
    # Page title
    st.title('Diabetes Prediction using Machine Learning')
    
    if check_login():
        # Get input from users
        col1, col2, col3 = st.columns(3)
        
        with col1:
            Pregnancies = st.text_input('Number of times pregnant')
            SkinThickness = st.text_input('Triceps skin fold thickness (mm)')
            DiabetesPedigreeFunction = st.text_input('Diabetes pedigree function')
            
        with col2:
            Glucose = st.text_input('Glucose level')
            Insulin = st.text_input('Insulin level (mu U/ml)')
            Age = st.text_input('Age (Years)')
            
        with col3:
            BloodPressure = st.text_input('Diastolic blood pressure (mm Hg)')
            BMI = st.text_input('BMI value')
        
        diabetes_diagnosis = ''
        
        # Button to predict
        if st.button('Diabetes Test Result'):
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness,
                          Insulin, BMI, DiabetesPedigreeFunction, Age]
            user_input = [float(x) for x in user_input]
            diabetes_prediction = diabetes_model.predict([user_input])
            
            if diabetes_prediction[0] == 0:
                diabetes_diagnosis = 'You are diabetic'
            else:
                diabetes_diagnosis = 'You are not diabetic'
                
        st.success(diabetes_diagnosis)

# Heart disease prediction page
if selected == 'Heart Disease Prediction':
    # Page title
    st.title('Heart Disease Prediction using Machine Learning')

    if check_login():
        col1, col2 = st.columns(2)
    
        with col1:
            age = st.text_input('Age')
    
        with col2:
            sex = st.text_input('Sex (1 = male; 0 = female)')
    
        with col1:
            cp = st.text_input('Chest pain types (0 - 3)')
    
        with col2:
            trestbps = st.text_input('Resting blood pressure (mm Hg)')
    
        with col1:
            chol = st.text_input('Serum cholestoral in mg/dl')
    
        with col2:
            fbs = st.text_input('Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)')
    
        with col1:
            restecg = st.text_input('Resting electrocardiographic results (0,1,2)')
    
        with col2:
            thalach = st.text_input('Maximum heart rate achieved')
    
        with col1:
            exang = st.text_input('Exercise induced angina (1 = yes; 0 = no)')
    
        with col2:
            oldpeak = st.text_input('ST depression induced by exercise')
    
        with col1:
            slope = st.text_input('Slope of the peak exercise ST segment')
    
        with col2:
            ca = st.text_input('Major vessels colored by flourosopy (0-3)')
    
        with col1:
            thal = st.text_input('Thalassemia: 0 = normal; 1 = fixed defect; 2 = reversible defect')
    
        # Code for Prediction
        heart_diagnosis = ''
    
        # Creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            user_input = [float(x) for x in user_input]
    
            heart_prediction = heart_model.predict([user_input])
    
            if heart_prediction[0] == 1:
                heart_diagnosis = 'You have heart disease'
            else:
                heart_diagnosis = 'You do not have any heart disease'
    
        st.success(heart_diagnosis)

# Parkinsons prediction page
if selected == 'Parkinsons Prediction':
    # Page title
    st.title('Parkinsons Prediction using Machine Learning')

    if check_login():
        col1, col2 = st.columns(2)
    
        with col1:
            fo = st.text_input('Average vocal fundamental frequency (Hz)')
    
        with col2:
            fhi = st.text_input('Maximum vocal fundamental frequency (Hz)')
    
        with col1:
            flo = st.text_input('Minimum vocal fundamental frequency (Hz)')
    
        with col2:
            Jitter_percent = st.text_input('MDVP: Jitter(%)')
    
        with col1:
            Jitter_Abs = st.text_input('MDVP: Jitter(Abs)(sec)')
    
        with col2:
            RAP = st.text_input('Relative average perturbation')
    
        with col1:
            PPQ = st.text_input('Pitch perturbation quotient')
    
        with col2:
            DDP = st.text_input('Jitter: Differential Dyshonia Parameter')
    
        with col1:
            Shimmer = st.text_input('MDVP: Shimmer (%)')
    
        with col2:
            Shimmer_dB = st.text_input('MDVP: Shimmer(dB)')
    
        with col1:
            APQ3 = st.text_input('Shimmer: Amplitude perturbation quotient over 3 cycles')
    
        with col2:
            APQ5 = st.text_input('Shimmer: Amplitude perturbation quotient over 5 cycles')
    
        with col1:
            APQ = st.text_input('MDVP: Amplitude Perturbation Quotient')
    
        with col2:
            DDA = st.text_input('Shimmer: Dysphonia dependent amplitude')
    
        with col1:
            NHR = st.text_input('Noise-to-Harmonics ratio')
    
        with col2:
            HNR = st.text_input('Harmonics-to-Noise ratio')
    
        with col1:
            RPDE = st.text_input('Recurrence period density entropy')
    
        with col2:
            DFA = st.text_input('Detrended fluctuation analysis')
    
        with col1:
            spread1 = st.text_input('Dispersion of the first fundamental frequency peak in the voice')
    
        with col2:
            spread2 = st.text_input('Spread of the second peak in the voice frequency spectrum')
    
        with col1:
            D2 = st.text_input('Dimension of voice signal')
    
        with col2:
            PPE = st.text_input('Pitch period entropy')
    
        # Code for Prediction
        parkinsons_diagnosis = ''
    
        # Creating a button for Prediction    
        if st.button("Parkinson's Test Result"):
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
            user_input = [float(x) for x in user_input]
    
            parkinsons_prediction = parkinsons_model.predict([user_input])
    
            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = 'You have Parkinson\'s disease'
            else:
                parkinsons_diagnosis = 'You do not have Parkinson\'s disease'
    
        st.success(parkinsons_diagnosis)
