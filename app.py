import pandas as pd
import joblib
import numpy as np
import streamlit as st

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1b0b2d 0%,
        #4a1025 50%,
        #7a1f2b 100%
    );
}

[data-testid="stSidebar"] * {
    color: white;
}

.stButton > button {
    width: 100%;
    background-color: #E23744;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

model = joblib.load('zomato_rating_prediction.pkl')
columns = joblib.load('columns.pkl')
rest_list = joblib.load('rest_list.pkl')
cuisine_list = joblib.load('cuisine_list.pkl')
city = joblib.load('city.pkl')
location = joblib.load('location.pkl')
type_list = joblib.load('type.pkl')

st.set_page_config(
    page_title="Zomato Rating Prediction",
    page_icon="🍽️",
    layout="wide")

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;">
        <a href="https://www.zomato.com" target="_blank">
            <img src="https://b.zmtcdn.com/images/logo/zomato_logo_2017.png"
                 width="180">
        </a>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <h3 style='color:white'>
    🔴 About
    </h3>
    """, unsafe_allow_html=True)
    st.caption("""
Predict ratings using:
• Location
• Cuisine
• Restaurant Type
• Online Order
• Table Booking
• Cost for Two
""")

    st.markdown("### 👨‍💻 Developed By")
    st.write("Manoranjan Behera")
    st.caption("Machine Learning Enthusiast")
    st.caption("Built with Python • Scikit-Learn • Streamlit")
    st.markdown("### 🔗 Connect With Me")
    st.markdown("""
<a href="https://www.linkedin.com/in/manoranjan-behera-70430b365/" target="_blank"
style="text-decoration:none;font-size:30px;">
💼 </a> """, unsafe_allow_html=True)
    st.markdown("""<a href="https://github.com/Manoranjan16" target="_blank"
style="text-decoration:none;font-size:30px;">💻</a>""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;'>
🍽️ Zomato Restaurant Rating Prediction
</h1>

<p style='text-align:center;font-size:20px;'>
Predict restaurant ratings using Machine Learning
</p>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    online_order = st.selectbox('🛒Online Order', ['Yes', "No"])
    book_table = st.selectbox("📅Book Table", ['Yes', 'No'])
    location_type = st.selectbox('📍Location', location)
    rest_type = st.selectbox('🏪Select Rest type', rest_list)
with col2:
    cuisines = st.multiselect("🍜Select Cuisines", cuisine_list)
    approx_cost = st.number_input("💰Approx cost for two", min_value=100)
    list_type = st.selectbox('🏷️Select the type', type_list)
    list_city = st.selectbox('🌆Select City', city)

st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 12px rgba(0,0,0,0.1);
">
""", unsafe_allow_html=True)

if st.button("🔍 Predict Rating", use_container_width=True):
    st.markdown("</div>", unsafe_allow_html=True)
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    #Label Encoding
    input_df['online_order'] = 1 if online_order == 'yes' else 0
    input_df['book_table'] = 1 if book_table == 'yes' else 0
    input_df['approx_cost(for two people)'] = approx_cost

    #OneHotEncoding
    if f"location_{location_type}" in input_df.columns:
        input_df[f"location_{location_type}"] = 1

    if f"rest_type_{rest_type}" in input_df.columns:
        input_df[f"rest_type_{rest_type}"] = 1

    if f"cuisines_{cuisines}" in input_df.columns:
        input_df[f"cuisines_{cuisines}"] = 1

    if f"listed_in(type)_{list_type}" in input_df.columns:
        input_df[f"listed_in(type)_{list_type}"] = 1

    if f"listed_in(city)_{list_city}" in input_df.columns:
        input_df[f"listed_in(city)_{list_city}"] = 1

    prediction = model.predict(input_df)
    rating = round(prediction[0],1)
    full_stars = int(rating)

    stars = "⭐" * full_stars + "☆" * (5-full_stars)

    st.markdown(f"""
<div style="
background:white;
padding:25px;
border-radius:15px;
margin-top:20px;
text-align:center;
">

<h1 style='color:#ff9800'>
{rating}/5
</h1>

<h2 style='color:#ff9800'>
{stars}
</h2>

</div>
""", unsafe_allow_html=True)
