# Download development fMRI dataset with anatomical data
import os
from pathlib import Path
from nilearn import datasets
import nibabel as nib
import pandas as pd

# Set up paths
project_root = Path(__file__).parent.parent
data_dir = project_root / "data"
outputs_dir = project_root / "outputs"

# Create directories if they don't exist
data_dir.mkdir(exist_ok=True)
outputs_dir.mkdir(exist_ok=True)

print(f"Project root: {project_root}")
print(f"Data directory: {data_dir}")
print(f"Outputs directory: {outputs_dir}")

# Download development fMRI dataset with more subjects and all data types
print("Downloading development fMRI dataset with anatomical data...")

try:
    # Try to download more subjects and all available data
    dataset = datasets.fetch_development_fmri(
        n_subjects=5,  # Download 5 subjects
        reduce_confounds=True,  # Get reduced confounds
        data_dir=str(data_dir),
        resume=True,  # Resume if partially downloaded
        verbose=1  # Verbose output
    )
    
    print(f"\nDataset attributes: {dir(dataset)}")
    print(f"Keys in dataset: {list(dataset.keys())}")
    
    # Check what data was downloaded
    for key, value in dataset.items():
        if isinstance(value, list):
            print(f"{key}: {len(value)} files")
            if len(value) > 0:
                print(f"  First file: {value[0]}")
        else:
            print(f"{key}: {value}")
    
    # Check if we have anatomical data
    if hasattr(dataset, 'anat') and dataset.anat:
        print(f"\n✓ Found anatomical data: {len(dataset.anat)} files")
        for i, anat_file in enumerate(dataset.anat):
            anat_img = nib.load(anat_file)
            print(f"  Subject {i+1} - Anat shape: {anat_img.shape}")
            print(f"  Location: {anat_file}")
    else:
        print("\n✗ No anatomical data found in dataset")
        
        # Let's check what files are actually available in the directory
        dev_fmri_dir = data_dir / "development_fmri"
        if dev_fmri_dir.exists():
            print(f"\nExploring {dev_fmri_dir} directory structure:")
            for root, dirs, files in os.walk(dev_fmri_dir):
                level = root.replace(str(dev_fmri_dir), '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files[:5]:  # Show first 5 files
                    print(f"{subindent}{file}")
                if len(files) > 5:
                    print(f"{subindent}... and {len(files) - 5} more files")
    
    # Check functional data
    if hasattr(dataset, 'func') and dataset.func:
        print(f"\n✓ Found functional data: {len(dataset.func)} files")
        for i, func_file in enumerate(dataset.func[:3]):  # Show first 3
            func_img = nib.load(func_file)
            print(f"  Subject {i+1} - Func shape: {func_img.shape}")
            print(f"  Location: {func_file}")
    
    # Check participants info
    participants_file = data_dir / "development_fmri" / "development_fmri" / "participants.tsv"
    if participants_file.exists():
        participants = pd.read_csv(participants_file, sep='\t')
        print(f"\n✓ Participants file found: {len(participants)} subjects total")
        print(f"Age range: {participants['Age'].min():.1f} - {participants['Age'].max():.1f} years")
        print(f"Available subjects: {participants['participant_id'].head(10).tolist()}")
        
except Exception as e:
    print(f"Error downloading development fMRI: {e}")
    import traceback
    traceback.print_exc()