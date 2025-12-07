import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configuration
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-size: 18px;
        padding: 0.5rem;
        border-radius: 10px;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for style selection
st.sidebar.title("🎨 Style Settings")
st.sidebar.markdown("Choose your preferred art style")

# Art style options
art_styles = {
    "All Styles": "",
    "Digital Art": "digital art style",
    "Oil Painting": "oil painting style",
    "Watercolor": "watercolor painting style",
    "Pastel Drawing": "soft pastel drawing style",
    "Sketch/Pencil": "pencil sketch style",
    "Photorealistic": "photorealistic, high quality photograph",
    "3D Render": "3D render, CGI",
    "Anime/Manga": "anime style illustration",
    "Comic Book": "comic book art style",
    "Pop Art": "pop art style",
    "Abstract": "abstract art style",
    "Impressionist": "impressionist painting style",
    "Cyberpunk": "cyberpunk art style",
    "Fantasy Art": "fantasy art style",
    "Vintage/Retro": "vintage retro art style"
}

selected_style = st.sidebar.selectbox(
    "Art Style:",
    options=list(art_styles.keys()),
    index=0,
    help="Select an art style to automatically apply to your prompt"
)

# Additional sidebar options
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Tips")
st.sidebar.markdown("""
- Choose a style above
- Describe your subject clearly
- Add details about colors and lighting
- The style will be added automatically
""")

# App header
st.title("🎨 AI Image Generator")
st.markdown("Generate stunning images from text descriptions using AI")
st.markdown("---")

# Check if API token is configured
if not HUGGINGFACE_TOKEN:
    st.error("⚠️ HuggingFace API token not found!")
    st.info("""
    **Setup Instructions:**
    1. Go to https://huggingface.co/settings/tokens
    2. Create a new token with 'Write' permissions
    3. Copy the token
    4. Create a `.env` file in the project directory
    5. Add: `HUGGINGFACE_TOKEN=your_token_here`
    6. Restart the application
    """)
    st.stop()

# Initialize the InferenceClient
@st.cache_resource
def get_client():
    return InferenceClient(token=HUGGINGFACE_TOKEN)

client = get_client()

# Main input area
prompt = st.text_area(
    "Enter your image description:",
    placeholder="e.g., A serene landscape with mountains at sunset, digital art style",
    height=100,
    help="Press Enter to generate, Shift+Enter for new line",
    key="prompt_input"
)

# Add custom JavaScript for Enter key behavior
st.markdown("""
    <script>
    const doc = window.parent.document;
    const textArea = doc.querySelector('textarea[aria-label="Enter your image description:"]');
    const generateButton = doc.querySelector('button[kind="primary"]');

    if (textArea) {
        textArea.addEventListener('keydown', function(e) {
            // If Enter is pressed without Shift
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                // Find and click the generate button
                const buttons = doc.querySelectorAll('button');
                buttons.forEach(button => {
                    if (button.textContent.includes('Generate Image')) {
                        button.click();
                    }
                });
            }
            // Shift+Enter will naturally create a new line (default behavior)
        });
    }
    </script>
    """, unsafe_allow_html=True)

# Additional settings in an expander
with st.expander("⚙️ Advanced Settings"):
    st.info(f"**Model:** {MODEL_NAME}")
    st.markdown("""
    **Tips for better results:**
    - Be specific and descriptive
    - Include style keywords (e.g., 'digital art', 'photorealistic', 'oil painting')
    - Mention lighting, colors, and mood
    - Add composition details (e.g., 'close-up', 'wide angle')
    """)

# Generate button
generate_button = st.button("🚀 Generate Image")

# Image generation logic
if generate_button:
    if not prompt.strip():
        st.warning("⚠️ Please enter a description for your image!")
    else:
        try:
            # Combine user prompt with selected style
            style_suffix = art_styles[selected_style]
            if style_suffix:
                full_prompt = f"{prompt}, {style_suffix}"
            else:
                full_prompt = prompt

            # Show the final prompt being used
            with st.expander("📝 Final Prompt Being Used"):
                st.write(full_prompt)

            with st.spinner("🎨 Generating your image... This may take 10-30 seconds..."):
                # Generate image using InferenceClient
                image = client.text_to_image(
                    prompt=full_prompt,
                    model=MODEL_NAME
                )

                # Display the generated image
                st.success("✅ Image generated successfully!")
                st.image(image, caption=f"Generated: {full_prompt}", use_column_width=True)

                # Convert PIL Image to bytes for download
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                # Download button
                st.download_button(
                    label="📥 Download Image",
                    data=byte_im,
                    file_name="generated_image.png",
                    mime="image/png"
                )

        except Exception as e:
            error_message = str(e)

            # Handle specific error cases
            if "authorization" in error_message.lower() or "unauthorized" in error_message.lower():
                st.error("🔒 **Authentication Error**")
                st.error("Your API token is invalid or doesn't have the required permissions.")
                st.info("""
                **Fix:**
                1. Go to https://huggingface.co/settings/tokens
                2. Create a new token with **'Write'** permissions
                3. Update your `.env` file with the new token
                4. Restart the application
                """)
            elif "rate limit" in error_message.lower():
                st.error("⏱️ **Rate Limit Exceeded**")
                st.warning("You've hit the free tier rate limit. Please wait a few minutes and try again.")
            elif "model" in error_message.lower():
                st.error("🤖 **Model Error**")
                st.error(f"There was an issue with the model: {MODEL_NAME}")
                st.info("The model might be temporarily unavailable. Try again in a few moments.")
            else:
                st.error("❌ **Error Generating Image**")
                st.error(f"Error details: {error_message}")
                st.info("Please try again or modify your prompt.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by HuggingFace 🤗 | Built with Streamlit</p>
    <p style='font-size: 12px;'>Using model: black-forest-labs/FLUX.1-schnell</p>
</div>
""", unsafe_allow_html=True)
