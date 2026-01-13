Group 3: Quality Assurance
===========================

.. note::
   **Branch Name:** ``feature/group-3-qa``
   
   **Objective:** Compute quality metrics to detect data problems

Background
----------

Quality assurance catches issues like excessive motion, scanner artifacts, or 
signal dropout before they contaminate your results.

**Why QA?**

- Detect motion artifacts early
- Identify problematic subjects/runs
- Monitor scanner stability
- Document data quality for publications

Requirements Checklist
----------------------

.. checkbox:: Add method ``quality_assurance(self, img)`` to ``PreprocessingPipeline`` class
.. checkbox:: Calculate temporal SNR (tSNR): mean signal / temporal standard deviation
.. checkbox:: Detect motion outliers using volume-to-volume intensity changes
.. checkbox:: Save QA report to ``outputs/sub-{subject_id}_qa_report.txt``
.. checkbox:: Return dictionary with metrics
.. checkbox:: Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def quality_assurance(self, img):
       """
       Compute quality metrics for functional data
       
       Calculates temporal signal-to-noise ratio and detects outlier
       volumes that may indicate motion or scanner artifacts.
       
       Parameters
       ----------
       img : Niimg-like object
           Preprocessed functional image (4D)
           
       Returns
       -------
       qa_metrics : dict
           Dictionary containing:
           - 'mean_tsnr': Average temporal SNR across brain
           - 'n_outlier_volumes': Number of outlier timepoints
           - 'outlier_volumes': List of outlier volume indices
           
       Notes
       -----
       Temporal SNR (tSNR) is computed as mean/std across time for each voxel.
       Higher tSNR indicates better data quality. Typical values: 20-100.
       
       Outliers are detected as volumes where global signal deviates >3 SD
       from the mean (simplified motion detection).
       """
       print("  → Running quality assurance checks...")
       
       data = img.get_fdata()  # Shape: (x, y, z, time)
       
       # TODO: Calculate temporal SNR
       # mean_signal = np.mean(data, axis=3)  # Average over time
       # std_signal = np.std(data, axis=3)    # Std dev over time
       # tsnr = mean_signal / (std_signal + 1e-10)  # Avoid division by zero
       # mean_tsnr = np.mean(tsnr[tsnr > 0])  # Average tSNR across brain
       
       # TODO: Detect outlier volumes
       # Global signal: average intensity in whole volume at each timepoint
       # volume_means = np.mean(data, axis=(0, 1, 2))  # Shape: (time,)
       # z_scores = (volume_means - volume_means.mean()) / volume_means.std()
       # outliers = np.where(np.abs(z_scores) > 3)[0]  # Indices where |z| > 3
       
       qa_metrics = {
           'mean_tsnr': mean_tsnr,
           'n_outlier_volumes': len(outliers),
           'outlier_volumes': outliers.tolist()
       }
       
       # TODO: Save report
       # report_file = self.output_dir / "qa_report.txt"
       # with open(report_file, 'w') as f:
       #     f.write(f"Quality Assurance Report\n")
       #     f.write(f"{'='*50}\n\n")
       #     f.write(f"Temporal SNR (tSNR)\n")
       #     f.write(f"  Mean tSNR: {mean_tsnr:.2f}\n\n")
       #     f.write(f"Motion Detection\n")
       #     f.write(f"  Outlier volumes: {len(outliers)}\n")
       #     if len(outliers) > 0:
       #         f.write(f"  Outlier indices: {outliers.tolist()}\n")
       # print(f"    Saved: {report_file.name}")
       
       print(f"  ✓ QA complete - Mean tSNR: {mean_tsnr:.2f}, Outliers: {len(outliers)}")
       return qa_metrics

Implementation Guide
--------------------

