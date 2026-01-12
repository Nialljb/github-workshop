Group Analysis Challenge Overview
==================================

The Mission
-----------

Your lab is building a collaborative fMRI preprocessing pipeline. Each team 
implements **one critical component**, then all components are integrated 
through Pull Requests to create a complete, working pipeline.

Dataset Information
-------------------

- **Format**: BIDS-formatted resting-state fMRI data
- **Location**: ``/data/shared/workshop/bids_dataset/``
- **Subjects**: 01, 02, 03
- **Access**: Read-only

Repository Structure
--------------------

.. code-block:: text

   neuroimaging-workshop/
   ├── README.md                    # Workshop instructions
   ├── requirements.txt             # Python dependencies
   ├── .gitignore                   # Files Git should ignore
   ├── data/
   │   └── .gitkeep                 # Placeholder
   ├── outputs/                     # Generated outputs (not committed)
   │   └── .gitkeep
   ├── src/
   │   ├── __init__.py
   │   └── run_analysis.py          # ← YOUR GROUP EDITS THIS
   └── tests/
       └── test_analysis.py         # Unit tests (optional)

Skeleton Code
-------------

**File:** ``src/run_analysis.py``

.. code-block:: python

   """
   Collaborative fMRI Preprocessing Pipeline
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
           print(f"✓ Loaded data: {img.shape}")
           return img
       
       # GROUP 1: IMPLEMENT SMOOTHING METHOD HERE
       
       # GROUP 2: IMPLEMENT SKULL-STRIPPING METHOD HERE
       
       # GROUP 3: IMPLEMENT QA METHOD HERE
       
       # GROUP 4: IMPLEMENT VISUALIZATION METHOD HERE
       
       def run_full_pipeline(self, subject_id):
           """Execute complete preprocessing pipeline"""
           print(f"\n{'='*60}")
           print(f"Processing Subject: {subject_id}")
           print(f"{'='*60}\n")
           
           img = self.load_data(subject_id)
           
           # Methods will be uncommented as PRs merge
           
           print("\n✓ Pipeline complete!")
           return img

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
     - ``feature/group-1-smoothing``
     - Spatial smoothing
     - ``smooth_image(self, img, fwhm=6.0)``
   * - 🟢 Group 2
     - ``feature/group-2-skullstrip``
     - Skull stripping
     - ``skull_strip(self, img)``
   * - 🟡 Group 3
     - ``feature/group-3-qa``
     - Quality assurance
     - ``quality_assurance(self, img)``
   * - 🟣 Group 4
     - ``feature/group-4-visualization``
     - Visualization
     - ``create_visualization(self, img, subject_id)``

See individual group task pages for detailed instructions.

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