Best Practices
==============

This page summarizes best practices for collaborative neuroimaging development.

Version Control Best Practices
-------------------------------

Commit Guidelines
~~~~~~~~~~~~~~~~~

**Commit Often:**

.. code-block:: bash

   # ✅ Good: Small, focused commits
   git commit -m "Add smoothing function"
   git commit -m "Add tests for smoothing"
   git commit -m "Add docstring to smoothing"
   
   # ❌ Bad: One giant commit at the end
   git commit -m "Added everything"

**Write Descriptive Messages:**

.. code-block:: text

   ✅ Good:
   Add skull stripping with EPI masking
   
   Implements automated brain extraction using nilearn's compute_epi_mask.
   - Computes mask from functional data (no T1 needed)
   - Reports brain coverage statistics
   - Saves mask for visual QA
   
   ❌ Bad:
   fixed stuff
   update
   changes

**Commit Complete Units:**

.. code-block:: text

   ✅ Commit together:
   - New function implementation
   - Tests for that function
   - Documentation for that function
   
   ❌ Don't commit:
   - Half-written functions
   - Commented-out debug code
   - Temporary test files

Branching Strategy
~~~~~~~~~~~~~~~~~~

**One Branch Per Feature:**

.. code-block:: bash

   ✅ Good:
   feature/add-smoothing
   feature/add-qa-metrics
   bugfix/skull-strip-timeout
   
   ❌ Bad:
   my-branch
   updates
   dev

**Keep Branches Short-Lived:**

- Create branch → Work → PR → Merge → Delete
- Aim for <3 days from creation to merge
- Long-lived branches accumulate conflicts

**Update Frequently:**

.. code-block:: bash

   # Daily or before starting new work
   git fetch upstream
   git rebase upstream/main

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**PR Size:**

.. code-block:: text

   ✅ Ideal PR:
   - 1 feature or fix
   - <300 lines changed
   - Can be reviewed in <30 minutes
   
   ❌ Avoid:
   - Multiple unrelated features
   - >1000 lines changed
   - Requires hours to review

**PR Description Template:**

.. code-block:: markdown

   ## Summary
   Brief description of what this PR does.
   
   ## Changes
   - Added X function
   - Modified Y to handle Z case
   - Fixed bug in W
   
   ## Testing
   - [ ] Tested with subject 01, 02, 03
   - [ ] All existing tests pass
   - [ ] Added new tests for new functionality
   
   ## Notes
   Any additional context or considerations.

**Before Submitting PR:**

- ☐ Code works and is tested
- ☐ All tests pass
- ☐ Code follows style guide
- ☐ Docstrings are complete
- ☐ No debug print statements
- ☐ No commented-out code
- ☐ Branch is up-to-date with main

Code Review Guidelines
~~~~~~~~~~~~~~~~~~~~~~

**As Author:**

- Respond to all comments
- Be open to feedback
- Don't take criticism personally
- Ask for clarification if needed
- Make requested changes promptly

**As Reviewer:**

- Be constructive and respectful
- Explain *why* for suggestions
- Approve good code quickly
- Focus on important issues
- Use "Request Changes" sparingly

**Review Checklist:**

- ☐ Code is clear and readable
- ☐ Functions have docstrings
- ☐ No hardcoded paths
- ☐ Error handling present
- ☐ Tests cover main functionality
- ☐ No obvious bugs

Coding Best Practices
---------------------

Python Style
~~~~~~~~~~~~

**Follow PEP 8:**

.. code-block:: bash

   # Check style with flake8
   pip install flake8
   flake8 src/

**Use Type Hints:**

.. code-block:: python

   # ✅ Good:
   def smooth_image(self, img: nib.Nifti1Image, fwhm: float = 6.0) -> nib.Nifti1Image:
       """Apply Gaussian smoothing"""
       ...
   
   # ❌ Acceptable but less clear:
   def smooth_image(self, img, fwhm=6.0):
       """Apply Gaussian smoothing"""
       ...

