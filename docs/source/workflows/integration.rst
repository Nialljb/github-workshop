Final Integration and Testing
==============================

Overview
--------

After all group PRs are merged, this page guides you through testing the 
complete integrated pipeline.

Merge Completion Checklist
---------------------------

Before final integration, verify:

.. checkbox:: Group 2 (Skull Stripping) PR merged
.. checkbox:: Group 1 (Smoothing) PR merged
.. checkbox:: Group 3 (QA) PR merged
.. checkbox:: Group 4 (Visualization) PR merged
.. checkbox:: All merge conflicts resolved
.. checkbox:: No failing tests

Updating Your Local Repository
-------------------------------

Step 1: Fetch All Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Get latest from instructor's repo
   git fetch upstream
   
   # See what's new
   git log upstream/main --oneline -10

**Expected output:**

.. code-block:: text

   f7d3e2a Merge pull request #4 from student4/feature/group-4-visualization
   e6c2d1b Merge pull request #3 from student3/feature/group-3-qa
   d5b1c0a Merge pull request #2 from student2/feature/group-1-smoothing
   c4a0b9f Merge pull request #1 from student1/feature/group-2-skullstrip
   b3e9a8d Initial pipeline skeleton

Step 2: Update Main Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Switch to main
   git checkout main
   
   # Merge upstream changes
   git merge upstream/main
   
   # Push to your fork
   git push origin main

Step 3: Verify All Changes Present
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check that all methods exist
   grep -n "def smooth_image" src/run_analysis.py
   grep -n "def skull_strip" src/run_analysis.py
   grep -n "def quality_assurance" src/run_analysis.py
   grep -n "def create_visualization" src/run_analysis.py

**Expected output:**

.. code-block:: text

   45:    def skull_strip(self, img):
   78:    def smooth_image(self, img, fwhm=6.0):
   112:    def quality_assurance(self, img):
   165:    def create_visualization(self, img, subject_id):

Activating Function Calls
--------------------------

The Complete Pipeline
~~~~~~~~~~~~~~~~~~~~~

Edit ``src/run_analysis.py`` in the ``run_full_pipeline`` method:

**Before (all commented):**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       print(f"\n{'='*60}")
       print(f"Processing Subject: {subject_id}")
       print(f"{'='*60}\n")
       
       img = self.load_data(subject_id)
       
       # GROUP 2: Uncomment after skull-stripping PR merged
       # img_stripped = self.skull_strip(img)
       
       # GROUP 1: Uncomment after smoothing PR merged
       # img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)
       
       # GROUP 3: Uncomment after QA PR merged
       # qa_report = self.quality_assurance(img_smoothed)
       
       # GROUP 4: Uncomment after visualization PR merged
       # self.create_visualization(img_smoothed, subject_id)
       
       print("\n✓ Pipeline complete!")
       return img

**After (all uncommented):**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       print(f"\n{'='*60}")
       print(f"Processing Subject: {subject_id}")
       print(f"{'='*60}\n")
       
       img = self.load_data(subject_id)
       
       # GROUP 2: Skull stripping
       img_stripped = self.skull_strip(img)
       
       # GROUP 1: Smoothing
       img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)
       
       # GROUP 3: Quality assurance
       qa_report = self.quality_assurance(img_smoothed)
       
       # GROUP 4: Visualization
       self.create_visualization(img_smoothed, subject_id)
       
       print("\n✓ Pipeline complete!")
       return img_smoothed

.. note::
   Notice the data flows: ``img`` → ``img_stripped`` → ``img_smoothed``

Running the Complete Pipeline
------------------------------

Step 1: Activate Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Activate virtual environment
   source venv/bin/activate
   
   # Verify Python packages
   pip list | grep nilearn
   pip list | grep matplotlib

Step 2: Run Pipeline
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run on first subject
   python src/run_analysis.py

**Expected output:**

