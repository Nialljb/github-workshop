Group 4: Visualization
======================

.. note::
   **Branch Name:** ``feature/group-4-visualization``
   
   **Objective:** Create comprehensive diagnostic visualization of processing results

Background
----------

Visualization is essential for quality control and result communication. A good 
diagnostic figure helps you:

- Verify all processing steps worked correctly
- Identify remaining artifacts or errors
- Document results for lab meetings and publications
- Communicate findings to collaborators

**Key visualization principles:**

- Show original and processed data side-by-side
- Use appropriate color maps for different data types
- Include clear labels and titles
- Save high-resolution figures for presentations

Requirements Checklist
----------------------

- ☐ Add method ``create_visualization(self, img, segmentation, subject_idx)``
- ☐ Generate multi-panel figure showing all processing stages
- ☐ Include: original, brain-extracted, bias-corrected, segmentation overlay
- ☐ Add tissue volume summary text
- ☐ Save figure to ``outputs/sub-{idx}_diagnostic.png``
- ☐ Use matplotlib and nilearn plotting
- ☐ Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def create_visualization(self, img, segmentation, subject_idx):
       """
       Create comprehensive diagnostic visualization
       
       Generates multi-panel figure showing all processing stages and
       tissue segmentation results.
       
       Parameters
       ----------
       img : Nifti1Image
           Final processed (bias-corrected) image
       segmentation : dict
           Segmentation results from tissue_segmentation()
       subject_idx : int
           Subject index for labeling
           
       Returns
       -------
       None
           Saves figure to outputs directory
           
       Notes
       -----
       Creates a 2x3 figure:
       - Top row: Processing stages (brain extraction, bias correction)
       - Bottom row: Tissue segmentation overlays (GM, WM, CSF)
       """
       from nilearn import plotting
       import matplotlib.pyplot as plt
       from pathlib import Path
       
       print("  → Creating diagnostic visualization...")
       
       # TODO: Load intermediate results
       # brain_img = nib.load(self.output_dir / "brain.nii.gz")
       # mask_img = nib.load(self.output_dir / "brain_mask.nii.gz")
       
       # TODO: Create figure with 2x3 subplots
       # fig = plt.figure(figsize=(15, 10))
       # gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
       
       # TODO: Row 1, Col 1 - Brain mask overlay
       # ax1 = fig.add_subplot(gs[0, 0])
       # plotting.plot_roi(mask_img, bg_img=brain_img, axes=ax1,
       #                   title='Brain Extraction', alpha=0.4, cmap='autumn')
       
       # TODO: Row 1, Col 2 - Bias corrected
       # ax2 = fig.add_subplot(gs[0, 1])
       # plotting.plot_anat(img, axes=ax2, title='Bias Corrected')
       
       # TODO: Row 1, Col 3 - All tissues composite
       # ax3 = fig.add_subplot(gs[0, 2])
       # # Create RGB composite of tissues
       # gm_data = segmentation['gm'].get_fdata()
       # wm_data = segmentation['wm'].get_fdata()
       # csf_data = segmentation['csf'].get_fdata()
       # composite = np.stack([gm_data, wm_data, csf_data], axis=-1)
       # # ... plot composite
       
       # TODO: Row 2 - Individual tissue overlays
       # ax4 = fig.add_subplot(gs[1, 0])
       # plotting.plot_roi(segmentation['gm'], bg_img=img, axes=ax4,
       #                   title='Gray Matter', cmap='Reds', alpha=0.5)
       
       # ax5 = fig.add_subplot(gs[1, 1])
       # plotting.plot_roi(segmentation['wm'], bg_img=img, axes=ax5,
       #                   title='White Matter', cmap='Blues', alpha=0.5)
       
       # ax6 = fig.add_subplot(gs[1, 2])
       # plotting.plot_roi(segmentation['csf'], bg_img=img, axes=ax6,
       #                   title='CSF', cmap='Greens', alpha=0.5)
       
       # TODO: Add text summary of volumes
       # volumes = segmentation['volumes_ml']
       # summary_text = (
       #     f"Subject {subject_idx}\n"
       #     f"GM:  {volumes['gm']:.1f} ml\n"
       #     f"WM:  {volumes['wm']:.1f} ml\n"
       #     f"CSF: {volumes['csf']:.1f} ml\n"
       #     f"Total: {sum(volumes.values()):.1f} ml"
       # )
       # fig.text(0.98, 0.02, summary_text, fontsize=10,
       #          verticalalignment='bottom', horizontalalignment='right',
       #          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
       
       # TODO: Save figure
       # output_file = self.output_dir / f"sub-{subject_idx}_diagnostic.png"
       # plt.savefig(output_file, dpi=150, bbox_inches='tight')
       # plt.close(fig)
       # print(f"    Saved: {output_file.name}")
       
       print("  ✓ Visualization complete")

Implementation Guide
--------------------

