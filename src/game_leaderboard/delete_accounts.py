import requests
import time

# TODO: Replace this list with your actual tokens
tokens = [
    "6b7287ccaccd83cdcdbe2430bed62ad748990fd2feed53e387633f4418314306",
    "your_second_token_here",
    "your_third_token_here"
]

url = "https://voidstrapp.pages.dev/api/account"

base_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://voidstrapp.pages.dev/pages/settings',
    'Content-Type': 'application/json',
    'Origin': 'https://voidstrapp.pages.dev',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=4'
}

payload = {
    "action": "delete-account",
    "confirm": "DELETE"
}

print(f"Starting script for {len(tokens)} tokens...\n")

for index, token in enumerate(tokens, start=1):
    # Create a copy of headers to avoid mutating the base template
    headers = base_headers.copy()
    headers['Authorization'] = f'Bearer {token}'
    
    # Mask the token for safer console logging    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code in (200, 204):
            print(f"[{index}/{len(tokens)}] Success: {token} | Status: {response.status_code}")
        else:
            print(f"[{index}/{len(tokens)}] Failed: {token} | Status: {response.status_code} | Response: {response.text.strip()}")
            
    except requests.exceptions.RequestException as e:
        print(f"[{index}/{len(tokens)}] ⚠️ Error: {token} | Exception: {e}")
    
    # Small delay to prevent overwhelming the server or triggering rate limits
    time.sleep(1.5)

print("done.")