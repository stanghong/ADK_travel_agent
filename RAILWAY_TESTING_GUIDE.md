# Railway Backend Testing Guide

## 🚀 Quick Start

### Option 1: Using Environment Variable (Recommended)
```bash
# Set your Railway backend URL
export RAILWAY_BACKEND_URL="https://your-railway-app.railway.app"

# Start the frontend
./start_railway_test.sh
```

### Option 2: Direct Streamlit Run
```bash
# Set environment variable and run
export RAILWAY_BACKEND_URL="https://your-railway-app.railway.app"
streamlit run app_railway.py --server.port 8501 --server.address 0.0.0.0
```

### Option 3: Edit File Directly
1. Open `app_railway.py`
2. Find line 13: `RAILWAY_URL = os.getenv('RAILWAY_BACKEND_URL', 'https://your-railway-app.railway.app')`
3. Replace `'https://your-railway-app.railway.app'` with your actual Railway URL
4. Run: `streamlit run app_railway.py --server.port 8501 --server.address 0.0.0.0`

## 🧪 Testing Steps

### 1. Test Backend Connection
```bash
# Test Railway backend directly
python test_railway_backend.py
```

### 2. Start Frontend
```bash
# Use the automated script
./start_railway_test.sh

# Or manually
streamlit run app_railway.py --server.port 8501 --server.address 0.0.0.0
```

### 3. Access Frontend
- Open browser: http://localhost:8501
- Check the status indicator (green = online, red = offline)
- Try sending a test message

## 🔧 Configuration

### Environment Variables
- `RAILWAY_BACKEND_URL`: Your Railway backend URL (e.g., `https://your-app.railway.app`)

### Frontend Features
- **Real-time Status**: Shows if Railway backend is online/offline
- **Session Management**: Automatically creates and manages sessions
- **Photo Upload**: Supports image analysis
- **Error Handling**: Graceful handling of connection issues

## 📋 Test Scenarios

### Basic Functionality
1. **Health Check**: Frontend should show "✅ Railway Backend Online"
2. **Session Creation**: Should create a session automatically
3. **Message Sending**: Should send messages and receive responses

### Advanced Features
1. **Photo Upload**: Upload an image and ask about it
2. **Weather Queries**: "What's the weather in Paris?"
3. **Tourist Information**: "What are the top attractions in Tokyo?"
4. **Restaurant Recommendations**: "Find restaurants in Rome"
5. **Time Queries**: "What time is it in New York?"

## 🐛 Troubleshooting

### Backend Offline
- Check if your Railway app is running
- Verify the URL is correct
- Check Railway logs for errors

### Session Errors
- Click "🔄 Refresh Session" in the sidebar
- Check if backend session management is working

### Connection Timeouts
- Increase timeout values in the code if needed
- Check network connectivity

### Photo Upload Issues
- Ensure image format is supported (PNG, JPG, JPEG)
- Check if backend supports photo processing

## 📁 Files Overview

- `app_railway.py`: Railway-specific frontend
- `test_railway_backend.py`: Backend connection tester
- `start_railway_test.sh`: Automated startup script
- `RAILWAY_TESTING_GUIDE.md`: This guide

## 🎯 Expected Results

### Successful Test
- ✅ Backend status shows "Online"
- ✅ Session ID is displayed in sidebar
- ✅ Messages are sent and responses received
- ✅ All travel assistant features work

### Common Issues
- ❌ "Backend Offline" - Check Railway URL and app status
- ❌ "Session not found" - Click refresh session
- ❌ "Connection error" - Check network and URL

## 🚀 Next Steps

Once testing is successful:
1. Deploy frontend to Streamlit Cloud or similar
2. Configure production environment variables
3. Set up monitoring and logging
4. Scale backend as needed

## 📞 Support

If you encounter issues:
1. Check Railway app logs
2. Verify environment variables
3. Test backend endpoints directly
4. Check network connectivity 