.. code-block:: text

   ============================================================
   Processing Subject: 01
   ============================================================
   
   ✓ Loaded data: (64, 64, 36, 180)
     → Computing brain mask...
       Brain mask: 27,648 / 147,456 voxels (18.7%)
       Saved: brain_mask.nii.gz
     ✓ Skull stripping complete
     → Applying spatial smoothing (FWHM=6.0mm)...
       Saved: smoothed_fwhm-6.0.nii.gz
     ✓ Smoothing complete
     → Running quality assurance checks...
       Saved: qa_report.txt
     ✓ QA complete - Mean tSNR: 45.23, Outliers: 3
     → Creating diagnostic visualizations...
       Saved: sub-01_diagnostic.png
     ✓ Visualization saved
   
   ✓ Pipeline complete!

Step 3: Verify Outputs
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check output directory
   ls -lh outputs/

**Expected files:**

.. code-block:: text

   brain_mask.nii.gz          # Group 2: Mask
   smoothed_fwhm-6.0.nii.gz   # Group 1: Smoothed data
   qa_report.txt              # Group 3: QA metrics
   sub-01_diagnostic.png      # Group 4: Visualization

Validation and Quality Checks
------------------------------

Check 1: Brain Mask
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Quick check with Python
   python -c "
   import nibabel as nib
   mask = nib.load('outputs/brain_mask.nii.gz')
   data = mask.get_fdata()
   print(f'Mask shape: {data.shape}')
   print(f'Brain voxels: {int(data.sum()):,}')
   print(f'Coverage: {data.sum()/data.size*100:.1f}%')
   "

**Expected output:**

.. code-block:: text

   Mask shape: (64, 64, 36)
   Brain voxels: 27,648
   Coverage: 18.7%

.. tip::
   Brain should be 15-25% of total volume for functional data.

Check 2: Smoothed Data
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -c "
   import nibabel as nib
   import numpy as np
   
   original = nib.load('/data/shared/workshop/bids_dataset/sub-01/func/sub-01_task-rest_run-1_bold.nii.gz')
   smoothed = nib.load('outputs/smoothed_fwhm-6.0.nii.gz')
   
   orig_data = original.get_fdata()
   smooth_data = smoothed.get_fdata()
   
   print(f'Original std: {orig_data.std():.2f}')
   print(f'Smoothed std: {smooth_data.std():.2f}')
   print(f'Reduction: {(1 - smooth_data.std()/orig_data.std())*100:.1f}%')
   "

**Expected output:**

.. code-block:: text

   Original std: 1234.56
   Smoothed std: 1198.23
   Reduction: 2.9%

Check 3: QA Report
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # View QA report
   cat outputs/qa_report.txt

**Expected output:**

.. code-block:: text

   Quality Assurance Report
   ==================================================
   
   Temporal SNR (tSNR)
     Mean tSNR: 45.23
     Interpretation: Good
   
   Motion Detection
     Total volumes: 180
     Outlier volumes: 3
     Outlier rate: 1.7%
     Outlier indices: [45, 89, 134]

.. success::
   tSNR of 45 is good quality for 3T fMRI data!

Check 4: Visualization
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Open diagnostic figure
   xdg-open outputs/sub-01_diagnostic.png  # Linux
   # open outputs/sub-01_diagnostic.png    # Mac
   # start outputs/sub-01_diagnostic.png   # Windows

**What to look for:**

- **Mean EPI:** Clear brain anatomy, no excessive blur
- **Temporal Std:** Cortex brighter than white matter
- **Carpet Plot:** No obvious vertical stripes (motion)
- **Global Signal:** Smooth with minimal spikes

Processing Multiple Subjects
-----------------------------

Batch Processing Script
~~~~~~~~~~~~~~~~~~~~~~~

Create ``scripts/batch_process.py``:

