Group 3: Tissue Segmentation
=============================

.. note::
   **Branch Name:** ``feature/group-3-segmentation``
   
   **Objective:** Segment brain into gray matter (GM), white matter (WM), and cerebrospinal fluid (CSF)

Background
----------

Tissue segmentation classifies each brain voxel into one of three tissue types:

- **Gray Matter (GM)**: Neural cell bodies (cortex, subcortical nuclei)
- **White Matter (WM)**: Myelinated axons connecting brain regions
- **Cerebrospinal Fluid (CSF)**: Fluid in ventricles and around brain

**Why segment tissues?**

- Measure tissue volumes (atrophy in disease)
- Create tissue-specific masks for analysis
- Generate partial volume estimates
- Basis for cortical thickness estimation

**How it works:**

Uses intensity differences between tissues in T1-weighted images:

- WM: Brightest (high myelin content)
- GM: Intermediate intensity
- CSF: Darkest (water)

Requirements Checklist
----------------------

.. checkbox:: Add method ``tissue_segmentation(self, img)`` to ``StructuralPipeline`` class
.. checkbox:: Implement 3-class segmentation (GM, WM, CSF)
.. checkbox:: Use FSL FAST algorithm (via nilearn interface)
.. checkbox:: Save tissue probability maps to ``outputs/``
.. checkbox:: Calculate and report tissue volumes
.. checkbox:: Return segmentation result as dictionary
.. checkbox:: Add comprehensive docstring

Code Template
-------------

.. code-block:: python

   def tissue_segmentation(self, img):
       """
       Segment brain into gray matter, white matter, and CSF
       
       Uses intensity-based clustering to classify each voxel into
       one of three tissue types.
       
       Parameters
       ----------
       img : Nifti1Image
           Bias-corrected brain image (3D)
           
       Returns
       -------
       segmentation : dict
           Dictionary containing:
           - 'gm': Gray matter probability map (Nifti1Image)
           - 'wm': White matter probability map (Nifti1Image)
           - 'csf': CSF probability map (Nifti1Image)
           - 'volumes_ml': Tissue volumes in milliliters
           
       Notes
       -----
       Uses a simple k-means clustering approach on intensity values.
       For production use, consider FSL FAST or SPM segmentation.
       """
       from sklearn.cluster import KMeans
       import numpy as np
       
       print("  → Segmenting tissues (GM, WM, CSF)...")
       
       # TODO: Get image data and mask
       # data = img.get_fdata()
       # brain_mask = data > 0
       # brain_voxels = data[brain_mask].reshape(-1, 1)
       
       # TODO: Normalize intensities to 0-1
       # brain_voxels_norm = (brain_voxels - brain_voxels.min()) / (brain_voxels.max() - brain_voxels.min())
       
       # TODO: K-means clustering (3 clusters)
       # kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
       # labels = kmeans.fit_predict(brain_voxels_norm)
       
       # TODO: Sort clusters by intensity (CSF=0, GM=1, WM=2)
       # cluster_means = [brain_voxels[labels == i].mean() for i in range(3)]
       # sorted_clusters = np.argsort(cluster_means)  # Sort: darkest to brightest
       
       # TODO: Create probability maps
       # gm_prob = np.zeros(data.shape)
       # wm_prob = np.zeros(data.shape)
       # csf_prob = np.zeros(data.shape)
       
       # csf_prob[brain_mask] = (labels == sorted_clusters[0]).astype(float)
       # gm_prob[brain_mask] = (labels == sorted_clusters[1]).astype(float)
       # wm_prob[brain_mask] = (labels == sorted_clusters[2]).astype(float)
       
       # TODO: Create NIfTI images
       # gm_img = nib.Nifti1Image(gm_prob, img.affine, img.header)
       # wm_img = nib.Nifti1Image(wm_prob, img.affine, img.header)
       # csf_img = nib.Nifti1Image(csf_prob, img.affine, img.header)
       
       # TODO: Calculate volumes
       # voxel_volume_ml = np.prod(img.header.get_zooms()) / 1000  # mm³ to ml
       # gm_volume = gm_prob.sum() * voxel_volume_ml
       # wm_volume = wm_prob.sum() * voxel_volume_ml
       # csf_volume = csf_prob.sum() * voxel_volume_ml
       
       # print(f"    GM volume:  {gm_volume:.1f} ml")
       # print(f"    WM volume:  {wm_volume:.1f} ml")
       # print(f"    CSF volume: {csf_volume:.1f} ml")
       
       # TODO: Save outputs
       # nib.save(gm_img, self.output_dir / "gm_prob.nii.gz")
       # nib.save(wm_img, self.output_dir / "wm_prob.nii.gz")
       # nib.save(csf_img, self.output_dir / "csf_prob.nii.gz")
       # print(f"    Saved: gm_prob.nii.gz, wm_prob.nii.gz, csf_prob.nii.gz")
       
       segmentation = {
           'gm': gm_img,
           'wm': wm_img,
           'csf': csf_img,
           'volumes_ml': {
               'gm': gm_volume,
               'wm': wm_volume,
               'csf': csf_volume
           }
       }
       
       print("  ✓ Tissue segmentation complete")
       return segmentation

