# Quick test to download and check neuroimaging data
import os
from pathlib import Path
from nilearn import datasets
import nibabel as nib

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

# Download dataset with both anatomical and functional data
print("Downloading neuroimaging dataset with anatomical data...")

try:
    # Try Haxby dataset first (multiple subjects with anat+func)
    print("Attempting to download Haxby dataset (6 subjects with anatomical)...")
    dataset = datasets.fetch_haxby(subjects=[1, 2], data_dir=str(data_dir))
    
    print("Successfully downloaded Haxby dataset")
    print(f"Available subjects: {len(dataset.anat)} subjects")
    print(f"Anatomical images: {len(dataset.anat)} files")
    print(f"Functional images: {len(dataset.func)} files")
    
    # Check first subject's anatomical
    if dataset.anat and len(dataset.anat) > 0:
        anat_img = nib.load(dataset.anat[0])
        print(f"\nSubject 1 - Anatomical image shape: {anat_img.shape}")
        print(f"Voxel size: {anat_img.header.get_zooms()}")
        print(f"File location: {dataset.anat[0]}")
    
    # Check first subject's functional
    if dataset.func and len(dataset.func) > 0:
        func_img = nib.load(dataset.func[0])
        print(f"\nSubject 1 - Functional image shape: {func_img.shape}")
        print(f"Voxel size: {func_img.header.get_zooms()}")
        print(f"File location: {dataset.func[0]}")
        
    # Show second subject if available
    if len(dataset.anat) > 1:
        anat_img2 = nib.load(dataset.anat[1])
        print(f"\nSubject 2 - Anatomical image shape: {anat_img2.shape}")
        print(f"File location: {dataset.anat[1]}")
        
except Exception as e:
    print(f"Error with Haxby dataset: {e}")
    print("Trying SPM auditory dataset (1 subject only)...")
    
    try:
        # SPM auditory has only 1 subject but good quality data
        dataset = datasets.fetch_spm_auditory(data_dir=str(data_dir))
        
        print("Successfully downloaded SPM auditory dataset (1 subject)")
        print(f"Anatomical image: {dataset.anat}")
        print(f"Functional images: {len(dataset.func)} files")
        
        # Check anatomical image
        if dataset.anat:
            anat_img = nib.load(dataset.anat)
            print(f"\nAnatomical image shape: {anat_img.shape}")
            print(f"Voxel size: {anat_img.header.get_zooms()}")
            print(f"File location: {dataset.anat}")
        
        # Check functional image
        if dataset.func:
            func_img = nib.load(dataset.func[0])
            print(f"\nFunctional image shape: {func_img.shape}")
            print(f"Voxel size: {func_img.header.get_zooms()}")
            print(f"File location: {dataset.func[0]}")
            
    except Exception as e2:
        print(f"Error with SPM dataset: {e2}")
        print("Trying MNI152 template + multiple ADHD subjects...")
        
        try:
            # Download anatomical template + multiple functional subjects
            mni_template = datasets.load_mni152_template(resolution=2, data_dir=str(data_dir))
            print(f"Downloaded MNI152 template: {mni_template}")
            
            # Download multiple ADHD subjects for functional data
            adhd_data = datasets.fetch_adhd(n_subjects=3, data_dir=str(data_dir))
            print(f"Downloaded {len(adhd_data.func)} functional datasets")
            
            # Check template
            template_img = nib.load(mni_template)
            print(f"\nMNI152 Template shape: {template_img.shape}")
            print(f"File location: {mni_template}")
            
            # Check multiple functional datasets
            for i, func_file in enumerate(adhd_data.func[:2]):  # Show first 2
                func_img = nib.load(func_file)
                print(f"\nSubject {i+1} - Functional shape: {func_img.shape}")
                print(f"File location: {func_file}")
                
        except Exception as e3:
            print(f"All download attempts failed: {e3}")
            print("You may need to download data manually or check your internet connection")