.. code-block:: python

   #!/usr/bin/env python
   """
   Batch process all subjects through pipeline
   """
   
   from pathlib import Path
   from src.run_analysis import PreprocessingPipeline
   
   def main():
       # Setup pipeline
       pipeline = PreprocessingPipeline(
           data_dir="/data/shared/workshop/bids_dataset",
           output_dir="./outputs"
       )
       
       # Get all subjects
       subjects = ['01', '02', '03']
       
       # Process each subject
       results = {}
       for subject_id in subjects:
           try:
               print(f"\n{'='*70}")
               print(f"PROCESSING SUBJECT {subject_id}")
               print(f"{'='*70}")
               
               result = pipeline.run_full_pipeline(subject_id)
               results[subject_id] = 'success'
               
           except Exception as e:
               print(f"✗ Error processing subject {subject_id}: {e}")
               results[subject_id] = 'failed'
       
       # Summary
       print(f"\n{'='*70}")
       print("BATCH PROCESSING SUMMARY")
       print(f"{'='*70}")
       for subject_id, status in results.items():
           icon = '✓' if status == 'success' else '✗'
           print(f"{icon} Subject {subject_id}: {status}")
   
   if __name__ == "__main__":
       main()

**Run batch processing:**

.. code-block:: bash

   python scripts/batch_process.py

Comparing Results Across Subjects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # scripts/compare_qa.py
   import pandas as pd
   import glob
   
   # Collect QA metrics
   qa_files = glob.glob('outputs/sub-*_qa_report.txt')
   
   data = []
   for qa_file in qa_files:
       subject_id = qa_file.split('sub-')[1].split('_')[0]
       
       with open(qa_file) as f:
           content = f.read()
           # Parse tSNR
           tsnr = float(content.split('Mean tSNR: ')[1].split('\n')[0])
           # Parse outliers
           n_outliers = int(content.split('Outlier volumes: ')[1].split('\n')[0])
       
       data.append({
           'subject': subject_id,
           'tsnr': tsnr,
           'outliers': n_outliers
       })
   
   # Create DataFrame
   df = pd.DataFrame(data)
   print(df)
   print(f"\nMean tSNR: {df['tsnr'].mean():.2f}")
   print(f"Mean outliers: {df['outliers'].mean():.1f}")

Performance Benchmarking
------------------------

Timing the Pipeline
~~~~~~~~~~~~~~~~~~~

Add timing to ``run_full_pipeline``:

.. code-block:: python

   import time
   
   def run_full_pipeline(self, subject_id):
       start_time = time.time()
       
       # ... existing code ...
       
       elapsed = time.time() - start_time
       print(f"\n✓ Pipeline complete in {elapsed:.1f} seconds!")

**Typical execution times:**

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Step
     - Time
     - Notes
   * - Data loading
     - 2-5s
     - Depends on disk I/O
   * - Skull stripping
     - 3-8s
     - Mask computation
   * - Smoothing
     - 5-10s
     - 3D convolution
   * - QA
     - 2-4s
     - Statistical calculations
   * - Visualization
     - 3-6s
     - Plotting and file I/O
   * - **Total**
     - **15-33s**
     - Per subject

Troubleshooting Integration Issues
-----------------------------------

Error: "NameError: name 'img_stripped' is not defined"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Function calls not in correct order.

**Solution:** Verify data flow:

.. code-block:: python

   img = self.load_data(subject_id)           # Original
   img_stripped = self.skull_strip(img)       # Operates on img
   img_smoothed = self.smooth_image(img_stripped)  # Operates on stripped

Error: Shape mismatch between steps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** One function changed image dimensions.

**Solution:** Add shape checks:

.. code-block:: python

   img = self.load_data(subject_id)
   print(f"After load: {img.shape}")
   
   img_stripped = self.skull_strip(img)
   print(f"After strip: {img_stripped.shape}")
   assert img.shape == img_stripped.shape, "Skull strip changed shape!"

Error: "FileNotFoundError: outputs/..."
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Output directory not created.

**Solution:** Already handled in ``__init__``, but verify:

.. code-block:: python

   self.output_dir.mkdir(parents=True, exist_ok=True)

Committing Final Integration
-----------------------------