Implementation Guide
--------------------

Step 1: Extract Brain Voxels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   
   # Get image data
   data = img.get_fdata()
   
   # Create brain mask (non-zero voxels)
   brain_mask = data > 0
   
   # Extract brain voxels as column vector for clustering
   brain_voxels = data[brain_mask].reshape(-1, 1)
   
   print(f"    Brain voxels: {len(brain_voxels):,}")

Step 2: Normalize Intensities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Normalize to 0-1 range for better clustering
   brain_voxels_norm = (brain_voxels - brain_voxels.min()) / (brain_voxels.max() - brain_voxels.min())

**Why normalize?**

- K-means is sensitive to scale
- Normalization puts all voxels on equal footing
- Improves cluster separation

Step 3: K-Means Clustering
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sklearn.cluster import KMeans
   
   # Create k-means with 3 clusters
   kmeans = KMeans(
       n_clusters=3,
       random_state=42,  # For reproducibility
       n_init=10,        # Number of initializations
       max_iter=300      # Maximum iterations
   )
   
   # Fit and predict cluster labels
   labels = kmeans.fit_predict(brain_voxels_norm)
   
   # labels is array of 0, 1, 2 for each voxel

Step 4: Identify Tissue Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Calculate mean intensity for each cluster
   cluster_means = [brain_voxels[labels == i].mean() for i in range(3)]
   
   # Sort clusters by intensity (darkest to brightest)
   sorted_clusters = np.argsort(cluster_means)
   
   # Assign tissue types:
   # sorted_clusters[0] = darkest = CSF
   # sorted_clusters[1] = middle = GM
   # sorted_clusters[2] = brightest = WM
   
   print(f"    CSF cluster: {sorted_clusters[0]} (mean: {cluster_means[sorted_clusters[0]]:.1f})")
   print(f"    GM cluster:  {sorted_clusters[1]} (mean: {cluster_means[sorted_clusters[1]]:.1f})")
   print(f"    WM cluster:  {sorted_clusters[2]} (mean: {cluster_means[sorted_clusters[2]]:.1f})")

Step 5: Create Probability Maps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Initialize probability maps (same shape as original image)
   gm_prob = np.zeros(data.shape)
   wm_prob = np.zeros(data.shape)
   csf_prob = np.zeros(data.shape)
   
   # Fill in probabilities (binary: 0 or 1)
   csf_prob[brain_mask] = (labels == sorted_clusters[0]).astype(float)
   gm_prob[brain_mask] = (labels == sorted_clusters[1]).astype(float)
   wm_prob[brain_mask] = (labels == sorted_clusters[2]).astype(float)
   
   # Create NIfTI images
   gm_img = nib.Nifti1Image(gm_prob, img.affine, img.header)
   wm_img = nib.Nifti1Image(wm_prob, img.affine, img.header)
   csf_img = nib.Nifti1Image(csf_prob, img.affine, img.header)

**Note:** This creates "hard" segmentation (0 or 1). Production tools like FSL FAST 
create "soft" segmentation (probabilities 0-1) accounting for partial volumes.

