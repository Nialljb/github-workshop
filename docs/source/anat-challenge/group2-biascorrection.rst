Group 2: Bias Field Correction

=============================
.. note::
   **Branch Name:** ``feature/group-2-biascorrection``
   
   **Objective:** Correct intensity inhomogeneities caused by MRI scanner

Background
----------

Bias field (intensity inhomogeneity) is a smooth, spatially-varying distortion in 
MRI signal intensity. It's caused by:

- Non-uniform radio-frequency coil sensitivity
- Magnetic field inhomogeneities
- Subject anatomy (proximity to coil)

**Why correct bias field?**

- Improves tissue segmentation accuracy
- Enables intensity-based analysis
- Facilitates image registration
- Reduces scanner-specific artifacts

**What it looks like:**

- Bright regions on one side of brain
- Dark regions on opposite side
- Smooth, gradual intensity changes (not anatomical)

Requirements Checklist
----------------------

.. checkbox:: Add method ``bias_field_correction(self, img)`` to ``StructuralPipeline`` class
.. checkbox:: Implement N4 bias field correction algorithm
.. checkbox:: Save corrected image to ``outputs/sub-{idx}_corrected.nii.gz``
.. checkbox:: Save estimated bias field to ``outputs/sub-{idx}_bias_field.nii.gz``
.. checkbox:: Print before/after intensity statistics
.. checkbox:: Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def bias_field_correction(self, img):
       """
       Correct intensity inhomogeneity (bias field)
       
       Uses N4 bias field correction algorithm to remove smooth intensity
       variations caused by scanner hardware.
       
       Parameters
       ----------
       img : Nifti1Image
           Input brain-extracted T1 image (3D)
           
       Returns
       -------
       corrected_img : Nifti1Image
           Bias-corrected T1 image
           
       Notes
       -----
       N4ITK (N4 bias field correction) is the standard algorithm for
       removing intensity inhomogeneities from MRI. Implementation uses
       SimpleITK library.
       
       References
       ----------
       Tustison et al. (2010) N4ITK: Improved N3 Bias Correction.
       IEEE Trans Med Imaging.
       """
       import SimpleITK as sitk
       
       print("  → Running N4 bias field correction...")
       
       # TODO: Convert nibabel to SimpleITK format
       # data = img.get_fdata()
       # sitk_img = sitk.GetImageFromArray(np.transpose(data, (2, 1, 0)))
       # Convert numpy types to Python floats for SimpleITK
       # spacing = [float(x) for x in img.header.get_zooms()[:3]]
       # sitk_img.SetSpacing(spacing)
       
       # TODO: Run N4 bias field correction
       # corrector = sitk.N4BiasFieldCorrectionImageFilter()
       # corrector.SetMaximumNumberOfIterations([50, 50, 50, 50])
       # corrected_sitk = corrector.Execute(sitk_img)
       
       # TODO: Get bias field
       # bias_field_sitk = sitk.Divide(sitk_img, corrected_sitk)
       
       # TODO: Convert back to nibabel format
       # corrected_data = np.transpose(sitk.GetArrayFromImage(corrected_sitk), (2, 1, 0))
       # bias_field_data = np.transpose(sitk.GetArrayFromImage(bias_field_sitk), (2, 1, 0))

       # Ensure proper data types and handle invalid values
       # corrected_data = corrected_data.astype(np.float32)
       # bias_field_data = bias_field_data.astype(np.float32)
        
       # # Replace any invalid values
       # corrected_data = np.nan_to_num(corrected_data, nan=0.0, posinf=0.0, neginf=0.0)
       # bias_field_data = np.nan_to_num(bias_field_data, nan=1.0, posinf=1.0, neginf=1.0) 
       
       # corrected_img = nib.Nifti1Image(corrected_data, img.affine, img.header)
       # bias_field_img = nib.Nifti1Image(bias_field_data, img.affine, img.header)
       
       # TODO: Print statistics
       # orig_mean = data[data > 0].mean()
       # corr_mean = corrected_data[corrected_data > 0].mean()
       # print(f"    Mean intensity: {orig_mean:.1f} → {corr_mean:.1f}")
       
       # TODO: Save outputs
       # corrected_file = self.output_dir / "corrected.nii.gz"
       # bias_file = self.output_dir / "bias_field.nii.gz"
       # nib.save(corrected_img, corrected_file)
       # nib.save(bias_field_img, bias_file)
       # print(f"    Saved: {corrected_file.name}, {bias_file.name}")
       
       print("  ✓ Bias correction complete")
       return corrected_img

