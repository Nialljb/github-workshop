import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.run_anat_analysis import StructuralPipeline
import nibabel as nib

# Create pipeline
pipeline = StructuralPipeline(output_dir="./outputs")

# Run full processing chain
img = pipeline.load_data(subject_idx=0)
brain_img = pipeline.skull_strip(img)
corrected_img = pipeline.bias_field_correction(brain_img)
segmentation = pipeline.tissue_segmentation(corrected_img)

# Test visualization
pipeline.create_visualization(corrected_img, segmentation, subject_idx=0)

# Verify output exists
output_file = Path("outputs/sub-0_diagnostic.png")
assert output_file.exists(), "Diagnostic figure not created"

# Check file size (should be >100KB for real plot)
file_size_kb = output_file.stat().st_size / 1024
assert file_size_kb > 100, f"File too small: {file_size_kb:.1f}KB"

print(f"✓ Diagnostic figure created: {file_size_kb:.1f}KB")
print("✓ All tests passed!")