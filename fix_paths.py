import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace 'assets/' with 'static/assets/' but avoid 'static/assets/'
# We look for 'assets/' that is NOT preceded by 'static/'
# Using negative lookbehind
new_content = re.sub(r'(?<!static/)assets/', 'static/assets/', content)

# Also fix any potential double slashes if they occur (though the regex above should prevent double static/)
# But just in case
new_content = new_content.replace('static/static/assets/', 'static/assets/')

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Fixed asset paths.")
