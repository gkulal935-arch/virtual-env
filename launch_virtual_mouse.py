#!/usr/bin/env python3
"""
Virtual Mouse Launcher for BBHC Library Management System
This script launches the virtual mouse control application
"""

import subprocess
import sys
import os
from pathlib import Path

def launch_virtual_mouse():
    """Launch the virtual mouse application"""
    try:
        # Get the directory of this script
        script_dir = Path(__file__).parent.absolute()
        virtual_mouse_script = script_dir / "virtual_mouse_app.py"
        
        # Check if the virtual mouse script exists
        if not virtual_mouse_script.exists():
            print(f"Error: Virtual mouse script not found at {virtual_mouse_script}")
            return False
        
        # Launch the virtual mouse application
        print("🚀 Launching Virtual Mouse Control...")
        print("📱 Please allow camera access when prompted")
        print("⌨️  Press 'Q' to quit the application")
        
        # Run the virtual mouse app
        result = subprocess.run([sys.executable, str(virtual_mouse_script)], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Virtual mouse application closed successfully")
        else:
            print(f"⚠️  Virtual mouse application exited with code {result.returncode}")
            
        return True
        
    except FileNotFoundError:
        print("❌ Error: Python interpreter not found")
        return False
    except Exception as e:
        print(f"❌ Error launching virtual mouse: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'cv2', 'mediapipe', 'pyautogui', 'PIL', 'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                from PIL import Image, ImageTk
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install -r {Path(__file__).parent / 'virtual_mouse_requirements.txt'}")
        return False
    
    print("✅ All required packages are installed")
    return True

if __name__ == "__main__":
    print("🎮 BBHC Library Virtual Mouse Control Launcher")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Launch virtual mouse
    success = launch_virtual_mouse()
    
    if not success:
        sys.exit(1)
