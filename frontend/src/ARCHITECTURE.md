# IPL Oracle - Architecture Documentation

## System Overview

IPL Oracle is a production-ready AI-powered cricket chatbot frontend built with React, TypeScript, and modern web technologies. It features client-side semantic search using Transformer models and integrates with a FastAPI backend for IPL-specific query answering.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  (Landing Page, Login, Register, Chat Dashboard)            │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     React Application                        │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Auth Context    │  │  Chat Components │                │
│  │  (Firebase Auth) │  │  (UI & Logic)    │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌──────────────────┐                    ┌──────────────────┐
│  Embeddings Gen  │                    │   Firebase Auth  │
│  (@xenova/trans) │                    │   Service        │
│  Client-side ML  │                    │   (Google Cloud) │
└──────────────────┘                    └──────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend API                              │
│              (FastAPI - iploracle-2wxn.onrender.com)        │
│                                                              │
│  POST /ask                                                   │
│  { query: string, vector: number[384] }                     │
│  ⟶ { query, answer, results }                               │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Authentication Layer

**Files**: 
- `/contexts/AuthContext.tsx`
- `/lib/firebase.ts`
- `/components/Login.tsx`
- `/components/Register.tsx`

**Responsibilities**:
- User authentication (email/password via Firebase)
- Session management and token refresh
- Protected route handling
- User profile management

**Flow**:
```
User → Login Form → Firebase Auth → Auth Context → Protected Routes
```

### 2. Chat Interface Layer

**Files**:
- `/components/ChatDashboard.tsx` (Container)
- `/components/ChatHeader.tsx` (Header with user info)
- `/components/ChatMessage.tsx` (Individual messages)
- `/components/ChatInput.tsx` (Input field)
- `/components/TypingIndicator.tsx` (Loading state)
- `/components/WelcomeScreen.tsx` (First-time UX)

**State Management**:
```typescript
// In ChatDashboard.tsx
const [messages, setMessages] = useState<Message[]>([]);
const [isLoading, setIsLoading] = useState(false);
const [isInitializing, setIsInitializing] = useState(true);
const [error, setError] = useState<string | null>(null);
const [showWelcome, setShowWelcome] = useState(true);
```

**Message Flow**:
```
User Input → ChatInput → handleSendMessage → API Call → Bot Response → ChatMessage
```

### 3. AI/ML Layer

**Files**:
- `/lib/embeddings.ts` (Transformer.js integration)
- `/lib/api.ts` (Backend communication)

**Embeddings Generation**:
```typescript
// Model: Xenova/all-MiniLM-L6-v2
// Dimensions: 384
// Method: Mean pooling with normalization

const pipeline = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
const embedding = await pipeline(text, { pooling: 'mean', normalize: true });
```

**API Communication**:
```typescript
// Request
POST /ask
{
  "query": "Who has the most runs in IPL?",
  "vector": [0.123, -0.456, ...] // 384 dimensions
}

// Response
{
  "query": "Who has the most runs in IPL?",
  "answer": {
    "concise": "Virat Kohli has the most runs...",
    "context": "Additional context...",
    "resources": [...]
  },
  "results": [...]
}
```

### 4. UI/UX Layer

**Design System**:
- **Colors**: IPL-themed orange, purple, blue gradients
- **Effects**: Glassmorphism with backdrop blur
- **Animations**: Motion (motion/react) for smooth transitions
- **Icons**: Lucide React

**Responsive Breakpoints**:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## Data Flow

### User Authentication Flow
```
1. User enters credentials
   ↓
2. Form validation
   ↓
3. Firebase Auth API call
   ↓
4. Auth state update in Context
   ↓
5. Redirect to Chat Dashboard
```

### Chat Message Flow
```
1. User types message and hits send
   ↓
2. Message added to UI immediately (optimistic update)
   ↓
3. Generate 384-dimensional embedding (client-side)
   ↓
4. Send { query, vector } to backend API
   ↓
5. Backend processes with semantic search
   ↓
6. Response received and parsed
   ↓
7. Bot message added to chat history
   ↓
8. UI scrolls to latest message
```

## State Management

### Global State (Context)
- **AuthContext**: User authentication state and methods
  - `user`: Current user object or null
  - `loading`: Auth check in progress
  - `signIn()`: Login method
  - `signUp()`: Registration method
  - `signOut()`: Logout method

### Local State (Component)
- **ChatDashboard**:
  - `messages`: Array of chat messages
  - `isLoading`: API request in progress
  - `isInitializing`: Model loading status
  - `error`: Error message if any
  - `showWelcome`: First-time user screen visibility

## Performance Optimizations

### 1. Code Splitting
- Lazy loading of routes and heavy components
- Dynamic imports for non-critical code

