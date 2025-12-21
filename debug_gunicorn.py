#!/usr/bin/env python3
import os
import sys
import subprocess

print("=== DEBUG GUNICORN START ===")
print(f"PORT: {os.environ.get('PORT')}")
print(f"PWD: {os.getcwd()}")
print(f"Python: {sys.executable}")
print(f"Files: {os.listdir('.')}")

# Test WSGI import
try:
    sys.path.insert(0, os.getcwd())
    from fusion_force.wsgi import application
    print("✓ WSGI imports successfully!")
except ImportError as e:
    print(f"✗ WSGI import FAILED: {e}")
    # Show fusion_force directory
    if os.path.exists('fusion_force'):
        print(f"fusion_force contents: {os.listdir('fusion_force')}")
    sys.exit(1)

# Run gunicorn with verbose output
cmd = [
    sys.executable, '-m', 'gunicorn',
    'fusion_force.wsgi:application',
    '--bind', f'0.0.0.0:{os.environ.get("PORT", "8000")}',
    '--workers', '1',
    '--access-logfile', '-',
    '--error-logfile', '-',
    '--log-level', 'debug'
]

print(f"\nCommand: {' '.join(cmd)}")
print("Starting Gunicorn...\n")

# Run and stream output
proc = subprocess.Popen(cmd, 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,
                       text=True,
                       bufsize=1,
                       universal_newlines=True)

# Stream output
for line in proc.stdout:
    print(line, end='')

# Wait
proc.wait()
print(f"\nGunicorn exited with code: {proc.returncode}")