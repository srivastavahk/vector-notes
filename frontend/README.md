# Audio Scribe AI (A fronted web-application) 📝

A modern, secure, and intelligent note-taking application built with React. Features include AI-powered semantic search, speech-to-text input, and a clean, responsive interface following GNOME Human Interface Guidelines.

![NotesApp Screenshot](https://via.placeholder.com/800x400/3b82f6/ffffff?text=NotesApp+Dashboard)

## ✨ Features

- **🔐 Secure Authentication** - User registration and login via Supabase
- **📝 Rich Note Management** - Create, edit, delete notes with tags
- **🎤 Speech-to-Text** - Voice input for note content (client-side)
- **🔍 Semantic Search** - AI-powered intelligent note search
- **📱 Responsive Design** - Optimized for desktop, tablet, and mobile
- **🎨 Modern UI** - Clean interface following GNOME guidelines
- **⚡ Real-time Updates** - Instant feedback and notifications
- **🏷️ Tag System** - Organize notes with custom tags
- **🌙 Loading States** - Smooth user experience with proper loading indicators

## 🛠️ Tech Stack

- **Framework**: React 18 (LTS)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **Authentication**: Supabase
- **Icons**: Lucide React
- **State Management**: React Context API
- **Speech Recognition**: Web Speech API

## 🚀 Quick Start

### Prerequisites

- Node.js (v18+ LTS)
- npm or yarn
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd notesapp-frontend
   ```

2. **Install dependencies**
   ```bash
   # Install React 18 LTS
   npm install react@^18.2.0 react-dom@^18.2.0

   # Install other dependencies
   npm install react-router-dom@^6.8.0 lucide-react@^0.263.1 @supabase/supabase-js@^2.38.0

   # Install dev dependencies
   npm install -D tailwindcss@^3.3.0 postcss@^8.4.29 autoprefixer@^10.4.15

   # Initialize Tailwind CSS
   npx tailwindcss init -p
   ```

3. **Environment Setup**

   Create `.env.local` in the root directory:
   ```env
   # Supabase Configuration
   VITE_SUPABASE_URL=your_supabase_project_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

   # Backend API Configuration
   VITE_API_BASE_URL=http://localhost:8000

   # App Configuration
   VITE_APP_NAME=NotesApp
   VITE_APP_VERSION=1.0.0
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
src/
├── components/
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Modal.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ConfirmDialog.jsx
│   ├── forms/                  # Form components
│   │   ├── AuthForm.jsx
│   │   ├── NoteForm.jsx
│   │   └── TextareaWithSpeech.jsx
│   ├── notes/                  # Note-related components
│   │   ├── NoteCard.jsx
│   │   └── NoteList.jsx
│   ├── layout/                 # Layout components
│   │   └── Header.jsx
│   ├── auth/                   # Authentication components
│   │   └── ProtectedRoute.jsx
│   └── notifications/          # Notification system
│       ├── Toast.jsx
│       └── ToastContainer.jsx
├── contexts/                   # React contexts
│   ├── AuthContext.jsx
│   └── ToastContext.jsx
├── hooks/                      # Custom hooks
│   ├── useSpeechToText.js
│   └── useApi.js
├── pages/                      # Page components
│   ├── Dashboard.jsx
│   └── AuthPage.jsx
├── services/                   # External services
│   ├── api.js
│   └── supabase.js
├── utils/                      # Utility functions
│   ├── constants.js
│   ├── helpers.js
│   └── validation.js
├── styles/                     # Global styles
│   └── globals.css
├── App.jsx                     # Main app component
└── main.jsx                    # App entry point
```

## 🔧 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## 🌐 Backend API Integration

The frontend connects to a FastAPI backend. Update the API base URL in your `.env.local`:

```env
# Development
VITE_API_BASE_URL=http://localhost:8000

# Production
VITE_API_BASE_URL=https://your-backend-api.vercel.app
```

### API Endpoints Used

- `POST /notes/` - Create a new note
- `GET /notes/` - Get all notes (paginated)
- `GET /notes/{id}` - Get specific note
- `PUT /notes/{id}` - Update note
- `DELETE /notes/{id}` - Delete note
- `GET /notes/search?q=query` - Semantic search

## 🔐 Authentication

The app uses Supabase for authentication. Set up your Supabase project:

1. Create a new project at [supabase.com](https://supabase.com)
2. Get your project URL and anon key from Settings > API
3. Add them to your `.env.local` file
4. Enable email authentication in Supabase dashboard

## 🎤 Speech-to-Text Feature

The app includes client-side speech recognition:

- **Supported Browsers**: Chrome, Edge, Safari
- **Languages**: English (US) by default
- **Privacy**: All processing happens in the browser
- **Usage**: Click the microphone icon in note forms

## 📱 Responsive Design

The app is fully responsive and tested on:

- **Desktop**: 1920x1080, 1366x768
- **Tablet**: iPad (768x1024), iPad Pro (1024x1366)
- **Mobile**: iPhone (375x667), Android (360x640)

## 🎨 Design Guidelines

Follows GNOME Human Interface Guidelines:

- **Typography**: Clear hierarchy with consistent spacing
- **Colors**: Accessible contrast ratios
- **Interactions**: Intuitive gestures and feedback
- **Layout**: Grid-based responsive design
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy using CLI**
   ```bash
   vercel
   ```

3. **Or connect GitHub repository**
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Add environment variables in dashboard
   - Deploy automatically

4. **Environment Variables in Vercel**
   Add these in your Vercel dashboard:
   ```
   VITE_SUPABASE_URL=your_production_supabase_url
   VITE_SUPABASE_ANON_KEY=your_production_anon_key
   VITE_API_BASE_URL=your_production_api_url
   VITE_APP_NAME=NotesApp
   VITE_APP_VERSION=1.0.0
   ```

### Deploy to Netlify

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy dist folder** to Netlify

3. **Set environment variables** in Netlify dashboard

## 🔧 Development Guide

### Adding New Components

1. Create component in appropriate directory under `src/components/`
2. Follow naming convention: `ComponentName.jsx`
3. Export as default export
4. Add PropTypes if using TypeScript later
5. Include in appropriate index file if needed

### State Management

- **Global State**: Use React Context (`AuthContext`, `ToastContext`)
- **Local State**: Use `useState` hook
- **Server State**: Use custom `useApi` hook
- **Form State**: Use controlled components

### Styling Guidelines

- Use Tailwind utility classes
- Follow mobile-first responsive design
- Maintain consistent spacing (4px base unit)
- Use semantic color names
- Test accessibility with screen readers

## 🧪 Testing

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Note CRUD operations
- [ ] Search functionality
- [ ] Speech-to-text feature
- [ ] Responsive design on all devices
- [ ] Error handling and loading states
- [ ] Keyboard navigation
- [ ] Screen reader compatibility

### Automated Testing (Future)

```bash
# Install testing dependencies
npm install -D @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm run test
```

## 📚 API Documentation

For backend API documentation, refer to:
- FastAPI automatic docs: `http://localhost:8000/docs`
- Redoc documentation: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Use Prettier for formatting
- Follow ESLint rules
- Use meaningful variable names
- Add comments for complex logic
- Keep components small and focused

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**1. Dependency conflicts with React versions**
```bash
npm install react@^18.2.0 react-dom@^18.2.0 --force
```

**2. Supabase connection issues**
- Check environment variables in `.env.local`
- Verify Supabase project settings
- Check browser network tab for errors

**3. Speech recognition not working**
- Ensure HTTPS in production
- Check browser compatibility
- Allow microphone permissions

**4. Tailwind styles not loading**
```bash
npx tailwindcss init -p
```

### Getting Help

- 📧 Email: support@notesapp.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/notesapp-frontend/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/notesapp-frontend/discussions)

## 🔄 Changelog

### v1.0.0 (2025-08-24)
- Initial release
- Authentication system
- CRUD operations for notes
- Speech-to-text functionality
- Semantic search integration
- Responsive design
- Toast notification system

---

**Built with ❤️ using React and modern web technologies**
