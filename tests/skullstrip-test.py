import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.run_anat_analysis import StructuralPipeline
import nibabel as nib

# Create pipeline
pipeline = StructuralPipeline(output_dir="./outputs")

# Load test data
img = pipeline.load_data(subject_idx=0)
print(f"Original shape: {img.shape}")

# Test skull stripping
brain_img = pipeline.skull_strip(img)
print(f"Brain shape: {brain_img.shape}")

# Verify outputs exist
from pathlib import Path
assert Path("outputs/brain_mask.nii.gz").exists()
assert Path("outputs/brain.nii.gz").exists()

# Verify shapes match
assert brain_img.shape == img.shape

# Load and check mask
mask = nib.load("outputs/brain_mask.nii.gz")
mask_data = mask.get_fdata()

# Brain should be 30-50% of volume
brain_frac = mask_data.sum() / mask_data.size
assert 0.2 < brain_frac < 0.6, f"Brain fraction {brain_frac:.1%} seems wrong"

print(f"✓ Brain fraction: {brain_frac:.1%}")
print("✓ All tests passed!")