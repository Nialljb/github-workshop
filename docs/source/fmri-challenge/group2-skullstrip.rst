Group 2: Skull Stripping
=========================

.. note::
   **Branch Name:** ``feature/group-2-skullstrip``
   
   **Objective:** Remove non-brain tissue (skull, eyes, neck) from functional images

Background
----------

Skull stripping focuses analysis on brain voxels only, improving signal quality 
and reducing computational load.

**Why skull strip?**

- Removes non-brain signal sources (eyes, vessels, skull)
- Reduces false positives in activation detection
- Speeds up processing (fewer voxels)
- Improves registration accuracy

Requirements Checklist
----------------------

.. checkbox:: Add method ``skull_strip(self, img)`` to ``PreprocessingPipeline`` class
.. checkbox:: Use ``nilearn.masking.compute_epi_mask()`` to create brain mask
.. checkbox:: Apply mask to remove non-brain voxels
.. checkbox:: Save mask to ``outputs/sub-{subject_id}_mask.nii.gz``
.. checkbox:: Print mask coverage statistics (% voxels retained)
.. checkbox:: Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def skull_strip(self, img):
       """
       Remove non-brain tissue using automated masking
       
       Creates a binary mask identifying brain voxels and applies
       it to the functional image to remove skull, eyes, and neck.
       
       Parameters
       ----------
       img : Niimg-like object
           Input functional image (4D)
           
       Returns
       -------
       masked_img : Nifti1Image
           Brain-only functional image
           
       Notes
       -----
       The mask is computed from the functional data itself using
       nilearn's compute_epi_mask, which uses intensity and morphological
       criteria to identify brain tissue.
       """
       from nilearn.masking import compute_epi_mask, apply_mask, unmask
       
       print("  → Computing brain mask...")
       
       # TODO: Compute EPI mask from functional data
       # mask = compute_epi_mask(img)
       
       # TODO: Apply mask to image
       # masked_data = apply_mask(img, mask)
       # masked_img = unmask(masked_data, mask)
       
       # TODO: Calculate and print statistics
       # mask_data = mask.get_fdata()
       # n_brain_voxels = mask_data.sum()
       # n_total_voxels = mask_data.size
       # coverage = (n_brain_voxels / n_total_voxels) * 100
       # print(f"    Brain mask: {n_brain_voxels:,} / {n_total_voxels:,} voxels ({coverage:.1f}%)")
       
       # TODO: Save mask
       # mask_file = self.output_dir / "brain_mask.nii.gz"
       # nib.save(mask, mask_file)
       # print(f"    Saved: {mask_file.name}")
       
       print(f"  ✓ Skull stripping complete")
       return masked_img

Implementation Guide
--------------------

Step 1: Import Required Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from nilearn.masking import compute_epi_mask, apply_mask, unmask

Step 2: Compute Brain Mask
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   mask = compute_epi_mask(img)

**What this does:**

- Analyzes intensity distribution across volumes
- Uses morphological operations (erosion, dilation)
- Creates binary mask (1 = brain, 0 = background)

Step 3: Apply Mask
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Extract brain voxels as 1D array
   masked_data = apply_mask(img, mask)
   
   # Reshape back to 4D image
   masked_img = unmask(masked_data, mask)

**Why two steps?**

- ``apply_mask``: Extracts only brain voxels (efficient for computation)
- ``unmask``: Puts voxels back in 3D space (needed for visualization)

Step 4: Calculate Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   mask_data = mask.get_fdata()
   n_brain_voxels = int(mask_data.sum())
   n_total_voxels = mask_data.size
   coverage = (n_brain_voxels / n_total_voxels) * 100
   print(f"    Brain mask: {n_brain_voxels:,} / {n_total_voxels:,} voxels ({coverage:.1f}%)")

Step 5: Save Mask
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   mask_file = self.output_dir / "brain_mask.nii.gz"
   nib.save(mask, mask_file)
   print(f"    Saved: {mask_file.name}")