Implementation Guide
--------------------

Step 1: Install SimpleITK
~~~~~~~~~~~~~~~~~~~~~~~~~~

Add to ``requirements.txt``:

.. code-block:: text

   SimpleITK>=2.2.0

Install:

.. code-block:: bash

   pip install SimpleITK

Step 2: Convert NiBabel to SimpleITK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import SimpleITK as sitk
   import numpy as np
   
   # Get data from nibabel image
   data = img.get_fdata()
   
   # SimpleITK expects (z, y, x) order, nibabel is (x, y, z)
   sitk_img = sitk.GetImageFromArray(np.transpose(data, (2, 1, 0)))
   
   # Set voxel spacing
   sitk_img.SetSpacing(img.header.get_zooms())

**Why the transpose?**

- NiBabel stores data as (x, y, z)
- SimpleITK expects (z, y, x)
- Transpose converts between conventions

Step 3: Run N4 Correction
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create N4 bias field correction filter
   corrector = sitk.N4BiasFieldCorrectionImageFilter()
   
   # Set parameters
   corrector.SetMaximumNumberOfIterations([50, 50, 50, 50])  # Multi-resolution
   corrector.SetConvergenceThreshold(0.001)
   
   # Run correction
   corrected_sitk = corrector.Execute(sitk_img)

**What these parameters mean:**

- ``SetMaximumNumberOfIterations([50, 50, 50, 50])``: 4 resolution levels, 50 iterations each
- ``SetConvergenceThreshold(0.001)``: Stop when change < 0.1%

Step 4: Extract Bias Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Bias field = Original / Corrected
   bias_field_sitk = sitk.Divide(sitk_img, corrected_sitk)

**Understanding the bias field:**

- Values > 1: Region was artificially brightened
- Values < 1: Region was artificially darkened
- Values ≈ 1: No bias

Step 5: Convert Back to NiBabel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Convert corrected image
   corrected_data = sitk.GetArrayFromImage(corrected_sitk)
   corrected_data = np.transpose(corrected_data, (2, 1, 0))  # Back to (x,y,z)
   corrected_img = nib.Nifti1Image(corrected_data, img.affine, img.header)
   
   # Convert bias field
   bias_field_data = sitk.GetArrayFromImage(bias_field_sitk)
   bias_field_data = np.transpose(bias_field_data, (2, 1, 0))
   bias_field_img = nib.Nifti1Image(bias_field_data, img.affine, img.header)

Step 6: Calculate Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Compare before and after (only non-zero voxels)
   orig_data = img.get_fdata()
   orig_mean = orig_data[orig_data > 0].mean()
   orig_std = orig_data[orig_data > 0].std()
   
   corr_mean = corrected_data[corrected_data > 0].mean()
   corr_std = corrected_data[corrected_data > 0].std()
   
   print(f"    Original  - Mean: {orig_mean:.1f}, Std: {orig_std:.1f}")
   print(f"    Corrected - Mean: {corr_mean:.1f}, Std: {corr_std:.1f}")
   print(f"    Coefficient of variation: {orig_std/orig_mean:.3f} → {corr_std/corr_mean:.3f}")

Step 7: Save Outputs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   corrected_file = self.output_dir / "corrected.nii.gz"
   bias_file = self.output_dir / "bias_field.nii.gz"
   
   nib.save(corrected_img, corrected_file)
   nib.save(bias_field_img, bias_file)
   
   print(f"    Saved: {corrected_file.name}, {bias_file.name}")

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
   
   # Load and skull strip
   img = pipeline.load_data(subject_idx=0)
   brain_img = pipeline.skull_strip(img)
   
   # Test bias correction
   corrected_img = pipeline.bias_field_correction(brain_img)
   
   # Verify outputs
   from pathlib import Path
   assert Path("outputs/corrected.nii.gz").exists()
   assert Path("outputs/bias_field.nii.gz").exists()
   
   # Verify shapes match
   assert corrected_img.shape == brain_img.shape
   
   # Load bias field and check range
   bias_field = nib.load("outputs/bias_field.nii.gz")
   bias_data = bias_field.get_fdata()
   
   # Bias field should be close to 1.0 (multiplicative factor)
   brain_data = brain_img.get_fdata()
   bias_values = bias_data[brain_data > 0]
   
   print(f"✓ Bias field range: {bias_values.min():.2f} - {bias_values.max():.2f}")
   print(f"✓ Bias field mean: {bias_values.mean():.2f}")
   print("✓ All tests passed!")

