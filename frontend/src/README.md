# IPL Oracle - AI-Powered Cricket Intelligence Chatbot

A modern, production-ready React + TypeScript frontend for an AI-powered IPL chatbot featuring real-time semantic search, Firebase authentication, and a futuristic glassmorphism design.

## 🏏 Features

### Core Functionality
- **AI-Powered Chat Interface**: Ask any question about IPL cricket and get intelligent, contextual answers
- **Semantic Search**: Uses 384-dimensional embeddings (sentence-transformers/all-MiniLM-L6-v2) for accurate query understanding
- **Stat-Agnostic Design**: Handles any IPL-related query without hardcoded assumptions
- **Real-time Responses**: Fast, streaming-like chat experience with typing indicators
- **Structured Responses**: Supports both plain text and rich structured answers with sources

### Authentication
- **Firebase Integration**: Secure email/password authentication
- **Protected Routes**: Automatic redirect to login for unauthenticated users
- **User Management**: Sign up, sign in, and sign out functionality
- **Profile Display**: Shows user's display name and email in the dashboard

### UI/UX
- **Modern Design**: Dark mode with glassmorphism effects and backdrop blur
- **IPL Theming**: Orange (#f97316), purple (#9333ea), and blue (#3b82f6) gradient accents
- **Smooth Animations**: Motion (formerly Framer Motion) animations throughout
- **Responsive Layout**: Optimized for desktop, tablet, and mobile devices
- **Welcome Screen**: First-time user experience with example questions
- **Error Handling**: Comprehensive error boundaries and user-friendly error messages

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- Firebase project configured (credentials in `/lib/firebase.ts`)
- Backend API running at `https://iploracle-2wxn.onrender.com`

### Installation

1. **Clone and install dependencies**:
```bash
npm install
```

2. **Configure environment variables**:
Create a `.env` file in the root directory:
```env
VITE_API_URL=https://iploracle-2wxn.onrender.com
```

3. **Run development server**:
```bash
npm run dev
```

4. **Build for production**:
```bash
npm run build
```

## 📁 Project Structure

```
/
├── components/
│   ├── AnimatedBackground.tsx    # Gradient background animation
│   ├── ChatDashboard.tsx         # Main chat interface container
│   ├── ChatHeader.tsx            # Header with user info and sign out
│   ├── ChatInput.tsx             # Message input with send button
│   ├── ChatMessage.tsx           # Individual message component
│   ├── ErrorBoundary.tsx         # Global error handling
│   ├── IPLDisclaimer.tsx         # Information disclaimer
│   ├── LandingPage.tsx           # Marketing landing page
│   ├── Login.tsx                 # Login form
│   ├── Register.tsx              # Registration form
│   ├── TypingIndicator.tsx       # Bot typing animation
│   └── WelcomeScreen.tsx         # First-time user screen
├── contexts/
│   └── AuthContext.tsx           # Firebase authentication context
├── lib/
│   ├── api.ts                    # Backend API integration
│   ├── embeddings.ts             # Local embeddings generation
│   └── firebase.ts               # Firebase configuration
├── App.tsx                       # Main application component
├── vite-env.d.ts                 # TypeScript environment types
└── README.md                     # This file
```

## 🔧 Technical Details

### Frontend Stack
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Motion (motion/react)** for animations
- **Lucide React** for icons

### AI/ML Integration
- **@xenova/transformers**: Browser-based Transformer.js for embeddings
- **Model**: Xenova/all-MiniLM-L6-v2 (384 dimensions)
- **Processing**: Client-side embedding generation (< 300MB memory)

### Backend Integration
- **Endpoint**: POST `/ask`
- **Request**: `{ query: string, vector: number[] }`
- **Response**: `{ query: string, answer: string | object, results: array }`

### Authentication
- **Firebase Auth**: Email/password authentication
- **Session Management**: Automatic token refresh and persistence
- **Protected Routes**: Context-based authentication checks

## 🎨 Design System

### Colors
- **Primary**: Orange (#f97316) - IPL brand color
- **Secondary**: Purple (#9333ea) - Accent color
- **Tertiary**: Blue (#3b82f6) - Accent color
- **Background**: Slate-950 - Dark background
- **Text**: White/Slate-100 - Primary text

### Effects
- **Glassmorphism**: Frosted glass effect with backdrop blur
- **Gradients**: Multi-color gradients for visual interest
- **Animations**: Smooth transitions and micro-interactions
- **Glow Effects**: Neon-style glows on interactive elements

## 📱 Responsive Design

- **Desktop**: Full-featured layout with sidebar and expanded chat
- **Tablet**: Optimized 2-column layout
- **Mobile**: Single-column stacked layout with touch-optimized controls

## 🔐 Security Considerations

- **Environment Variables**: API keys and secrets stored in environment variables
- **Firebase Security**: Secure authentication with Firebase
- **API Validation**: Input validation and sanitization
- **Error Handling**: Safe error messages without exposing internals

## 🐛 Error Handling

### User-Facing Errors
- Network failures
- API timeouts
- Embedding generation failures
- Authentication errors

### Technical Errors
- Model initialization failures
- Invalid API responses
- Runtime exceptions

### Recovery Strategies
- Automatic retry logic
- Graceful degradation
- User-friendly error messages
- Error boundary fallbacks

## 🚀 Performance Optimization

- **Code Splitting**: Lazy loading of routes and components
- **Memoization**: React.memo and useMemo for expensive operations
- **Debouncing**: Input debouncing for API calls
- **Caching**: Response caching for repeated queries
- **Bundle Size**: Optimized dependencies (< 300MB runtime memory)

## 📊 Usage Examples

### Ask About Stats
```
"Who has the most runs in IPL history?"
"What's the highest team score in an IPL match?"
```

### Ask About Players
```
"Tell me about Virat Kohli's IPL performance"
"Which bowler has the most wickets?"
```

### Ask About Teams
```
"Which team won the most IPL titles?"
"Compare Mumbai Indians and Chennai Super Kings"
```

### Ask About Matches
```
"What happened in the 2019 IPL final?"
"Most memorable IPL matches"
```

## 🔄 Future Enhancements

- [ ] Voice input support
- [ ] Multi-language support
- [ ] Export chat history
- [ ] Favorite questions
- [ ] Share responses
- [ ] Dark/light theme toggle
- [ ] Advanced filters
- [ ] Statistical visualizations

## 📄 License

This project is part of the IPL Oracle system. All rights reserved.

## 🤝 Contributing

This is a private project. For questions or issues, contact the development team.

## 📞 Support

For technical support or questions:
- Check the error logs in the browser console
- Verify Firebase configuration
- Ensure backend API is accessible
- Review environment variables

---

Built with ❤️ for cricket fans worldwide
