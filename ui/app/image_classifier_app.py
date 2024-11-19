from typing import Optional

import requests
import streamlit as st
from app.settings import API_BASE_URL
from PIL import Image


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user
    and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    
    # Construct the API endpoint URL using `API_BASE_URL` and `/login`.
    url_api = API_BASE_URL + "/login"

    # Set up the request headers and data payload
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        'grant_type':'',
        'username': username,
        'password': password,
        'scope':'',
        'client_id':'',
        'client_secret':''
    }

    # API request
    response = requests.post(url_api, headers=headers, data=payload)

    #  If successful, extract the token from the JSON response.
    #  Return the token if login is successful, otherwise return `None`.
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else: 
        return None



def predict(token: str, uploaded_file: Image) -> requests.Response:
    """This function calls the predict endpoint of the API to classify the uploaded
    image.

    Args:
        token (str): token to authenticate the user
        uploaded_file (Image): image to classify

    Returns:
        requests.Response: response from the API
    """

    #  Dictionary with the file data
    img_dict = {"file": (uploaded_file.name, uploaded_file.getvalue())}

    
    #  POST request to the predict endpoint.
    headers = {'Authorization': f"Bearer {token}"}
    response = requests.post(API_BASE_URL+'/model/predict', files=img_dict, headers=headers)

    return response


def send_feedback(
    token: str, feedback: str, score: float, prediction: str, image_file_name: str
) -> requests.Response:
    """This function calls the feedback endpoint of the API to send feedback about
    the classification.

    Args:
        token (str): token to authenticate the user
        feedback (str): string with feedback
        score (float): confidence score of the prediction
        prediction (str): predicted class
        image_file_name (str): name of the image file

    Returns:
        requests.Response: _description_
    """

    # Dictionary with the feedback data including.
    feedback_dic = {
        "feedback": feedback,
        "score": score,
        "predicted_class": prediction,
        "image_file_name": image_file_name
    }
    

    # POST request to the feedback endpoint.
    response = requests.post(API_BASE_URL+'/feedback', headers=headers, json=feedback_dic)
    headers = {'Authorization': f"Bearer {token}"}

    return response


# User interface
st.set_page_config(page_title="Image Classifier", page_icon="📷")
st.markdown(
    "<h1 style='text-align: center; color: #4B89DC;'>Image Classifier</h1>",
    unsafe_allow_html=True,
)

# Login Form
if "token" not in st.session_state:
    st.markdown("## Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your credentials.")
else:
    st.success("You are logged in!")


if "token" in st.session_state:
    token = st.session_state.token

    # Load Image
    uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    print(type(uploaded_file))

    # Show image if loaded
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", width=300)

    if "classification_done" not in st.session_state:
        st.session_state.classification_done = False

    # Classification button
    if st.button("Classify"):
        if uploaded_file is not None:
            response = predict(token, uploaded_file)
            if response.status_code == 200:
                result = response.json()
                st.write(f"**Prediction:** {result['prediction']}")
                st.write(f"**Score:** {result['score']}")
                st.session_state.classification_done = True
                st.session_state.result = result
            else:
                st.error("Error classifying image. Please try again.")
        else:
            st.warning("Please upload an image before classifying.")

    # Show feedback form if classification is done
    if st.session_state.classification_done:
        st.markdown("## Feedback")
        feedback = st.text_area("If the prediction was wrong, please provide feedback.")
        if st.button("Send Feedback"):
            if feedback:
                token = st.session_state.token
                result = st.session_state.result
                score = result["score"]
                prediction = result["prediction"]
                image_file_name = result.get("image_file_name", "uploaded_image")
                response = send_feedback(
                    token, feedback, score, prediction, image_file_name
                )
                if response.status_code == 201:
                    st.success("Thanks for your feedback!")
                else:
                    st.error("Error sending feedback. Please try again.")
            else:
                st.warning("Please provide feedback before sending.")
                st.warning("Please provide feedback before sending.")

    # Footer
    st.markdown("<hr style='border:2px solid #4B89DC;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #4B89DC;'>2024 Image Classifier App</p>",
        unsafe_allow_html=True,
    )