Step 6: Calculate Volumes
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get voxel dimensions from header
   voxel_dims = img.header.get_zooms()  # (x, y, z) in mm
   
   # Calculate volume of one voxel
   voxel_volume_mm3 = np.prod(voxel_dims)
   voxel_volume_ml = voxel_volume_mm3 / 1000  # Convert mm³ to ml
   
   # Calculate tissue volumes
   gm_volume = gm_prob.sum() * voxel_volume_ml
   wm_volume = wm_prob.sum() * voxel_volume_ml
   csf_volume = csf_prob.sum() * voxel_volume_ml
   
   print(f"    GM volume:  {gm_volume:.1f} ml")
   print(f"    WM volume:  {wm_volume:.1f} ml")
   print(f"    CSF volume: {csf_volume:.1f} ml")
   print(f"    Total:      {gm_volume + wm_volume + csf_volume:.1f} ml")

**Expected volumes (healthy adult):**

- Gray matter: 600-800 ml
- White matter: 400-600 ml
- CSF: 150-250 ml
- Total brain: ~1200-1500 ml

Step 7: Save Outputs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Save probability maps
   nib.save(gm_img, self.output_dir / "gm_prob.nii.gz")
   nib.save(wm_img, self.output_dir / "wm_prob.nii.gz")
   nib.save(csf_img, self.output_dir / "csf_prob.nii.gz")
   
   print(f"    Saved: gm_prob.nii.gz, wm_prob.nii.gz, csf_prob.nii.gz")

Step 8: Return Results
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   segmentation = {
       'gm': gm_img,
       'wm': wm_img,
       'csf': csf_img,
       'volumes_ml': {
           'gm': gm_volume,
           'wm': wm_volume,
           'csf': csf_volume
       }
   }
   
   return segmentation

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
   
   # Load, skull strip, bias correct
   img = pipeline.load_data(subject_idx=0)
   brain_img = pipeline.skull_strip(img)
   corrected_img = pipeline.bias_field_correction(brain_img)
   
   # Test segmentation
   segmentation = pipeline.tissue_segmentation(corrected_img)
   
   # Verify outputs exist
   from pathlib import Path
   assert Path("outputs/gm_prob.nii.gz").exists()
   assert Path("outputs/wm_prob.nii.gz").exists()
   assert Path("outputs/csf_prob.nii.gz").exists()
   
   # Verify structure
   assert 'gm' in segmentation
   assert 'wm' in segmentation
   assert 'csf' in segmentation
   assert 'volumes_ml' in segmentation
   
   # Check volumes are reasonable
   volumes = segmentation['volumes_ml']
   total_volume = volumes['gm'] + volumes['wm'] + volumes['csf']
   
   assert 1000 < total_volume < 2500, f"Total volume {total_volume:.0f}ml seems wrong"
   assert 400 < volumes['gm'] < 1200, f"GM volume {volumes['gm']:.0f}ml seems wrong"
   assert 200 < volumes['wm'] < 600, f"WM volume {volumes['wm']:.0f}ml seems wrong"
   
   print(f"✓ GM:  {volumes['gm']:.1f} ml")
   print(f"✓ WM:  {volumes['wm']:.1f} ml")
   print(f"✓ CSF: {volumes['csf']:.1f} ml")
   print(f"✓ Total: {total_volume:.1f} ml")
   print("✓ All tests passed!")

Expected output:

.. code-block:: text

     → Segmenting tissues (GM, WM, CSF)...
       Brain voxels: 2,456,789
       CSF cluster: 0 (mean: 145.3)
       GM cluster:  1 (mean: 387.2)
       WM cluster:  2 (mean: 524.8)
       GM volume:  652.3 ml
       WM volume:  478.9 ml
       CSF volume: 183.4 ml
       Total:      1314.6 ml
       Saved: gm_prob.nii.gz, wm_prob.nii.gz, csf_prob.nii.gz
     ✓ Tissue segmentation complete
   ✓ GM:  652.3 ml
   ✓ WM:  478.9 ml
   ✓ CSF: 183.4 ml
   ✓ Total: 1314.6 ml
   ✓ All tests passed!

Visual Quality Check
--------------------

