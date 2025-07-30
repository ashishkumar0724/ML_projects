# app.py
import streamlit as st
# Import core logic
import classifier
import utils.sms_generator as sms_gen
import streamlit as st

# --- Streamlit UI ---
st.title("📱 SMS Spam Classifier")
st.markdown("Enter an SMS message below to classify it as **Spam** or **Ham** using different models.")

# --- Model Selection ---
st.sidebar.header("⚙️ Model Selection")
selected_model_name = st.sidebar.selectbox(
    "Choose a model:",
    list(classifier.AVAILABLE_MODELS.keys())
)
model_filename = classifier.get_model_filename(selected_model_name)

# Load selected model (with error handling in UI)
model = None
if model_filename:
    try:
        with st.spinner(f"Loading {selected_model_name}..."):
            model = classifier.load_model(model_filename)
        st.sidebar.success(f"Loaded: {selected_model_name}")
    except FileNotFoundError as e:
        st.sidebar.error(str(e))
        st.error("Selected model file not found. Please check the models directory.")
        st.stop()
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")
        st.error("Failed to load the selected model.")
        st.stop()
else:
    st.error("Invalid model selection.")
    st.stop()

# --- SMS Generation Section ---
st.sidebar.header("🤖 SMS Generator")
gen_option = st.sidebar.radio(
    "Generate test SMS:",
    ["None", "Ham (Normal)", "Spam", "Random"]
)

# --- Main Interface ---
# Initialize session state for generated SMS
if 'generated_sms' not in st.session_state:
    st.session_state.generated_sms = ""

# Handle SMS generation button click
if st.sidebar.button("Generate SMS"):
    try:
        if gen_option == "Ham (Normal)":
            generated_sms = sms_gen.generate_ham_sms()
        elif gen_option == "Spam":
            generated_sms = sms_gen.generate_spam_sms()
        elif gen_option == "Random":
            generated_sms = sms_gen.generate_random_sms()
        else:
            generated_sms = ""
        st.session_state.generated_sms = generated_sms
        # Note: Streamlit usually updates state automatically, no explicit rerun usually needed here
    except Exception as e:
        st.sidebar.error(f"Error generating SMS: {e}")

# SMS input with generated content
user_input = st.text_area(
    "Enter SMS message:",
    value=st.session_state.generated_sms,
    placeholder="Type your message here or use the generator...",
    height=150,
    key="sms_input"
)

# Buttons row
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Clear"):
        st.session_state.generated_sms = ""
        st.rerun()  # Use st.rerun() or st.experimental_rerun() depending on your Streamlit version
with col2:
    # Predict button
    classify_clicked = st.button("Classify", type="primary")

# Placeholder for prediction results
prediction_placeholder = st.empty()

# Handle prediction
if classify_clicked:
    if not user_input.strip():
        with prediction_placeholder.container():
            st.warning("Please enter a message.")
    else:
        try:
            # Preprocess input (exactly as in training)
            cleaned_input = classifier.clean_text(user_input)
            # Make prediction
            prediction, probability_spam, has_probability = classifier.get_prediction_and_probability(model,
                                                                                                      cleaned_input)

            label = "Spam" if prediction == 1 else "Ham"
            # Display result in the placeholder below the buttons
            with prediction_placeholder.container():
                st.subheader("🔍 Prediction Result")
                st.write(f"**Model Used:** {selected_model_name}")
                st.write(f"**Label:** {label}")
                if has_probability:
                    st.write(f"**Confidence (Probability of Spam):** {probability_spam:.4f}")
                    st.progress(float(probability_spam))
                else:
                    st.write(
                        f"**Confidence Score:** {probability_spam:.4f} (Pseudo-probability from decision function)")
                    st.progress(float(probability_spam))
                    st.info(
                        "ℹ️Note: This model doesn't provide true probabilities. This confidence is derived from SVM decision function using sigmoid transformation")
                # Add some color coding
                if prediction == 1:
                    st.error("🚨 CLASSIFIED AS SPAM")
                else:
                    st.success("✅ CLASSIFIED AS HAM")

        except Exception as e:
            with prediction_placeholder.container():
                st.error(f"An error occurred during prediction: {e}")

# --- Information Sections (Optional) ---
with st.expander("ℹ️ About the Models"):
    st.markdown("""
    **Available Models:**
    - **Hybrid Ensemble Model**: Combines multiple algorithms.(Logistic regression + Linear SVM )
    - **Linear SVM Model**: Support Vector Machine.
    - **Logistic Regression Model**: Linear probabilistic model.
    """)

with st.expander("📋 How to Use"):
    st.markdown("""
    1. Select a Model from the sidebar.
    2. Enter an SMS message manually or use the generator.
    3. Click "Classify" to see the prediction.
    """)

# --- Footer ---
st.markdown("---")
st.caption("📱 SMS Spam Classification App")
