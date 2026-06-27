#!/usr/bin/env python3
import json
import os
import argparse
import shutil
from pathlib import Path

def generate_playlist_html(playlist_json, output_folder=None):
    """
    Read playlist.json, extract video URLs, and generate an HTML file
    with the videos list in the output folder.
    
    Args:
        playlist_json: Path to the playlist.json file
        output_folder: Optional path to the folder where the HTML will be generated.
                       Defaults to the same folder as the JSON file.
    """
    
    # Define paths
    base_dir = Path(__file__).parent
    playlist_json = Path(playlist_json).resolve()
    output_folder = Path(output_folder).resolve() if output_folder else playlist_json.parent
    template_html = base_dir / "index_playlist.html"
    output_html = output_folder / f"{playlist_json.stem}.html"
    
    # Validate paths
    if not playlist_json.exists():
        raise FileNotFoundError(f"Playlist file not found: {playlist_json}")
    
    if not template_html.exists():
        raise FileNotFoundError(f"Template file not found: {template_html}")
    
    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Read playlist.json and extract video URLs
    print(f"Reading playlist from {playlist_json}...")
    with open(playlist_json, 'r') as f:
        playlist_data = json.load(f)
    
    videos = [item['url'] for item in playlist_data.get('items', [])]
    print(f"Found {len(videos)} videos")
    
    if not videos:
        raise ValueError("No videos found in playlist.json")
    
    # Read the template HTML
    print(f"Reading template from {template_html}...")
    with open(template_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create JavaScript array of videos
    video_list_js = ",\n\t\t".join([f'"{url}"' for url in videos])
    
    # Replace placeholders
    html_content = html_content.replace("{video_list}", video_list_js)
    html_content = html_content.replace("{video_0}", videos[0])
    
    # CSS path will be local (in same folder as HTML)
    html_content = html_content.replace('href="./video.css"', 'href="./video.css"')
    
    # Write the output HTML
    print(f"Writing generated HTML to {output_html}...")
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Copy video.css to output folder
    css_source = base_dir / "video.css"
    css_dest = output_folder / "video.css"
    if css_source.exists():
        print(f"Copying video.css to {css_dest}...")
        shutil.copy2(css_source, css_dest)
    else:
        print(f"Warning: video.css not found at {css_source}")
    
    print(f"✓ Success! Generated {output_html}")
    print(f"  Videos in playlist: {len(videos)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an index.html playlist from a playlist.json file"
    )
    parser.add_argument(
        "playlist_json",
        help="Path to the playlist.json file"
    )
    parser.add_argument(
        "output_folder",
        nargs="?",
        help="Optional path to the output folder where the HTML will be generated. Defaults to the JSON file's folder"
    )
    
    args = parser.parse_args()
    
    try:
        generate_playlist_html(args.playlist_json, args.output_folder)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in playlist file: {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
