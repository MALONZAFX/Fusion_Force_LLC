# test_gunicorn.py
import sys
import subprocess

try:
    # Try to import gunicorn
    import gunicorn
    print(f"✅ Gunicorn version: {gunicorn.__version__}")
except ImportError as e:
    print(f"❌ Gunicorn not installed: {e}")
    sys.exit(1)

# Test if the WSGI application can be imported
try:
    from fusion_force.wsgi import application
    print("✅ WSGI application imported successfully")
except ImportError as e:
    print(f"❌ Cannot import WSGI application: {e}")
    sys.exit(1)

print("✅ All imports successful!")