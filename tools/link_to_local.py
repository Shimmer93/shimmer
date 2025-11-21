import re
import os
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

def download_image(url, save_dir):
    """Download an image from a URL and save it locally."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(unquote(parsed_url.path))
        
        # If no filename, generate one from the URL hash
        if not filename or '.' not in filename:
            ext = '.png'  # Default extension
            filename = f"image_{abs(hash(url))}{ext}"
        
        # Ensure save directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        # Save the image
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_markdown_file(md_file_path):
    """Process a markdown file to download images and update links."""
    md_file = Path(md_file_path)
    
    if not md_file.exists():
        print(f"File not found: {md_file_path}")
        return

    # Create images directory in shimmer/assets/img/intext (relative to repo root)
    repo_root = Path(__file__).parent.parent  # Go up from tools/ to repo root
    images_dir = repo_root / "shimmer" / "assets" / "img" / "intext"
    
    # Read the markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image links: ![alt](url) and ![alt](url "title")
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.finditer(image_pattern, content)
    
    # Process each image link
    for match in matches:
        alt_text = match.group(1)
        url = match.group(2).split()[0]  # Remove optional title
        
        # Skip if already a local path
        if not url.startswith(('http://', 'https://')):
            continue
        
        print(f"Downloading: {url}")
        local_path = download_image(url, images_dir)
        
        if local_path:
            # Convert to relative path from the markdown file to assets/img
            relative_path = os.path.relpath(local_path, md_file.parent)
            # Use forward slashes for markdown
            relative_path = relative_path.replace('\\', '/')
            
            # Replace the URL in content
            old_link = match.group(0)
            new_link = f"![{alt_text}]({relative_path})"
            content = content.replace(old_link, new_link)
            print(f"Replaced with: {relative_path}")
    
    # Write the updated content back to the file
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processing complete for {md_file_path}")

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Usage: python link_to_local.py <markdown_file.md>")
        sys.exit(1)
    
    md_file = sys.argv[1]
    process_markdown_file(md_file)