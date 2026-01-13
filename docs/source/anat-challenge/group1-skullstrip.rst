Group 1: Skull Stripping
=============================
.. note::
   **Branch Name:** ``feature/group-1-skullstrip``
   
   **Objective:** Remove skull, scalp, and non-brain tissue from structural MRI

Background
----------

Skull stripping (brain extraction) is the first critical step in structural MRI processing. 
It isolates brain tissue from non-brain structures (skull, scalp, eyes, neck).

**Why skull strip?**

- Improves registration accuracy
- Reduces computation time for subsequent processing
- Prevents non-brain tissue from contaminating analysis
- Essential for tissue segmentation

Requirements Checklist
----------------------

- ☐ Add method ``skull_strip(self, img)`` to ``StructuralPipeline`` class
- ☐ Use ``nilearn.masking.compute_brain_mask()`` to create brain mask
- ☐ Apply mask to extract brain-only image
- ☐ Save mask to ``outputs/sub-{idx}_brain_mask.nii.gz``
- ☐ Save brain to ``outputs/sub-{idx}_brain.nii.gz``
- ☐ Print mask statistics (% voxels retained)
- ☐ Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def skull_strip(self, img):
       """
       Remove skull and non-brain tissue
       
       Extracts brain tissue by computing a binary brain mask and applying
       it to the structural image.
       
       Parameters
       ----------
       img : Nifti1Image
           Input T1-weighted structural image (3D)
           
       Returns
       -------
       brain_img : Nifti1Image
           Brain-only structural image
           
       Notes
       -----
       Uses nilearn's compute_brain_mask which employs intensity thresholding
       and morphological operations to identify brain voxels.
       """
       from nilearn import masking
       
       print("  → Computing brain mask...")
       
       # TODO: Compute brain mask
       # mask = masking.compute_brain_mask(img)
       
       # TODO: Get mask data and calculate statistics
       # mask_data = mask.get_fdata()
       # n_brain_voxels = int(mask_data.sum())
       # n_total_voxels = mask_data.size
       # brain_fraction = n_brain_voxels / n_total_voxels
       # print(f"    Brain voxels: {n_brain_voxels:,} / {n_total_voxels:,} ({brain_fraction*100:.1f}%)")
       
       # TODO: Apply mask to extract brain
       # brain_data = img.get_fdata()
       # brain_data[mask_data == 0] = 0  # Set non-brain to zero
       # brain_img = nib.Nifti1Image(brain_data, img.affine, img.header)
       
       # TODO: Save outputs
       # mask_file = self.output_dir / "brain_mask.nii.gz"
       # brain_file = self.output_dir / "brain.nii.gz"
       # nib.save(mask, mask_file)
       # nib.save(brain_img, brain_file)
       # print(f"    Saved: {mask_file.name}, {brain_file.name}")
       
       print("  ✓ Skull stripping complete")
       return brain_img

Implementation Guide
--------------------

Step 1: Import Required Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from nilearn import masking
   import nibabel as nib

Step 2: Compute Brain Mask
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   mask = masking.compute_brain_mask(img)

**What this does:**

- Analyzes intensity histogram
- Applies threshold to separate brain from background
- Uses morphological operations (erosion/dilation) to clean mask
- Returns binary mask (1 = brain, 0 = non-brain)

**Parameters you can tune:**

.. code-block:: python

   mask = masking.compute_brain_mask(
       img,
       threshold=0.5,      # Intensity threshold (0-1)
       connected=True,     # Keep only largest connected component
       opening=2           # Morphological opening radius (voxels)
   )

Step 3: Calculate Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   mask_data = mask.get_fdata()
   n_brain_voxels = int(mask_data.sum())
   n_total_voxels = mask_data.size
   brain_fraction = n_brain_voxels / n_total_voxels
   
   print(f"    Brain voxels: {n_brain_voxels:,} / {n_total_voxels:,} ({brain_fraction*100:.1f}%)")

**Expected values:**

- Brain fraction for structural MRI: ~30-40% of total volume
- Lower than functional MRI because higher resolution

Step 4: Apply Mask
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get image data
   brain_data = img.get_fdata().copy()  # Copy to avoid modifying original
   
   # Apply mask (set non-brain voxels to zero)
   brain_data[mask_data == 0] = 0
   
   # Create new image with same header/affine
   brain_img = nib.Nifti1Image(brain_data, img.affine, img.header)

