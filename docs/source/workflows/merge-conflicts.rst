Resolving Merge Conflicts
==========================

What is a Merge Conflict?
--------------------------

A merge conflict occurs when:

1. You and another person modify **the same lines** of the same file
2. Git doesn't know which version to keep
3. Git asks **you** to decide

.. important::
   **Conflicts are normal!** They're not errors - just Git asking for your help.

When Do Conflicts Occur?
-------------------------

Conflicts happen during:

- **Merging branches:** ``git merge main``
- **Rebasing:** ``git rebase main``
- **Pulling changes:** ``git pull upstream main``
- **Cherry-picking:** ``git cherry-pick <commit>``

Example Scenario
~~~~~~~~~~~~~~~~

.. code-block:: text

   You (Group 1) added:
   img_smoothed = self.smooth_image(img, fwhm=6.0)
   
   Instructor added (same location):
   print("Starting preprocessing pipeline...")
   
   Both modified line 85 → CONFLICT!

Understanding Conflict Markers
-------------------------------

When a conflict occurs, Git adds special markers to the file:

.. code-block:: python

   <<<<<<< HEAD (Current Change)
   print("Starting preprocessing pipeline...")
   
   img_stripped = self.skull_strip(img)
   =======
   # GROUP 1: Call smoothing method
   img_smoothed = self.smooth_image(img, fwhm=6.0)
   >>>>>>> a3f2b9c (Incoming Change)

**Anatomy of conflict markers:**

