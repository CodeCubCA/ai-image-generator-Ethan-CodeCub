---
title: AI Image Generator
emoji: 🎨
colorFrom: red
colorTo: pink
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
---

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zrsH8x_3)

# AI Image Generator

A web application that generates images from text descriptions using HuggingFace's FLUX.1-schnell model and Streamlit.

## Features

- Generate images from text prompts using AI
- Clean and user-friendly interface
- Download generated images
- Real-time loading indicators
- Comprehensive error handling
- Tips for better prompt writing

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your HuggingFace API Token

1. Go to [HuggingFace Settings - Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name (e.g., "Image Generator")
4. Select **"Write"** permissions (or at minimum "Make calls to the serverless Inference API")
5. Click "Generate token"
6. Copy the token (starts with `hf_...`)

**Important:** Read-only tokens will NOT work for the Inference API!

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
HUGGINGFACE_TOKEN=your_token_here
```

Or copy the example file and edit it:

```bash
cp .env.example .env
# Then edit .env and add your token
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage

1. Enter a detailed description of the image you want to generate
2. Click "Generate Image"
3. Wait 10-30 seconds for the AI to generate your image
4. Download the image using the download button

### Tips for Better Results

- **Be specific and descriptive**: Instead of "a cat", try "a fluffy orange cat sitting on a windowsill at sunset"
- **Include style keywords**: "digital art", "photorealistic", "oil painting", "3D render"
- **Mention lighting and colors**: "warm lighting", "vibrant colors", "moody atmosphere"
- **Add composition details**: "close-up portrait", "wide angle landscape", "bird's eye view"

### Example Prompts

- "A serene mountain landscape at sunset with pink and orange skies, digital art style"
- "A futuristic city with neon lights and flying cars, cyberpunk aesthetic"
- "A cozy coffee shop interior with warm lighting, plants, and wooden furniture"
- "A majestic dragon flying over a medieval castle, fantasy art style"

## Model Information

This application uses the **FLUX.1-schnell** model from Black Forest Labs, which offers:
- Fast generation times (10-30 seconds)
- High-quality outputs
- Public accessibility
- Good prompt understanding

## Rate Limits

The HuggingFace free tier has rate limits. If you encounter rate limit errors, wait a few minutes before trying again.

## Troubleshooting

### Authentication Error
- Make sure your token has "Write" permissions
- Verify the token is correctly copied into the `.env` file
- Restart the application after updating the token

### Rate Limit Error
- Wait a few minutes before trying again
- Consider upgrading to HuggingFace Pro for higher limits

### Model Unavailable
- The model might be temporarily down
- Try again in a few minutes
- Check HuggingFace status page

## Technologies Used

- **Streamlit**: Web interface framework
- **HuggingFace Inference API**: AI model hosting
- **FLUX.1-schnell**: Text-to-image AI model
- **Python**: Backend programming language

## License

This project is open source and available for educational purposes.
