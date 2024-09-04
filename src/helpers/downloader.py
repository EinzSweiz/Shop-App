import requests
from pathlib import Path

def download_to_local(url:str, download_from_path:Path, parent_mkdir:bool=True):
    
    if not isinstance(download_from_path, Path):
        raise ValueError(f'{download_from_path} should be pathlib from Path object')

    if parent_mkdir:
        download_from_path.parent.mkdir(exist_ok=True, parents=True)    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        download_from_path.write_bytes(response.content)
        return True  # Indicate success if no exceptions were raised
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')
        return False  # Indicate failure

