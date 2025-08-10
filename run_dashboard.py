#!/usr/bin/env python3
"""
NBA Salary Dashboard - Quick Start Script
========================================

This script helps you quickly set up and run the NBA salary dashboard.
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print the dashboard banner"""
    print("🏀" + "=" * 60 + "🏀")
    print("   NBA SALARY DASHBOARD - QUICK START")
    print("🏀" + "=" * 60 + "🏀")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check if requirements.txt exists
        if not Path("requirements.txt").exists():
            print("❌ Error: requirements.txt not found")
            return False
        
        # Install packages
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_files():
    """Check if all required files are present"""
    print("\n📁 Checking required files...")
    
    required_files = [
        "app.py",
        "nba_salary_scraper.py",
        "index.html",
        "style.css",
        "script.js"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def start_dashboard():
    """Start the Flask dashboard"""
    print("\n🚀 Starting NBA Salary Dashboard...")
    print("   Please wait while the server starts...")
    
    try:
        # Set environment variables
        os.environ['FLASK_ENV'] = 'development'
        
        # Import and run the Flask app
        from app import app
        
        print("\n✅ Dashboard is starting!")
        print("🌐 Opening dashboard in your web browser...")
        print("📊 Dashboard URL: http://localhost:5000")
        print("\n" + "=" * 60)
        print("DASHBOARD FEATURES:")
        print("• 💰 Player salary data organized by teams")
        print("• 📊 Interactive charts and visualizations")
        print("• 🏀 Team payroll comparisons")
        print("• 🔍 Player search and filtering")
        print("• 📁 Data export functionality")
        print("• 📈 Salary analysis and insights")
        print("=" * 60)
        print("\n⚠️  Note: Initial data loading may take a few moments")
        print("   The scraper needs to collect salary data from web sources")
        print("\n🛑 To stop the dashboard, press Ctrl+C")
        print()
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open("http://localhost:5000")
            except:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
        return True
    except ImportError as e:
        print(f"\n❌ Error importing Flask app: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        return False

def main():
    """Main function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check required files
    if not check_files():
        print("\n❌ Setup incomplete. Please ensure all files are present.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        print("   Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Start the dashboard
    print("\n🎉 Setup complete! Starting dashboard...")
    start_dashboard()

if __name__ == "__main__":
    main()