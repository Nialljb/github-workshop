Git Branching Workflow
======================

Overview
--------

This page explains how to use Git branches effectively for collaborative 
neuroimaging development.

What is a Branch?
-----------------

A branch is a parallel version of your code. Think of it as a separate timeline 
where you can experiment without affecting the main codebase.

.. code-block:: text

   main:      A---B---C---F---G     (stable, tested code)
                   \       /
   feature:         D---E            (experimental work)

**Benefits of branching:**

- Work on features without breaking main code
- Multiple people work simultaneously
- Easy to abandon failed experiments
- Clear history of what changed when

Creating Your Branch
--------------------

Step 1: Start from Latest Main
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always create branches from the latest version of ``main``:

.. code-block:: bash

   # Make sure you're on main
   git checkout main
   
   # Get latest changes from instructor's repo
   git fetch upstream
   git merge upstream/main
   
   # Push to keep your fork in sync
   git push origin main

.. warning::
   **Never create branches from outdated main!** This causes merge conflicts later.

Step 2: Create Feature Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create and switch to new branch
   git checkout -b feature/group-1-smoothing
   
   # Verify you're on the new branch
   git branch
   # Output: * feature/group-1-smoothing

**Branch naming conventions:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Prefix
     - Use Case
   * - ``feature/``
     - New functionality (e.g., ``feature/group-1-smoothing``)
   * - ``bugfix/``
     - Bug fixes (e.g., ``bugfix/skull-strip-error``)
   * - ``docs/``
     - Documentation updates (e.g., ``docs/add-examples``)
   * - ``refactor/``
     - Code cleanup (e.g., ``refactor/simplify-qa``)

.. tip::
   Use descriptive names: ``feature/group-1-smoothing`` is better than ``feature/task1``

Step 3: Verify Branch Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Show current branch
   git branch
   
   # Show all branches (local and remote)
   git branch -a
   
   # Show branch relationships
   git log --oneline --graph --all -10

Working on Your Branch
----------------------

Making Changes
~~~~~~~~~~~~~~

1. **Edit files** in VS Code
2. **Test your changes** frequently
3. **Commit often** (every logical unit of work)

.. code-block:: bash

   # Check what changed
   git status
   git diff
   
   # Stage changes
   git add src/run_analysis.py
   
   # Commit
   git commit -m "Add smoothing function skeleton"

.. tip::
   **Commit early, commit often.** Small commits are easier to review and debug.

Commit Message Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Good commit messages follow this structure:

.. code-block:: text

   Short summary (50 chars or less)
   
   More detailed explanation if needed. Wrap at 72 characters.
   Explain what changed and why, not how.
   
   - Use bullet points for multiple changes
   - Reference issues: Closes #123
   - Add context for future readers

**Examples:**

.. code-block:: text

   ✅ GOOD:
   Add smoothing function with configurable FWHM
   
   Implements Gaussian smoothing using nilearn.image.smooth_img().
   FWHM parameter defaults to 6mm but can be configured.
   Saves output to outputs/ directory for inspection.

.. code-block:: text

   ❌ BAD:
   updated stuff
   
   fixed things
   
   changes

Pushing Your Branch
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Push to YOUR fork (origin)
   git push origin feature/group-1-smoothing
   
   # If this is the first push, set upstream
   git push --set-upstream origin feature/group-1-smoothing

