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
   ``https://github.com/Nialljb/github-workshop.git``

1. Navigate to the repository on GitHub
2. Click the **Fork** button (top right corner)
3. Select your account as the destination
4. Wait for fork to complete (usually 5-10 seconds)

You now have: ``https://github.com/YOUR_USERNAME/github-workshop``

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

Step 3: SSH Keys for Mac Users
-------------------------------

For secure authentication with GitHub, you'll need SSH keys. This is especially 
important for pushing changes to your repository.

Check for Existing Keys
~~~~~~~~~~~~~~~~~~~~~~~

First, check if you already have SSH keys:

.. code-block:: bash

   ls ~/.ssh

If you see files like ``id_rsa`` and ``id_rsa.pub``, you already have a key pair.
You can skip to adding the public key to GitHub below.

Expected output with existing keys:

.. code-block:: text

   authorized_keys  id_rsa      id_rsa.pub   config   known_hosts

Generate New RSA Key
~~~~~~~~~~~~~~~~~~~~

If you don't have keys, create a new RSA key pair:

.. code-block:: bash

   ssh-keygen -t rsa

.. warning::
   If you have an existing ``id_rsa`` file, this command will overwrite it! 
   Press Ctrl+C to cancel if you want to keep your existing key.

When prompted:

1. **File location**: Press Enter to use the default location (``~/.ssh/id_rsa``)
2. **Passphrase**: Enter a strong passphrase for security (recommended)

Add Public Key to GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~

Copy your public key to the clipboard:

.. code-block:: bash

   cat ~/.ssh/id_rsa.pub

This will display your public key. Copy the entire output.

Then:

1. Go to GitHub → Settings → SSH and GPG keys
2. Click **New SSH key**
3. Give it a descriptive title (e.g., "HPC Workstation")
4. Paste your public key in the "Key" field
5. Click **Add SSH key**

Test SSH Connection
~~~~~~~~~~~~~~~~~~~

Verify your SSH key works with GitHub:

.. code-block:: bash

   ssh -T git@github.com

You should see a message like:

.. code-block:: text

   Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.

.. note::
   Now you can use SSH URLs (``git@github.com:username/repo.git``) instead of 
   HTTPS URLs when cloning repositories for better security and convenience.

Step 4: Add Upstream Remote
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

Step 5: Create Python Environment
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

Step 6: Install Dependencies
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

Step 7: Verify Data Access
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