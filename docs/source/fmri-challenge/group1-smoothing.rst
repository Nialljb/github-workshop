Group 1: Spatial Smoothing
==========================

.. note::
   **Branch Name:** ``feature/group-1-smoothing``
   
   **Objective:** Implement Gaussian smoothing to reduce high-frequency noise in fMRI data

Background
----------

Spatial smoothing increases signal-to-noise ratio by averaging each voxel with its 
neighbors using a Gaussian kernel. It's one of the most common preprocessing steps 
in fMRI analysis.

**Why smooth fMRI data?**

- Increases signal-to-noise ratio (SNR)
- Reduces effects of anatomical variability across subjects
- Satisfies statistical assumptions (Gaussian random field theory)
- Improves validity of group-level analyses

Requirements Checklist
----------------------

.. checkbox:: Add method ``smooth_image(self, img, fwhm=6.0)`` to ``PreprocessingPipeline`` class
.. checkbox:: Use ``nilearn.image.smooth_img()`` function
.. checkbox:: FWHM parameter should be configurable (default: 6mm)
.. checkbox:: Save smoothed image to ``outputs/sub-{subject_id}_smoothed.nii.gz``
.. checkbox:: Print smoothing parameters to console
.. checkbox:: Add comprehensive docstring with parameters and return value

Code Template
-------------

Add this method to the ``PreprocessingPipeline`` class in ``src/run_analysis.py``:

.. code-block:: python

   def smooth_image(self, img, fwhm=6.0):
       """
       Apply Gaussian smoothing to functional image
       
       Spatial smoothing reduces noise by averaging each voxel
       with its neighbors using a Gaussian kernel.
       
       Parameters
       ----------
       img : Niimg-like object
           Input functional image (4D: x, y, z, time)
       fwhm : float, optional
           Full-width half-maximum of Gaussian kernel in mm
           Default: 6.0 (common for fMRI)
           
       Returns
       -------
       smoothed_img : Nifti1Image
           Smoothed functional image (same shape as input)
           
       Examples
       --------
       >>> pipeline = PreprocessingPipeline(...)
       >>> img = pipeline.load_data('01')
       >>> smoothed = pipeline.smooth_image(img, fwhm=6.0)
       """
       from nilearn.image import smooth_img
       
       print(f"  → Applying spatial smoothing (FWHM={fwhm}mm)...")
       
       # TODO: Implement smoothing
       # smoothed_img = smooth_img(img, fwhm=fwhm)
       
       # TODO: Save output
       # output_file = self.output_dir / f"smoothed_fwhm-{fwhm}.nii.gz"
       # nib.save(smoothed_img, output_file)
       # print(f"    Saved: {output_file.name}")
       
       print(f"  ✓ Smoothing complete")
       return smoothed_img

Implementation Guide
--------------------

Step 1: Import Required Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``smooth_img`` function is already imported at the top of the file. If not, add:

.. code-block:: python

   from nilearn.image import smooth_img

Step 2: Implement Smoothing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace the first TODO with:

.. code-block:: python

   smoothed_img = smooth_img(img, fwhm=fwhm)

**What this does:**

- Applies 3D Gaussian smoothing to each volume in the 4D image
- FWHM (Full Width at Half Maximum) controls kernel size
- Larger FWHM = more smoothing = more blurring

Step 3: Save Output
~~~~~~~~~~~~~~~~~~~

Replace the second TODO with:

.. code-block:: python

   output_file = self.output_dir / f"smoothed_fwhm-{fwhm}.nii.gz"
   nib.save(smoothed_img, output_file)
   print(f"    Saved: {output_file.name}")

**Why save outputs?**

- Allows visual inspection of results
- Enables reuse without reprocessing
- Facilitates debugging

Step 4: Test Your Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a test script ``test_smoothing.py``:

