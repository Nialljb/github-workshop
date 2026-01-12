Git Fundamentals
================

The Problem: Version Control Chaos
-----------------------------------

The Old Way (Don't Do This!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   analysis_v1.py
   analysis_v2.py
   analysis_v2_final.py
   analysis_v2_final_REALLY.py
   analysis_v2_final_REALLY_submitted.py

**Problems:**

- Which version was submitted?
- What changed between v2 and v2_final?
- Can't collaborate without emailing files
- No way to recover if you break something

The Git Way
~~~~~~~~~~~

.. code-block:: text

   analysis.py  (One file)

**Git tracks:**

- Every version of every file
- Who made each change and when
- Why changes were made (commit messages)
- Multiple people working simultaneously
- Full history with ability to revert

Core Concepts
-------------

Repository (Repo)
~~~~~~~~~~~~~~~~~

A repository is a project folder with version control containing:

- Your code files (``*.py``, ``*.txt``, etc.)
- A hidden ``.git/`` directory (Git's database)
- Optional: ``.gitignore`` (tells Git which files to ignore)

Commit
~~~~~~

A commit is a **snapshot** of your entire project at one point in time.

Each commit includes:

- All file contents at that moment
- Your name and email
- Timestamp
- Commit message (description of changes)
- Unique ID (SHA hash like ``a3f2b9c``)

**Think of commits like save points in a video game.**

Example commit history:

.. code-block:: text

   * a3f2b9c (HEAD -> main) Fix bug in smoothing kernel size
   * 8d4e1fa Add skull stripping function
   * 2c9b7e3 Initial pipeline skeleton

Branch
~~~~~~

A branch is a **parallel version** of your code. The default branch is ``main``.

**Branches let multiple people work simultaneously without interfering.**

.. code-block:: text

   main:      A---B---C---F---G     (stable code)
                   \       /
   feature:         D---E            (experimental)

Pull Request (PR)
~~~~~~~~~~~~~~~~~

A Pull Request is a **request to merge** your branch into another branch.

PRs are a GitHub feature (not part of Git) that adds:

- Code review (others comment on your code)
- Discussion thread
- Automated testing (CI/CD)
- Approval workflow

Merge
~~~~~

Merging combines two branches together. Git automatically figures out how to 
combine changes, **unless** both branches modified the same lines (merge conflict).

Essential Commands
------------------

Checking Status
~~~~~~~~~~~~~~~

.. code-block:: bash

   git status

This shows:

- Which branch you're on
- Which files have changed
- Which files are staged for commit
- Which files are untracked

**Run this command frequently!**

Example output:

.. code-block:: text

   On branch feature/group-1-smoothing
   Changes not staged for commit:
     modified:   src/run_analysis.py
   
   Untracked files:
     outputs/smoothed.nii.gz

Creating and Switching Branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create new branch and switch to it
   git checkout -b feature/group-1-smoothing

This is equivalent to:

.. code-block:: bash

   git branch feature/group-1-smoothing    # Create
   git checkout feature/group-1-smoothing  # Switch

Branch naming conventions:

.. code-block:: text

   feature/description    # New functionality
   bugfix/description     # Fix a bug
   docs/description       # Documentation
   refactor/description   # Code cleanup

Staging Changes
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Stage specific file
   git add src/run_analysis.py
   
   # Stage all changed files
   git add .
   
   # Stage all Python files
   git add *.py

Why stage files?
^^^^^^^^^^^^^^^^

Git has a two-step commit process:

1. **Stage** (``git add``): "These are the changes I want to include"
2. **Commit** (``git commit``): "Save these staged changes permanently"

This lets you commit only **some** changes, not all of them.

Committing Changes
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git commit -m "Add smoothing function with configurable FWHM"

Good commit messages:

.. code-block:: text

   ✓ "Add smoothing function with configurable FWHM"
   ✓ "Fix bug: skull stripping failed on 2D images"
   ✓ "Refactor QA code to use numpy vectorization"

Bad commit messages:

.. code-block:: text

   ✗ "update"
   ✗ "asdf"
   ✗ "fixes"

Multi-line commit message:

.. code-block:: bash

   git commit

This opens VS Code editor:

.. code-block:: text

   Add smoothing function for fMRI preprocessing
   
   - Implemented Gaussian smoothing using nilearn
   - FWHM parameter defaults to 6mm but is configurable
   - Saves smoothed image to outputs directory
   - Tested with subject 01
   
   Closes #12

Pushing to Remote
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/group-1-smoothing

Understanding remotes:

- **origin**: Your fork on GitHub (your copy)
- **upstream**: Original repository (shared central repo)

.. code-block:: text

   origin:    github.com/YOUR_USERNAME/neuroimaging-workshop
   upstream:  github.com/INSTRUCTOR/neuroimaging-workshop

You push to ``origin`` (your fork), then create PR to ``upstream``.

Pulling Latest Changes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git pull upstream main

Why pull from upstream?
^^^^^^^^^^^^^^^^^^^^^^^

While you work on your branch, **other people's PRs are being merged**. 
You need to get those changes to keep your code up-to-date.

Branching Strategy
------------------

For this workshop:

.. code-block:: text

   main (protected)
   ├── feature/group-1-smoothing
   ├── feature/group-2-skullstrip
   ├── feature/group-3-qa
   └── feature/group-4-visualization

Workflow:

1. Everyone starts from the same ``main`` branch
2. Each group creates a **feature branch** for their task
3. Groups work independently on their branches
4. Groups submit **Pull Requests** to merge back to ``main``
5. Instructor reviews and merges PRs one at a time
6. Other groups **pull latest changes** and rebase if needed