**Meaningful Names:**

.. code-block:: python

   # ✅ Good:
   mean_tsnr = np.mean(tsnr[tsnr > 0])
   n_outlier_volumes = len(outliers)
   
   # ❌ Bad:
   x = np.mean(t[t > 0])
   n = len(o)

Function Design
~~~~~~~~~~~~~~~

**Single Responsibility:**

.. code-block:: python

   # ✅ Good: Each function does one thing
   def skull_strip(self, img):
       """Remove non-brain tissue"""
       mask = self._compute_mask(img)
       return self._apply_mask(img, mask)
   
   # ❌ Bad: Function does too much
   def process(self, img):
       """Strip skull, smooth, run QA, and visualize"""
       ...  # Too many responsibilities!

**Document Everything:**

.. code-block:: python

   def smooth_image(self, img, fwhm=6.0):
       """
       Apply Gaussian smoothing to functional image
       
       Parameters
       ----------
       img : Niimg-like object
           Input functional image (4D: x, y, z, time)
       fwhm : float, optional
           Full-width half-maximum of Gaussian kernel in mm
           Default: 6.0
           
       Returns
       -------
       smoothed_img : Nifti1Image
           Smoothed functional image
           
       Raises
       ------
       ValueError
           If fwhm is not positive
           
       Examples
       --------
       >>> pipeline = PreprocessingPipeline(...)
       >>> img = pipeline.load_data('01')
       >>> smoothed = pipeline.smooth_image(img, fwhm=6.0)
       """

**Handle Errors Gracefully:**

.. code-block:: python

   # ✅ Good:
   def load_data(self, subject_id):
       file_path = self.data_dir / f"sub-{subject_id}" / "func" / "..."
       
       if not file_path.exists():
           raise FileNotFoundError(
               f"Cannot find functional data for subject {subject_id} at {file_path}"
           )
       
       try:
           img = nib.load(file_path)
       except Exception as e:
           raise IOError(f"Failed to load {file_path}: {e}")
       
       return img
   
   # ❌ Bad:
   def load_data(self, subject_id):
       return nib.load(self.data_dir / f"sub-{subject_id}" / "func" / "...")

**Use Pathlib for File Paths:**

.. code-block:: python

   # ✅ Good:
   from pathlib import Path
   
   output_file = self.output_dir / f"sub-{subject_id}_smoothed.nii.gz"
   if output_file.exists():
       print(f"File exists: {output_file}")
   
   # ❌ Bad:
   import os
   
   output_file = os.path.join(self.output_dir, f"sub-{subject_id}_smoothed.nii.gz")
   if os.path.exists(output_file):
       print(f"File exists: {output_file}")

Neuroimaging-Specific Practices
--------------------------------

Data Handling
~~~~~~~~~~~~~

**Always Check Image Dimensions:**

.. code-block:: python

   def smooth_image(self, img, fwhm=6.0):
       # Check input is 4D
       if len(img.shape) != 4:
           raise ValueError(f"Expected 4D image, got shape {img.shape}")
       
       smoothed = smooth_img(img, fwhm=fwhm)
       
       # Verify output shape matches input
       assert smoothed.shape == img.shape, "Smoothing changed shape!"
       
       return smoothed

**Preserve Image Headers:**

.. code-block:: python

   # ✅ Good: Preserve affine and header
   smoothed = smooth_img(img, fwhm=fwhm)  # nilearn preserves these
   nib.save(smoothed, output_file)
   
   # ❌ Bad: Create new image without proper header
   smoothed_data = gaussian_filter(img.get_fdata(), sigma=fwhm)
   new_img = nib.Nifti1Image(smoothed_data, affine=np.eye(4))  # Wrong!

**Use BIDS Conventions:**

