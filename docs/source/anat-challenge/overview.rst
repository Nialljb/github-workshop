Group Analysis Challenge Overview
==================================

The Mission
-----------

Your lab is building a collaborative structural MRI processing pipeline. Each team 
implements **one critical component**, then all components are integrated 
through Pull Requests to create a complete, working pipeline.

Dataset Information
-------------------

We'll use the **Haxby Dataset** - a classic visual object recognition fMRI dataset
that includes both anatomical and functional data.

- **Format**: NIfTI T1-weighted anatomical + BOLD functional images
- **Access**: Automatically downloaded via nilearn
- **Subjects**: 3 subjects (perfect for 3-4 workshop groups)
- **Anatomical**: 124×256×256 voxels at ~1mm resolution
- **Functional**: 40×64×64×1452 timepoints (visual task data)
- **Extras**: Pre-computed ROI masks for visual cortex regions

**Data Location:**

All groups will work with the same shared dataset located in:
``data/haxby2001/`` - 3 subjects available for testing and comparison

The dataset will be downloaded to your workspace using the provided download script.

Repository Structure
--------------------

.. code-block:: text

   neuroimaging-workshop/
   ├── README.md                    # Workshop instructions
   ├── requirements.txt             # Python dependencies
   ├── .gitignore                   # Files Git should ignore
   ├── data/                        # Downloaded datasets
   │   ├── haxby2001/              # Main workshop dataset
   │   │   ├── subj1/              # Group 1 data
   │   │   │   └── anat.nii.gz     # T1 anatomical image
   │   │   ├── subj2/              # Group 2 data
   │   │   │   └── anat.nii.gz     
   │   │   ├── subj3/              # Group 3 data
   │   │   │   └── anat.nii.gz
   │   │   └── mask.nii.gz         # Shared brain mask
   │   └── .gitkeep                
   ├── outputs/                     # Generated outputs (not committed)
   │   ├── subj1_brain_mask.nii.gz # Example outputs
   │   ├── subj1_brain.nii.gz
   │   └── .gitkeep
   ├── src/
   │   ├── __init__.py
   │   └── run_analysis.py          # ← YOUR GROUP EDITS THIS
   ├── scripts/
   │   ├── download_workshop_data.py # Data download script
   │   └── batch_process.py         # Batch processing utilities
   ├── tests/
   │   └── test_analysis.py         # Unit tests (optional)
   └── docs/
       └── datasets_summary.md     # Data overview

Skeleton Code
-------------

**File:** ``src/run_analysis.py``

.. code-block:: python

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
```

Data Setup
----------

**Option 1: Automatic Download (Recommended)**

The pipeline automatically downloads data when needed. Simply run your code and it will detect missing data and download it:

.. code-block:: python

   # This will auto-download if data doesn't exist
   pipeline = StructuralPipeline(output_dir="./outputs")
   result = pipeline.run_full_pipeline(subject_idx=0)

**Option 2: Manual Download**

If you prefer to download data explicitly beforehand:

.. code-block:: bash

   # In your workshop directory
   cd neuroimaging-workshop
   
   # Activate virtual environment
   source venv/bin/activate
   
   # Install required packages
   pip install nilearn nibabel matplotlib
   
   # Download Haxby dataset (3 subjects)
   python scripts/download_workshop_data.py

This will download:

- **3 subjects** with T1 anatomical images (~1mm resolution)
- **Functional data** for advanced analyses (optional)
- **Brain masks** and ROI masks for reference
- **Task labels** for stimulus-based analysis

**Verify your data:**

.. code-block:: python

   import nibabel as nib
   
   # Check subject 1 data
   img = nib.load('data/haxby2001/subj1/anat.nii.gz')
   print(f"Shape: {img.shape}")
   print(f"Voxel size: {img.header.get_zooms()[:3]} mm")
   # Expected: (124, 256, 256) at ~1x1x1mm

Group Tasks
-----------

.. list-table::
   :header-rows: 1
   :widths: 10 20 30 40

   * - Group
     - Branch Name
     - Task
     - Method
   * - 🔵 Group 1
     - ``feature/group-1-skullstrip``
     - Skull stripping (brain extraction)
     - ``skull_strip(self, img)``
   * - 🟢 Group 2
     - ``feature/group-2-biascorrection``
     - Bias field correction
     - ``bias_field_correction(self, img)``
   * - 🟡 Group 3
     - ``feature/group-3-segmentation``
     - Tissue segmentation (GM/WM/CSF)
     - ``tissue_segmentation(self, img)``
   * - 🟣 Group 4
     - ``feature/group-4-visualization``
     - Multi-panel visualization
     - ``create_visualization(self, img, seg, subject_idx)``

See individual group task pages for detailed instructions.

Why Structural MRI?
-------------------

Structural MRI processing is fundamental to neuroimaging:

- **Brain extraction**: Remove skull and non-brain tissue
- **Bias correction**: Remove intensity inhomogeneities from scanner
- **Tissue segmentation**: Separate gray matter, white matter, CSF
- **Quality control**: Visualize results for quality assurance

These preprocessing steps are prerequisites for:

- Volumetric analysis (measuring brain structure volumes)
- Cortical thickness estimation
- Registration to standard space
- Statistical analysis

Workshop Timeline
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Phase
     - Description
   * - **Phase 1** (15 min)
     - Repository setup: Fork, clone, create branch
   * - **Phase 2** (40 min)
     - Group coding sprint: Implement your task
   * - **Phase 3** (25 min)
     - Pull requests and code review
   * - **Phase 4** (20 min)
     - Merge conflict resolution and integration
   * - **Phase 5** (Demo)
     - Final integration: Test complete pipeline


Dataset Citation
~~~~~~~~~~~~~~~~

If you use this data in publications:

.. code-block:: text

   Haxby, J.V., Gobbini, M.I., Furey, M.L., Ishai, A., Schouten, J.L.,
   and Pietrini, P. (2001). Distributed and overlapping representations
   of faces and objects in ventral temporal cortex. Science 293, 2425-2430.
```
