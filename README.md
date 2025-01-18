# FlyonUI Component Assistant 🎨

An AI-powered assistant that helps generate FlyonUI components from descriptions and images. Built with Streamlit, OpenAI GPT-4 Vision, and OpenCV.

## Features

- 💬 Chat interface for component requests
- 🖼️ Image upload and analysis
- 🎨 Color scheme detection
- 📐 UI element recognition
- 💻 Code generation with FlyonUI components
- 🔄 Persistent chat history

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ragent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

5. Start the PostgreSQL database with pgvector:
```bash
docker-compose up -d
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## Usage

1. **Text-based Generation**
   - Type your component requirements in the chat
   - The assistant will generate FlyonUI component code

2. **Image-based Generation**
   - Upload a UI design image in the sidebar
   - The assistant will analyze the design using OpenCV
   - Request specific components based on the design

3. **Chat History**
   - Your conversation history is preserved
   - Use the "Clear Chat" button to start fresh

## Database Management

- Start database:
```bash
docker-compose up -d
```

- Stop database:
```bash
docker-compose down
```

- View logs:
```bash
docker-compose logs -f
```

## Project Structure

```
ragent/
├── streamlit_app.py    # Main Streamlit application
├── ui_agents.py        # FlyonUI agent implementation
├── docker-compose.yml  # Docker configuration
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

## Troubleshooting

1. **Database Connection Issues**
   - Ensure Docker is running
   - Check if the database container is up: `docker ps`
   - Verify the connection settings in `ui_agents.py`

2. **Image Analysis Issues**
   - Ensure OpenCV is properly installed
   - Check image format (supported: PNG, JPG, JPEG)
   - Verify OpenAI API key is set correctly

## Contributing

Feel free to submit issues and enhancement requests! 