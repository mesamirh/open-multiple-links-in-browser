import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import re
from urllib.parse import urlparse
import json
from pathlib import Path

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

def get_browser_profiles(browser_name, browser_path):
    """Get available profiles for the selected browser."""
    profiles = {}
    
    if sys.platform == "darwin":  # macOS
        user_data_paths = {
            "Google Chrome": str(Path.home() / "Library/Application Support/Google/Chrome"),
            "Microsoft Edge": str(Path.home() / "Library/Application Support/Microsoft Edge"),
            "Brave Browser": str(Path.home() / "Library/Application Support/BraveSoftware/Brave-Browser"),
            "Firefox": str(Path.home() / "Library/Application Support/Firefox/Profiles"),
        }
    elif sys.platform == "win32":  # Windows
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        user_data_paths = {
            "Google Chrome": os.path.join(local_app_data, "Google/Chrome/User Data"),
            "Microsoft Edge": os.path.join(local_app_data, "Microsoft/Edge/User Data"),
            "Brave Browser": os.path.join(local_app_data, "BraveSoftware/Brave-Browser/User Data"),
            "Firefox": os.path.join(os.environ.get("APPDATA", ""), "Mozilla/Firefox/Profiles"),
        }
    else:  # Linux
        user_data_paths = {
            "Google Chrome": str(Path.home() / ".config/google-chrome"),
            "Microsoft Edge": str(Path.home() / ".config/microsoft-edge"),
            "Brave Browser": str(Path.home() / ".config/BraveSoftware/Brave-Browser"),
            "Firefox": str(Path.home() / ".mozilla/firefox"),
        }

    if browser_name in user_data_paths:
        profile_path = Path(user_data_paths[browser_name])
        
        if "Firefox" in browser_name:
            # Handle Firefox profiles
            if profile_path.exists():
                for profile in profile_path.glob("*.*/"):
                    if (profile / "prefs.js").exists():
                        profiles[profile.name] = str(profile)
        else:
            # Handle Chromium-based browsers
            local_state_path = profile_path / "Local State"
            if local_state_path.exists():
                try:
                    with open(local_state_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if "profile" in data and "info_cache" in data["profile"]:
                            for profile_name in data["profile"]["info_cache"]:
                                profiles[profile_name] = profile_name
                except (json.JSONDecodeError, KeyError):
                    pass

    # If no profiles were found, add Default
    if not profiles:
        profiles["Default"] = None

    return profiles

def open_links_in_browser(browser_name, browser_path, urls, profile=None):
    """Open a list of URLs in the specified browser with optional profile."""
    if sys.platform == "darwin":  # macOS
        for url in urls:
            try:
                cmd = ["open", "-a", browser_path]
                
                # Add profile arguments for supported browsers
                if profile and profile != "default":
                    if "Google Chrome" in browser_name:
                        cmd.extend(["--args", "--profile-directory=" + profile])
                    elif "Firefox" in browser_name:
                        cmd.extend(["--args", "-P", profile])
                    elif "Microsoft Edge" in browser_name:
                        cmd.extend(["--args", "--profile-directory=" + profile])
                    elif "Brave Browser" in browser_name:
                        cmd.extend(["--args", "--profile-directory=" + profile])
                
                cmd.append(url)
                subprocess.run(cmd)
                print(f"Opening: {url}")
            except subprocess.SubprocessError as e:
                print(f"Error opening {url}: {str(e)}")
    else:
        for url in urls:
            try:
                cmd = [browser_path]
                
                # Add profile arguments for supported browsers
                if profile and profile != "default":
                    if "chrome" in browser_path.lower() or "edge" in browser_path.lower() or "brave" in browser_path.lower():
                        cmd.append("--profile-directory=" + profile)
                    elif "firefox" in browser_path.lower():
                        cmd.extend(["-P", profile])
                
                cmd.append(url)
                subprocess.run(cmd, capture_output=True, stderr=subprocess.PIPE)
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
        
    # Get user browser selection
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
    
    # Get available profiles
    profiles = get_browser_profiles(selected_browser, browser_path)
    
    if len(profiles) > 1:
        print("\nAvailable profiles:")
        for idx, profile in enumerate(profiles.keys(), 1):
            print(f"{idx}. {profile}")
        
        # Get user profile selection
        while True:
            try:
                profile_choice = int(input("\nSelect a profile (enter number): "))
                if 1 <= profile_choice <= len(profiles):
                    break
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        selected_profile = list(profiles.keys())[profile_choice - 1]
    else:
        selected_profile = "default"
    
    # Read and process URLs
    urls = read_urls_from_file("links.txt")
    
    print(f"\nOpening URLs in {selected_browser} with profile '{selected_profile}'...")
    open_links_in_browser(selected_browser, browser_path, urls, selected_profile)
    print("Done!")

if __name__ == "__main__":
    main()