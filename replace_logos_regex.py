import re

new_logo_path = "assets/new_logo.png"

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Helper to remove attributes
def remove_attr(tag_str, attr_name):
    # This regex tries to find attr="value" or attr='value' or just attr
    # It handles spaces around = and handles newlines inside tag
    pattern = re.compile(r'\s+' + re.escape(attr_name) + r'(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'))?', re.IGNORECASE | re.DOTALL)
    return pattern.sub('', tag_str)

# Helper to replace attribute value
def replace_attr(tag_str, attr_name, new_value):
    # Remove existing
    tag_str = remove_attr(tag_str, attr_name)
    # Add new at the end before closing > or />
    # Find the end of the tag
    if tag_str.endswith('/>'):
        return tag_str[:-2] + f' {attr_name}="{new_value}" />'
    elif tag_str.endswith('>'):
        return tag_str[:-1] + f' {attr_name}="{new_value}">'
    return tag_str

# 1. Replace favicons and apple icons
# Look for <link ... rel="icon" ...> or similar
def replace_link_href(match):
    tag = match.group(0)
    if 'logo' in tag.lower() or 'icon' in tag.lower(): # Check if it's related to logo/icon
        # Check if it has rel="icon" or similar
        if re.search(r'rel=["\'](?:shortcut )?icon["\']', tag, re.IGNORECASE) or \
           re.search(r'rel=["\']apple-touch-icon["\']', tag, re.IGNORECASE):
            tag = remove_attr(tag, 'sizes')
            tag = replace_attr(tag, 'href', new_logo_path)
    return tag

content = re.sub(r'<link[^>]*>', replace_link_href, content, flags=re.IGNORECASE)

# 2. Replace images
# Look for <img ...>
def replace_img_src(match):
    tag = match.group(0)
    # Check if src contains 'logo' OR class contains 'logo'
    src_match = re.search(r'src=["\']([^"\']*)["\']', tag, re.IGNORECASE)
    class_match = re.search(r'class=["\']([^"\']*)["\']', tag, re.IGNORECASE)
    
    is_logo = False
    if src_match and 'logo' in src_match.group(1).lower():
        is_logo = True
    if class_match and 'logo' in class_match.group(1).lower():
        is_logo = True
        
    # Also check specific known logo filenames if 'logo' is not in name (unlikely but safe)
    if not is_logo and src_match:
        src = src_match.group(1)
        if 'fsgmbh' in src.lower(): # Fanshop GmbH
            is_logo = True

    if is_logo:
        tag = remove_attr(tag, 'srcset')
        tag = remove_attr(tag, 'sizes')
        tag = remove_attr(tag, 'width')
        tag = remove_attr(tag, 'height')
        tag = replace_attr(tag, 'src', new_logo_path)
        # Add a style for width to prevent it being too huge if no css applies
        # We append a style attribute or modify existing
        if 'style=' in tag:
            # Simple hack: just append to the style string if possible, or replace.
            # But let's just leave it to CSS classes if possible.
            pass
        else:
             # Add a default width just in case
             tag = replace_attr(tag, 'style', 'max-width: 200px; height: auto;')
             
    return tag

content = re.sub(r'<img[^>]*>', replace_img_src, content, flags=re.IGNORECASE)

# 3. Replace meta tags
def replace_meta_content(match):
    tag = match.group(0)
    # Check property og:image, twitter:image, etc.
    if re.search(r'property=["\'](?:og:image|og:image:secure_url)["\']', tag, re.IGNORECASE) or \
       re.search(r'name=["\'](?:twitter:image|msapplication-TileImage)["\']', tag, re.IGNORECASE):
        tag = replace_attr(tag, 'content', new_logo_path)
    return tag

content = re.sub(r'<meta[^>]*>', replace_meta_content, content, flags=re.IGNORECASE)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done replacing logos with Regex.")
