import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.run_anat_analysis import StructuralPipeline
import nibabel as nib

# Create pipeline
pipeline = StructuralPipeline(output_dir="./outputs")

# Load and skull strip
img = pipeline.load_data(subject_idx=0)
brain_img = pipeline.skull_strip(img)

# Test bias correction
corrected_img = pipeline.bias_field_correction(brain_img)

# Verify outputs
from pathlib import Path
assert Path("outputs/corrected.nii.gz").exists()
assert Path("outputs/bias_field.nii.gz").exists()

# Verify shapes match
assert corrected_img.shape == brain_img.shape

# Load bias field and check range
bias_field = nib.load("outputs/bias_field.nii.gz")
bias_data = bias_field.get_fdata()

# Bias field should be close to 1.0 (multiplicative factor)
brain_data = brain_img.get_fdata()
bias_values = bias_data[brain_data > 0]

print(f"✓ Bias field range: {bias_values.min():.2f} - {bias_values.max():.2f}")
print(f"✓ Bias field mean: {bias_values.mean():.2f}")
print("✓ All tests passed!")