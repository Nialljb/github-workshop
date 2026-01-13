"""
Collaborative Structural MRI Processing Pipeline
"""

import os
from pathlib import Path
import nibabel as nib
from nilearn import datasets, plotting, image
import numpy as np
import matplotlib.pyplot as plt


class StructuralPipeline:
    """Modular structural MRI processing pipeline"""

    def __init__(self, output_dir):
        """
        Initialize structural processing pipeline

        Parameters
        ----------
        output_dir : str or Path
            Path to save outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, subject_idx=0):
        """
        Load structural MRI data from local Haxby dataset

        Parameters
        ----------
        subject_idx : int
            Subject index (0-based, max 2 for 3 subjects)

        Returns
        -------
        img : Nifti1Image
            T1-weighted structural MRI image
        """
        print(f"Loading subject {subject_idx+1} from local Haxby dataset...")

        # Check if data exists, download if needed
        data_path = Path("data/haxby2001")
        subject_dirs = ["subj1", "subj2", "subj3"]

        if subject_idx >= len(subject_dirs):
            raise ValueError(f"Subject index {subject_idx} out of range. Max: {len(subject_dirs)-1}")

        img_path = data_path / subject_dirs[subject_idx] / "anat.nii.gz"

        # Auto-download if data doesn't exist
        if not img_path.exists():
            print("📥 Dataset not found locally. Downloading Haxby dataset...")
            self._download_dataset()

            # Check again after download
            if not img_path.exists():
                raise FileNotFoundError(f"Download failed. Data not found at {img_path}")

        img = nib.load(str(img_path))

        print(f"✓ Loaded anatomical data: {img.shape}")
        print(f"✓ Voxel size: {img.header.get_zooms()[:3]} mm")
        return img

    def _download_dataset(self):
        """Download Haxby dataset if not already present"""
        try:
            from nilearn import datasets
            print("Downloading Haxby dataset (3 subjects)...")
            dataset = datasets.fetch_haxby(subjects=[1, 2, 3], data_dir="data/")
            print("✅ Download complete!")
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print("Manual download option:")
            print("Run: python scripts/download_workshop_data.py")
            raise
        return img

    # GROUP 1: IMPLEMENT SKULL STRIPPING METHOD HERE

    # GROUP 2: IMPLEMENT BIAS FIELD CORRECTION METHOD HERE

    # GROUP 3: IMPLEMENT TISSUE SEGMENTATION METHOD HERE

    # GROUP 4: IMPLEMENT VISUALIZATION METHOD HERE


    def run_full_pipeline(self, subject_idx=0):
        """
        Execute complete structural processing pipeline

        Parameters
        ----------
        subject_idx : int
            Subject index

        Returns
        -------
        img : Nifti1Image
            Final processed image
        """
        print(f"\n{'='*60}")
        print(f"Processing Subject: {subject_idx}")
        print(f"{'='*60}\n")

        # Load data
        img = self.load_data(subject_idx)

        # GROUP 1: Uncomment after skull stripping PR merged
        # img_brain = self.skull_strip(img)

        # GROUP 2: Uncomment after bias correction PR merged
        # img_corrected = self.bias_field_correction(img_brain)

        # GROUP 3: Uncomment after segmentation PR merged
        # segmentation = self.tissue_segmentation(img_corrected)

        # GROUP 4: Uncomment after visualization PR merged
        # self.create_visualization(img_corrected, segmentation, subject_idx)

        print("\n✓ Pipeline complete!")
        return img


if __name__ == "__main__":
    # Example usage
    pipeline = StructuralPipeline(output_dir="./outputs")

    # Process first subject
    result = pipeline.run_full_pipeline(subject_idx=0)