import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import re
from urllib.parse import urlparse

def clean_url(url):
    """Clean and validate URL."""
    # Remove whitespace and normalize
    url = url.strip()
    
    # Skip empty lines
    if not url:
        return None
        
    # Add http:// if no protocol specified
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    # Validate URL format
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
        return None
    except:
        return None

def read_urls_from_file(filename):
    """Read and process URLs from file, handling various formats."""
    try:
        with open(filename, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Split by any combination of newlines
        raw_urls = re.split(r'\s*[\r\n]+\s*', content)
        
        # Clean and validate URLs
        urls = []
        for url in raw_urls:
            clean = clean_url(url)
            if clean:
                urls.append(clean)
                
        return urls
    except FileNotFoundError:
        print("links.txt not found. Please create it with one URL per line.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading URLs: {str(e)}")
        sys.exit(1)

def detect_browsers():
    """Detect installed browsers based on the operating system."""
    browsers = {}
    
    if sys.platform == "darwin":  # macOS
        common_paths = {
            "Google Chrome": "/Applications/Google Chrome.app",
            "Firefox": "/Applications/Firefox.app",
            "Safari": "/Applications/Safari.app",
            "Microsoft Edge": "/Applications/Microsoft Edge.app",
            "Brave Browser": "/Applications/Brave Browser.app",
            "Opera": "/Applications/Opera.app",
            "Vivaldi": "/Applications/Vivaldi.app",
            "Opera GX": "/Applications/Opera GX.app",
            "Chromium": "/Applications/Chromium.app",
            "Tor Browser": "/Applications/Tor Browser.app",
            "Waterfox": "/Applications/Waterfox.app",
            "LibreWolf": "/Applications/LibreWolf.app",
            "Arc": "/Applications/Arc.app",
            "Orion": "/Applications/Orion.app",
            "Min": "/Applications/Min.app",
            "Beam": "/Applications/Beam.app",
            "Epic Privacy Browser": "/Applications/Epic Privacy Browser.app",
            "Yandex": "/Applications/Yandex.app",
            "SRWare Iron": "/Applications/SRWare Iron.app",
            "Pale Moon": "/Applications/Pale Moon.app"
        }
        for name, path in common_paths.items():
            if os.path.exists(path):
                browsers[name] = path
                
    elif sys.platform == "win32":  # Windows
        program_files = [
            os.environ.get("PROGRAMFILES", "C:/Program Files"),
            os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", "C:/Users/Current/AppData/Local")
        ]
        common_paths = {
            "Google Chrome": "Google/Chrome/Application/chrome.exe",
            "Firefox": "Mozilla Firefox/firefox.exe",
            "Microsoft Edge": "Microsoft/Edge/Application/msedge.exe",
            "Brave Browser": "BraveSoftware/Brave-Browser/Application/brave.exe",
            "Opera": "Opera/launcher.exe",
            "Vivaldi": "Vivaldi/Application/vivaldi.exe",
            "Opera GX": "Opera Software/Opera GX/launcher.exe",
            "Chromium": "Chromium/Application/chrome.exe",
            "Tor Browser": "Tor Browser/Browser/firefox.exe",
            "Waterfox": "Waterfox/waterfox.exe",
            "LibreWolf": "LibreWolf/librewolf.exe",
            "Min": "Min/min.exe",
            "Epic Privacy Browser": "Epic Privacy Browser/epic.exe",
            "Yandex": "Yandex/Browser/browser.exe",
            "SRWare Iron": "SRWare Iron/iron.exe",
            "Pale Moon": "Pale Moon/palemoon.exe",
            "Maxthon": "Maxthon/Bin/Maxthon.exe",
            "Comodo Dragon": "Comodo/Dragon/dragon.exe",
            "Slim Browser": "Slimjet/slimjet.exe"
        }
        for name, rel_path in common_paths.items():
            for prog_dir in program_files:
                full_path = os.path.join(prog_dir, rel_path)
                if os.path.exists(full_path):
                    browsers[name] = full_path
                    break
                    
    else:  # Linux
        common_browsers = {
            "Google Chrome": ["google-chrome", "chrome"],
            "Firefox": ["firefox"],
            "Microsoft Edge": ["microsoft-edge"],
            "Brave Browser": ["brave-browser"],
            "Opera": ["opera"],
            "Vivaldi": ["vivaldi"],
            "Opera GX": ["opera-gx"],
            "Chromium": ["chromium", "chromium-browser"],
            "Tor Browser": ["tor-browser"],
            "Waterfox": ["waterfox"],
            "LibreWolf": ["librewolf"],
            "Min": ["min"],
            "Epic Privacy Browser": ["epic"],
            "Yandex": ["yandex-browser"],
            "SRWare Iron": ["iron"],
            "Pale Moon": ["palemoon"],
            "Falkon": ["falkon"],
            "Konqueror": ["konqueror"],
            "Midori": ["midori"],
            "GNOME Web": ["epiphany"]
        }
        for name, cmds in common_browsers.items():
            for cmd in cmds:
                if subprocess.run(["which", cmd], capture_output=True, text=True).returncode == 0:
                    browsers[name] = cmd
                    break
                    
    return browsers

def open_links_in_browser(browser_name, browser_path, urls):
    """Open a list of URLs in the specified browser."""
    if sys.platform == "darwin":  # macOS
        browser_app = browser_path
        for url in urls:
            try:
                subprocess.run(["open", "-a", browser_app, url])
                print(f"Opening: {url}")
            except subprocess.SubprocessError as e:
                print(f"Error opening {url}: {str(e)}")
            
    else:
        try:
            # Try using webbrowser module first
            browser = webbrowser.get(browser_path)
            for url in urls:
                try:
                    browser.open_new_tab(url)
                    print(f"Opening: {url}")
                except Exception as e:
                    print(f"Error opening {url}: {str(e)}")
        except webbrowser.Error:
            # Fallback to subprocess
            print(f"Using fallback method for {browser_name}...")
            for url in urls:
                try:
                    subprocess.run([browser_path, url], 
                                 capture_output=True, 
                                 stderr=subprocess.PIPE)
                    print(f"Opening: {url}")
                except subprocess.SubprocessError as e:
                    print(f"Error opening {url}: {str(e)}")

def main():
    # Detect installed browsers
    browsers = detect_browsers()
    
    if not browsers:
        print("No supported browsers detected on your system.")
        sys.exit(1)
        
    # Display available browsers
    print("\nDetected browsers:")
    for idx, browser in enumerate(browsers.keys(), 1):
        print(f"{idx}. {browser}")
        
    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect a browser (enter number): "))
            if 1 <= choice <= len(browsers):
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
            
    selected_browser = list(browsers.keys())[choice - 1]
    browser_path = browsers[selected_browser]
    
    # Read and process URLs
    urls = read_urls_from_file("links.txt")
    
    print(f"\nOpening URLs in {selected_browser}...")
    open_links_in_browser(selected_browser, browser_path, urls)
    print("Done!")

if __name__ == "__main__":
    main()