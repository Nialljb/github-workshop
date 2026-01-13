"""
Unit tests for structural MRI pipeline

Run with: pytest tests/test_pipeline.py
"""

import pytest
import numpy as np
from pathlib import Path
import nibabel as nib

from src.run_analysis import StructuralPipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance for testing"""
    return StructuralPipeline(output_dir="./test_outputs")


@pytest.fixture
def test_image(pipeline):
    """Load test image"""
    return pipeline.load_data(subject_idx=0)


def test_load_data(pipeline):
    """Test data loading"""
    img = pipeline.load_data(subject_idx=0)
    
    assert img is not None
    assert len(img.shape) == 3  # 3D structural image
    assert img.shape[0] > 0
    assert img.shape[1] > 0
    assert img.shape[2] > 0


def test_skull_strip(pipeline, test_image):
    """Test skull stripping"""
    brain_img = pipeline.skull_strip(test_image)
    
    # Check output
    assert brain_img is not None
    assert brain_img.shape == test_image.shape
    
    # Check mask was created
    mask_file = Path("test_outputs/brain_mask.nii.gz")
    assert mask_file.exists()
    
    # Check brain was saved
    brain_file = Path("test_outputs/brain.nii.gz")
    assert brain_file.exists()
    
    # Check brain fraction is reasonable
    mask = nib.load(mask_file)
    mask_data = mask.get_fdata()
    brain_fraction = mask_data.sum() / mask_data.size
    assert 0.2 < brain_fraction < 0.6


def test_bias_correction(pipeline, test_image):
    """Test bias field correction"""
    brain_img = pipeline.skull_strip(test_image)
    corrected_img = pipeline.bias_field_correction(brain_img)
    
    # Check output
    assert corrected_img is not None
    assert corrected_img.shape == brain_img.shape
    
    # Check outputs were saved
    assert Path("test_outputs/corrected.nii.gz").exists()
    assert Path("test_outputs/bias_field.nii.gz").exists()


def test_tissue_segmentation(pipeline, test_image):
    """Test tissue segmentation"""
    brain_img = pipeline.skull_strip(test_image)
    corrected_img = pipeline.bias_field_correction(brain_img)
    segmentation = pipeline.tissue_segmentation(corrected_img)
    
    # Check structure
    assert 'gm' in segmentation
    assert 'wm' in segmentation
    assert 'csf' in segmentation
    assert 'volumes_ml' in segmentation
    
    # Check volumes are reasonable
    volumes = segmentation['volumes_ml']
    total = volumes['gm'] + volumes['wm'] + volumes['csf']
    
    assert 1000 < total < 2000  # Total brain volume
    assert 400 < volumes['gm'] < 1000
    assert 200 < volumes['wm'] < 800
    assert 50 < volumes['csf'] < 400


def test_visualization(pipeline, test_image):
    """Test visualization creation"""
    brain_img = pipeline.skull_strip(test_image)
    corrected_img = pipeline.bias_field_correction(brain_img)
    segmentation = pipeline.tissue_segmentation(corrected_img)
    
    pipeline.create_visualization(corrected_img, segmentation, subject_idx=0)
    
    # Check output file
    output_file = Path("test_outputs/sub-0_diagnostic.png")
    assert output_file.exists()
    
    # Check file size (should be substantial)
    file_size = output_file.stat().st_size
    assert file_size > 100000  # > 100KB


def test_full_pipeline(pipeline):
    """Test complete pipeline"""
    result = pipeline.run_full_pipeline(subject_idx=0)
    
    assert result is not None
    
    # Check all outputs exist
    outputs = [
        "brain_mask.nii.gz",
        "brain.nii.gz",
        "corrected.nii.gz",
        "bias_field.nii.gz",
        "gm_prob.nii.gz",
        "wm_prob.nii.gz",
        "csf_prob.nii.gz",
        "sub-0_diagnostic.png"
    ]
    
    for output in outputs:
        assert (Path("test_outputs") / output).exists(), f"Missing: {output}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])