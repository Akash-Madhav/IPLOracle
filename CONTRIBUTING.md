# 🤝 Contributing to IPL Oracle

Thank you for your interest in contributing to IPL Oracle! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, browser, Node.js version, Python version)

Example:
```
Title: Backend crashes when querying with empty string

Description:
The backend returns a 500 error when sending an empty query string.

Steps to Reproduce:
1. Start the backend server
2. Send POST request to /ask with {"query": "", "vector": [...]}
3. Observe 500 error

Expected: Return validation error
Actual: Server crashes

Environment: Ubuntu 22.04, Python 3.11, FastAPI 0.121.3
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title**
- **Provide detailed description**
- **Explain current behavior and expected behavior**
- **Include mockups** if suggesting UI changes
- **Explain why this enhancement would be useful**

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Follow coding standards** (see below)
5. **Test your changes**
6. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
7. **Push to your fork** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

#### Pull Request Guidelines

- Keep changes focused and atomic
- Update documentation if needed
- Add tests for new features
- Ensure all tests pass
- Follow the existing code style
- Reference related issues

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Setup Steps

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/IPLOracle.git
cd IPLOracle
```

2. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

3. Set up frontend:
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your configuration
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions small and focused
- Use meaningful variable names

Example:
```python
def calculate_average_runs(player_stats: List[Dict]) -> float:
    """
    Calculate average runs scored by a player.
    
    Args:
        player_stats: List of dictionaries containing player statistics
        
    Returns:
        Average runs as a float
    """
    total_runs = sum(stat['runs'] for stat in player_stats)
    return total_runs / len(player_stats) if player_stats else 0.0
```

### TypeScript/React (Frontend)

- Use TypeScript for type safety
- Follow functional component patterns
- Use React hooks appropriately
- Keep components small and reusable
- Use meaningful component and variable names

Example:
```typescript
interface PlayerCardProps {
  playerName: string;
  runs: number;
  wickets: number;
}

export function PlayerCard({ playerName, runs, wickets }: PlayerCardProps) {
  return (
    <div className="player-card">
      <h3>{playerName}</h3>
      <p>Runs: {runs}</p>
      <p>Wickets: {wickets}</p>
    </div>
  );
}
```

### Commit Messages

Use clear, descriptive commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

Examples:
```
feat: add player comparison feature
fix: resolve crash when query is empty
docs: update API documentation
refactor: simplify embedding generation logic
```

## Testing

### Backend Tests

Run tests:
```bash
cd backend
python test_backend.py
```

Add tests for new features in `test_backend.py`

### Frontend Tests

Currently no automated tests. Manual testing required:
1. Start both backend and frontend
2. Test authentication flow
3. Test query functionality
4. Test error handling

## Documentation

Update documentation when making changes:

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment changes
- Add inline comments for complex logic
- Update API documentation for endpoint changes

## Project Structure

```
IPLOracle/
├── backend/
│   ├── data/              # IPL statistics
│   ├── models/            # Pydantic models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── main.py            # Application entry
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── lib/           # Utilities
│   │   └── App.tsx        # Main app
│   └── public/            # Static assets
└── docs/                  # Documentation
```

## Areas for Contribution

### High Priority

- [ ] Add rate limiting to backend
- [ ] Implement caching for repeated queries
- [ ] Add unit tests for frontend
- [ ] Improve error handling
- [ ] Add loading states for embedding generation

### Medium Priority

- [ ] Add more IPL statistics
- [ ] Implement query history
- [ ] Add export functionality
- [ ] Improve UI/UX design
- [ ] Add dark mode toggle

### Low Priority

- [ ] Add voice input
- [ ] Implement query suggestions
- [ ] Add multi-language support
- [ ] Create mobile app
- [ ] Add data visualization charts

## Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in GitHub Discussions
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to IPL Oracle! 🏏
