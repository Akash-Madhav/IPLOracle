# 🏏 IPL Oracle

IPL Oracle is a full-stack cricket intelligence chatbot that provides intelligent answers to questions about Indian Premier League (IPL) statistics, players, teams, and matches. It uses semantic search powered by Pinecone vector database and Gemini AI for natural language responses.

## 🌟 Features

- **Semantic Search**: Uses Pinecone vector database with embeddings for intelligent search across IPL data
- **AI-Powered Responses**: Gemini 2.5 Flash generates natural, conversational answers
- **Real-time Chat Interface**: Beautiful, responsive React frontend with authentication
- **Client-Side Embeddings**: Generates embeddings in the browser using Transformers.js
- **Fast API Backend**: Python FastAPI backend with async support
- **Firebase Authentication**: Secure user authentication

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (React +      │
│   TypeScript)   │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│   Backend       │
│   (FastAPI)     │
└────────┬────────┘
         │
         ├─────────┐
         │         │
┌────────▼─────┐ ┌▼────────────┐
│  Pinecone    │ │   Gemini    │
│  Vector DB   │ │   AI API    │
└──────────────┘ └─────────────┘
```

## 📁 Project Structure

```
IPLOracle/
├── backend/                 # FastAPI backend
│   ├── data/               # IPL player statistics CSV
│   ├── models/             # Pydantic models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── main.py             # FastAPI application entry
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── lib/            # Utility functions
│   │   └── App.tsx         # Main application
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Pinecone API account
- Google Gemini API key
- Firebase project (for authentication)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_REGION=us-east-1
PINECONE_CLOUD=aws
GEMINI_API_KEY=your_gemini_api_key
```

5. Build the Pinecone index (first time only):
```bash
python services/pinecone_build_index.py
```

6. Run the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```env
VITE_API_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Backend Endpoints

#### `POST /ask`
Query the IPL Oracle with a question.

**Request Body:**
```json
{
  "query": "Who scored the most runs in IPL 2023?",
  "vector": [0.123, 0.456, ...]  // 384-dimensional embedding
}
```

**Response:**
```json
{
  "query": "Who scored the most runs in IPL 2023?",
  "answer": "Shubman Gill scored the most runs in IPL 2023 with 890 runs...",
  "results": [
    {
      "Player_Name": "Shubman Gill",
      "Year": 2023,
      "Runs": 890,
      ...
    }
  ]
}
```

#### `GET /health`
Health check endpoint.

#### `POST /admin/rebuild-index`
Rebuild the Pinecone vector index from the CSV data.

#### `GET /admin/memory`
Get current memory usage statistics.

## 🛠️ Development

### Running Tests

Backend tests:
```bash
cd backend
python test_backend.py
```

### Building for Production

Frontend build:
```bash
cd frontend
npm run build
```

The production build will be in `frontend/build/`

## 🚀 Deployment

### Deploy to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service for the backend
3. Set environment variables in Render dashboard
4. Create a Static Site for the frontend
5. Configure build command: `npm run build`
6. Configure publish directory: `build`
7. **24/7 Backend Keep-Alive (Prevent Idle Sleep)**: Set up a free monitor at [UptimeRobot.com](https://uptimerobot.com) targeting `https://your-backend.onrender.com/health` every 5 minutes so Render never sleeps.

### Environment Variables

Make sure to set all required environment variables in your deployment platform:
- `PINECONE_API_KEY`
- `PINECONE_REGION`
- `PINECONE_CLOUD`
- `GEMINI_API_KEY`
- Firebase configuration variables

## 🔒 Security

- All API keys are stored in environment variables
- Frontend uses Firebase Authentication
- CORS is configured for security
- Input validation on all endpoints
- Regular dependency updates via `npm audit`

## 📊 Data

The IPL player statistics are stored in `backend/data/ipl_players.csv`. The data includes:
- Player names
- Years
- Matches played
- Runs scored
- Wickets taken
- And more statistics

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- IPL for the cricket data
- Pinecone for vector search
- Google Gemini for AI capabilities
- Xenova/Transformers.js for client-side embeddings

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ for cricket fans
