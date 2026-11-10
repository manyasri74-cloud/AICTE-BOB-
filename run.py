"""
Quick setup and run script for Travel Planner Agent
Run: python run.py
"""

import subprocess
import sys
import os


def check_python_version():
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required.")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")


def install_requirements():
    print("\n📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
    print("✅ Dependencies installed")


def check_env():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("WATSONX_API_KEY", "")
    project_id = os.getenv("WATSONX_PROJECT_ID", "")

    print("\n🔑 IBM Credentials Check:")
    if api_key and api_key != "your_ibm_cloud_api_key_here":
        print("   ✅ WATSONX_API_KEY is set")
    else:
        print("   ⚠️  WATSONX_API_KEY not configured — running in Demo mode")
        print("      → Sign up at https://cloud.ibm.com/registration")
        print("      → Copy your API key from https://cloud.ibm.com/iam/apikeys")

    if project_id and project_id != "your_watsonx_project_id_here":
        print("   ✅ WATSONX_PROJECT_ID is set")
    else:
        print("   ⚠️  WATSONX_PROJECT_ID not configured")
        print("      → Create a project at https://dataplatform.cloud.ibm.com/wx/home")


def run_app():
    print("\n🌍 Starting Travel Planner Agent (Streamlit)...")
    print("   URL: http://localhost:8501\n")
    os.system(f"{sys.executable} -m streamlit run streamlit_app.py")


if __name__ == "__main__":
    check_python_version()
    install_requirements()
    check_env()
    run_app()