.. code-block:: python

   # ✅ Good: BIDS-compliant naming
   func_file = (
       data_dir / 
       f"sub-{subject_id}" / 
       "func" / 
       f"sub-{subject_id}_task-rest_run-{run_id}_bold.nii.gz"
   )
   
   # ❌ Bad: Non-standard naming
   func_file = data_dir / f"subject{subject_id}_fMRI.nii"

Memory Management
~~~~~~~~~~~~~~~~~

**Don't Load Everything at Once:**

.. code-block:: python

   # ✅ Good: Process one subject at a time
   for subject_id in subjects:
       img = load_data(subject_id)
       result = process(img)
       save_result(result, subject_id)
       del img, result  # Free memory
   
   # ❌ Bad: Load all subjects into memory
   all_data = [load_data(sid) for sid in subjects]
   results = [process(img) for img in all_data]

**Use Lazy Loading When Possible:**

.. code-block:: python

   # nilearn loads images lazily by default
   from nilearn import image
   
   # This doesn't load data into memory yet
   img = image.load_img('func.nii.gz')
   
   # Data is loaded only when accessed
   data = img.get_fdata()

Quality Control
~~~~~~~~~~~~~~~

**Always Visualize Results:**

.. code-block:: python

   def skull_strip(self, img):
       mask = compute_epi_mask(img)
       
       # Save mask for visual inspection
       mask_file = self.output_dir / "brain_mask.nii.gz"
       nib.save(mask, mask_file)
       
       # Log statistics
       coverage = mask.get_fdata().sum() / mask.get_fdata().size
       print(f"Brain coverage: {coverage*100:.1f}%")
       
       return apply_mask(img, mask)

**Add Sanity Checks:**

.. code-block:: python

   def quality_assurance(self, img):
       data = img.get_fdata()
       mean_tsnr = ...
       
       # Sanity checks
       if mean_tsnr < 5:
           warnings.warn(f"Very low tSNR ({mean_tsnr:.1f}). Check data quality!")
       if mean_tsnr > 200:
           warnings.warn(f"Suspiciously high tSNR ({mean_tsnr:.1f}). Check calculation!")
       
       return {'mean_tsnr': mean_tsnr}

Project Organization
--------------------

Directory Structure
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   project/
   ├── README.md              # Project overview
   ├── requirements.txt       # Python dependencies
   ├── .gitignore            # Files to ignore
   ├── src/                  # Source code
   │   ├── __init__.py
   │   └── pipeline.py
   ├── tests/                # Unit tests
   │   ├── __init__.py
   │   └── test_pipeline.py
   ├── scripts/              # Utility scripts
   │   └── batch_process.py
   ├── docs/                 # Documentation
   │   └── usage.md
   └── data/                 # Data (or symlink to data)
       └── README.md

**.gitignore Template:**

.. code-block:: text

   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   venv/
   env/
   
   # Data files
   *.nii
   *.nii.gz
   *.dcm
   
   # Outputs
   outputs/
   results/
   figures/
   
   # IDE
   .vscode/
   .idea/
   *.swp
   
   # OS
   .DS_Store
   Thumbs.db

Documentation
~~~~~~~~~~~~~

**README.md Template:**

.. code-block:: markdown

   # Project Name
   
   Brief description of the project.
   
   ## Installation
```bash
   git clone https://github.com/username/project.git
   cd project
   pip install -r requirements.txt
```
   
   ## Usage
```python
   from src.pipeline import PreprocessingPipeline
   
   pipeline = PreprocessingPipeline(...)
   result = pipeline.run(subject_id='01')
```
   
   ## Documentation
   
   See `docs/` directory for detailed documentation.
   
   ## Contributing
   
   1. Fork the repository
   2. Create a feature branch
   3. Make your changes
   4. Submit a pull request
   
   ## License
   
   MIT License (or your chosen license)

HPC-Specific Practices
----------------------

Environment Management
~~~~~~~~~~~~~~~~~~~~~~

**Use Module System:**