Testing Your Implementation
----------------------------

.. code-block:: python

   from src.run_analysis import PreprocessingPipeline
   import nibabel as nib
   
   pipeline = PreprocessingPipeline(
       data_dir="/data/shared/workshop/bids_dataset",
       output_dir="./outputs"
   )
   
   # Load and skull-strip
   img = pipeline.load_data(subject_id="01")
   masked_img = pipeline.skull_strip(img)
   
   # Verify shapes match
   assert img.shape == masked_img.shape, "Shapes should match"
   
   # Verify background is zero
   mask = nib.load("outputs/brain_mask.nii.gz")
   mask_data = mask.get_fdata()
   
   # Brain should be less than 50% of total volume
   brain_fraction = mask_data.sum() / mask_data.size
   assert brain_fraction < 0.5, f"Brain should be <50% of volume, got {brain_fraction:.1%}"
   
   print(f"✓ Brain occupies {brain_fraction:.1%} of volume")
   print("✓ All tests passed!")

Expected output:

.. code-block:: text

   ✓ Loaded data: (64, 64, 36, 180)
     → Computing brain mask...
       Brain mask: 27,648 / 147,456 voxels (18.7%)
       Saved: brain_mask.nii.gz
     ✓ Skull stripping complete
   ✓ Brain occupies 18.7% of volume
   ✓ All tests passed!

Understanding the Mask
-----------------------

The brain mask is a 3D binary image where:

- **1** = brain voxel (keep)
- **0** = non-brain voxel (discard)

**Visualization tip:** Load the mask in FSLeyes or another viewer to inspect quality.

.. code-block:: bash

   # If FSLeyes is available
   fsleyes outputs/brain_mask.nii.gz

Common Issues
-------------

Issue: Mask includes too much non-brain tissue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Default threshold too lenient

**Solution:** Adjust the lower_cutoff parameter:

.. code-block:: python

   mask = compute_epi_mask(img, lower_cutoff=0.3)  # More aggressive

Issue: Mask excludes brain regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Threshold too aggressive or signal dropout

**Solution:** 

1. Check data quality (signal dropout in inferior regions?)
2. Adjust parameters:

.. code-block:: python

   mask = compute_epi_mask(
       img, 
       lower_cutoff=0.2,  # Less aggressive
       connected=True,    # Keep only largest connected component
       opening=2          # Morphological opening radius
   )

Issue: Mask computation very slow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Computing mask from all 180 volumes

**Solution:** Use subset of volumes:

.. code-block:: python

   # Use middle 20 volumes for mask computation
   from nilearn import image
   middle_vols = image.index_img(img, slice(80, 100))
   mask = compute_epi_mask(middle_vols)

Merge Priority
--------------

.. important::
   **Group 2 should be merged FIRST** because:
   
   - No dependencies on other groups
   - Other groups' features operate on skull-stripped data
   - Reduces merge conflicts

After your PR merges, other groups will update:

.. code-block:: python

   # Group 1's smoothing will operate on stripped data
   img_stripped = self.skull_strip(img)
   img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)

Git Workflow
------------

.. code-block:: bash

   git status
   git add src/run_analysis.py
   git commit -m "Add skull stripping with EPI masking
   
   - Implemented automated brain mask using nilearn
   - Computes mask from functional data (no T1 needed)
   - Reports brain coverage statistics
   - Saves mask for visual QA
   - Tested: ~19% voxels retained (expected for functional)"
   
   git push origin feature/group-2-skullstrip

Helpful Resources
-----------------

- `Nilearn masking module <https://nilearn.github.io/stable/modules/masking.html>`_
- `EPI masking explained <https://nilearn.github.io/stable/auto_examples/04_glm_first_level/plot_bids_features.html#masking>`_
- `Brain extraction methods comparison <https://www.frontiersin.org/articles/10.3389/fninf.2013.00042/full>`_