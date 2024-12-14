import streamlit as st
import tensorflow as tf
import numpy as np

# TensorFlow Model Prediction
def model_prediction(test_image):
    model = load_model()  # Load the pre-trained model
    # Preprocess the input image
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = np.expand_dims(tf.keras.preprocessing.image.img_to_array(image), axis=0)
    # Predict using the model
    prediction = model.predict(input_arr)
    predicted_index = np.argmax(prediction)
    return predicted_index

def load_model():
    return tf.keras.models.load_model('trained_model.keras')

# Sidebar for navigation
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Choose Page", ["Home", "About", "Recognition"])

# Home Page
if app_mode == "Home":
    st.header("Plant Disease Recognition System")
    st.image("leaf-spot-fungus.webp", use_column_width=True)
    st.markdown("""
    ## Welcome to the Plant Disease Recognition System! 🌿🔍
    This platform identifies plant diseases using advanced machine learning techniques. Simply upload an image of a plant, and our system will analyze it to detect potential diseases.

    ### How It Works:
    1. **Upload Image**: Navigate to the **Recognition** page and upload a plant image.
    2. **Analysis**: The system processes the image and predicts potential diseases.
    3. **View Results**: Check the predictions and take appropriate actions.

    ### Features:
    - **Accuracy**: Powered by state-of-the-art AI.
    - **Ease of Use**: Intuitive interface for seamless navigation.
    - **Speed**: Results in seconds.

    Navigate to the **Recognition** page to start using the system!
    """)

# About Page
elif app_mode == "About":
    st.header("About the Project")
    st.markdown("""
    ### Dataset Information:
    - **Source**: Offline augmentation of an existing dataset available on GitHub.
    - **Content**:
      - Train Set: 70,295 images
      - Validation Set: 17,572 images
      - Test Set: 33 images (created separately for testing purposes)
    - **Classes**: 38 categories of healthy and diseased crop leaves.

    This system aims to simplify plant disease identification and contribute to sustainable agriculture practices.
    """)

# Recognition Page
elif app_mode == "Recognition":
    st.header("Disease Recognition")
    test_image = st.file_uploader("Upload an Image:")
    if st.button("Show Image"):
        st.image(test_image, use_column_width=True)
    
    if st.button("Predict"):
        with st.spinner("Processing..."):
            predicted_index = model_prediction(test_image)
            # Define class names
            class_names = [
                'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
                'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
                'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
                'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight',
                'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight',
                'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
                'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
                'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
            ]
            st.success(f"The model predicts: {class_names[predicted_index]}")