.. code-block:: bash

   # .bashrc or job script
   module load python/3.9
   module load git/2.30
   module load fsl/6.0

**Create Project-Specific Environments:**

.. code-block:: bash

   # Create environment
   python -m venv ~/envs/fmri_project
   source ~/envs/fmri_project/bin/activate
   pip install -r requirements.txt

Resource Management
~~~~~~~~~~~~~~~~~~~

**Request Appropriate Resources:**

.. code-block:: bash

   # SLURM job script
   #!/bin/bash
   #SBATCH --job-name=fmri_preproc
   #SBATCH --time=02:00:00          # 2 hours (be realistic)
   #SBATCH --mem=8G                 # 8GB RAM (based on testing)
   #SBATCH --cpus-per-task=4        # 4 CPUs
   #SBATCH --output=logs/%j.out     # Log file
   
   # Load modules
   module load python/3.9
   
   # Activate environment
   source ~/envs/fmri_project/bin/activate
   
   # Run analysis
   python scripts/batch_process.py

**Monitor Resource Usage:**

.. code-block:: python

   import psutil
   import time
   
   def process_subject(subject_id):
       start_time = time.time()
       start_mem = psutil.virtual_memory().used / 1e9
       
       # ... processing ...
       
       end_time = time.time()
       end_mem = psutil.virtual_memory().used / 1e9
       
       print(f"Subject {subject_id}:")
       print(f"  Time: {end_time - start_time:.1f}s")
       print(f"  Memory: {end_mem - start_mem:.1f}GB")

Security Practices
------------------

**Never Commit Sensitive Data:**

.. code-block:: text

   ❌ Don't commit:
   - Passwords
   - API keys
   - Personal health information (PHI)
   - Participant identifiable data
   - SSH private keys

**Use Environment Variables:**

.. code-block:: python

   # ✅ Good:
   import os
   api_key = os.environ.get('NEUROIMAGING_API_KEY')
   
   # ❌ Bad:
   api_key = "abc123def456"  # Hardcoded!

**Add PHI to .gitignore:**

.. code-block:: text

   # .gitignore
   participants.tsv       # May contain dates of birth, etc.
   *_demographic.csv
   sourcedata/           # Original DICOM files

Common Pitfalls to Avoid
------------------------

Git Pitfalls
~~~~~~~~~~~~

- ❌ Force pushing to ``main`` or shared branches
- ❌ Committing large binary files
- ❌ Not pulling before starting work
- ❌ Vague commit messages
- ❌ Mixing multiple unrelated changes in one commit

Code Pitfalls
~~~~~~~~~~~~~

- ❌ Hardcoded file paths
- ❌ No error handling
- ❌ Missing docstrings
- ❌ Not testing code before committing
- ❌ Leaving debug print statements

Neuroimaging Pitfalls
~~~~~~~~~~~~~~~~~~~~~

- ❌ Not checking image orientations
- ❌ Assuming all images have same dimensions
- ❌ Not preserving image headers
- ❌ Forgetting to mask before group analysis
- ❌ Not documenting preprocessing parameters

Checklist for Production Code
------------------------------

Before deploying code for real research:

- ☐ All functions have docstrings
- ☐ Unit tests cover >80% of code
- ☐ Code follows style guide (flake8 passes)
- ☐ No hardcoded paths
- ☐ Comprehensive error handling
- ☐ Logging implemented for debugging
- ☐ Resource usage tested on HPC
- ☐ Documentation is complete
- ☐ Peer review completed
- ☐ Preprocessing parameters documented
- ☐ Version control for reproducibility

Resources
---------

- `PEP 8 Style Guide <https://peps.python.org/pep-0008/>`_
- `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_
- `BIDS Specification <https://bids-specification.readthedocs.io/>`_
- `Nilearn Best Practices <https://nilearn.github.io/stable/building_blocks/manual_pipeline.html>`_
- `Software Carpentry <https://software-carpentry.org/>`_