.. code-block:: text

   <<<<<<< HEAD
      ↑
      Current changes (what's in main)
      
   =======
      ↑
      Divider between the two versions
      
   >>>>>>> a3f2b9c
      ↑
      Your changes (from your branch)

VS Code Conflict Interface
---------------------------

VS Code detects conflicts and shows helpful buttons:

.. image:: /_static/vscode_conflict.png
   :alt: VS Code conflict interface
   :align: center

**Options:**

1. **Accept Current Change** - Keep only main's version (lose your work)
2. **Accept Incoming Change** - Keep only your version (lose their work)
3. **Accept Both Changes** - Keep both (often the right choice)
4. **Compare Changes** - See detailed diff side-by-side

.. tip::
   For most workshop conflicts, **Accept Both Changes** is the right choice.

Step-by-Step Conflict Resolution
---------------------------------

Scenario: Group 1 Rebasing After Group 2 Merges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Setup:**

- Group 2's skull stripping PR was just merged to main
- Your Group 1 smoothing branch is now behind

**Step 1: Trigger the Rebase**

.. code-block:: bash

   # Update your local main
   git fetch upstream
   git checkout main
   git merge upstream/main
   
   # Switch to your feature branch
   git checkout feature/group-1-smoothing
   
   # Rebase onto updated main
   git rebase main

**Git Output:**

.. code-block:: text

   Auto-merging src/run_analysis.py
   CONFLICT (content): Merge conflict in src/run_analysis.py
   error: could not apply a3f2b9c... Add smoothing function
   
   Resolve all conflicts manually, mark them as resolved with
   "git add/rm <conflicted_files>", then run "git rebase --continue".

.. note::
   **Don't panic!** This is expected. Git has paused and is waiting for your help.

**Step 2: Open Conflicted File**

.. code-block:: bash

   # See which files have conflicts
   git status

**Output:**

.. code-block:: text

   rebase in progress; onto b2d8f4a
   You are currently rebasing branch 'feature/group-1-smoothing' on 'b2d8f4a'.
   
   Unmerged paths:
     both modified:   src/run_analysis.py

**Open in VS Code:**

.. code-block:: bash

   code src/run_analysis.py

**Step 3: Examine the Conflict**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       print(f"\n{'='*60}")
       print(f"Processing Subject: {subject_id}")
       print(f"{'='*60}\n")
       
       img = self.load_data(subject_id)
       
   <<<<<<< HEAD (from main)
       # GROUP 2: Call skull-strip method
       img_stripped = self.skull_strip(img)
   =======
       # GROUP 1: Call smoothing method
       img_smoothed = self.smooth_image(img, fwhm=6.0)
   >>>>>>> a3f2b9c (your commit)

**Step 4: Decide Resolution Strategy**

**Analysis:**

- Main added skull stripping (Group 2's work)
- Your branch added smoothing (Group 1's work)
- Both are needed!
- Smoothing should operate on **stripped** data

**Resolution:**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       print(f"\n{'='*60}")
       print(f"Processing Subject: {subject_id}")
       print(f"{'='*60}\n")
       
       img = self.load_data(subject_id)
       
       # GROUP 2: Call skull-strip method
       img_stripped = self.skull_strip(img)
       
       # GROUP 1: Call smoothing method (operates on stripped data)
       img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)

**Key changes:**

1. Kept Group 2's skull stripping
2. Kept Group 1's smoothing
3. Changed input to smoothing from ``img`` → ``img_stripped``
4. **Deleted all conflict markers** (``<<<<<<<``, ``=======``, ``>>>>>>>``)

**Step 5: Mark as Resolved**

.. code-block:: bash

   # Stage the resolved file
   git add src/run_analysis.py
   
   # Verify status
   git status

**Output:**

.. code-block:: text

   rebase in progress; onto b2d8f4a
   You are currently rebasing branch 'feature/group-1-smoothing' on 'b2d8f4a'.
   
   Changes to be committed:
     modified:   src/run_analysis.py

**Step 6: Continue the Rebase**

.. code-block:: bash

   # Continue rebase process
   git rebase --continue

.. note::
   If you have multiple commits, Git may pause again for additional conflicts. 
   Repeat steps 2-6 for each conflict.

**Step 7: Push Updated Branch**

.. code-block:: bash

   # Force push because rebase rewrote history
   git push origin feature/group-1-smoothing --force

.. success::
   Your PR on GitHub automatically updates with the resolved conflict!

Common Conflict Patterns
------------------------

Pattern 1: Both Added Same Function Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   <<<<<<< HEAD
   def process_data(self, img):
       """Group 2's implementation"""
       return self.skull_strip(img)
   =======
   def process_data(self, img):
       """Group 1's implementation"""
       return self.smooth_image(img)
   >>>>>>> your-commit

**Resolution:** Rename one function to avoid collision:

.. code-block:: python

   def skull_strip(self, img):
       """Group 2's implementation"""
       return self._compute_mask(img)
   
   def smooth_image(self, img):
       """Group 1's implementation"""
       return smooth_img(img, fwhm=6.0)

Pattern 2: Different Import Statements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   <<<<<<< HEAD
   from nilearn import masking, image
   import numpy as np
   =======
   from nilearn import image
   import matplotlib.pyplot as plt
   import numpy as np
   >>>>>>> your-commit

**Resolution:** Combine and sort alphabetically:

.. code-block:: python

   from nilearn import image, masking
   import matplotlib.pyplot as plt
   import numpy as np

Pattern 3: Comments in Same Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   <<<<<<< HEAD
   # TODO: Add error handling
   =======
   # FIXME: Validate FWHM parameter
   >>>>>>> your-commit

**Resolution:** Keep both if both are useful:

.. code-block:: python

   # TODO: Add error handling
   # FIXME: Validate FWHM parameter

Pattern 4: Sequential Function Calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   img = self.load_data(subject_id)
   
   <<<<<<< HEAD
   img = self.skull_strip(img)
   img = self.quality_check(img)
   =======
   img = self.smooth_image(img)
   img = self.denoise(img)
   >>>>>>> your-commit

**Resolution:** Determine logical order:

.. code-block:: python

   img = self.load_data(subject_id)
   img = self.skull_strip(img)      # Remove non-brain first
   img = self.denoise(img)           # Then denoise
   img = self.smooth_image(img)      # Then smooth
   img = self.quality_check(img)     # Finally QA

Conflict Resolution Strategies
-------------------------------

Strategy 1: Accept Both Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When to use:** Both changes are independent and needed.

**Example:**

.. code-block:: python

   # Before (conflict):
   <<<<<<< HEAD
   self.output_dir.mkdir(parents=True, exist_ok=True)
   =======
   self.data_dir.mkdir(parents=True, exist_ok=True)
   >>>>>>>
   
   # After (resolution):
   self.output_dir.mkdir(parents=True, exist_ok=True)
   self.data_dir.mkdir(parents=True, exist_ok=True)

Strategy 2: Accept One Side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When to use:** One change is clearly better or more up-to-date.

**Example:**

.. code-block:: python

   # Keep instructor's bug fix, discard old code
   <<<<<<< HEAD
   mask = compute_epi_mask(img, lower_cutoff=0.3)  # Fixed threshold
   =======
   mask = compute_epi_mask(img)  # Old, problematic
   >>>>>>>
   
   # Resolution: Keep HEAD version
   mask = compute_epi_mask(img, lower_cutoff=0.3)

Strategy 3: Hybrid Solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When to use:** Need elements from both, combined logically.

**Example:**

.. code-block:: python

   <<<<<<< HEAD
   print(f"Processing {subject_id}")
   img = self.load_data(subject_id)
   =======
   img = self.load_data(subject_id)
   print(f"Loaded: {img.shape}")
   >>>>>>>
   
   # Resolution: Combine both messages
   print(f"Processing {subject_id}")
   img = self.load_data(subject_id)
   print(f"Loaded: {img.shape}")

Strategy 4: Rewrite Completely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**When to use:** Both versions are wrong or incompatible.

**Example:**

.. code-block:: python

   <<<<<<< HEAD
   # Old approach
   result = slow_method(data)
   =======
   # Different old approach
   result = other_slow_method(data)
   >>>>>>>
   
   # Resolution: Use better approach found during conflict resolution
   result = fast_vectorized_method(data)

Preventing Conflicts
--------------------

1. Pull/Rebase Frequently
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Update your branch daily
   git fetch upstream
   git rebase upstream/main

**Why:** Smaller, more frequent merges = fewer conflicts.

2. Communicate with Team
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   In team chat:
   "I'm working on lines 45-60 of run_analysis.py today"

**Why:** Avoid working on same code sections simultaneously.

3. Keep PRs Small and Focused
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   ✅ Good PR: Add one function (50 lines)
   ❌ Bad PR: Refactor entire file (500 lines)

**Why:** Smaller changes = less overlap with others.

4. Use Clear Markers
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ============================================================
   # GROUP 1: IMPLEMENT SMOOTHING METHOD BELOW THIS LINE
   # ============================================================

**Why:** Makes it obvious which section belongs to which group.

Aborting Conflicts
------------------

If You Get Stuck
~~~~~~~~~~~~~~~~

**During rebase:**

.. code-block:: bash

   # Abort rebase, return to state before rebase started
   git rebase --abort

**During merge:**

.. code-block:: bash

   # Abort merge, return to state before merge started
   git merge --abort

.. warning::
   Aborting throws away your conflict resolution work!

Starting Over
~~~~~~~~~~~~~

.. code-block:: bash

   # If you want to start fresh:
   git rebase --abort  # or git merge --abort
   
   # Reset to your last pushed commit
   git fetch origin
   git reset --hard origin/feature/group-1-smoothing

Testing After Resolution
-------------------------

Always test after resolving conflicts:

.. code-block:: bash

   # Run your code
   python src/run_analysis.py
   
   # Run tests if available
   python -m pytest tests/
   
   # Check syntax
   python -m py_compile src/run_analysis.py

**Why:** Conflicts can introduce subtle bugs even if resolution looks correct.

Advanced Conflict Tools
-----------------------

Using Git Mergetool
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Launch visual merge tool
   git mergetool

**Configures tools like:**

- Meld (Linux)
- KDiff3 (cross-platform)
- P4Merge (cross-platform)
- VS Code (built-in)

Configuring VS Code as Mergetool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git config --global merge.tool vscode
   git config --global mergetool.vscode.cmd 'code --wait $MERGED'

**Then use:**

.. code-block:: bash

   git mergetool

Viewing Three-Way Diff
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # See base (common ancestor), theirs, and yours
   git show :1:src/run_analysis.py  # Base
   git show :2:src/run_analysis.py  # Ours (HEAD)
   git show :3:src/run_analysis.py  # Theirs (incoming)

Troubleshooting
---------------

Problem: "CONFLICT (modify/delete)"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** You modified a file that was deleted in main.

**Resolution:**

.. code-block:: bash

   # If file should be deleted:
   git rm src/old_file.py
   
   # If file should be kept:
   git add src/old_file.py

Problem: Too Many Conflicts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** 50+ conflicts in one file.

**Solution:**

.. code-block:: bash

   # Abort and reconsider approach
   git rebase --abort
   
   # Option 1: Break into smaller commits
   git rebase -i main  # Interactive rebase
   
   # Option 2: Ask instructor to review PR before merging

Problem: Conflicts in Binary Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Conflict in ``.nii.gz`` file (binary data).

**Resolution:**

.. code-block:: bash

   # Choose one version:
   git checkout --ours outputs/data.nii.gz   # Keep yours
   git checkout --theirs outputs/data.nii.gz # Keep theirs
   
   git add outputs/data.nii.gz

.. warning::
   Better solution: Don't commit large data files! Add to ``.gitignore``.

Real Workshop Scenario
----------------------

Intentional Conflict Exercise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The instructor will create an intentional conflict to teach resolution:

**Instructor's change to main:**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       ...
       img = self.load_data(subject_id)
       
       print("Starting preprocessing pipeline...")  # NEW LINE
       
       img_stripped = self.skull_strip(img)

**Your Group 1 branch:**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       ...
       img = self.load_data(subject_id)
       
       img_smoothed = self.smooth_image(img, fwhm=6.0)  # YOUR LINE

**When you rebase:**

.. code-block:: python

   <<<<<<< HEAD
       print("Starting preprocessing pipeline...")
       
       img_stripped = self.skull_strip(img)
   =======
       img_smoothed = self.smooth_image(img, fwhm=6.0)
   >>>>>>> your-commit

**Correct resolution:**

.. code-block:: python

   def run_full_pipeline(self, subject_id):
       ...
       img = self.load_data(subject_id)
       
       print("Starting preprocessing pipeline...")
       
       img_stripped = self.skull_strip(img)
       img_smoothed = self.smooth_image(img_stripped, fwhm=6.0)

Best Practices Summary
----------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Do ✅
     - Don't ❌
   * - Read conflict carefully before resolving
     - Blindly accept one side
   * - Test after resolving
     - Assume it works
   * - Keep both changes when possible
     - Delete others' work
   * - Ask for help if unsure
     - Guess and hope for the best
   * - Rebase frequently to minimize conflicts
     - Wait until the end to sync
   * - Delete conflict markers completely
     - Leave ``<<<<<<<`` in the file
   * - Consider logical order of operations
     - Just mash code together

Further Reading
---------------

- `Git Merge Conflicts <https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts>`_
- `Resolving Merge Conflicts <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line>`_
- `VS Code Merge Conflicts <https://code.visualstudio.com/docs/sourcecontrol/overview#_merge-conflicts>`_