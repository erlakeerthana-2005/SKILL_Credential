import os

files_to_update = [
    r'd:\SKILL\frontend\style.css',
    r'd:\SKILL\frontend\dashboard.css'
]

for file_path in files_to_update:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace #fff with var(--text) for dynamic white/dark tracking
    content = content.replace('color: #fff;', 'color: var(--text);')
    content = content.replace('color: #ffffff;', 'color: var(--text);')
    # Change glass border/backgrounds to use dark alpha
    content = content.replace('rgba(255, 255, 255, 0.02)', 'rgba(0, 0, 0, 0.02)')
    content = content.replace('rgba(255, 255, 255, 0.05)', 'rgba(0, 0, 0, 0.05)')
    content = content.replace('rgba(255, 255, 255, 0.03)', 'rgba(0, 0, 0, 0.03)')
    content = content.replace('rgba(255, 255, 255, 0.08)', 'rgba(0, 0, 0, 0.08)')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated CSS files successfully.")
