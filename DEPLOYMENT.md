# 🚀 Deployment Guide

This guide covers deploying the IPL Oracle application to production.

## Deployment Options

### Option 1: Render (Recommended)

#### Backend Deployment

1. **Create a new Web Service** in Render:
   - Connect your GitHub repository
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**:
   ```
   PINECONE_API_KEY=your_key
   PINECONE_REGION=us-east-1
   PINECONE_CLOUD=aws
   GEMINI_API_KEY=your_key
   ENV=production
   ```

3. **Configure the Service**:
   - Instance Type: Standard (512 MB recommended minimum)
   - Auto-Deploy: Yes
   - Health Check Path: `/health`

#### Frontend Deployment

1. **Create a new Static Site** in Render:
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`

2. **Set Environment Variables**:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   VITE_FIREBASE_API_KEY=your_key
   VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your-project
   VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_id
   VITE_FIREBASE_APP_ID=your_id
   ```

### Option 2: Docker

#### Backend Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t ipl-oracle-backend ./backend
docker run -p 8000:8000 --env-file backend/.env ipl-oracle-backend
```

#### Frontend Dockerfile

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Build and run:
```bash
docker build -t ipl-oracle-frontend ./frontend
docker run -p 80:80 ipl-oracle-frontend
```

### Option 3: Vercel (Frontend Only)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy frontend:
```bash
cd frontend
vercel --prod
```

3. Set environment variables in Vercel dashboard

Backend needs to be deployed separately (use Render, Railway, or AWS Lambda)

## Database Setup

### Initialize Pinecone Index

Before first deployment, run the index builder:

```bash
cd backend
python services/pinecone_build_index.py
```

This creates the `ipl-players` index and uploads all embeddings.

## Environment Variables Reference

### Backend (.env)
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_REGION`: Pinecone region (e.g., us-east-1)
- `PINECONE_CLOUD`: Cloud provider (aws, gcp, or azure)
- `GEMINI_API_KEY`: Google Gemini API key
- `ENV`: Set to "production" in production

### Frontend (.env)
- `VITE_API_URL`: Backend API URL
- `VITE_FIREBASE_API_KEY`: Firebase API key
- `VITE_FIREBASE_AUTH_DOMAIN`: Firebase auth domain
- `VITE_FIREBASE_PROJECT_ID`: Firebase project ID
- `VITE_FIREBASE_STORAGE_BUCKET`: Firebase storage bucket
- `VITE_FIREBASE_MESSAGING_SENDER_ID`: Firebase sender ID
- `VITE_FIREBASE_APP_ID`: Firebase app ID

## Performance Optimization

### Backend
1. Enable caching for repeated queries
2. Use connection pooling for Pinecone
3. Implement rate limiting
4. Monitor memory usage

### Frontend
1. Code splitting for large chunks
2. Lazy load embedding model
3. Implement service workers for offline support
4. Enable gzip compression

## Monitoring

### Health Checks
- Backend: `GET /health`
- Memory usage: `GET /admin/memory`

### Logging
- Check application logs in Render dashboard
- Monitor Pinecone usage in Pinecone console
- Track Gemini API usage in Google Cloud Console

## Troubleshooting

### Backend Issues

**Issue**: Backend starts but crashes after first query
**Solution**: Check PINECONE_API_KEY and GEMINI_API_KEY are set correctly

**Issue**: High memory usage
**Solution**: Reduce batch size in Pinecone queries, enable garbage collection

**Issue**: Slow response times
**Solution**: Check Pinecone region matches your deployment region, optimize vector dimensions

### Frontend Issues

**Issue**: Cannot connect to backend
**Solution**: Verify VITE_API_URL is correct and CORS is configured

**Issue**: Authentication fails
**Solution**: Check Firebase configuration variables

**Issue**: Large bundle size
**Solution**: Implement code splitting, lazy load Transformers.js

## Security Checklist

- [ ] All API keys in environment variables
- [ ] CORS configured with specific origins
- [ ] Rate limiting enabled
- [ ] HTTPS enabled for production
- [ ] Firebase security rules configured
- [ ] Input validation on all endpoints
- [ ] Regular dependency updates

## Scaling

### Horizontal Scaling
- Deploy multiple backend instances behind a load balancer
- Use Redis for session management
- Implement distributed caching

### Vertical Scaling
- Increase instance size for backend
- Optimize vector search with better indexes
- Use CDN for frontend assets

## Cost Optimization

1. **Pinecone**: Use serverless tier for development
2. **Gemini**: Monitor token usage, implement caching
3. **Render**: Use autoscaling to handle traffic spikes
4. **Firebase**: Optimize authentication flows

## Backup and Recovery

1. Regularly backup IPL data CSV
2. Version control for Pinecone indexes
3. Document Firebase configuration
4. Maintain environment variable backups

## Support

For deployment issues, check:
- Application logs
- Render/Vercel build logs
- Browser console for frontend errors
- Network tab for API issues
