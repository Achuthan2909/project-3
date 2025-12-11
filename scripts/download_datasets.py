import os
import json
import requests
import tarfile
from pathlib import Path
from datasets import load_dataset
import pandas as pd

BASE_DIR = Path(__file__).parent
DATASETS_DIR = BASE_DIR / "datasets"
PROMPTS_DIR = BASE_DIR / "prompts"

DATASETS_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)

def download_file(url, output_path):
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='')
    print(f"\n✓ Downloaded to {output_path}")

def extract_tar(tar_path, extract_to):
    print(f"Extracting {tar_path}...")
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(extract_to)
    print(f"✓ Extracted to {extract_to}")

def download_empathetic_dialogues():
    print("\n=== Downloading EmpatheticDialogues ===")
    dataset_dir = DATASETS_DIR / "empathetic_dialogues"
    dataset_dir.mkdir(exist_ok=True)
    
    tar_path = dataset_dir / "empatheticdialogues.tar.gz"
    if not tar_path.exists():
        url = "https://dl.fbaipublicfiles.com/parlai/empatheticdialogues/empatheticdialogues.tar.gz"
        download_file(url, tar_path)
        extract_tar(tar_path, dataset_dir)
    else:
        print("✓ EmpatheticDialogues already downloaded")
    
    return dataset_dir

def download_dailydialog():
    print("\n=== Downloading DailyDialog ===")
    dataset_dir = DATASETS_DIR / "dailydialog"
    dataset_dir.mkdir(exist_ok=True)
    
    try:
        dataset = load_dataset("daily_dialog")
        
        for split in ['train', 'validation', 'test']:
            if split in dataset:
                df = dataset[split].to_pandas()
                output_file = dataset_dir / f"dailydialog_{split}.csv"
                df.to_csv(output_file, index=False)
                print(f"✓ Saved {split} split ({len(df)} samples)")
        
        return dataset_dir
    except Exception as e:
        print(f"Error downloading DailyDialog: {e}")
        print("You can manually download from: https://www.aclweb.org/anthology/I17-1099/")
        return None

def download_emotions_dataset():
    print("\n=== Downloading Emotions Dataset ===")
    dataset_dir = DATASETS_DIR / "emotions"
    dataset_dir.mkdir(exist_ok=True)
    
    try:
        dataset = load_dataset("dair-ai/emotion")
        
        for split in ['train', 'validation', 'test']:
            if split in dataset:
                df = dataset[split].to_pandas()
                output_file = dataset_dir / f"emotions_{split}.csv"
                df.to_csv(output_file, index=False)
                print(f"✓ Saved {split} split ({len(df)} samples)")
        
        return dataset_dir
    except Exception as e:
        print(f"Error downloading Emotions dataset: {e}")
        return None

def download_blended_skill_talk():
    print("\n=== Downloading BlendedSkillTalk ===")
    dataset_dir = DATASETS_DIR / "blended_skill_talk"
    dataset_dir.mkdir(exist_ok=True)
    
    try:
        dataset = load_dataset("blended_skill_talk")
        
        for split in ['train', 'validation', 'test']:
            if split in dataset:
                df = dataset[split].to_pandas()
                output_file = dataset_dir / f"blended_skill_talk_{split}.csv"
                df.to_csv(output_file, index=False)
                print(f"✓ Saved {split} split ({len(df)} samples)")
        
        return dataset_dir
    except Exception as e:
        print(f"Error downloading BlendedSkillTalk: {e}")
        print("Note: This dataset may require ParlAI setup")
        return None

def create_dataset_info():
    info = {
        "datasets": {
            "empathetic_dialogues": {
                "name": "EmpatheticDialogues",
                "source": "Facebook Research",
                "citation": "Rashkin et al. (2019)",
                "size": "~25k conversations",
                "covers_indicators": ["L4.1", "L4.2", "L4.7"],
                "scenario_types": ["job_loss", "health", "relationship", "grief", "financial", "academic", "loneliness"],
                "path": "datasets/empathetic_dialogues"
            },
            "dailydialog": {
                "name": "DailyDialog",
                "source": "ACL 2017",
                "citation": "Li et al. (2017)",
                "size": "~13k conversations",
                "covers_indicators": ["L4.1", "L4.4"],
                "scenario_types": ["general"],
                "path": "datasets/dailydialog"
            },
            "emotions": {
                "name": "Emotions Dataset",
                "source": "HuggingFace",
                "citation": "dair-ai/emotion",
                "size": "~131k text entries",
                "covers_indicators": ["L4.1"],
                "scenario_types": ["general"],
                "path": "datasets/emotions"
            }
        },
        "download_date": str(Path().cwd()),
        "notes": "Datasets downloaded for Phase 2 evaluation"
    }
    
    info_file = BASE_DIR / "dataset_info.json"
    with open(info_file, 'w') as f:
        json.dump(info, f, indent=2)
    print(f"\n✓ Created dataset info file: {info_file}")

def main():
    print("=" * 60)
    print("Downloading Datasets for Phase 2")
    print("=" * 60)
    
    downloaded = []
    
    emp_dir = download_empathetic_dialogues()
    if emp_dir:
        downloaded.append("EmpatheticDialogues")
    
    dd_dir = download_dailydialog()
    if dd_dir:
        downloaded.append("DailyDialog")
    
    emo_dir = download_emotions_dataset()
    if emo_dir:
        downloaded.append("Emotions")
    
    bst_dir = download_blended_skill_talk()
    if bst_dir:
        downloaded.append("BlendedSkillTalk")
    
    create_dataset_info()
    
    print("\n" + "=" * 60)
    print("Download Summary:")
    print("=" * 60)
    for ds in downloaded:
        print(f"✓ {ds}")
    print(f"\nTotal datasets downloaded: {len(downloaded)}")
    print(f"\nNext steps:")
    print("1. Review datasets in data/datasets/")
    print("2. Run dataset_mapper.py to analyze coverage")
    print("3. Create custom prompts for gaps")

if __name__ == "__main__":
    main()

