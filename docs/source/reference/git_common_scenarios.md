# Common Git Scenarios

This guide walks through common problems developers face and how Git helps solve them.

## Scenario 1: Accidental File Deletion

### The Problem

You're working on a project and accidentally delete an important file. Without version control, this file would be lost forever unless you have a separate backup.

```bash
# Oops! Accidentally deleted the file
rm important_config.py
```

### The Solution

Git tracks all your files in commits, so you can restore deleted files easily:

```bash
# Check the status to see what happened
git status

# Restore the file from the last commit
git checkout HEAD important_config.py

# Or restore it from a specific commit
git checkout abc123 important_config.py
```

**Key Takeaway:** Git acts as a time machine for your files. Every commit is a snapshot you can return to.

---

## Scenario 2: Breaking Changes

### The Problem

You've been working for hours and made changes across multiple files. Now your code doesn't work, and you can't remember everything you changed.

```python
# Original working code
def calculate_total(items):
    return sum(items)

# After "improvements" - now broken
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity  # But items are just numbers!
    return total
```

### The Solution

Use Git to see exactly what changed and revert if needed:

```bash
# See all changes since last commit
git diff

# See changes in a specific file
git diff calculate.py

# Discard all changes and go back to last commit
git reset --hard HEAD

# Or just discard changes in one file
git checkout -- calculate.py
```

**Key Takeaway:** Git lets you experiment fearlessly because you can always go back.

---

## Scenario 3: Collaboration Conflicts

### The Problem

You and your teammate both edited the same file. When you try to combine your work, Git finds conflicting changes in the same location.

```python
# Your version
def greet(name):
    return f"Hello, {name}!"

# Your teammate's version  
def greet(name):
    return f"Hi there, {name}!"
```

### The Solution

Git marks conflicts clearly and lets you decide how to resolve them:

```bash
# Try to merge your teammate's changes
git pull origin main

# Git shows a conflict
# CONFLICT (content): Merge conflict in greetings.py
```

The file will show both versions:

```python
def greet(name):
<<<<<<< HEAD
    return f"Hello, {name}!"
=======
    return f"Hi there, {name}!"
>>>>>>> teammate-branch
```

You decide which to keep (or combine them):

```python
def greet(name):
    return f"Hello there, {name}!"
```

Then complete the merge:

```bash
# Stage the resolved file
git add greetings.py

# Complete the merge
git commit -m "Merge greeting changes, combined both versions"
```

**Key Takeaway:** Git makes collaboration safe by showing you exactly where conflicts occur.

---

## Scenario 4: Experimental Features

### The Problem

You want to try adding a new feature, but you don't want to risk breaking the working code. You need to experiment without affecting the stable version.

### The Solution

Create a branch for experimental work:

```bash
# Create and switch to a new branch
git checkout -b experimental-feature

# Now you can make changes freely
# Edit files, test, experiment...

# If it works, merge it back
git checkout main
git merge experimental-feature

# If it doesn't work, just delete the branch
git branch -d experimental-feature
```

**Key Takeaway:** Branches let you work on multiple versions of your code simultaneously without interference.

---

## Scenario 5: Finding When Bugs Were Introduced

### The Problem

Your tests are failing, but they worked last week. You need to find out which commit introduced the bug.

### The Solution

Use Git's history to investigate:

```bash
# See the commit history
git log --oneline

# Look at a specific file's history
git log --oneline myfile.py

# See what changed in a specific commit
git show abc123

# Or use bisect to automatically find the bad commit
git bisect start
git bisect bad  # Current version is bad
git bisect good abc123  # This old commit was good
# Git will check out middle commits for you to test
# Mark each as good or bad until it finds the culprit
```

**Key Takeaway:** Git's history lets you track down exactly when and how bugs were introduced.

---

## Quick Reference

| Problem | Git Command |
|---------|-------------|
| Undo changes to a file | `git checkout -- filename` |
| See what changed | `git diff` |
| Go back to previous commit | `git reset --hard HEAD~1` |
| Create experimental branch | `git checkout -b branch-name` |
| Restore deleted file | `git checkout HEAD filename` |
| View history | `git log --oneline` |
| Resolve merge conflict | Edit file, `git add`, `git commit` |
