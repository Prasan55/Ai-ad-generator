
# AI Short Ad Generator 🎬

An AI-powered full-stack web application that generates short advertising concepts and explores automated video generation using Google's Gemini and Veo APIs.

The application allows users to provide product information and generate structured advertising scenes, including visual prompts and voiceover scripts. Celery is used for background processing, while FFmpeg is used for video processing and scene assembly.

>
> The core storyboard-generation workflow is implemented. Video generation and final media assembly depend on API availability, quota limits, and successful processing of the individual scene files.

---

## 🚀 Features

- Generate AI-powered advertising concepts from product information.
- Generate structured scene-based ad storyboards.
- Generate visual prompts for individual scenes.
- Generate voiceover scripts for advertising scenes.
- Integrate Google Gemini API for AI content generation.
- Integrate Google Veo API for AI video generation.
- Use Celery for asynchronous background processing.
- Use temporary files to manage generated video scenes.
- Combine generated video scenes using FFmpeg.
- Track the status of the advertising generation process.

---

## 🛠️ Tech Stack

### Frontend

- React.js
- JavaScript
- HTML5
- TailwindCSS

### Backend

- Python
- Django
- Django REST Framework

### AI & Processing

- Google Gemini API
- Google Veo API
- Celery
- Redis
- FFmpeg

### Storage

- Temporary file storage using Python's `tempfile`
- Local media storage for generated files (depending on configuration)

---

## 🏗️ Project Architecture

```text
React Frontend
      |
      | HTTP Request
      v
Django REST Framework
      |
      v
Create AdGeneration Record
      |
      v
Celery Background Task
      |
      v
Gemini API
      |
      v
Generate Structured Storyboard
      |
      v
Validate Scene Data
      |
      v
Generate Individual Video Scenes
      |
      v
Google Veo API
      |
      v
Download Generated Scene Files
      |
      v
Temporary MP4 Files
      |
      v
FFmpeg
      |
      v
Final Advertisement Video
```

---

## 📁 Project Workflow

### 1. User submits product information

The user provides information such as:

- Product name
- Product description
- Target audience
- Advertising platform
- Advertising tone
- Desired duration

### 2. Generate advertising storyboard

The backend sends the product information to the Gemini API.

Gemini generates structured scene data containing information such as:

```json
{
  "title": "Level Up Your Dorm",
  "concept": "A short gaming advertisement for students",
  "total_duration": 10,
  "target_audience": "Students",
  "platform": "Instagram",
  "scenes": [
    {
      "scene_number": 1,
      "duration": 5,
      "visual_prompt": "A student playing a game in a dorm room",
      "voiceover": "Upgrade your gaming experience."
    }
  ]
}
```

The generated response is validated using Pydantic models before further processing.

### 3. Generate video scenes

Each scene is processed through the video-generation workflow.

The Veo API is used to generate video content based on the scene's visual prompt.

The generated video is saved as a temporary MP4 file using Python's `tempfile` module.

### 4. Combine video scenes

FFmpeg is used to combine the generated scene files into a single video.

The application creates a concat file containing the paths to the individual scene videos.

### 5. Final video processing

The generated scenes are assembled into a final advertising video.

> Note: The current implementation is focused on the scene-generation and video-assembly workflow. Voiceover audio mixing and other post-processing features may require additional implementation.

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Node.js and npm
- Redis
- FFmpeg
- Git

You also need a Google API key with access to the Gemini/Veo APIs you intend to use.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

cd YOUR_REPOSITORY
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Backend setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the backend directory.

Example:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

GEMINI_API_KEY=your_google_api_key

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

> Never commit your real API keys or secret keys to GitHub.
>
> The environment variable names above are examples. Use the exact names configured in your Django settings and Gemini service.

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Start the Django development server

```bash
python manage.py runserver
```

The backend will run at:

```text
http://127.0.0.1:8000/
```

### 6. Start Redis

Make sure Redis is running locally or that your configured Redis server is accessible.

### 7. Start Celery worker

The command depends on your project structure.

Example for Windows:

```bash
celery -A your_project worker --pool=solo -l info
```

Example for Linux/macOS:

```bash
celery -A your_project worker -l info
```

Replace `your_project` with the Django project package containing your Celery configuration.

### 8. Frontend setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

---

## 🔑 API Workflow

The application follows an asynchronous processing approach.

```text
POST /api/generate-ad/
        |
        v
Create AdGeneration
        |
        v
Dispatch Celery Task
        |
        v
Gemini Storyboard Generation
        |
        v
Veo Scene Generation
        |
        v
FFmpeg Scene Assembly
        |
        v
Update Generation Status
```

The actual endpoint URLs depend on the project's Django URL configuration.

---

## 📦 Temporary File Handling

Generated scene videos are temporarily stored on the server using Python's `tempfile` module.

Example:

```python
import tempfile

temp_file = tempfile.NamedTemporaryFile(
    suffix=".mp4",
    delete=False
)

temp_file.close()
```

The generated video is then downloaded into the temporary file.

Temporary files are removed after the scene assembly workflow completes.

> For production deployment, temporary files should be managed carefully, particularly when Celery workers run on different machines or containers. Shared storage or object storage may be required.

---

## 🎞️ FFmpeg Processing

FFmpeg is used to combine generated video scenes.

The application creates a concat file containing the scene video paths.

Example:

```text
file '/path/to/scene_1.mp4'
file '/path/to/scene_2.mp4'
file '/path/to/scene_3.mp4'
```

The FFmpeg concat demuxer is then used to combine the scene files.

Example command:

```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy final_file.mp4
```

The `-c copy` option avoids re-encoding when the input files are compatible.

If the scene files have incompatible formats, codecs, or stream configurations, video normalization or re-encoding may be required.

---

## ⚠️ Current Limitations

- Video generation depends on the availability and usage limits of the Google Gemini and Veo APIs.
- API rate limits may prevent multiple scenes from being generated simultaneously.
- Temporary local storage is not suitable for all deployment environments.
- Voiceover audio generation and synchronization may require additional implementation.
- Final video assembly depends on successful generation of all required scene files.
- Video processing and output storage may need further optimization for production deployment.

---


---

## 📚 Learning Objectives

This project was developed to explore:

- Full-stack web application development.
- Django REST Framework API design.
- Asynchronous background processing with Celery.
- Integration of generative AI APIs.
- Structured AI output validation.
- Video processing using FFmpeg.
- Temporary file management in Python.
- Handling long-running tasks and API limitations.
- Designing an extensible AI-powered application architecture.

---

## 🔒 Security Notes

- Keep API keys in environment variables.
- Do not commit `.env` files containing secrets.
- Use appropriate Django security settings for production.
- Validate user input before processing.
- Handle external API errors safely.
- Configure appropriate permissions for generated media.
- Avoid exposing sensitive server paths in API responses.

---

## 👨‍💻 Author

**Prasanna Karki**

GitHub: (https://github.com/Prasan55)

---

## 📄 License

This project is intended for learning and portfolio development.
