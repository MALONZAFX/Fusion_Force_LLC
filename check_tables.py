# check_tables.py - CORRECTED
import django
import os
import sys

# Add the project directory to Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Set the correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion_force.settings')  # ← This is correct!

django.setup()

from django.db import connection

print("=== Checking Database Tables ===")

with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print(f"\nFound {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\n=== Checking main_homecontent ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='main_homecontent';")
    if cursor.fetchone():
        print("✓ main_homecontent table exists")
        
        # Check structure
        cursor.execute("PRAGMA table_info(main_homecontent);")
        columns = cursor.fetchall()
        print(f"  Columns: {len(columns)}")
        for col in columns:
            print(f"    - {col[1]} ({col[2]})")
        
        # Count rows
        cursor.execute("SELECT COUNT(*) FROM main_homecontent;")
        count = cursor.fetchone()[0]
        print(f"  Rows: {count}")
    else:
        print("✗ main_homecontent table does NOT exist")

print("\n=== Testing HomeContent Model ===")
try:
    from main.models import HomeContent
    count = HomeContent.objects.count()
    print(f"HomeContent.objects.count() = {count}")
    
    if count == 0:
        print("Creating a default HomeContent record...")
        HomeContent.objects.create(
            title="Fusion Force LLC",
            subtitle="Pamela Robinson - Making the Impossible Possible",
            is_active=True
        )
        print("✓ Created default record")
        
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")