Step 1: Create Integration Commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check what changed
   git diff src/run_analysis.py
   
   # Stage changes
   git add src/run_analysis.py
   
   # Commit with descriptive message
   git commit -m "Integrate all preprocessing components
   
   - Uncommented all function calls in run_full_pipeline()
   - Verified correct data flow between components
   - Tested on subjects 01, 02, 03
   - All outputs generated successfully
   
   Pipeline order:
   1. Skull stripping (Group 2)
   2. Smoothing (Group 1)
   3. QA metrics (Group 3)
   4. Visualization (Group 4)"

Step 2: Push Integration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Push to your fork
   git push origin main

.. note::
   Typically, instructor handles final integration. This is for reference if 
   you want to test the complete pipeline locally.

Documentation and Reporting
---------------------------

Creating a Summary Report
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # scripts/generate_report.py
   import matplotlib.pyplot as plt
   import pandas as pd
   
   # Collect results
   subjects = ['01', '02', '03']
   tsnr_values = [45.2, 42.8, 48.1]
   outliers = [3, 5, 2]
   
   # Create summary figure
   fig, axes = plt.subplots(1, 2, figsize=(10, 4))
   
   # tSNR plot
   axes[0].bar(subjects, tsnr_values, color='steelblue')
   axes[0].set_xlabel('Subject')
   axes[0].set_ylabel('Mean tSNR')
   axes[0].set_title('Data Quality Across Subjects')
   axes[0].axhline(y=40, color='r', linestyle='--', alpha=0.5)
   
   # Outliers plot
   axes[1].bar(subjects, outliers, color='coral')
   axes[1].set_xlabel('Subject')
   axes[1].set_ylabel('Number of Outlier Volumes')
   axes[1].set_title('Motion Artifacts')
   
   plt.tight_layout()
   plt.savefig('outputs/summary_report.png', dpi=150)
   print("✓ Summary report saved")

Exporting Pipeline
------------------

For Use in Future Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create a clean copy of the pipeline
   mkdir -p ~/my_projects/fmri_pipeline
   cp src/run_analysis.py ~/my_projects/fmri_pipeline/
   cp requirements.txt ~/my_projects/fmri_pipeline/

.. code-block:: python

   # Example usage in future project
   from fmri_pipeline import PreprocessingPipeline
   
   pipeline = PreprocessingPipeline(
       data_dir="/path/to/my/bids/data",
       output_dir="/path/to/my/outputs"
   )
   
   result = pipeline.run_full_pipeline(subject_id="42")

Next Steps
----------

After completing the workshop:

1. **For Your Research:**

   - Adapt pipeline for your specific data
   - Add project-specific preprocessing steps
   - Integrate with existing analysis workflows

2. **Improve the Code:**

   - Add command-line interface
   - Implement parallel processing
   - Add more comprehensive tests
   - Create configuration files

3. **Collaboration:**

   - Set up lab GitHub organization
   - Create shared analysis templates
   - Establish code review practices

4. **Advanced Topics:**

   - Containerization (Docker/Singularity)
   - CI/CD for automated testing
   - HPC job submission integration

Workshop Completion Checklist
------------------------------

.. checkbox:: All group PRs successfully merged
.. checkbox:: Complete pipeline runs without errors
.. checkbox:: All outputs generated correctly
.. checkbox:: QA metrics within expected ranges
.. checkbox:: Visualizations look correct
.. checkbox:: Tested on multiple subjects
.. checkbox:: Code committed to repository
.. checkbox:: Understanding of Git workflows achieved

Congratulations!
----------------

🎉 You've successfully completed the Collaborative Neuroimaging Workshop!

You've learned:

- ✅ VS Code remote development on HPC
- ✅ Git branching and pull requests
- ✅ Collaborative code review
- ✅ Merge conflict resolution
- ✅ Modular neuroimaging pipeline development
- ✅ Professional software development practices

Further Learning
----------------

- `Nilearn Advanced Tutorials <https://nilearn.github.io/stable/auto_examples/index.html>`_
- `fMRIPrep <https://fmriprep.org/>`_ - Production preprocessing pipeline
- `BIDS Apps <https://bids-apps.neuroimaging.io/>`_ - Containerized neuroimaging tools
- `Neurohackademy <https://neurohackademy.org/>`_ - Advanced neuroimaging + software skills