Group 4: Visualization
======================

.. note::
   **Branch Name:** ``feature/group-4-visualization``
   
   **Objective:** Create diagnostic plots for quality checking preprocessing results

Background
----------

Visualization is essential for catching preprocessing errors that metrics alone 
might miss. A good diagnostic figure helps you:

- Verify preprocessing worked correctly
- Identify remaining artifacts
- Communicate results to collaborators
- Document data quality for publications

Requirements Checklist
----------------------

.. checkbox:: Add method ``create_visualization(self, img, subject_id)`` to ``PreprocessingPipeline`` class
.. checkbox:: Generate multi-panel figure with Mean EPI, Temporal Std Dev, Carpet Plot, Global Signal
.. checkbox:: Save figure to ``outputs/sub-{subject_id}_diagnostic.png``
.. checkbox:: Use matplotlib for plotting
.. checkbox:: Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def create_visualization(self, img, subject_id):
       """
       Create diagnostic visualization of preprocessed data
       
       Generates a multi-panel figure showing key preprocessing outputs
       for quality assurance and debugging.
       
       Parameters
       ----------
       img : Niimg-like object
           Preprocessed functional image (4D)
       subject_id : str
           Subject identifier (used in title and filename)
           
       Returns
       -------
       None
           Saves figure to outputs directory
           
       Notes
       -----
       Figure panels:
       1. Mean EPI: Average signal across time (anatomical reference)
       2. Temporal Std: Standard deviation map (motion/artifacts appear bright)
       3. Carpet plot: Heatmap of voxel intensities over time
       4. Global signal: Mean intensity timeseries
       """
       from nilearn import plotting
       import matplotlib.pyplot as plt
       
       print("  → Creating diagnostic visualizations...")
       
       data = img.get_fdata()
       
       # TODO: Create figure with 2x2 subplots
       # fig, axes = plt.subplots(2, 2, figsize=(12, 10))
       # fig.suptitle(f'Preprocessing Diagnostics - Subject {subject_id}', 
       #              fontsize=16, fontweight='bold')
       
       # TODO: Panel 1 - Mean EPI (top-left)
       # mean_img = image.mean_img(img)
       # plotting.plot_epi(mean_img, axes=axes[0, 0], 
       #                   title="Mean EPI", colorbar=True)
       
       # TODO: Panel 2 - Temporal Std Dev Map (top-right)
       # std_data = np.std(data, axis=3)
       # mid_slice = std_data.shape[2] // 2
       # im = axes[0, 1].imshow(std_data[:, :, mid_slice], cmap='hot')
       # axes[0, 1].set_title("Temporal Std Dev (mid-slice)")
       # axes[0, 1].axis('off')
       # plt.colorbar(im, ax=axes[0, 1])
       
       # TODO: Panel 3 - Carpet Plot (bottom-left)
       # n_voxels = 1000
       # flat_data = data.reshape(-1, data.shape[3])
       # random_idx = np.random.choice(flat_data.shape[0], n_voxels, replace=False)
       # sample_voxels = flat_data[random_idx, :]
       # im = axes[1, 0].imshow(sample_voxels, aspect='auto', cmap='gray')
       # axes[1, 0].set_title("Carpet Plot (1000 random voxels)")
       # axes[1, 0].set_xlabel("Time (volumes)")
       # axes[1, 0].set_ylabel("Voxels")
       
       # TODO: Panel 4 - Global Signal (bottom-right)
       # global_signal = np.mean(data, axis=(0, 1, 2))
       # axes[1, 1].plot(global_signal, linewidth=0.8)
       # axes[1, 1].set_title("Global Signal Timeseries")
       # axes[1, 1].set_xlabel("Volume")
       # axes[1, 1].set_ylabel("Mean Intensity")
       # axes[1, 1].grid(True, alpha=0.3)
       
       # TODO: Save figure
       # plt.tight_layout()
       # output_file = self.output_dir / f"sub-{subject_id}_diagnostic.png"
       # plt.savefig(output_file, dpi=150, bbox_inches='tight')
       # plt.close()
       # print(f"    Saved: {output_file.name}")
       
       print(f"  ✓ Visualization saved")

Implementation Guide
--------------------

Step 1: Create Figure Layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   from nilearn import plotting, image
   import numpy as np
   
   # Create 2x2 subplot grid
   fig, axes = plt.subplots(2, 2, figsize=(12, 10))
   fig.suptitle(
       f'Preprocessing Diagnostics - Subject {subject_id}',
       fontsize=16,
       fontweight='bold',
       y=0.98
   )
   
   # Get data array
   data = img.get_fdata()

Step 2: Panel 1 - Mean EPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate mean across time
   mean_img = image.mean_img(img)
   
   # Plot using nilearn
   plotting.plot_epi(
       mean_img,
       axes=axes[0, 0],
       title="Mean EPI",
       colorbar=True,
       cmap='gray'
   )

