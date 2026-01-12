Troubleshooting Guide
=====================

This page provides solutions to common problems encountered during the workshop.

Git Issues
----------

Cannot Push to Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   error: failed to push some refs to 'https://github.com/...'
   hint: Updates were rejected because the remote contains work that you do
   hint: not have locally.

**Cause:** Remote branch has commits you don't have locally.

**Solution:**

.. code-block:: bash

   # Pull latest changes first
   git pull origin feature/your-branch
   
   # Resolve any conflicts, then push
   git push origin feature/your-branch

**Alternative (if you're sure your version is correct):**

.. code-block:: bash

   # Force push (use with caution!)
   git push origin feature/your-branch --force

.. warning::
   Only use ``--force`` on your feature branches, never on ``main``!

Accidentally Committed to Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** You made commits on ``main`` instead of a feature branch.

**Solution 1: Move commits to new branch**

.. code-block:: bash

   # Create new branch with your commits
   git branch feature/my-work
   
   # Reset main to match upstream
   git fetch upstream
   git reset --hard upstream/main
   
   # Switch to your feature branch
   git checkout feature/my-work
   
   # Your commits are now safely on the feature branch

**Solution 2: Cherry-pick specific commits**

.. code-block:: bash

   # Note the commit hash
   git log --oneline
   
   # Create and switch to new branch
   git checkout -b feature/my-work upstream/main
   
   # Cherry-pick the commit
   git cherry-pick <commit-hash>

Merge Conflict During Rebase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   CONFLICT (content): Merge conflict in src/run_analysis.py
   error: could not apply a3f2b9c... Add smoothing function

**Solution:**

.. code-block:: bash

   # 1. Open conflicted file in VS Code
   code src/run_analysis.py
   
   # 2. Look for conflict markers:
   #    <<<<<<< HEAD
   #    =======
   #    >>>>>>> commit-message
   
   # 3. Resolve conflicts (choose changes to keep)
   
   # 4. Remove conflict markers
   
   # 5. Stage resolved file
   git add src/run_analysis.py
   
   # 6. Continue rebase
   git rebase --continue

**If you want to abort:**

.. code-block:: bash

   git rebase --abort

See :doc:`../workflows/merge-conflicts` for detailed conflict resolution guide.

Detached HEAD State
~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   You are in 'detached HEAD' state.

**Cause:** Checked out a specific commit instead of a branch.

**Solution:**

.. code-block:: bash

   # If you made changes you want to keep:
   git checkout -b new-branch-name
   
   # If you want to discard changes:
   git checkout main

Lost Commits After Reset
~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Accidentally used ``git reset --hard`` and lost work.

**Solution:** Use reflog to recover

.. code-block:: bash

   # View recent Git operations
   git reflog
   
   # Output shows:
   # a1b2c3d HEAD@{0}: reset: moving to HEAD~1
   # e4f5g6h HEAD@{1}: commit: My important work  ← This one!
   # i7j8k9l HEAD@{2}: commit: Previous commit
   
   # Recover the lost commit
   git checkout e4f5g6h
   
   # Create branch to save it
   git checkout -b recovered-work

Wrong Remote Repository
~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Pushing to wrong repository (upstream instead of origin).

**Solution:**

.. code-block:: bash

   # Check current remotes
   git remote -v
   
   # If origin points to wrong repo, update it:
   git remote set-url origin https://github.com/YOUR_USERNAME/repo.git
   
   # Verify
   git remote -v

Cannot Clone Repository
~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   Permission denied (publickey).
   fatal: Could not read from remote repository.

**Cause:** SSH key not configured or not authorized.

**Solution 1: Use HTTPS instead**

.. code-block:: bash

   git clone https://github.com/username/repo.git

**Solution 2: Configure SSH key**

.. code-block:: bash

   # Generate SSH key (if you don't have one)
   ssh-keygen -t ed25519 -C "your.email@example.com"
   
   # Copy public key
   cat ~/.ssh/id_ed25519.pub
   
   # Add to GitHub:
   # 1. Go to GitHub Settings → SSH Keys
   # 2. Click "New SSH key"
   # 3. Paste key and save

VS Code Remote Issues
---------------------

Cannot Connect to HPC
~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   Could not establish connection to "hpc-cluster"

**Solutions:**

1. **Check VPN connection:**

   .. code-block:: bash
   
      # Test connectivity
      ping hpc.institution.edu

2. **Verify SSH config:**

   .. code-block:: bash
   
      # Test SSH connection
      ssh hpc-cluster
      
      # If password needed but you have key:
      ssh -v hpc-cluster  # Verbose output for debugging

3. **Check SSH permissions:**

   .. code-block:: bash
   
      chmod 700 ~/.ssh
      chmod 600 ~/.ssh/id_rsa
      chmod 644 ~/.ssh/id_rsa.pub

4. **Restart VS Code:**

   - Close all VS Code windows
   - Reopen and try connecting again

Connection Keeps Dropping
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** VS Code Remote-SSH disconnects frequently.

**Solution:** Update SSH config with keep-alive settings

.. code-block:: ssh

   Host hpc-cluster
       HostName hpc.institution.edu
       User your_username
       ServerAliveInterval 30
       ServerAliveCountMax 5
       TCPKeepAlive yes
       Compression yes

Python Extension Not Working
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** IntelliSense, linting not working on remote.

**Solution 1: Select correct interpreter**

.. code-block:: text

   1. Press F1
   2. Type "Python: Select Interpreter"
   3. Choose the correct Python path

**Solution 2: Reinstall Python extension remotely**

.. code-block:: text

   1. In VS Code, click Extensions (Ctrl+Shift+X)
   2. Find "Python" extension
   3. Click "Install in SSH: hpc-cluster"
   4. Reload window (F1 → "Developer: Reload Window")

**Solution 3: Check Python path**

.. code-block:: bash

   # In VS Code integrated terminal
   which python
   python --version

Slow Remote Performance
~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** VS Code on remote is very slow.

**Solutions:**

1. **Disable unnecessary extensions remotely:**

   - Only install essential extensions on remote
   - Disable heavy extensions (e.g., GitLens, Docker)

2. **Use terminal for heavy operations:**

   .. code-block:: bash
   
      # Instead of using VS Code search on large directories:
      grep -r "pattern" src/

3. **Exclude directories from file watching:**

   In workspace settings (``.vscode/settings.json``):

   .. code-block:: json
   
      {
          "files.watcherExclude": {
              "**/data/**": true,
              "**/outputs/**": true,
              "**/.git/objects/**": true
          }
      }

Terminal Not Opening
~~~~~~~~~~~~~~~~~~~~

**Problem:** Integrated terminal fails to open.

**Solution:**

.. code-block:: text

   1. Press F1
   2. Type "Terminal: Kill All Terminals"
   3. Press F1
   4. Type "Developer: Reload Window"
   5. Try opening terminal again (Ctrl+Shift+`)

Python/Environment Issues
-------------------------

Module Not Found
~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   ModuleNotFoundError: No module named 'nilearn'

**Solutions:**

1. **Verify virtual environment is activated:**

   .. code-block:: bash
   
      # Your prompt should show (venv)
      which python
      # Should show: /home/username/workshop/venv/bin/python

2. **Activate environment:**

   .. code-block:: bash
   
      source venv/bin/activate

3. **Install dependencies:**

   .. code-block:: bash
   
      pip install -r requirements.txt

4. **Verify installation:**

   .. code-block:: bash
   
      pip list | grep nilearn

Wrong Python Version
~~~~~~~~~~~~~~~~~~~~

**Problem:** Using Python 2.x instead of 3.x

**Check version:**

.. code-block:: bash

   python --version

**Solution:**

.. code-block:: bash

   # Use python3 explicitly
   python3 -m venv venv
   source venv/bin/activate
   python --version  # Should show 3.x

Virtual Environment Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Virtual environment not activating.

**Solution 1: Recreate environment**

.. code-block:: bash

   # Remove old environment
   rm -rf venv
   
   # Create new one
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

**Solution 2: Use full path**

.. code-block:: bash

   # Instead of:
   source venv/bin/activate
   
   # Use full path:
   source ~/workshop/neuroimaging-workshop/venv/bin/activate

Package Installation Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   ERROR: Could not install packages due to an EnvironmentError

**Solution 1: Use --user flag**

.. code-block:: bash

   pip install --user -r requirements.txt

**Solution 2: Check HPC policies**

.. code-block:: bash

   # On some HPC systems, use --break-system-packages
   pip install --break-system-packages -r requirements.txt

**Solution 3: Check disk quota**

.. code-block:: bash

   # Check disk usage
   quota -s
   df -h ~

Neuroimaging Errors
-------------------

File Not Found
~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   FileNotFoundError: Cannot find: /data/shared/workshop/bids_dataset/...

**Solutions:**

1. **Verify data path:**

   .. code-block:: bash
   
      ls /data/shared/workshop/bids_dataset/
      ls /data/shared/workshop/bids_dataset/sub-01/

2. **Check subject ID format:**

   .. code-block:: python
   
      # Correct:
      subject_id = "01"  # String, zero-padded
      
      # Incorrect:
      subject_id = 1  # Integer
      subject_id = "1"  # Not zero-padded

3. **Check BIDS structure:**

   .. code-block:: text
   
      data/
      └── sub-01/
          └── func/
              └── sub-01_task-rest_run-1_bold.nii.gz

Memory Error
~~~~~~~~~~~~

**Error:**

.. code-block:: text

   MemoryError: Unable to allocate array

**Solutions:**

1. **Process one subject at a time:**

   .. code-block:: python
   
      # ✅ Good:
      for subject_id in subjects:
          img = load_data(subject_id)
          process(img)
          del img  # Free memory
   
      # ❌ Bad:
      all_imgs = [load_data(sid) for sid in subjects]

2. **Use lazy loading:**

   .. code-block:: python
   
      from nilearn import image
      
      # Doesn't load data until accessed
      img = image.load_img('func.nii.gz')

3. **Request more memory on HPC:**

   .. code-block:: bash
   
      #SBATCH --mem=16G  # Increase from 8G

Shape Mismatch
~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   ValueError: Shape (64, 64, 36) doesn't match (64, 64, 36, 180)

**Cause:** Passing 3D image to function expecting 4D.

**Solution:** Check dimensions

.. code-block:: python

   print(f"Image shape: {img.shape}")
   
   # If 3D but need 4D:
   if len(img.shape) == 3:
       img = image.new_img_like(img, img.get_fdata()[..., np.newaxis])

Invalid Affine
~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   ValueError: Affine matrix must be 4x4

**Solution:** Always use image's original affine

.. code-block:: python

   # ✅ Good:
   new_img = nib.Nifti1Image(processed_data, img.affine, img.header)
   
   # ❌ Bad:
   new_img = nib.Nifti1Image(processed_data, np.eye(4))

Low tSNR Warning
~~~~~~~~~~~~~~~~

**Problem:** tSNR < 10, unexpectedly low.

**Possible Causes:**

1. **Forgot to skull-strip:** Background noise inflates std

   .. code-block:: python
   
      # Make sure you're computing tSNR on masked data
      img_stripped = self.skull_strip(img)
      qa = self.quality_assurance(img_stripped)

2. **Motion artifacts:** Check carpet plot for vertical lines

3. **Scanner issues:** Compare with other subjects

**Solution:** Review QA outputs

.. code-block:: bash

   # Check diagnostic figure
   xdg-open outputs/sub-01_diagnostic.png
   
   # Review QA report
   cat outputs/qa_report.txt

HPC-Specific Issues
-------------------

Module Not Available
~~~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   module: command not found

**Solution 1: Source module system**

.. code-block:: bash

   # Add to ~/.bashrc
   source /etc/profile.d/modules.sh

**Solution 2: Use full path**

.. code-block:: bash

   # Instead of module load:
   export PATH=/opt/apps/python/3.9/bin:$PATH

Job Fails Silently
~~~~~~~~~~~~~~~~~~

**Problem:** SLURM job completes but no output.

**Check:**

.. code-block:: bash

   # View job output
   cat slurm-<job-id>.out
   
   # Check job status
   sacct -j <job-id>

**Common causes:**

1. **Wrong Python path:** Check which python is used
2. **Environment not activated:** Activate in job script
3. **File permissions:** Check output directory is writable

Out of Disk Quota
~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   OSError: [Errno 122] Disk quota exceeded

**Solution:**

.. code-block:: bash

   # Check quota
   quota -s
   
   # Find large files
   du -sh ~/* | sort -h
   
   # Clean up
   rm -rf ~/workshop/venv  # Recreate if needed
   rm -rf ~/.cache/pip

Job Timeout
~~~~~~~~~~~

**Problem:** Job killed after reaching time limit.

**Solution:** Request more time or optimize code

.. code-block:: bash

   # In SLURM script, increase time:
   #SBATCH --time=04:00:00  # 4 hours instead of 2
   
   # Or optimize your code to run faster

Permissions Denied
~~~~~~~~~~~~~~~~~~

**Error:**

.. code-block:: text

   PermissionError: [Errno 13] Permission denied: '/data/shared/workshop/'

**Cause:** Trying to write to read-only directory.

**Solution:** Write to your home directory or scratch

.. code-block:: python

   # ✅ Good:
   output_dir = Path("~/workshop/outputs").expanduser()
   
   # ❌ Bad:
   output_dir = Path("/data/shared/workshop/outputs")

Workshop-Specific Issues
------------------------

Cannot Create Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** "No changes between branches" when creating PR.

**Cause:** You forked after instructor made changes, or you're comparing wrong branches.

**Solution:**

.. code-block:: bash

   # Make sure you have commits:
   git log origin/main..feature/your-branch
   
   # If empty, you need to make changes:
   # 1. Edit files
   # 2. Commit
   # 3. Push
   git add src/run_analysis.py
   git commit -m "Add my feature"
   git push origin feature/your-branch

PR Shows Unexpected Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** PR includes files you didn't change.

**Cause:** Branch created from outdated main.

**Solution:**

.. code-block:: bash

   # Rebase onto latest main
   git fetch upstream
   git rebase upstream/main
   git push origin feature/your-branch --force

Group Functions Interfere
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Two groups' functions have same name.

**Solution:** Use descriptive, unique names

.. code-block:: python

   # ✅ Good:
   def smooth_image(self, img, fwhm=6.0):  # Clear, specific
   
   def skull_strip(self, img):  # Clear, specific
   
   # ❌ Bad:
   def process(self, img):  # Too generic!

Tests Failing After Merge
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Tests pass locally but fail after PR merge.

**Possible Causes:**

1. **Tests depend on local file paths**
2. **Missing dependencies**
3. **Different Python version**

**Solution:**

.. code-block:: python

   # Use relative paths
   data_dir = Path(__file__).parent.parent / "data"
   
   # Not absolute paths
   data_dir = Path("/home/myname/workshop/data")

Debugging Strategies
--------------------

General Debugging Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # 1. Add print statements
   print(f"Image shape: {img.shape}")
   print(f"Data type: {img.get_data_dtype()}")
   
   # 2. Check intermediate values
   print(f"Mean: {data.mean()}")
   print(f"Std: {data.std()}")
   print(f"Min/Max: {data.min()}, {data.max()}")
   
   # 3. Verify assumptions
   assert len(img.shape) == 4, f"Expected 4D, got {img.shape}"
   assert img.shape[3] > 0, "No time points!"

Using Python Debugger
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Insert breakpoint
   import pdb; pdb.set_trace()
   
   # When execution stops:
   # n = next line
   # s = step into function
   # c = continue
   # p variable = print variable
   # q = quit

VS Code Debugger
~~~~~~~~~~~~~~~~

.. code-block:: text

   1. Click in left margin to set breakpoint (red dot)
   2. Press F5 to start debugging
   3. Use debug toolbar:
      - Continue (F5)
      - Step Over (F10)
      - Step Into (F11)
      - Step Out (Shift+F11)
   4. Inspect variables in left panel

Logging Instead of Print
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger(__name__)
   
   def smooth_image(self, img, fwhm=6.0):
       logger.debug(f"Input shape: {img.shape}")
       logger.info(f"Smoothing with FWHM={fwhm}")
       
       smoothed = smooth_img(img, fwhm=fwhm)
       
       logger.debug(f"Output shape: {smoothed.shape}")
       return smoothed

Getting Help
------------

Where to Ask for Help
~~~~~~~~~~~~~~~~~~~~~

**During Workshop:**

1. Raise hand or ask in chat
2. Share screen to show error
3. Check with teammates first

**After Workshop:**

1. Post in course forum/Slack
2. Create GitHub issue in repository
3. Email instructor
4. Stack Overflow (for technical issues)

How to Ask Good Questions
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Include:**

1. **What you're trying to do**
2. **What you tried**
3. **Full error message**
4. **Code that reproduces the error**
5. **Your environment** (Python version, OS, etc.)

**Example:**

.. code-block:: text

   I'm trying to skull-strip functional data but getting an error.
   
   Code:
```python
   img = self.load_data('01')
   stripped = self.skull_strip(img)
```
   
   Error:
```
   ValueError: Affine must be 4x4, got shape (3, 3)
```
   
   Environment:
   - Python 3.9
   - nilearn 0.10.0
   - Ubuntu 22.04 on HPC cluster
   
   I've already tried... [what you tried]

Creating Minimal Reproducible Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Instead of full pipeline, isolate the problem:
   
   import nibabel as nib
   from nilearn.masking import compute_epi_mask
   
   # Load minimal test data
   img = nib.load('test_data.nii.gz')
   
   # Reproduce error
   mask = compute_epi_mask(img)  # This is where it fails

Additional Resources
--------------------

Quick Reference Commands
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Git
   git status                    # Check status
   git diff                      # See changes
   git log --oneline            # View history
   git reflog                   # Find lost commits
   
   # VS Code
   Ctrl+Shift+P                 # Command palette
   Ctrl+Shift+G                 # Source control
   Ctrl+`                       # Toggle terminal
   F1                           # Command palette
   
   # Python
   python -c "import sys; print(sys.version)"  # Check Python version
   pip list                                     # List installed packages
   which python                                 # Find Python path

Documentation Links
~~~~~~~~~~~~~~~~~~~

- Git: https://git-scm.com/doc
- VS Code Remote: https://code.visualstudio.com/docs/remote/ssh
- Nilearn: https://nilearn.github.io/
- NumPy: https://numpy.org/doc/
- Matplotlib: https://matplotlib.org/