Expected output:

.. code-block:: text

     → Running N4 bias field correction...
       Original  - Mean: 425.3, Std: 187.6
       Corrected - Mean: 428.1, Std: 165.2
       Coefficient of variation: 0.441 → 0.386
       Saved: corrected.nii.gz, bias_field.nii.gz
     ✓ Bias correction complete
   ✓ Bias field range: 0.78 - 1.34
   ✓ Bias field mean: 1.01
   ✓ All tests passed!

Visual Quality Check
--------------------

.. code-block:: python

   from nilearn import plotting
   import matplotlib.pyplot as plt
   
   # Load data
   original = nib.load("outputs/brain.nii.gz")
   corrected = nib.load("outputs/corrected.nii.gz")
   bias_field = nib.load("outputs/bias_field.nii.gz")
   
   # Create comparison figure
   fig, axes = plt.subplots(1, 3, figsize=(15, 4))
   
   plotting.plot_anat(original, axes=axes[0], title="Original")
   plotting.plot_anat(corrected, axes=axes[1], title="Bias Corrected")
   plotting.plot_anat(bias_field, axes=axes[2], title="Bias Field", 
                      cmap='coolwarm', vmin=0.8, vmax=1.2)
   
   plt.tight_layout()
   plt.savefig("outputs/bias_correction_qa.png", dpi=150)
   print("Saved: outputs/bias_correction_qa.png")

**What to look for:**

- **Original**: Uneven brightness (one side brighter)
- **Corrected**: More uniform intensity across brain
- **Bias field**: Smooth gradient (bright = was corrected up, dark = corrected down)

Common Issues
-------------

Issue: "ImportError: No module named SimpleITK"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:**

.. code-block:: bash

   pip install SimpleITK

Issue: Correction Makes Image Look Worse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** N4 over-corrects or introduces artifacts

**Solution:** Adjust iteration parameters

.. code-block:: python

   # Less aggressive
   corrector.SetMaximumNumberOfIterations([25, 25, 25, 25])
   
   # Or fewer resolution levels
   corrector.SetMaximumNumberOfIterations([50, 50])

Issue: Very Slow Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** N4 takes >5 minutes per image

**Solution:** Reduce iterations or resolution levels

.. code-block:: python

   # Faster (but less accurate)
   corrector.SetMaximumNumberOfIterations([20, 20, 20])

For production: Run on HPC with more resources

Issue: Memory Error
~~~~~~~~~~~~~~~~~~~

**Problem:** Out of memory during processing

**Solution:** Process on HPC or reduce image resolution temporarily

.. code-block:: python

   from nilearn import image
   
   # Downsample for testing
   img_small = image.resample_img(img, target_affine=np.eye(3)*2)  # 2mm voxels
   
   # Run bias correction on smaller image
   corrected_small = bias_field_correction(img_small)

Understanding N4 Algorithm
---------------------------

**N4ITK (N4 bias field correction) is the gold standard for bias correction.**

How it works:

1. **Estimate bias field**: Fits smooth polynomial to intensity variations
2. **Multi-resolution**: Starts coarse, refines progressively
3. **Iterative refinement**: Alternates between estimating bias and correcting
4. **B-spline fitting**: Uses smooth splines to model the bias field

**Mathematical model:**

.. code-block:: text

   Observed intensity = True intensity × Bias field + Noise
   
   Goal: Estimate Bias field to recover True intensity

**Why B-splines?**

- Smooth, continuous curves
- Local control (changing one region doesn't affect distant regions)
- Efficient to compute

Git Workflow
------------

.. code-block:: bash

   git add src/run_analysis.py requirements.txt
   git commit -m "Add N4 bias field correction
   
   - Implemented N4ITK algorithm using SimpleITK
   - Saves corrected image and estimated bias field
   - Reports intensity statistics before/after
   - Reduces coefficient of variation by ~12%
   - Added SimpleITK to requirements"
   
   git push origin feature/group-2-biascorrection

Helpful Resources
-----------------

- `N4ITK Original Paper <https://ieeexplore.ieee.org/document/5445030>`_
- `SimpleITK Documentation <https://simpleitk.readthedocs.io/>`_
- `SimpleITK N4 Example <https://simpleitk.org/doxygen/latest/html/classitk_1_1simple_1_1N4BiasFieldCorrectionImageFilter.html>`_
- `ANTs N4 Tutorial <http://stnava.github.io/ANTs/>`_
