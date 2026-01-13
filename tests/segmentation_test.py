import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.run_anat_analysis import StructuralPipeline
import nibabel as nib


# Create pipeline
pipeline = StructuralPipeline(output_dir="./outputs")

# Load, skull strip, bias correct
img = pipeline.load_data(subject_idx=0)
brain_img = pipeline.skull_strip(img)
corrected_img = pipeline.bias_field_correction(brain_img)

# Test segmentation
segmentation = pipeline.tissue_segmentation(corrected_img)

# Verify outputs exist
from pathlib import Path
assert Path("outputs/gm_prob.nii.gz").exists()
assert Path("outputs/wm_prob.nii.gz").exists()
assert Path("outputs/csf_prob.nii.gz").exists()

# Verify structure
assert 'gm' in segmentation
assert 'wm' in segmentation
assert 'csf' in segmentation
assert 'volumes_ml' in segmentation

# Check volumes are reasonable (adult brain ranges)
volumes = segmentation['volumes_ml']
total_volume = volumes['gm'] + volumes['wm'] + volumes['csf']

assert 1000 < total_volume < 2500, f"Total volume {total_volume:.0f}ml seems wrong"
assert 400 < volumes['gm'] < 1000, f"GM volume {volumes['gm']:.1f}ml seems wrong"
assert 300 < volumes['wm'] < 1200, f"WM volume {volumes['wm']:.1f}ml seems wrong"
assert 100 < volumes['csf'] < 600, f"CSF volume {volumes['csf']:.1f}ml seems wrong"

print(f"✓ GM:  {volumes['gm']:.1f} ml")
print(f"✓ WM:  {volumes['wm']:.1f} ml")
print(f"✓ CSF: {volumes['csf']:.1f} ml")
print(f"✓ Total: {total_volume:.1f} ml")
print("✓ All tests passed!")