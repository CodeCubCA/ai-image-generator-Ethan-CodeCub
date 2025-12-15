import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
import io
import random
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
# Try to get token from Streamlit secrets first (for HF Spaces), then fall back to .env
try:
    HUGGINGFACE_TOKEN = st.secrets.get("HUGGINGFACE_TOKEN", os.getenv("HUGGINGFACE_TOKEN"))
except:
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

MODEL_NAME = "black-forest-labs/FLUX.1-schnell"

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Initialize image history in session state (must be before sidebar)
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

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
    "All Styles": ", use the best artistic style choice for this subject, highly detailed, professional quality",
    "None": "",
    "Anime": ", anime style, vibrant colors, Studio Ghibli inspired, detailed illustration",
    "Realistic": ", photorealistic, highly detailed, 8K resolution, professional photography",
    "Digital Art": ", digital painting, artstation trending, concept art, highly detailed",
    "Watercolor": ", watercolor painting, soft colors, artistic, gentle brushstrokes",
    "Oil Painting": ", oil painting, classical art, textured, rich colors, fine art",
    "3D Render": ", 3D render, CGI, octane render, unreal engine, photorealistic 3D",
    "Sketch/Pencil": ", pencil sketch, hand-drawn, detailed line art, graphite drawing",
    "Cyberpunk": ", cyberpunk style, neon lights, futuristic, sci-fi, dark atmosphere",
    "Fantasy": ", fantasy art, magical, enchanted, epic, mystical atmosphere"
}

selected_style = st.sidebar.selectbox(
    "Art Style:",
    options=list(art_styles.keys()),
    index=0,
    help="Select an art style to automatically apply to your prompt"
)

# Image size options
st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 Image Size")

image_sizes = {
    "Square (1024x1024)": (1024, 1024),
    "Portrait (768x1024)": (768, 1024),
    "Landscape (1024x768)": (1024, 768),
    "Wide (1280x720)": (1280, 720),
    "Ultra Wide (1920x1080)": (1920, 1080),
    "Small Square (512x512)": (512, 512)
}

selected_size = st.sidebar.selectbox(
    "Image Dimensions:",
    options=list(image_sizes.keys()),
    index=0,
    help="Choose the size of the generated image"
)

# Random prompt generator
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎲 Random Generation")

random_prompts = [
    "A majestic mountain landscape at golden hour",
    "A cozy coffee shop on a rainy day",
    "A futuristic cityscape with flying cars",
    "A magical forest with glowing mushrooms",
    "A peaceful beach at sunset",
    "A steampunk airship in the clouds",
    "A dragon sleeping on a pile of treasure",
    "A astronaut exploring an alien planet",
    "A Japanese garden with cherry blossoms",
    "A medieval castle on a cliff",
    "A cyberpunk street with neon signs",
    "A lighthouse during a storm",
    "A fantasy library with floating books",
    "A vintage car on route 66",
    "A underwater coral reef city",
    "A snowy cabin in the woods",
    "A hot air balloon over countryside",
    "A mystical portal in ancient ruins",
    "A robot reading in a library",
    "A treehouse village in giant trees"
]

if st.sidebar.button("🎲 Generate Random Image", help="Click to generate a random image with random style and size"):
    st.session_state.random_mode = True
    st.session_state.random_prompt = random.choice(random_prompts)
    st.session_state.random_style = random.choice(list(art_styles.keys()))
    st.session_state.random_size = random.choice(list(image_sizes.keys()))
    st.rerun()

# Additional sidebar options
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Tips")
st.sidebar.markdown("""
- Choose a style and size above
- Describe your subject clearly
- Add details about colors and lighting
- Click the dice for random generation
""")

# Image History in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🖼️ Image History")

if len(st.session_state.image_history) > 0:
    st.sidebar.markdown(f"**{len(st.session_state.image_history)} images saved**")

    if st.sidebar.button("🗑️ Clear All History"):
        st.session_state.image_history = []
        st.rerun()

    # Toggle to show/hide history
    if 'show_history' not in st.session_state:
        st.session_state.show_history = False

    if st.sidebar.button("📂 View Image History" if not st.session_state.show_history else "📂 Hide Image History"):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()

    # Show history if toggled
    if st.session_state.show_history:
        st.sidebar.markdown("---")
        for idx, img_data in enumerate(st.session_state.image_history):
            with st.sidebar.expander(f"Image {idx + 1}", expanded=False):
                st.image(img_data['image'], use_column_width=True)
                st.write(f"**Style:** {img_data['style']}")
                st.write(f"**Size:** {img_data['size']}")
                timestamp = img_data['timestamp'].strftime("%I:%M:%S %p")
                st.write(f"**Time:** {timestamp}")

                # Show prompt
                if len(img_data['prompt']) > 50:
                    st.write(f"**Prompt:** {img_data['prompt'][:50]}...")
                else:
                    st.write(f"**Prompt:** {img_data['prompt']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥",
                        data=img_data['image_bytes'],
                        file_name=f"image_{idx+1}.png",
                        mime="image/png",
                        key=f"sidebar_download_{idx}"
                    )
                with col2:
                    if st.button("🗑️", key=f"delete_{idx}"):
                        st.session_state.image_history.pop(idx)
                        st.rerun()
else:
    st.sidebar.info("No images yet. Generate some!")

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

# Check if random mode is activated
if 'random_mode' in st.session_state and st.session_state.random_mode:
    generate_button = True
    prompt = st.session_state.random_prompt
    selected_style = st.session_state.random_style
    selected_size = st.session_state.random_size
    st.session_state.random_mode = False

    # Display what was randomly selected
    st.info(f"🎲 **Random Generation Mode**\n\n**Prompt:** {prompt}\n\n**Style:** {selected_style}\n\n**Size:** {selected_size}")

# Image generation logic
if generate_button:
    if not prompt.strip():
        st.warning("⚠️ Please enter a description for your image!")
    else:
        try:
            # Combine user prompt with selected style
            style_suffix = art_styles[selected_style]
            if style_suffix:
                full_prompt = f"{prompt}{style_suffix}"
            else:
                full_prompt = prompt

            # Get selected image dimensions
            width, height = image_sizes[selected_size]

            # Show the final prompt being used
            with st.expander("📝 Final Prompt Being Used"):
                st.write(full_prompt)
                st.write(f"**Size:** {width}x{height}")

            with st.spinner("🎨 Generating your image... This may take 10-30 seconds..."):
                # Generate image using InferenceClient
                image = client.text_to_image(
                    prompt=full_prompt,
                    model=MODEL_NAME,
                    width=width,
                    height=height
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

                # Add to image history
                image_data = {
                    'image': image,
                    'prompt': full_prompt,
                    'style': selected_style,
                    'size': selected_size,
                    'timestamp': datetime.now(),
                    'image_bytes': byte_im
                }
                st.session_state.image_history.insert(0, image_data)

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