.. code-block:: python

   from nilearn import plotting
   import matplotlib.pyplot as plt
   
   # Load data
   img = nib.load("outputs/corrected.nii.gz")
   gm = nib.load("outputs/gm_prob.nii.gz")
   wm = nib.load("outputs/wm_prob.nii.gz")
   csf = nib.load("outputs/csf_prob.nii.gz")
   
   # Create comparison figure
   fig, axes = plt.subplots(2, 2, figsize=(12, 10))
   
   # Background image
   plotting.plot_anat(img, axes=axes[0, 0], title="Original")
   
   # Tissue overlays
   plotting.plot_roi(gm, bg_img=img, axes=axes[0, 1], 
                     title="Gray Matter", colorbar=True, cmap='Reds')
   plotting.plot_roi(wm, bg_img=img, axes=axes[1, 0], 
                     title="White Matter", colorbar=True, cmap='Blues')
   plotting.plot_roi(csf, bg_img=img, axes=axes[1, 1], 
                     title="CSF", colorbar=True, cmap='Greens')
   
   plt.tight_layout()
   plt.savefig("outputs/segmentation_qa.png", dpi=150)
   print("Saved: outputs/segmentation_qa.png")

**What to look for:**

- **Gray matter**: Should cover cortex and subcortical structures
- **White matter**: Should be in brain interior
- **CSF**: Should be in ventricles and around brain

Common Issues
-------------

Issue: Volumes Don't Sum to Brain Volume
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Some voxels not classified

**Cause:** K-means should classify all voxels, so this shouldn't happen with our implementation

**Check:**

.. code-block:: python

   # Verify all brain voxels are classified
   total_classified = gm_prob.sum() + wm_prob.sum() + csf_prob.sum()
   total_brain = brain_mask.sum()
   assert abs(total_classified - total_brain) < 1

Issue: Unrealistic Tissue Proportions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** E.g., 90% GM, 5% WM, 5% CSF

**Cause:** Bias field not corrected properly, or poor clustering

**Solution:** 

1. Verify bias correction ran successfully
2. Check that clusters are well-separated:

.. code-block:: python

   # Print cluster statistics
   for i in range(3):
       cluster_voxels = brain_voxels[labels == i]
       print(f"Cluster {i}: mean={cluster_voxels.mean():.1f}, std={cluster_voxels.std():.1f}, n={len(cluster_voxels)}")

Issue: Slow K-Means Clustering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Takes >5 minutes

**Solution:** Reduce n_init parameter

.. code-block:: python

   # Faster (but potentially less optimal)
   kmeans = KMeans(n_clusters=3, random_state=42, n_init=3, max_iter=100)

Understanding Tissue Segmentation
----------------------------------

**Simple K-Means Approach (This Workshop):**

Pros:
- Fast
- No additional dependencies
- Educational (shows core concept)

Cons:
- No partial volume modeling
- Sensitive to bias field
- Less accurate than specialized tools

**Production Tools:**

For real research, use:

- **FSL FAST**: Hidden Markov Random Field model
- **SPM Segment**: Unified segmentation with registration
- **FreeSurfer**: Surface-based cortical segmentation
- **ANTs Atropos**: N-tissue segmentation with priors

**Why K-Means Works:**

T1-weighted images have distinct intensity peaks for each tissue:

.. code-block:: text

   Intensity Histogram:
   
   Count
   |        CSF    GM      WM
   |         ↓     ↓       ↓
   |        ***   ***     ***
   |       *   * *   *   *   *
   |      *     *     * *     *
   |_____*_____|_____|_*_______|______ Intensity
        Low         Mid      High

K-means finds these three peaks automatically.

Git Workflow
------------

.. code-block:: python

   git add src/run_analysis.py requirements.txt
   git commit -m "Add tissue segmentation using k-means
   
   - Implemented 3-class segmentation (GM, WM, CSF)
   - Uses k-means clustering on intensity values
   - Calculates tissue volumes in milliliters
   - Saves probability maps for each tissue type
   - Tested: GM ~650ml, WM ~480ml, CSF ~185ml
   - Added scikit-learn to requirements"
   
   git push origin feature/group-3-segmentation

Helpful Resources
-----------------

- `FSL FAST <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST>`_
- `SPM Segmentation <https://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#page=33>`_
- `Brain Tissue Segmentation Review <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3417427/>`_
- `K-means clustering (sklearn) <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html>`_