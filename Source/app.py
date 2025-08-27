from flask import Flask, request, render_template, jsonify, url_for
from groq_client import generate_image_prompt
import os
import uuid
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src", "uploads"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Limit uploads to 16MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_prompt():
    """API endpoint to generate prompts from images"""
    try:
        prompt_style = request.form.get(
            "style", "detailed"
        )  # Default to detailed style

        # Define the prompt template based on selected style
        prompt_templates = {
            "detailed": (
                "Analyze this image and generate a detailed, cinematic, professional prompt "
                "that captures its artistic style, mood, lighting, composition, and subject matter. "
                "Include any references to existing products, movies, or art styles that the image resembles. "
                "The prompt should be descriptive enough to recreate a similar image using an image generation AI. "
                "Focus only on visual elements visible in the image. "
                "The output must be the prompt only, without any additional text."
            ),
            "midjourney": (
                "Analyze this image and generate a detailed MidJourney-style prompt that would recreate "
                "this exact image. Include specific style indicators, camera details, lighting description, "
                "mood, and composition. Use the syntax: [subject], [details], [environment], [lighting], "
                "[camera details], [style], [artist reference] --ar [aspect ratio] --v 6. "
                "The output must be the prompt only, without any additional text."
            ),
            "dalle": (
                "Analyze this image and create a detailed DALL-E style prompt that would recreate "
                "this exact image. Focus on subjects, artistic style, color palette, composition, and mood. "
                "Be specific but concise. The output must be the prompt only, without any additional text."
            ),
        }

        question = prompt_templates.get(prompt_style, prompt_templates["detailed"])

        # Check if the request is for a file upload or image URL
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                # Generate unique filename to prevent overwriting
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                logging.info(f"Image saved to {filepath}")

                # Generate prompt from the uploaded image
                prompt = generate_image_prompt(filepath, question)

                if request.headers.get("Accept") == "application/json":
                    return jsonify({"prompt": prompt, "status": "success"})
                else:
                    return render_template("result.html", prompt=prompt)

            else:
                error = "Invalid file type. Please upload an image (png, jpg, jpeg, gif, webp)."
                return jsonify({"error": error, "status": "error"}), 400

        elif "image_url" in request.form:
            image_url = request.form["image_url"]
            if not image_url.startswith(("http://", "https://")):
                error = "Invalid image URL. Must start with http:// or https://"
                return jsonify({"error": error, "status": "error"}), 400

            # Generate prompt from the image URL
            prompt = generate_image_prompt(image_url, question)

            if request.headers.get("Accept") == "application/json":
                return jsonify({"prompt": prompt, "status": "success"})
            else:
                return render_template(
                    "result.html", prompt=prompt, image_url=image_url
                )

        else:
            error = "No image uploaded or URL provided"
            return jsonify({"error": error, "status": "error"}), 400

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


# API documentation route
@app.route("/api", methods=["GET"])
def api_docs():
    """Show API documentation"""
    return render_template("api.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