.. code-block:: python

   from src.run_analysis import PreprocessingPipeline
   
   pipeline = PreprocessingPipeline(
       data_dir="/data/shared/workshop/bids_dataset",
       output_dir="./outputs"
   )
   
   # Load test subject
   img = pipeline.load_data(subject_id="01")
   print(f"Original shape: {img.shape}")
   
   # Test smoothing
   smoothed = pipeline.smooth_image(img, fwhm=6.0)
   print(f"Smoothed shape: {smoothed.shape}")
   
   # Verify smoothing reduces high-frequency noise
   data_before = img.get_fdata()
   data_after = smoothed.get_fdata()
   
   print(f"Std before: {data_before.std():.2f}")
   print(f"Std after: {data_after.std():.2f}")
   assert data_after.std() < data_before.std(), "Smoothing should reduce variance"
   
   print("✓ All tests passed!")

Run the test:

.. code-block:: bash

   python test_smoothing.py

Expected output:

.. code-block:: text

   ✓ Loaded data: (64, 64, 36, 180)
     → Applying spatial smoothing (FWHM=6.0mm)...
       Saved: smoothed_fwhm-6.0.nii.gz
     ✓ Smoothing complete
   Original shape: (64, 64, 36, 180)
   Smoothed shape: (64, 64, 36, 180)
   Std before: 1234.56
   Std after: 1198.23
   ✓ All tests passed!

Common Issues
-------------

Issue: "ValueError: FWHM must be positive"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** FWHM parameter is negative or zero

**Solution:** Add validation at the start of your function:

.. code-block:: python

   if fwhm <= 0:
       raise ValueError(f"FWHM must be positive, got {fwhm}")

Issue: Output file not created
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Output directory doesn't exist

**Solution:** The ``__init__`` method already creates the output directory, but verify:

.. code-block:: python

   self.output_dir.mkdir(parents=True, exist_ok=True)

Issue: Memory error on large datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Loading entire 4D image into memory

**Solution:** For this workshop, the sample data is small enough. In production, 
consider using ``nilearn``'s lazy loading or processing chunks.

Understanding FWHM
------------------

.. image:: /_static/gaussian_kernel.png
   :alt: Gaussian smoothing kernel
   :align: center

FWHM (Full Width at Half Maximum) is the width of the Gaussian kernel at half its 
maximum height.

**Common FWHM values:**

- **2-4mm**: Light smoothing, preserves fine detail
- **6-8mm**: Standard smoothing for group analysis (most common)
- **10-12mm**: Heavy smoothing, better SNR but loses spatial detail

**Rule of thumb:** FWHM should be approximately 2-3 times your voxel size.

Git Workflow
------------

Once your implementation is complete and tested:

.. code-block:: bash

   # Check what changed
   git status
   git diff src/run_analysis.py
   
   # Stage changes
   git add src/run_analysis.py
   
   # Commit with descriptive message
   git commit -m "Add smoothing function with configurable FWHM
   
   - Implemented Gaussian smoothing using nilearn.image.smooth_img
   - FWHM parameter defaults to 6mm but accepts any positive value
   - Saves smoothed output to outputs directory
   - Tested with subject 01: verified reduced variance"
   
   # Push to your fork
   git push origin feature/group-1-smoothing

See :doc:`../workflows/pull-requests` for creating a Pull Request.

Helpful Resources
-----------------

- `Nilearn smoothing documentation <https://nilearn.github.io/stable/modules/generated/nilearn.image.smooth_img.html>`_
- `Why smooth fMRI data? <https://nilearn.github.io/stable/auto_examples/04_glm_first_level/plot_fmri_smoothing.html>`_
- `Understanding FWHM <https://andysbrainbook.readthedocs.io/en/latest/fMRI_Short_Course/fMRI_04_Preprocessing.html#smoothing>`_

Next Steps
----------

After your PR is merged, the pipeline will call your function:

.. code-block:: python

   # In run_full_pipeline()
   img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)

Your smoothed data will be used by:

- **Group 3** (QA): Calculate tSNR on smoothed data
- **Group 4** (Visualization): Create plots of smoothed data