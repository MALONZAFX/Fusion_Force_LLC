import os
import re

def fix_html_files():
    templates_dir = 'templates/main/'
    
    # Find all HTML files
    html_files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
    
    for html_file in html_files:
        file_path = os.path.join(templates_dir, html_file)
        print(f"Processing: {html_file}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Add {% load static %} at the top
        if '{% load static %}' not in content:
            content = content.replace('<!DOCTYPE html>', '{% load static %}\n<!DOCTYPE html>')
        
        # Fix CSS paths
        content = content.replace('href="css/', 'href="{% static \'css/')
        content = content.replace('.css"', '.css\' %}"')
        
        # Fix JS paths  
        content = content.replace('src="js/', 'src="{% static \'js/')
        content = content.replace('.js"', '.js\' %}"')
        
        # Fix image paths
        content = content.replace('src="img/', 'src="{% static \'images/')
        content = content.replace('src=\"img/', 'src=\"{% static \'images/')
        content = re.sub(r'\.(jpg|jpeg|png|gif|svg|ico)"', r'\' %}"', content)
        content = re.sub(r'\.(jpg|jpeg|png|gif|svg|ico)\"', r'\' %}"', content)
        
        # Fix lib/asset paths
        content = content.replace('href="lib/', 'href="{% static \'assets/')
        content = content.replace('src="lib/', 'src="{% static \'assets/')
        
        # Fix .css and .js endings for lib/ assets
        content = re.sub(r'assets/([^\"\']+)\.(css|js)"', r"assets/\1.\2' %}", content)
        
        # Write back the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f'  Fixed: {html_file}')

if __name__ == '__main__':
    fix_html_files()
    print("\nAll HTML files have been updated with Django template tags!")
