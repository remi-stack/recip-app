"""
Recipe Generator Application
This app uses the Gemini API to generate a recipe based on the user's input.
"""

# pip install streamlit
# pip install google-genai
# pip install pillow
import streamlit as st
from google import genai
from PIL import Image

# ------------------------------
# Page configuration and CSS
# ------------------------------
st.set_page_config(page_title="Gemini Recipe Generator", page_icon="🍳", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #333333;
    }
    .subheader {
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 20px;
        color: #555555;
    }
    body {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------
# Header Image and Titles
# ------------------------------
# Load and display a header image (update the path or URL accordingly)
try:
    import requests
    from io import BytesIO

    response = requests.get("https://images.unsplash.com/photo-1542010589005-d1eacc3918f2?q=80&w=2092&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    image = Image.open(BytesIO(response.content))
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, width=650)
except Exception as e:
    st.warning("Header image could not be loaded. Please check the image path.")

st.markdown("<div class='header'>Gemini Recipe Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Ask for a recipe and let the Gemini API cook up something delicious!</div>", unsafe_allow_html=True)

# ------------------------------
# Recipe Request Form
# ------------------------------
with st.form(key="recipe_form"):
    recipe_input = st.text_input("Enter a recipe", placeholder="e.g., Italian pasta recipe with tomatoes")
    submit_button = st.form_submit_button(label="Generate Recipe")

if submit_button:
    if recipe_input.strip():
        st.info("Generating your recipe, please wait...")
        try:
            # Initialize the Gemini API client
            client = genai.Client(api_key=st.secrets["api"]["key"])
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Give me the recipe of {recipe_input} for a family dinner with 4 people. Make it short and simple with effective markdown display",
            )
            
            # Display the response (assuming the API returns Markdown formatted text)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred while generating the recipe: {e}")
    else:
        st.warning("Please enter a recipe prompt before submitting.")