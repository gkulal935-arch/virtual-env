# 🎮 Virtual Mouse Control System for BBHC Library

This system provides two ways to control your computer mouse using hand gestures through your webcam:

1. **Web-based Virtual Mouse** - Runs in your browser
2. **Python Desktop Application** - Standalone application with advanced features

## 🚀 Quick Start

### Option 1: Web-based Virtual Mouse
1. Navigate to the home page of your BBHC Library Management System
2. Click the **"Virtual Mouse Control"** button
3. Allow camera access when prompted
4. Move your hand in front of the camera to control the mouse
5. Touch your thumb and index finger to click

### Option 2: Python Desktop Application
1. From the virtual mouse page, click **"🐍 Launch Python App"**
2. A standalone desktop application will open
3. Click **"🚀 Start Virtual Mouse"** to begin
4. Use the same hand gestures to control your mouse

## 📋 Features

### Web-based Version
- ✅ Real-time hand tracking
- ✅ Virtual mouse cursor
- ✅ Click gesture recognition
- ✅ Hand skeleton visualization
- ✅ Responsive design
- ✅ No installation required

### Python Desktop Version
- ✅ All web features plus:
- ✅ Adjustable smoothing controls
- ✅ Customizable click threshold
- ✅ Toggle hand landmarks display
- ✅ Real-time camera feed
- ✅ Performance optimization
- ✅ Professional GUI interface

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Webcam
- Modern web browser (for web version)

### Install Python Dependencies
```bash
cd library_Mgt_BBHC
pip install -r virtual_mouse_requirements.txt
```

### Required Packages
- `opencv-python` - Computer vision and camera handling
- `mediapipe` - Hand tracking and gesture recognition
- `pyautogui` - Mouse control automation
- `Pillow` - Image processing
- `numpy` - Numerical operations

## 🎯 How It Works

### Hand Detection
- Uses MediaPipe Hands for real-time hand landmark detection
- Tracks 21 key points on your hand
- Provides smooth, accurate hand positioning

### Mouse Control
- Index finger tip controls cursor position
- Thumb and index finger pinch gesture triggers clicks
- Smooth interpolation for natural movement

### Gesture Recognition
- **Open Hand**: Move mouse cursor
- **Pinch Gesture**: Click (thumb touches index finger)
- **No Hand**: Cursor disappears

## 🔧 Configuration

### Web Version
- Automatically adjusts to your screen size
- Optimized for most webcams
- No additional configuration needed

### Python Version
- **Smoothing**: Adjust cursor movement smoothness (0.1 - 0.9)
- **Click Threshold**: Set distance for click detection (10 - 100 pixels)
- **Landmarks**: Toggle hand skeleton display

## 📱 Usage Instructions

### Basic Operation
1. **Start**: Click the start button or navigate to the virtual mouse page
2. **Position**: Sit 1-2 feet from your webcam
3. **Lighting**: Ensure good, even lighting on your hands
4. **Movement**: Move your hand slowly and deliberately
5. **Click**: Pinch thumb and index finger together

### Advanced Tips
- Keep your hand clearly visible to the camera
- Avoid rapid hand movements for better accuracy
- Use the smoothing controls to reduce jitter
- Adjust click threshold based on your hand size

## 🚨 Troubleshooting

### Common Issues

#### Camera Not Working
- Check camera permissions in your browser/system
- Ensure no other applications are using the camera
- Try refreshing the page or restarting the application

#### Hand Not Detected
- Improve lighting conditions
- Move closer to the camera
- Ensure your hand is fully visible
- Check if MediaPipe is loading correctly

#### Cursor Jumpy
- Reduce hand movement speed
- Increase smoothing factor (Python version)
- Check for camera frame rate issues
- Ensure stable internet connection (web version)

#### Click Not Working
- Adjust click threshold (Python version)
- Ensure thumb and index finger are clearly visible
- Practice the pinch gesture
- Check if pyautogui is working correctly

### Performance Issues
- Close other applications using the camera
- Reduce browser tabs (web version)
- Lower camera resolution if needed
- Check system resources

## 🔒 Security Notes

- Camera access is required for functionality
- No video data is stored or transmitted
- Hand tracking runs locally on your device
- Web version uses secure HTTPS connections

## 🆘 Support

### For Web Version
- Check browser console for errors
- Ensure JavaScript is enabled
- Try different browsers (Chrome recommended)

### For Python Version
- Check Python console for error messages
- Verify all dependencies are installed
- Ensure camera is not in use by other applications

## 🔄 Updates

The system automatically checks for updates to MediaPipe models and will download them as needed. Ensure you have a stable internet connection for the best experience.

## 📄 License

This virtual mouse system is part of the BBHC Library Management System and follows the same licensing terms.

---

**🎉 Enjoy your hands-free computing experience! 🎉**
