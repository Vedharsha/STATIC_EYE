import requests
import os
import pandas as pd
from tqdm import tqdm

ANDROZOO_API_KEY = "your_androzoo_api_key_here"
ANDROZOO_URL = "https://androzoo.uni.lu/api/download"

def download_apk(sha256, output_dir):
    params = {
        'apikey': ANDROZOO_API_KEY,
        'sha256': sha256
    }
    response = requests.get(ANDROZOO_URL, params=params, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(output_dir, f"{sha256}.apk")
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return file_path
    else:
        print(f"Failed to download APK {sha256}")
        return None

def download_androzoo_dataset(output_dir, num_samples=1000):
    # Load the AndroZoo metadata CSV (you need to download this separately)
    df = pd.read_csv('androzoo_metadata.csv')
    
    # Filter for recent APKs (e.g., last 2 years)
    df['dex_date'] = pd.to_datetime(df['dex_date'])
    recent_apks = df[df['dex_date'] > (df['dex_date'].max() - pd.Timedelta(days=730))]
    
    # Sample APKs
    sampled_apks = recent_apks.sample(n=num_samples, random_state=42)
    
    # Download APKs
    downloaded_apks = []
    for _, row in tqdm(sampled_apks.iterrows(), total=num_samples):
        apk_path = download_apk(row['sha256'], output_dir)
        if apk_path:
            # Use VirusTotal detection as a simple vulnerability label
            is_vulnerable = row['vt_detection'] > 0
            downloaded_apks.append((apk_path, row['sha256'], is_vulnerable))
    
    return downloaded_apks