Step 5: Save Outputs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   mask_file = self.output_dir / "brain_mask.nii.gz"
   brain_file = self.output_dir / "brain.nii.gz"
   
   nib.save(mask, mask_file)
   nib.save(brain_img, brain_file)
   
   print(f"    Saved: {mask_file.name}, {brain_file.name}")

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
   
   # Load test data
   img = pipeline.load_data(subject_idx=0)
   print(f"Original shape: {img.shape}")
   
   # Test skull stripping
   brain_img = pipeline.skull_strip(img)
   print(f"Brain shape: {brain_img.shape}")
   
   # Verify outputs exist
   from pathlib import Path
   assert Path("outputs/brain_mask.nii.gz").exists()
   assert Path("outputs/brain.nii.gz").exists()
   
   # Verify shapes match
   assert brain_img.shape == img.shape
   
   # Load and check mask
   mask = nib.load("outputs/brain_mask.nii.gz")
   mask_data = mask.get_fdata()
   
   # Brain should be 30-50% of volume
   brain_frac = mask_data.sum() / mask_data.size
   assert 0.2 < brain_frac < 0.6, f"Brain fraction {brain_frac:.1%} seems wrong"
   
   print(f"✓ Brain fraction: {brain_frac:.1%}")
   print("✓ All tests passed!")

Expected output:

.. code-block:: text

   Loading subject 0 from IXI dataset...
   ✓ Loaded data: (256, 256, 150)
   Original shape: (256, 256, 150)
     → Computing brain mask...
       Brain voxels: 2,456,789 / 9,830,400 (25.0%)
       Saved: brain_mask.nii.gz, brain.nii.gz
     ✓ Skull stripping complete
   Brain shape: (256, 256, 150)
   ✓ Brain fraction: 25.0%
   ✓ All tests passed!

Visual Quality Check
--------------------

View the results to verify quality:

.. code-block:: python

   from nilearn import plotting
   import matplotlib.pyplot as plt
   
   # Load outputs
   img = nib.load("outputs/brain.nii.gz")
   mask = nib.load("outputs/brain_mask.nii.gz")
   
   # Create comparison figure
   fig, axes = plt.subplots(1, 2, figsize=(12, 4))
   
   # Original with mask overlay
   plotting.plot_roi(mask, bg_img=img, axes=axes[0], 
                     title="Brain Mask Overlay", alpha=0.4)
   
   # Brain extracted
   plotting.plot_anat(img, axes=axes[1], title="Brain Extracted")
   
   plt.tight_layout()
   plt.savefig("outputs/skull_strip_qa.png", dpi=150)
   print("Saved: outputs/skull_strip_qa.png")

Common Issues
-------------

Issue: Mask Includes Too Much Non-Brain Tissue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Mask includes eyes, skull, or neck

**Solution:** Adjust threshold parameter

.. code-block:: python

   # More conservative (stricter)
   mask = masking.compute_brain_mask(img, threshold=0.6)

Issue: Mask Excludes Brain Regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Parts of brain (e.g., inferior temporal lobes) are cut off

**Solution:** Lower threshold or adjust opening parameter

.. code-block:: python

   # More lenient
   mask = masking.compute_brain_mask(img, threshold=0.3, opening=1)

Issue: Multiple Disconnected Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Mask has multiple separate blobs

**Solution:** Use connected component filtering

.. code-block:: python

   mask = masking.compute_brain_mask(img, connected=True)

This keeps only the largest connected component (the brain).

Understanding the Algorithm
----------------------------

How ``compute_brain_mask`` Works:

1. **Histogram Analysis**: Analyzes intensity distribution
2. **Thresholding**: Separates brain from background based on intensity
3. **Morphological Opening**: Removes small objects and smooths boundaries
4. **Connected Components**: Optionally keeps only largest connected region
5. **Binary Mask**: Returns 0/1 mask

**Visualization of Process:**

.. code-block:: text

   Original Image → Threshold → Morphological → Connected → Final
                                  Opening      Components    Mask
   
   [Brain+Skull] → [Binary]  → [Cleaned]   → [Brain Only] → [Mask]

Merge Priority
--------------

.. important::
   **Group 1 should be merged FIRST** because:
   
   - All subsequent processing operates on brain-extracted images
   - Bias correction works better on brain-only data
   - Tissue segmentation requires skull-stripped input

Git Workflow
------------

.. code-block:: bash

   git status
   git add src/run_analysis.py
   git commit -m "Add skull stripping with brain mask
   
   - Implemented brain extraction using nilearn
   - Computes binary brain mask from T1 image
   - Reports brain volume statistics
   - Saves mask and brain for QA
   - Tested: ~35% brain fraction (expected for T1)"
   
   git push origin feature/group-1-skullstrip

Helpful Resources
-----------------

- `Nilearn masking module <https://nilearn.github.io/stable/modules/masking.html>`_
- `Brain extraction review <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3555498/>`_
- `FSL BET tool <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET>`_ (popular alternative method)
```
