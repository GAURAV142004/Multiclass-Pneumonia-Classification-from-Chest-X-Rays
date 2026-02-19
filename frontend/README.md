# Frontend - Pneumonia Detection System

## Overview

React-based medical-grade UI for chest X-ray analysis with responsive design and professional medical styling.

## Architecture

### Components

- **Navbar** - Navigation with auth controls
- **ProtectedRoute** - Authentication wrapper
- **Disclaimer** - Medical disclaimer banner

### Pages

- **Login** - User authentication
- **Signup** - User registration
- **Dashboard** - Main landing page with system overview
- **Upload** - X-ray image upload interface
- **Results** - Prediction results with images
- **Profile** - User profile and scan history

### Services

- **api.js** - Axios-based API client
  - Request/response interceptors
  - JWT token management
  - Error handling

### Context

- **AuthContext** - Global authentication state
  - User session management
  - Login/logout functions
  - Token persistence

## Styling

### TailwindCSS Configuration

Custom medical theme:
```js
colors: {
  medical: {
    primary: '#1e40af',
    secondary: '#3b82f6',
    accent: '#60a5fa',
    dark: '#1e3a8a',
    light: '#dbeafe',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
  }
}
```

### Design Principles

- Clinical color palette (blues, grays, white)
- Clear typography with Inter font
- High contrast for readability
- Professional, not casual
- Consistent spacing and shadows

## Key Features

### Authentication Flow

1. User signs up with email/password
2. Backend returns JWT token
3. Token stored in localStorage
4. Automatically attached to API requests
5. Auto-redirect on 401 errors

### Upload Flow

1. User selects X-ray image
2. Client validates file (type, size)
3. Preview displayed
4. Upload with progress tracking
5. Redirect to results on completion

### Results Display

- Prediction label with confidence
- Original vs segmented images
- Stage information
- Probability breakdowns
- Clinical interpretation
- Medical disclaimer

## API Integration

### Base Configuration

```js
const API_BASE_URL = 'http://localhost:8000';
```

Override with environment variable:
```env
VITE_API_URL=http://your-backend-url
```

### Endpoints Used

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`
- `GET /api/v1/users/history`
- `POST /api/v1/inference/predict`

## State Management

### Local State (useState)
- Form inputs
- Loading states
- Error messages
- File uploads

### Global State (Context)
- User authentication
- Current user data
- Session persistence

### Router State
- Results data passed via `navigate()`
- Prevents unnecessary API calls

## Running the Frontend

### Development
```powershell
npm run dev
```
Runs on: `http://localhost:3000`

### Production Build
```powershell
npm run build
npm run preview
```

### Linting
```powershell
npm run lint
```

## Environment Variables

Create `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

## File Upload Handling

### Validation
- File types: JPEG, JPG, PNG
- Max size: 10MB
- Client-side validation before upload

### Preview
- ObjectURL for instant preview
- Cleanup on component unmount

### Progress Tracking
- Axios onUploadProgress callback
- Visual progress bar
- Status updates

## Error Handling

### Network Errors
- Caught in API interceptors
- User-friendly error messages
- Automatic token refresh (401)

### Form Validation
- Client-side validation
- Server error display
- Field-specific feedback

### Image Upload Errors
- File type validation
- Size limit checks
- Backend error messages

## Responsive Design

### Breakpoints (TailwindCSS)
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

### Mobile Considerations
- Touch-friendly buttons
- Responsive grid layouts
- Stacked mobile views
- Accessible navigation

## Performance Optimization

### Code Splitting
- React Router lazy loading
- Dynamic imports for heavy components

### Image Optimization
- Base64 encoding from backend
- Lazy image loading
- Thumbnail generation

### Bundle Size
- Tree shaking enabled
- Production builds optimized
- Dependencies minimized

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Focus indicators
- Color contrast compliance

## Troubleshooting

### CORS Errors
- Check backend CORS configuration
- Verify API URL in `.env`
- Check browser console

### Authentication Issues
- Clear localStorage
- Check token expiration
- Verify backend is running

### Build Errors
```powershell
# Clean install
Remove-Item -Recurse -Force node_modules
npm install
```

### API Connection
```powershell
# Test backend
curl http://localhost:8000/health
```

## Development Tips

### Hot Module Replacement
- Vite provides instant HMR
- Changes reflect immediately
- State preserved during updates

### Component Structure
```jsx
// Recommended pattern
const Component = () => {
  // Hooks
  // Event handlers
  // Effects
  // Render
};
```

### API Calls
```jsx
// Always handle loading and errors
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');

try {
  setLoading(true);
  const response = await api.method();
  // Handle success
} catch (err) {
  setError(err.message);
} finally {
  setLoading(false);
}
```

## Deployment

### Build for Production
```powershell
npm run build
```

Output: `dist/` directory

### Deploy Options
- Vercel (recommended)
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Custom server (Nginx)

### Environment Configuration
Set production `VITE_API_URL` in hosting platform

## Future Enhancements

- [ ] Offline support (PWA)
- [ ] Image zoom/pan functionality
- [ ] Batch upload
- [ ] Export reports as PDF
- [ ] Dark mode
- [ ] Multi-language support