Step 1: Load Intermediate Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import nibabel as nib
   from pathlib import Path
   
   # Load saved intermediate files
   brain_img = nib.load(self.output_dir / "brain.nii.gz")
   mask_img = nib.load(self.output_dir / "brain_mask.nii.gz")
   
   # Segmentation is passed as parameter
   gm_img = segmentation['gm']
   wm_img = segmentation['wm']
   csf_img = segmentation['csf']

Step 2: Create Figure Layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   
   # Create figure with 2 rows, 3 columns
   fig = plt.figure(figsize=(15, 10))
   gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
   
   # Add overall title
   fig.suptitle(f'Structural MRI Processing - Subject {subject_idx}',
                fontsize=16, fontweight='bold')

Step 3: Panel 1 - Brain Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from nilearn import plotting
   
   # Top-left: Brain mask overlay
   ax1 = fig.add_subplot(gs[0, 0])
   plotting.plot_roi(
       mask_img,
       bg_img=brain_img,
       axes=ax1,
       title='1. Brain Extraction',
       alpha=0.4,
       cmap='autumn'
   )

Step 4: Panel 2 - Bias Correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Top-middle: Bias corrected image
   ax2 = fig.add_subplot(gs[0, 1])
   plotting.plot_anat(
       img,
       axes=ax2,
       title='2. Bias Field Corrected',
       cmap='gray'
   )

Step 5: Panel 3 - Tissue Composite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   
   # Top-right: RGB composite of all tissues
   ax3 = fig.add_subplot(gs[0, 2])
   
   # Get tissue data
   gm_data = segmentation['gm'].get_fdata()
   wm_data = segmentation['wm'].get_fdata()
   csf_data = segmentation['csf'].get_fdata()
   
   # Create RGB composite (Red=GM, Green=WM, Blue=CSF)
   # Show middle sagittal slice
   mid_slice = img.shape[0] // 2
   
   rgb_slice = np.zeros((*gm_data.shape[1:], 3))
   rgb_slice[:, :, 0] = gm_data[mid_slice, :, :]    # Red channel = GM
   rgb_slice[:, :, 1] = wm_data[mid_slice, :, :]    # Green channel = WM
   rgb_slice[:, :, 2] = csf_data[mid_slice, :, :]   # Blue channel = CSF
   
   ax3.imshow(rgb_slice.T, origin='lower', interpolation='nearest')
   ax3.set_title('3. Tissue Composite\n(R=GM, G=WM, B=CSF)')
   ax3.axis('off')

Step 6: Panels 4-6 - Individual Tissues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Bottom-left: Gray matter
   ax4 = fig.add_subplot(gs[1, 0])
   plotting.plot_roi(
       segmentation['gm'],
       bg_img=img,
       axes=ax4,
       title='Gray Matter',
       cmap='Reds',
       alpha=0.6
   )
   
   # Bottom-middle: White matter
   ax5 = fig.add_subplot(gs[1, 1])
   plotting.plot_roi(
       segmentation['wm'],
       bg_img=img,
       axes=ax5,
       title='White Matter',
       cmap='Blues',
       alpha=0.6
   )
   
   # Bottom-right: CSF
   ax6 = fig.add_subplot(gs[1, 2])
   plotting.plot_roi(
       segmentation['csf'],
       bg_img=img,
       axes=ax6,
       title='CSF',
       cmap='Greens',
       alpha=0.6
   )

Step 7: Add Volume Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get volumes
   volumes = segmentation['volumes_ml']
   total_volume = sum(volumes.values())
   
   # Create summary text
   summary_text = (
       f"Subject {subject_idx}\n"
       f"─────────────────\n"
       f"GM:    {volumes['gm']:>6.1f} ml\n"
       f"WM:    {volumes['wm']:>6.1f} ml\n"
       f"CSF:   {volumes['csf']:>6.1f} ml\n"
       f"─────────────────\n"
       f"Total: {total_volume:>6.1f} ml"
   )
   
   # Add text box to figure
   fig.text(
       0.98, 0.02,
       summary_text,
       fontsize=10,
       family='monospace',
       verticalalignment='bottom',
       horizontalalignment='right',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
   )

Step 8: Save Figure
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Save high-resolution figure
   output_file = self.output_dir / f"sub-{subject_idx}_diagnostic.png"
   plt.savefig(
       output_file,
       dpi=150,
       bbox_inches='tight',
       facecolor='white'
   )
   
   # Close to free memory
   plt.close(fig)
   
   print(f"    Saved: {output_file.name}")

Testing Your Implementation
----------------------------

.. code-block:: python

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

Expected output:

.. code-block:: text

     → Creating diagnostic visualization...
       Saved: sub-0_diagnostic.png
     ✓ Visualization complete
   ✓ Diagnostic figure created: 487.3KB
   ✓ All tests passed!

Advanced Visualizations (Optional)
-----------------------------------

If you finish early, try adding:

**1. Multiple Slice Views**

.. code-block:: python

   # Show axial, sagittal, coronal views
   display = plotting.plot_anat(
       img,
       display_mode='ortho',
       cut_coords=(0, 0, 0),
       title='Orthogonal Views'
   )

