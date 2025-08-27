# Image Prompt Generator

An AI-powered web application that analyzes images and generates detailed prompts for image generation tools like DALL-E, Midjourney, or Stable Diffusion. This project is part of a cloud deployment and DevOps demonstration.

## Features

-   Upload images or provide image URLs
-   AI-powered image analysis using Groq API and Llama 4 Scout model
-   Generate detailed, Midjourney-style, or DALL-E optimized prompts
-   RESTful API for integration with other services
-   Containerized for easy deployment

## Getting Started

### Prerequisites

-   Python 3.8 or higher
-   Groq API key (get one at [console.groq.com](https://console.groq.com))

### Installation

1. Clone the repository

```
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment

```
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Set up environment variables

```
cp .env.example .env
```

Edit the `.env` file and add your Groq API key

### Running the Application

```
python Source/app.py
```

Visit `http://localhost:5000` in your browser.

## API Usage

### Generate a prompt from an image file

```bash
curl -X POST http://localhost:5000/generate \
  -H "Accept: application/json" \
  -F "image=@/path/to/image.jpg" \
  -F "style=midjourney"
```

### Generate a prompt from an image URL

```bash
curl -X POST http://localhost:5000/generate \
  -H "Accept: application/json" \
  -F "image_url=https://example.com/image.jpg" \
  -F "style=detailed"
```

## Project Structure

```
.
├── Source/
│   ├── app.py                # Main Flask application
│   ├── groq_client.py        # Groq API client for image analysis
│   ├── static/               # Static assets (CSS, JS)
│   └── templates/            # HTML templates
├── src/
│   └── uploads/              # Uploaded images directory
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Deployment

This application is designed to be deployed on Azure using:

-   Docker containerization
-   Azure Container Registry
-   Azure Container Apps
-   CI/CD with GitHub Actions
-   Infrastructure as Code (Bicep or Terraform)

For detailed deployment instructions, refer to the deployment documentation.

## License

[MIT License](LICENSE)