**What this shows:** Average brain anatomy over the entire scan.

**What to look for:**

- Clear brain boundaries
- No excessive blurring
- Symmetric left/right hemispheres

Step 3: Panel 2 - Temporal Standard Deviation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate std over time
   std_data = np.std(data, axis=3)
   
   # Show middle axial slice
   mid_slice = std_data.shape[2] // 2
   im = axes[0, 1].imshow(
       std_data[:, :, mid_slice],
       cmap='hot',
       interpolation='nearest'
   )
   axes[0, 1].set_title("Temporal Std Dev (mid-slice)")
   axes[0, 1].axis('off')
   plt.colorbar(im, ax=axes[0, 1], fraction=0.046)

**What this shows:** Where signal varies most over time.

**What to look for:**

- Gray matter should be brighter than white matter (more signal change)
- Edges/ventricles appear bright (pulsation, motion)
- Uniform brightness across cortex (no dropout)

Step 4: Panel 3 - Carpet Plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Sample random voxels for visualization
   n_voxels = 1000
   flat_data = data.reshape(-1, data.shape[3])  # (all_voxels, time)
   
   # Randomly sample voxels
   random_idx = np.random.choice(
       flat_data.shape[0],
       n_voxels,
       replace=False
   )
   sample_voxels = flat_data[random_idx, :]
   
   # Plot as heatmap
   im = axes[1, 0].imshow(
       sample_voxels,
       aspect='auto',
       cmap='gray',
       interpolation='nearest'
   )
   axes[1, 0].set_title("Carpet Plot (1000 random voxels)")
   axes[1, 0].set_xlabel("Time (volumes)")
   axes[1, 0].set_ylabel("Voxels")
   plt.colorbar(im, ax=axes[1, 0], fraction=0.046)

**What this shows:** Intensity of all voxels over time.

**What to look for:**

- Smooth gradual changes (good)
- Vertical stripes = sudden intensity change across all voxels (motion!)
- Horizontal bands = voxels with different baseline intensity

Step 5: Panel 4 - Global Signal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate mean intensity at each timepoint
   global_signal = np.mean(data, axis=(0, 1, 2))
   
   # Plot timeseries
   axes[1, 1].plot(global_signal, linewidth=0.8, color='steelblue')
   axes[1, 1].set_title("Global Signal Timeseries")
   axes[1, 1].set_xlabel("Volume")
   axes[1, 1].set_ylabel("Mean Intensity")
   axes[1, 1].grid(True, alpha=0.3)
   
   # Add mean line
   axes[1, 1].axhline(
       global_signal.mean(),
       color='red',
       linestyle='--',
       alpha=0.5,
       label=f'Mean: {global_signal.mean():.1f}'
   )
   axes[1, 1].legend()

**What this shows:** Average brain signal over time.

**What to look for:**

- Slow drift/trend (scanner instability)
- Sudden spikes (motion artifacts)
- Oscillations (physiological noise)

Step 6: Save Figure
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Adjust spacing
   plt.tight_layout()
   
   # Save to file
   output_file = self.output_dir / f"sub-{subject_id}_diagnostic.png"
   plt.savefig(
       output_file,
       dpi=150,
       bbox_inches='tight',
       facecolor='white'
   )
   
   # Close figure to free memory
   plt.close(fig)
   
   print(f"    Saved: {output_file.name}")

Testing Your Implementation
----------------------------

.. code-block:: python

   from src.run_analysis import PreprocessingPipeline
   from pathlib import Path
   
   pipeline = PreprocessingPipeline(
       data_dir="/data/shared/workshop/bids_dataset",
       output_dir="./outputs"
   )
   
   # Load and visualize
   img = pipeline.load_data(subject_id="01")
   pipeline.create_visualization(img, subject_id="01")
   
   # Verify output exists
   output_file = Path("outputs/sub-01_diagnostic.png")
   assert output_file.exists(), "Output file not created"
   
   # Check file size (should be >10KB)
   file_size_kb = output_file.stat().st_size / 1024
   assert file_size_kb > 10, f"Output too small: {file_size_kb:.1f} KB"
   
   print("✓ Visualization created successfully!")
   print(f"✓ File size: {file_size_kb:.1f} KB")
   
   # Open in default viewer
   import subprocess
   subprocess.run(['xdg-open', str(output_file)])  # Linux
   # subprocess.run(['open', str(output_file)])  # Mac
   # subprocess.run(['start', str(output_file)])  # Windows

Expected output:

.. code-block:: text

   ✓ Loaded data: (64, 64, 36, 180)
     → Creating diagnostic visualizations...
       Saved: sub-01_diagnostic.png
     ✓ Visualization saved
   ✓ Visualization created successfully!
   ✓ File size: 245.3 KB