Step 1: Calculate Temporal SNR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   
   # Get 4D data array
   data = img.get_fdata()  # Shape: (x, y, z, time)
   
   # Calculate mean and std over time (axis=3)
   mean_signal = np.mean(data, axis=3)  # Shape: (x, y, z)
   std_signal = np.std(data, axis=3)    # Shape: (x, y, z)
   
   # Compute tSNR for each voxel
   tsnr = mean_signal / (std_signal + 1e-10)  # Add small value to avoid division by zero
   
   # Average tSNR across all brain voxels (ignore background zeros)
   mean_tsnr = np.mean(tsnr[tsnr > 0])

**What is tSNR?**

Temporal SNR measures how much the signal varies over time:

- **High tSNR** (>50): Good data quality, stable signal
- **Medium tSNR** (20-50): Acceptable quality
- **Low tSNR** (<20): Poor quality, excessive noise/motion

Step 2: Detect Motion Outliers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate global signal (mean intensity at each timepoint)
   volume_means = np.mean(data, axis=(0, 1, 2))  # Shape: (time,)
   
   # Standardize to z-scores
   z_scores = (volume_means - volume_means.mean()) / volume_means.std()
   
   # Find outliers (|z| > 3 means >3 standard deviations from mean)
   outliers = np.where(np.abs(z_scores) > 3)[0]

**Why use global signal?**

Sudden changes in global signal often indicate:

- Head motion
- Scanner artifacts
- Physiological noise spikes

Step 3: Create Report Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   qa_metrics = {
       'mean_tsnr': float(mean_tsnr),
       'n_outlier_volumes': int(len(outliers)),
       'outlier_volumes': outliers.tolist()
   }

Step 4: Save Text Report
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   report_file = self.output_dir / "qa_report.txt"
   with open(report_file, 'w') as f:
       f.write(f"Quality Assurance Report\n")
       f.write(f"{'='*50}\n\n")
       
       f.write(f"Temporal SNR (tSNR)\n")
       f.write(f"  Mean tSNR: {mean_tsnr:.2f}\n")
       f.write(f"  Interpretation: ", end="")
       if mean_tsnr > 50:
           f.write("Excellent\n")
       elif mean_tsnr > 20:
           f.write("Good\n")
       else:
           f.write("Poor - check for artifacts\n")
       f.write("\n")
       
       f.write(f"Motion Detection\n")
       f.write(f"  Total volumes: {data.shape[3]}\n")
       f.write(f"  Outlier volumes: {len(outliers)}\n")
       f.write(f"  Outlier rate: {len(outliers)/data.shape[3]*100:.1f}%\n")
       if len(outliers) > 0:
           f.write(f"  Outlier indices: {outliers.tolist()}\n")
       f.write("\n")
   
   print(f"    Saved: {report_file.name}")

Testing Your Implementation
----------------------------

.. code-block:: python

   from src.run_analysis import PreprocessingPipeline
   
   pipeline = PreprocessingPipeline(
       data_dir="/data/shared/workshop/bids_dataset",
       output_dir="./outputs"
   )
   
   # Load and run QA
   img = pipeline.load_data(subject_id="01")
   qa_metrics = pipeline.quality_assurance(img)
   
   # Verify metrics are reasonable
   assert 10 < qa_metrics['mean_tsnr'] < 200, \
       f"tSNR seems unrealistic: {qa_metrics['mean_tsnr']}"
   assert qa_metrics['n_outlier_volumes'] < 20, \
       f"Too many outliers: {qa_metrics['n_outlier_volumes']}"
   
   print(f"✓ tSNR: {qa_metrics['mean_tsnr']:.2f}")
   print(f"✓ Outliers: {qa_metrics['n_outlier_volumes']}")
   print("✓ All tests passed!")
   
   # View report
   with open("outputs/qa_report.txt") as f:
       print("\nQA Report:")
       print(f.read())

Expected output:

