Creating and Managing Pull Requests
====================================

What is a Pull Request?
-----------------------

A Pull Request (PR) is a request to merge your branch into another branch. 
It's called a "pull request" because you're asking the project maintainer to 
"pull" your changes.

PRs provide:

- Code review (others can comment)
- Discussion thread
- Automated testing (CI/CD)
- Approval workflow

Creating a Pull Request
-----------------------

Step 1: Navigate to GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~

After pushing your branch, GitHub shows a banner:

.. code-block:: text

   Your recently pushed branch: feature/group-1-smoothing
   [Compare & pull request]  ← Click this button

Alternatively:

1. Go to your fork: ``github.com/YOUR_USERNAME/neuroimaging-workshop``
2. Click "Pull requests" tab
3. Click "New pull request"

Step 2: Configure PR Target
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. danger::
   **Critical: Set the correct base repository!**
   
   **Default base:** YOUR_USERNAME/neuroimaging-workshop  
   **Correct base:** INSTRUCTOR_NAME/neuroimaging-workshop
   
   **You must change this!**

1. Click "base repository" dropdown
2. Select ``INSTRUCTOR_NAME/neuroimaging-workshop``
3. Ensure base branch is ``main``
4. Ensure compare branch is ``feature/group-1-smoothing``

Step 3: Fill Out PR Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Title:**

.. code-block:: text

   Group 1: Add spatial smoothing function

**Description:**

.. code-block:: markdown

   ## Summary
   Implements Gaussian spatial smoothing for fMRI preprocessing.
   
   ## Changes
   - Added `smooth_image()` method to `PreprocessingPipeline` class
   - Configurable FWHM parameter (default: 6mm)
   - Saves smoothed output to `outputs/` directory
   
   ## Testing
   - [x] Tested with subject 01
   - [x] Verified output file creation
   - [x] No errors or warnings
   
   ## Dependencies
   None - can be merged first

Step 4: Request Review
~~~~~~~~~~~~~~~~~~~~~~~

1. On right sidebar, click "Reviewers"
2. Select instructor username
3. Click "Create pull request"

Managing Concurrent PRs
-----------------------

The Challenge
~~~~~~~~~~~~~

All 4 groups work simultaneously and submit PRs around the same time. We can't 
merge all PRs at once because they modify the same file.

Merge Strategy: Sequential Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recommended merge order:

.. code-block:: text

   1. GROUP 2 (Skull Stripping) ← Merge FIRST
        ↓ (other groups rebase)
   2. GROUP 1 (Smoothing)        ← Merge SECOND
        ↓ (other groups rebase)
   3. GROUP 3 (QA)               ← Merge THIRD
        ↓ (other groups rebase)
   4. GROUP 4 (Visualization)    ← Merge LAST

Why this order?

- Group 2 first: Independent, no dependencies
- Group 1 second: Operates on skull-stripped data
- Group 3 third: QA runs on preprocessed data
- Group 4 last: Visualizes all previous outputs

Updating Your PR After Upstream Changes
----------------------------------------

After a PR merges, other groups must update their branches.

Option 1: Rebase (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What is rebase?

Rebase **replays** your commits on top of the latest ``main``:

.. code-block:: text

   Before rebase:
   main:          A---B---C (Group 2 merged)
   your branch:   A---B---D---E (your work)
   
   After rebase:
   main:          A---B---C
   your branch:   A---B---C---D'---E' (your work, updated)

Steps:

.. code-block:: bash

   # 1. Fetch latest changes
   git fetch upstream
   
   # 2. Switch to main
   git checkout main
   
   # 3. Merge upstream changes
   git merge upstream/main
   
   # 4. Switch to feature branch
   git checkout feature/group-1-smoothing
   
   # 5. Rebase onto updated main
   git rebase main
   
   # 6. Force push to update PR
   git push origin feature/group-1-smoothing --force

.. warning::
   Rebase rewrites history. Use ``--force`` only on YOUR feature branches, 
   NEVER on ``main``!

Option 2: Merge (Alternative)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Merge creates a new commit combining two branches:

.. code-block:: text

   Before merge:
   main:          A---B---C
   your branch:   A---B---D---E
   
   After merge:
   main:          A---B---C
   your branch:   A---B---D---E---F (merge commit)
                          \       /
                           ---C---

Steps:

.. code-block:: bash

   # 1-4. Same as rebase
   
   # 5. Merge instead of rebase
   git merge main
   
   # 6. Normal push (no --force)
   git push origin feature/group-1-smoothing

Instructor Communication
------------------------

After merging each PR, the instructor should announce:

.. code-block:: text

   Group 2's skull stripping PR has been merged! 🎉
   
   Groups 1, 3, 4: Please update your branches:
   
   git fetch upstream
   git checkout main
   git merge upstream/main
   git checkout feature/group-X-yourfeature
   git rebase main
   git push origin feature/group-X-yourfeature --force
   
   Merge order:
   ✅ Group 2 (Skull Stripping)
   ⏳ Group 1 (Smoothing) - reviewing now
   ⏳ Group 3 (QA) - in queue
   ⏳ Group 4 (Visualization) - in queue