Understanding the Plots
------------------------

Mean EPI
~~~~~~~~

.. image:: /_static/example_mean_epi.png
   :alt: Mean EPI example
   :width: 400px

Shows anatomical reference. Good for:

- Checking registration quality
- Identifying signal dropout
- Verifying skull stripping worked

Temporal Std Dev
~~~~~~~~~~~~~~~~

.. image:: /_static/example_std_dev.png
   :alt: Temporal Std Dev example
   :width: 400px

Hot colors = high variability. Expected:

- Gray matter: High (neural activity + noise)
- White matter: Low (less activity)
- Edges/vessels: High (pulsation)

Carpet Plot
~~~~~~~~~~~

.. image:: /_static/example_carpet.png
   :alt: Carpet plot example
   :width: 400px

Each row = one voxel's timeseries. Look for:

- **Vertical lines**: Motion spikes (bad)
- **Gradual changes**: Drift (may need detrending)
- **Horizontal bands**: Different tissue types

Global Signal
~~~~~~~~~~~~~

.. image:: /_static/example_global.png
   :alt: Global signal example
   :width: 400px

Average intensity over time. Problems:

- **Linear trend**: Scanner warming up
- **Sudden jumps**: Motion
- **High-frequency oscillations**: Physiology or scanner noise

Common Issues
-------------

Issue: "AttributeError: 'Axes' object has no attribute 'plot_epi'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Trying to use nilearn plotting on matplotlib axes incorrectly

**Solution:** Use ``plotting.plot_epi()`` correctly:

.. code-block:: python

   # Correct
   plotting.plot_epi(mean_img, axes=axes[0, 0])
   
   # Incorrect
   axes[0, 0].plot_epi(mean_img)

Issue: Figure looks squished or cut off
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Adjust figure size and layout:

.. code-block:: python

   fig, axes = plt.subplots(2, 2, figsize=(14, 12))  # Larger
   plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave room for title

Issue: Carpet plot memory error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Too many voxels to plot

**Solution:** Already implemented - we sample only 1000 random voxels

Issue: Plot colors look washed out
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Adjust colormap limits:

.. code-block:: python

   # For std dev map, clip to 95th percentile
   vmax = np.percentile(std_data, 95)
   im = axes[0, 1].imshow(
       std_data[:, :, mid_slice],
       cmap='hot',
       vmax=vmax
   )

Advanced Visualizations (Optional)
-----------------------------------

If you finish early, try adding:

**1. Multiple Slices**

.. code-block:: python

   # Show axial, sagittal, coronal
   plotting.plot_stat_map(
       mean_img,
       axes=axes[0, 0],
       display_mode='ortho',
       cut_coords=(0, 0, 0)
   )

**2. Motion Parameters (if available)**

.. code-block:: python

   # If you have motion parameters from realignment
   motion = np.loadtxt('motion_params.txt')
   axes[1, 1].plot(motion[:, :3], label=['x', 'y', 'z'])
   axes[1, 1].legend()
   axes[1, 1].set_ylabel('Translation (mm)')

**3. Power Spectrum**

.. code-block:: python

   from scipy import signal
   freqs, psd = signal.welch(global_signal, fs=1/TR)
   axes[1, 1].semilogy(freqs, psd)
   axes[1, 1].set_xlabel('Frequency (Hz)')
   axes[1, 1].set_ylabel('Power')

Merge Timing
------------

.. note::
   **Group 4 should be merged LAST** because:
   
   - Depends on all previous preprocessing steps
   - Visualizes outputs from Groups 1, 2, 3
   - No other groups depend on visualization

After all PRs merge, the final pipeline will be:

.. code-block:: python

   img = self.load_data(subject_id)
   img_stripped = self.skull_strip(img)          # Group 2
   img_smoothed = self.smooth_image(img_stripped)  # Group 1
   qa_report = self.quality_assurance(img_smoothed)  # Group 3
   self.create_visualization(img_smoothed, subject_id)  # Group 4

Git Workflow
------------

.. code-block:: bash

   git add src/run_analysis.py
   git commit -m "Add diagnostic visualization
   
   - Generate 4-panel diagnostic figure
   - Mean EPI for anatomical reference
   - Temporal std dev to show variability
   - Carpet plot for time series QA
   - Global signal timeseries
   - Saves high-res PNG for reports
   - Tested: generates 250KB figure"
   
   git push origin feature/group-4-visualization

Helpful Resources
-----------------

- `Nilearn plotting <https://nilearn.github.io/stable/plotting/index.html>`_
- `Matplotlib gallery <https://matplotlib.org/stable/gallery/index.html>`_
- `Carpet plots explained <https://www.sciencedirect.com/science/article/pii/S1053811916303871>`_
- `fMRI QA visualization <https://mriqc.readthedocs.io/en/stable/>`_