### 2. Model Caching
- Transformer model cached in IndexedDB
- First load: ~150MB download
- Subsequent loads: Instant (from cache)

### 3. Memoization
```typescript
// Example from ChatMessage.tsx
const formattedTime = useMemo(
  () => message.timestamp.toLocaleTimeString(),
  [message.timestamp]
);
```

### 4. Debouncing
- Input debouncing for search/filter operations
- Prevents excessive API calls

### 5. Virtual Scrolling (Future)
- For very long chat histories
- Render only visible messages

## Error Handling Strategy

### 1. Network Errors
```typescript
try {
  const response = await askIPLOracle(query);
} catch (error) {
  // Fallback error message
  setError('Unable to reach IPL Oracle. Please check your connection.');
}
```

### 2. Model Loading Errors
```typescript
try {
  await initEmbeddings();
} catch (error) {
  setError('Failed to initialize AI model. Please refresh the page.');
}
```

### 3. Authentication Errors
```typescript
// In AuthContext.tsx
if (error.code === 'auth/invalid-credential') {
  throw new Error('Invalid email or password');
}
```

### 4. Runtime Errors
- React ErrorBoundary component catches uncaught exceptions
- Displays user-friendly error screen with reload option

## Security Considerations

### 1. Environment Variables
- API URLs stored in `.env` file
- Firebase config in separate file
- Never commit sensitive data to version control

### 2. Input Validation
- Email format validation
- Password strength requirements
- Query sanitization before API calls

### 3. Authentication
- Firebase handles secure token management
- Automatic token refresh
- Protected routes check auth state

### 4. API Communication
- HTTPS only
- CORS configured on backend
- Request/response validation

## Scalability Considerations

### Current Limits
- **Memory**: < 300MB runtime (with model loaded)
- **Messages**: No limit (consider pagination for 1000+ messages)
- **Concurrent Users**: Limited by Firebase free tier

### Future Scaling
1. **Message Pagination**: Load messages in chunks
2. **Model Offloading**: Server-side embeddings generation
3. **Caching**: Redis cache for common queries
4. **CDN**: Static asset delivery via CDN
5. **Load Balancing**: Multiple backend instances

## Testing Strategy

### Unit Tests (Recommended)
- Component rendering tests
- Function logic tests
- API integration tests

### Integration Tests (Recommended)
- Auth flow end-to-end
- Chat flow end-to-end
- Error handling scenarios

### E2E Tests (Recommended)
- Complete user journeys
- Cross-browser testing
- Mobile responsiveness

## Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
# Output: /dist folder
```

### Environment Variables
```env
VITE_API_URL=https://iploracle-2wxn.onrender.com
```

### Hosting Options
- **Vercel**: Zero-config deployment
- **Netlify**: Simple drag-and-drop
- **Firebase Hosting**: Integrated with auth
- **AWS S3 + CloudFront**: Scalable solution

## Monitoring & Analytics

### Recommended Tools
1. **Firebase Analytics**: User behavior tracking
2. **Sentry**: Error monitoring and tracking
3. **LogRocket**: Session replay and debugging
4. **Google Analytics**: Usage metrics

### Key Metrics to Track
- Authentication success/failure rate
- Average response time
- Error frequency by type
- User retention and engagement
- Model initialization time

## Future Enhancements

### Short-term (1-3 months)
- [ ] Voice input support
- [ ] Export chat history
- [ ] Favorite/bookmark questions
- [ ] Response feedback (thumbs up/down)

### Medium-term (3-6 months)
- [ ] Multi-language support
- [ ] Advanced filtering and search
- [ ] Statistical visualizations
- [ ] Share responses on social media

### Long-term (6+ months)
- [ ] Real-time collaborative chats
- [ ] Custom model fine-tuning
- [ ] Integration with IPL official API
- [ ] Mobile app (React Native)

## Troubleshooting Guide

### Common Issues

**Issue**: Model not loading
- **Solution**: Check browser compatibility (need WebAssembly)
- **Solution**: Clear IndexedDB cache and refresh

**Issue**: Authentication errors
- **Solution**: Verify Firebase config in `/lib/firebase.ts`
- **Solution**: Check Firebase console for project status

**Issue**: API timeout
- **Solution**: Check backend status at render.com
- **Solution**: Verify `VITE_API_URL` environment variable

**Issue**: Blank screen after login
- **Solution**: Check browser console for errors
- **Solution**: Clear browser cache and reload

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Monitor Firebase usage and quotas
- Review error logs weekly
- Performance audit quarterly

### Dependency Updates
```bash
# Check for outdated packages
npm outdated

# Update non-breaking changes
npm update

# Update major versions manually
npm install package@latest
```

---

For questions or contributions, contact the development team.
