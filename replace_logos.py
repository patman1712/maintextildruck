from bs4 import BeautifulSoup
import re

# Read index.html
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
new_logo_path = "assets/new_logo.svg"

# 1. Replace favicons
for link in soup.find_all('link', rel=lambda x: x and ('icon' in x or 'apple-touch-icon' in x)):
    if 'logo' in link.get('href', '').lower():
        print(f"Replacing favicon: {link['href']}")
        link['href'] = new_logo_path
        # Remove sizes to avoid confusion
        if 'sizes' in link.attrs:
            del link['sizes']

# 2. Replace images
# Find images with 'logo' in src or class or parent class
for img in soup.find_all('img'):
    src = img.get('src', '')
    classes = img.get('class', [])
    parent_classes = img.parent.get('class', []) if img.parent else []
    
    is_logo = 'logo' in src.lower() or \
              any('logo' in c.lower() for c in classes) or \
              any('logo' in c.lower() for c in parent_classes)
    
    if is_logo:
        print(f"Replacing image: {src}")
        img['src'] = new_logo_path
        # Remove srcset and sizes as they might point to old images
        if 'srcset' in img.attrs:
            del img['srcset']
        if 'sizes' in img.attrs:
            del img['sizes']
        # Reset width/height to avoid distortion if aspect ratio is different
        # or set a standard width if needed. For now, let's remove hardcoded dimensions
        # so CSS can handle it, or keep them if they are layout critical?
        # Let's remove them to be safe with SVG scaling
        if 'width' in img.attrs:
            del img['width']
        if 'height' in img.attrs:
            del img['height']
        # Add a class to style it if needed
        img['class'] = img.get('class', []) + ['new-logo-replaced']

# 3. Replace meta tags for social media
for meta in soup.find_all('meta', property=lambda x: x and 'image' in x):
    content = meta.get('content', '')
    if 'logo' in content.lower():
        print(f"Replacing meta image: {content}")
        # Note: Social media scrapers won't see local localhost assets, 
        # but for consistency in the code we change it.
        # However, an SVG might not be valid for OG tags usually, but let's point to it anyway.
        meta['content'] = new_logo_path

with open("index.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Done replacing logos.")
