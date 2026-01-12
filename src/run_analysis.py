"""
Collaborative fMRI Preprocessing Pipeline
Workshop Exercise - Neuroimaging with Git & HPC
"""

import os
from pathlib import Path
import nibabel as nib
from nilearn import image
import numpy as np
import matplotlib.pyplot as plt


class PreprocessingPipeline:
    """Modular fMRI preprocessing pipeline"""
    
    def __init__(self, data_dir, output_dir):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self, subject_id, run_id=1):
        """Load BIDS formatted functional data"""
        func_file = (
            self.data_dir / 
            f"sub-{subject_id}" / 
            "func" / 
            f"sub-{subject_id}_task-rest_run-{run_id}_bold.nii.gz"
        )
        
        if not func_file.exists():
            raise FileNotFoundError(f"Cannot find: {func_file}")
            
        img = nib.load(func_file)
        print(f"Loaded data shape: {img.shape}")
        return img
    
    # GROUP 1: ADD SMOOTHING METHOD HERE
    
    # GROUP 2: ADD SKULL-STRIPPING METHOD HERE
    
    # GROUP 3: ADD QA CHECK METHOD HERE
    
    # GROUP 4: ADD VISUALIZATION METHOD HERE
    
    def run_full_pipeline(self, subject_id):
        """Execute complete preprocessing pipeline"""
        print(f"\n{'='*60}")
        print(f"Processing Subject: {subject_id}")
        print(f"{'='*60}\n")
        
        # Load data
        img = self.load_data(subject_id)
        
        # GROUP 2: Call skull-strip method
        # img_stripped = self.skull_strip(img)
        
        # GROUP 1: Call smoothing method
        # img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)
        
        # GROUP 3: Call QA method
        # qa_report = self.quality_assurance(img_smoothed)
        
        # GROUP 4: Call visualization method
        # self.create_visualization(img_smoothed, subject_id)
        
        print("\nPipeline complete!")
        return img


if __name__ == "__main__":
    # Example usage
    pipeline = PreprocessingPipeline(
        data_dir="/data/shared/workshop/bids_dataset",
        output_dir="./outputs"
    )
    
    # Process first subject
    result = pipeline.run_full_pipeline(subject_id="01")