.. important::
   Always push to ``origin`` (your fork), never to ``upstream`` (instructor's repo).

Keeping Your Branch Updated
----------------------------

Why Update Your Branch?
~~~~~~~~~~~~~~~~~~~~~~~

While you work, other people's PRs get merged into ``main``. Your branch becomes 
outdated, increasing the risk of merge conflicts.

.. code-block:: text

   When you started:
   main:          A---B
   your branch:   A---B---C---D
   
   After Group 2's PR merges:
   main:          A---B---E---F  (you're missing E and F!)
   your branch:   A---B---C---D

Method 1: Rebase (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is rebase?**

Rebase replays your commits on top of the latest ``main``:

.. code-block:: text

   Before rebase:
   main:          A---B---E---F
   your branch:   A---B---C---D
   
   After rebase:
   main:          A---B---E---F
   your branch:   A---B---E---F---C'---D'  (your commits moved)

**Steps:**

.. code-block:: bash

   # 1. Fetch latest changes
   git fetch upstream
   
   # 2. Update your local main
   git checkout main
   git merge upstream/main
   
   # 3. Switch to your feature branch
   git checkout feature/group-1-smoothing
   
   # 4. Rebase onto latest main
   git rebase main

**If conflicts occur:**

.. code-block:: bash

   # Git stops and shows conflicts
   # Edit conflicted files in VS Code
   # Look for markers: <<<<<<<, =======, >>>>>>>
   
   # After resolving conflicts:
   git add <conflicted-file>
   git rebase --continue
   
   # If you want to abort:
   git rebase --abort

**Push rebased branch:**

.. code-block:: bash

   # Rebase rewrites history, so you need --force
   git push origin feature/group-1-smoothing --force

.. warning::
   **Only use** ``--force`` **on your feature branches, never on** ``main``!

Method 2: Merge (Alternative)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**What is merge?**

Merge creates a new commit that combines two branches:

.. code-block:: text

   Before merge:
   main:          A---B---E---F
   your branch:   A---B---C---D
   
   After merge:
   main:          A---B---E---F
   your branch:   A---B---C---D---G  (merge commit)
                           \       /
                            ---E---F

**Steps:**

.. code-block:: bash

   # 1-3. Same as rebase
   
   # 4. Merge instead of rebase
   git merge main
   
   # Resolve conflicts if any
   git add <conflicted-file>
   git commit
   
   # Push (no --force needed)
   git push origin feature/group-1-smoothing

**Rebase vs Merge:**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Rebase
     - Merge
   * - History
     - Linear, clean
     - Shows true history with merge commits
   * - Conflicts
     - Resolve per commit
     - Resolve once
   * - Force push
     - Required
     - Not needed
   * - Best for
     - Feature branches
     - Long-lived branches

.. tip::
   **For this workshop, use rebase** to keep history clean and easy to follow.

Viewing Branch History
----------------------

Useful Commands
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Show commits on current branch
   git log --oneline
   
   # Show graphical history
   git log --oneline --graph --all
   
   # Compare with main
   git log main..feature/group-1-smoothing
   
   # Show what changed in each commit
   git log -p
   
   # Show files changed
   git log --stat

**Example output:**

.. code-block:: text

   * d4f2a9c (HEAD -> feature/group-1-smoothing) Add smoothing tests
   * c3e1b8f Add smoothing implementation
   * a2d9c7f Add smoothing function skeleton
   * b1e8f6a (upstream/main, origin/main, main) Initial pipeline skeleton

VS Code Git Integration
~~~~~~~~~~~~~~~~~~~~~~~~

**Visual branch view:**

1. Click Source Control icon (``Ctrl+Shift+G``)
2. Click three dots (``...``) → View → Show Graph

**Benefits:**

- See commits visually
- Click commits to see changes
- Right-click for actions (cherry-pick, revert, etc.)

Switching Between Branches
---------------------------

.. code-block:: bash

   # Switch to main
   git checkout main
   
   # Switch to feature branch
   git checkout feature/group-1-smoothing
   
   # Create and switch to new branch
   git checkout -b feature/new-task

.. warning::
   **Uncommitted changes warning:**
   
   If you have uncommitted changes, Git won't let you switch branches:
   
   .. code-block:: text
   
      error: Your local changes to the following files would be overwritten
   
   **Solutions:**
   
   1. Commit your changes: ``git commit -am "WIP: save progress"``
   2. Stash your changes: ``git stash`` (retrieve later with ``git stash pop``)
   3. Discard your changes: ``git checkout -- <file>`` (careful!)

Deleting Branches
-----------------

After Your PR Merges
~~~~~~~~~~~~~~~~~~~~

Once your PR is merged, you can delete the feature branch:

.. code-block:: bash

   # Delete local branch
   git branch -d feature/group-1-smoothing
   
   # Delete remote branch (on your fork)
   git push origin --delete feature/group-1-smoothing

.. tip::
   GitHub offers a "Delete branch" button after merging PRs.

If You Need to Abandon a Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Force delete (even if not merged)
   git branch -D feature/bad-idea
   
   # Delete from remote
   git push origin --delete feature/bad-idea

Common Branching Scenarios
---------------------------

Scenario 1: I Made Changes on Main by Mistake
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # You're on main with uncommitted changes
   git status
   # Output: Changes not staged for commit
   
   # Create branch from current state
   git checkout -b feature/group-1-smoothing
   
   # Your changes are now on the feature branch!
   git add .
   git commit -m "Add smoothing function"

Scenario 2: I Committed to Main Instead of a Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # You're on main with commits that should be on a branch
   git log  # See your commits
   
   # Create branch from current state
   git branch feature/group-1-smoothing
   
   # Reset main to match upstream
   git fetch upstream
   git reset --hard upstream/main
   
   # Switch to your feature branch
   git checkout feature/group-1-smoothing
   # Your commits are now safely on the feature branch

Scenario 3: I Want to Try Two Different Approaches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create two branches from main
   git checkout main
   git checkout -b feature/approach-1
   # ... work on approach 1 ...
   
   git checkout main
   git checkout -b feature/approach-2
   # ... work on approach 2 ...
   
   # Later, delete the approach you don't want
   git branch -D feature/approach-1

Scenario 4: Multiple People Working on Same Feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Person A creates branch
   git checkout -b feature/group-1-smoothing
   git push origin feature/group-1-smoothing
   
   # Person B clones and checks out the same branch
   git fetch origin
   git checkout feature/group-1-smoothing
   
   # Both work and push regularly
   git pull origin feature/group-1-smoothing  # Get teammate's changes
   git push origin feature/group-1-smoothing   # Share your changes

Branch Protection
-----------------

The instructor has protected the ``main`` branch with these rules:

.. code-block:: yaml

   Branch protection rules:
   - Require pull request reviews before merging
   - Require status checks to pass
   - Require branches to be up to date before merging
   - Do not allow bypassing the above settings

**What this means for you:**

- ❌ Cannot push directly to ``main``
- ✅ Must create PR from feature branch
- ✅ PR must be reviewed before merging
- ✅ Branch must be updated with latest main

Best Practices Summary
----------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Do ✅
     - Don't ❌
   * - Create branches from latest main
     - Create branches from outdated main
   * - Use descriptive branch names
     - Use vague names (``my-branch``)
   * - Commit frequently with good messages
     - Make one giant commit at the end
   * - Keep branches focused on one feature
     - Mix multiple unrelated changes
   * - Update branch regularly (rebase)
     - Let branch get far behind main
   * - Delete branches after merging
     - Let old branches accumulate
   * - Push to origin (your fork)
     - Push to upstream (instructor's repo)

Troubleshooting
---------------

Problem: "fatal: not a git repository"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** You're not in the repository directory.

.. code-block:: bash

   cd ~/workshop/neuroimaging-workshop

Problem: "error: pathspec 'feature/...' did not match any file(s)"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Branch doesn't exist. Create it:

.. code-block:: bash

   git checkout -b feature/group-1-smoothing

Problem: Can't switch branches (uncommitted changes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Commit or stash changes:

.. code-block:: bash

   # Option 1: Commit
   git commit -am "WIP: save progress"
   
   # Option 2: Stash (temporary save)
   git stash
   git checkout other-branch
   git stash pop  # Restore changes later

Problem: Accidentally deleted important branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solution:** Use reflog to recover:

.. code-block:: bash

   # Find deleted branch commit
   git reflog
   
   # Recreate branch at that commit
   git checkout -b feature/recovered <commit-hash>

Further Reading
---------------

- `Git Branching Documentation <https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>`_
- `Interactive Git Tutorial <https://learngitbranching.js.org/>`_
- `Atlassian Git Branching <https://www.atlassian.com/git/tutorials/using-branches>`_