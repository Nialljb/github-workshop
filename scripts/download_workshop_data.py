# Download Haxby dataset with anatomical and functional data
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

print("Downloading Haxby dataset (3 subjects with anatomical + functional data)...")

try:
    # Download 3 subjects from Haxby dataset
    dataset = datasets.fetch_haxby(subjects=[1, 2, 3], data_dir=str(data_dir))
    
    print(f"\n✅ Successfully downloaded Haxby dataset")
    print(f"Available data types: {list(dataset.keys())}")
    
    # Display anatomical data info
    print(f"\n📂 Anatomical Data:")
    print(f"   {len(dataset.anat)} T1-weighted structural images")
    for i, anat_file in enumerate(dataset.anat):
        anat_img = nib.load(anat_file)
        print(f"   Subject {i+1}: {anat_img.shape} voxels - {Path(anat_file).name}")
        print(f"   └── Voxel size: {anat_img.header.get_zooms()[:3]} mm")
    
    # Display functional data info  
    print(f"\n🎬 Functional Data:")
    print(f"   {len(dataset.func)} BOLD fMRI files")
    for i, func_file in enumerate(dataset.func):
        func_img = nib.load(func_file)
        print(f"   Subject {i+1}: {func_img.shape} (spatial + {func_img.shape[3]} timepoints)")
        print(f"   └── Voxel size: {func_img.header.get_zooms()[:3]} mm, TR: {func_img.header.get_zooms()[3]} s")
    
    # Display additional data
    print(f"\n🎯 Additional Data:")
    if hasattr(dataset, 'mask'):
        print(f"   • Brain mask: {Path(dataset.mask).name}")
    
    mask_types = [k for k in dataset.keys() if k.startswith('mask_') and k != 'mask']
    if mask_types:
        print(f"   • ROI masks: {', '.join([k.replace('mask_', '') for k in mask_types])}")
    
    if hasattr(dataset, 'session_target'):
        print(f"   • Task labels: {len(dataset.session_target)} sessions with stimulus labels")
    
    # Summary for workshop use
    print(f"\n🎓 Workshop Ready:")
    print(f"   • Groups 1-3 can each use a different subject for anatomical challenges")
    print(f"   • All anatomical processing steps possible: skull stripping, bias correction, segmentation")
    print(f"   • Functional data available for preprocessing and visualization challenges")
    print(f"   • ROI masks provided for advanced analyses")
    
    print(f"\n📁 Data location: {data_dir}/haxby2001/")
    
except Exception as e:
    print(f"❌ Error downloading Haxby dataset: {e}")
    import traceback
    traceback.print_exc()