**2. 3D Surface Rendering**

.. code-block:: python

   from nilearn import surface
   
   # Extract surface from segmentation
   # (requires more complex processing)

**3. Histogram Comparison**

.. code-block:: python

   # Show intensity histogram before/after bias correction
   fig, ax = plt.subplots(1, 2, figsize=(12, 4))
   
   # Before
   brain_data = brain_img.get_fdata()
   ax[0].hist(brain_data[brain_data > 0], bins=100, alpha=0.7)
   ax[0].set_title('Before Bias Correction')
   ax[0].set_xlabel('Intensity')
   
   # After
   corr_data = img.get_fdata()
   ax[1].hist(corr_data[corr_data > 0], bins=100, alpha=0.7)
   ax[1].set_title('After Bias Correction')
   ax[1].set_xlabel('Intensity')

**4. Volume Chart**

.. code-block:: python

   # Bar chart of tissue volumes
   fig, ax = plt.subplots(figsize=(8, 5))
   
   tissues = list(volumes.keys())
   values = list(volumes.values())
   colors = ['red', 'blue', 'green']
   
   ax.bar(tissues, values, color=colors, alpha=0.7)
   ax.set_ylabel('Volume (ml)')
   ax.set_title('Tissue Volumes')
   ax.grid(axis='y', alpha=0.3)

Common Issues
-------------

Issue: "ValueError: 'axes' must be a matplotlib Axes"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Passing wrong type to nilearn plotting

**Solution:**

.. code-block:: python

   # Correct
   ax = fig.add_subplot(gs[0, 0])
   plotting.plot_anat(img, axes=ax)
   
   # Incorrect
   plotting.plot_anat(img, axes=gs[0, 0])

Issue: Plots Look Squished or Distorted
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Adjust figure size and spacing

.. code-block:: python

   fig = plt.figure(figsize=(18, 12))  # Larger
   gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.4)  # More space

Issue: Text Overlaps with Plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Adjust text position

.. code-block:: python

   # Move text box
   fig.text(0.99, 0.01, summary_text, ...)  # Further right/down

Issue: Image Orientations Don't Match
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Different slices shown in each panel

**Solution:** Specify consistent cut coordinates

.. code-block:: python

   # Use same cut coordinates for all plots
   cut_coords = (0, 0, 10)  # (x, y, z)
   
   plotting.plot_anat(img, axes=ax, cut_coords=cut_coords)

Understanding Visualization Choices
------------------------------------

**Color Maps:**

- **Anatomical images**: Grayscale ('gray')
- **Masks/ROIs**: Single color with transparency ('Reds', 'Blues')
- **Functional/statistical**: Diverging colors ('RdBu_r', 'coolwarm')

**Alpha (Transparency):**

- 0.0 = fully transparent
- 0.5 = semi-transparent (good for overlays)
- 1.0 = fully opaque

**Display Modes:**

.. code-block:: python

   display_mode='ortho'   # 3 views: axial, sagittal, coronal
   display_mode='x'       # Sagittal only
   display_mode='y'       # Coronal only
   display_mode='z'       # Axial only
   display_mode='mosaic'  # Multiple slices

**Resolution (DPI):**

- **Screen viewing**: 72-100 DPI
- **Presentations**: 150 DPI (workshop default)
- **Publications**: 300+ DPI

Git Workflow
------------

.. code-block:: bash

   git add src/run_analysis.py
   git commit -m "Add comprehensive diagnostic visualization
   
   - Creates 2x3 panel figure showing all processing stages
   - Brain extraction, bias correction, and segmentation
   - Individual tissue overlays (GM, WM, CSF)
   - RGB composite of all tissues
   - Summary text box with volumes
   - Saves 150 DPI figure for presentations
   - Tested: generates ~500KB PNG"
   
   git push origin feature/group-4-visualization

Helpful Resources
-----------------

- `Nilearn plotting <https://nilearn.github.io/stable/plotting/index.html>`_
- `Matplotlib gallery <https://matplotlib.org/stable/gallery/index.html>`_
- `Scientific visualization best practices <https://www.nature.com/articles/nmeth.1618>`_
- `Color map advice <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`_

Presentation Tips
-----------------

For lab meetings and publications:

1. **Save multiple formats:**

   .. code-block:: python
   
      plt.savefig(f"sub-{subject_idx}_diagnostic.png", dpi=300)  # High-res
      plt.savefig(f"sub-{subject_idx}_diagnostic.pdf")  # Vector (scalable)

2. **Use consistent styling across subjects**

3. **Add scale bars if showing actual sizes**

4. **Include institution/study watermark if needed:**

   .. code-block:: python
   
      fig.text(0.02, 0.98, 'My Lab - Confidential',
               fontsize=8, alpha=0.5)

5. **Consider accessibility:**
   - Use colorblind-friendly palettes
   - Ensure sufficient contrast
   - Add text labels, not just colors