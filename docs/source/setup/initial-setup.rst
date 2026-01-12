Initial Setup for Group Challenge
==================================

Understanding Forks vs Clones
------------------------------

What's the difference?
~~~~~~~~~~~~~~~~~~~~~~

**Fork** (GitHub action):

- Creates your own copy **on GitHub**
- You own this copy and can modify it freely
- Used for contributing to projects you don't have write access to

**Clone** (Git action):

- Downloads a repository from GitHub to your local machine (HPC)
- Creates a working copy you can edit

Typical workflow:

.. code-block:: text

   1. Fork (GitHub) → github.com/YOUR_NAME/project
   2. Clone (Git) → Downloads to HPC workspace
   3. Make changes locally
   4. Push to your fork
   5. Create PR from fork to original repo

Step 1: Fork the Repository
----------------------------

.. note::
   Instructor provides: ``https://github.com/INSTRUCTOR_NAME/neuroimaging-workshop``

1. Navigate to the repository on GitHub
2. Click the **Fork** button (top right corner)
3. Select your account as the destination
4. Wait for fork to complete (usually 5-10 seconds)

You now have: ``https://github.com/YOUR_USERNAME/neuroimaging-workshop``

Step 2: Clone to HPC Workspace
-------------------------------

Open VS Code integrated terminal:

.. code-block:: bash

   # Navigate to workshop directory
   cd ~/workshop
   
   # Clone YOUR fork (replace YOUR_USERNAME)
   git clone https://github.com/YOUR_USERNAME/neuroimaging-workshop.git
   
   # Enter the repository
   cd neuroimaging-workshop

.. important::
   Clone **YOUR fork**, not the instructor's repository. You don't have write 
   access to the instructor's repository.

Step 3: Add Upstream Remote
----------------------------

What is a remote?
~~~~~~~~~~~~~~~~~

A remote is a bookmark to a repository on GitHub. By default, you have one 
remote called ``origin`` (your fork). We're adding a second remote called 
``upstream`` (the instructor's original repo).

**Why?** You need to fetch updates from the instructor's repo as other 
students' PRs get merged.

.. code-block:: bash

   # Add upstream remote (replace INSTRUCTOR_NAME)
   git remote add upstream https://github.com/INSTRUCTOR_NAME/neuroimaging-workshop.git
   
   # Verify both remotes exist
   git remote -v

Expected output:

.. code-block:: text

   origin    https://github.com/YOUR_USERNAME/neuroimaging-workshop.git (fetch)
   origin    https://github.com/YOUR_USERNAME/neuroimaging-workshop.git (push)
   upstream  https://github.com/INSTRUCTOR_NAME/neuroimaging-workshop.git (fetch)
   upstream  https://github.com/INSTRUCTOR_NAME/neuroimaging-workshop.git (push)

Remember:

- **origin** = your fork (you push here)
- **upstream** = instructor's repo (you pull from here)

Step 4: Create Python Environment
----------------------------------

.. code-block:: bash

   # Load Python module if needed
   module load python/3.9
   
   # Create virtual environment
   python -m venv venv
   
   # Activate environment
   source venv/bin/activate

Why use a virtual environment?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Virtual environments isolate your project's Python packages:

- Different projects can use different package versions
- No conflicts with system Python
- Easy to recreate environment on another machine
- Clean pip install list specific to this project

Step 5: Install Dependencies
-----------------------------

.. code-block:: bash

   pip install --upgrade pip
   pip install -r requirements.txt

``requirements.txt`` contents:

.. code-block:: text

   nibabel>=5.0.0
   nilearn>=0.10.0
   numpy>=1.24.0
   matplotlib>=3.7.0
   scipy>=1.10.0
   pandas>=2.0.0

Understanding requirements.txt:

- ``package>=5.0.0``: Install version 5.0.0 or newer
- Ensures everyone has compatible versions
- Pin exact versions for reproducibility: ``nibabel==5.0.1``

Step 6: Verify Data Access
---------------------------

.. code-block:: bash

   # Check if BIDS dataset exists
   ls /data/shared/workshop/bids_dataset/

Expected output:

.. code-block:: text

   sub-01/  sub-02/  sub-03/  dataset_description.json  participants.tsv

Test data loading:

.. code-block:: bash

   python -c "
   import nibabel as nib
   from pathlib import Path
   
   data_dir = Path('/data/shared/workshop/bids_dataset')
   img_file = data_dir / 'sub-01' / 'func' / 'sub-01_task-rest_run-1_bold.nii.gz'
   
   if img_file.exists():
       img = nib.load(img_file)
       print(f'✓ Successfully loaded: {img.shape}')
   else:
       print('✗ Data file not found')
   "

.. tip::
   You're now ready to start the group challenge!