.. code-block:: text

   ✓ Loaded data: (64, 64, 36, 180)
     → Running quality assurance checks...
       Saved: qa_report.txt
     ✓ QA complete - Mean tSNR: 45.23, Outliers: 3
   ✓ tSNR: 45.23
   ✓ Outliers: 3
   ✓ All tests passed!
   
   QA Report:
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

Understanding the Metrics
--------------------------

Temporal SNR (tSNR)
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   tSNR = mean_signal / std_signal

**Typical values:**

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - tSNR Range
     - Quality
     - Action
   * - > 50
     - Excellent
     - Proceed with analysis
   * - 20-50
     - Good
     - Proceed with analysis
   * - 10-20
     - Poor
     - Check for artifacts
   * - < 10
     - Very Poor
     - Likely unusable

**Factors affecting tSNR:**

- Field strength (3T vs 7T)
- Voxel size (larger voxels = higher SNR)
- Brain region (cortex vs deep structures)
- Motion (head movement reduces SNR)

Motion Outliers
~~~~~~~~~~~~~~~

Volumes with |z-score| > 3 indicate sudden intensity changes.

**What causes outliers?**

- Head motion (most common)
- Scanner artifacts (spike noise)
- Physiological noise (breathing, heartbeat)

**Acceptable outlier rates:**

- **<5%**: Good data quality
- **5-10%**: Acceptable (may need scrubbing)
- **>10%**: Poor quality (consider excluding subject)

Common Issues
-------------

Issue: tSNR is extremely low (<10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Possible causes:**

1. Forgot to skull-strip (background noise inflates std)
2. Motion artifacts
3. Scanner malfunction

**Solution:** Check intermediate outputs, review raw data.

Issue: All volumes flagged as outliers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Z-score calculation on data with trend/drift

**Solution:** Remove linear trend first:

.. code-block:: python

   from scipy import signal
   volume_means_detrended = signal.detrend(volume_means)
   z_scores = (volume_means_detrended - volume_means_detrended.mean()) / volume_means_detrended.std()

Issue: tSNR varies dramatically across brain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Expected:** Lower tSNR in regions with:

- Signal dropout (orbitofrontal cortex, temporal poles)
- Large vessels
- CSF pulsation

**Solution:** This is normal. Report mean tSNR and consider region-specific QA.

Advanced QA (Optional Extensions)
----------------------------------

If you finish early, consider adding:

**1. Framewise Displacement**

.. code-block:: python

   # Estimate motion from volume-to-volume intensity changes
   dvars = np.sqrt(np.mean(np.diff(data, axis=3)**2, axis=(0, 1, 2)))

**2. tSNR Map**

.. code-block:: python

   # Save tSNR as a 3D image for visualization
   tsnr_img = nib.Nifti1Image(tsnr, img.affine, img.header)
   nib.save(tsnr_img, self.output_dir / "tsnr_map.nii.gz")

**3. Time Series Plot**

.. code-block:: python

   import matplotlib.pyplot as plt
   plt.figure(figsize=(10, 4))
   plt.plot(volume_means)
   plt.axhline(volume_means.mean(), color='r', linestyle='--', label='Mean')
   plt.scatter(outliers, volume_means[outliers], color='red', s=50, label='Outliers')
   plt.xlabel('Volume')
   plt.ylabel('Global Signal')
   plt.legend()
   plt.savefig(self.output_dir / "global_signal.png")

Git Workflow
------------

.. code-block:: bash

   git add src/run_analysis.py
   git commit -m "Add quality assurance metrics
   
   - Calculate temporal SNR (tSNR) across brain
   - Detect motion outliers using z-score method
   - Generate detailed QA report
   - Return metrics dict for programmatic access
   - Tested: tSNR ~45, <2% outlier rate"
   
   git push origin feature/group-3-qa

Helpful Resources
-----------------

- `fMRI QA best practices <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5664927/>`_
- `Understanding tSNR <https://mriquestions.com/signal-to-noise-ratio.html>`_
- `MRIQC: Automated QA <https://mriqc.readthedocs.io/>`_