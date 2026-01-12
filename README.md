# Neuroimaging Workshop: Collaborative fMRI Pipeline

Welcome to the **Collaborative Neuroimaging Workshop**! This repository contains a modular fMRI preprocessing pipeline that you'll build together using Git, GitHub, and VS Code on HPC.

## 🎯 Learning Objectives

- Master VS Code Remote-SSH for HPC development
- Implement collaborative Git workflows (branch, PR, merge)
- Build modular neuroimaging analysis code
- Practice code review and conflict resolution

## 📁 Repository Structure
```
neuroimaging-workshop/
├── README.md              # You are here
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py
│   └── run_analysis.py   # Main pipeline (you'll edit this!)
├── outputs/              # Generated preprocessing outputs
└── tests/                # Unit tests (bonus!)
```

## 🚀 Quick Start

### 1. Fork This Repository
Click the "Fork" button (top right) to create your own copy.

### 2. Clone to HPC
```bash
git clone https://github.com/YOUR_USERNAME/neuroimaging-workshop.git
cd neuroimaging-workshop
```

### 3. Setup Environment
```bash
module load python/3.9
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Verify Data Access
```bash
ls /data/shared/workshop/bids_dataset/
# Should show: sub-01/ sub-02/ sub-03/ ...
```

## 👥 Group Tasks

### Group 1: Spatial Smoothing 🔵
**Branch**: `feature/group-1-smoothing`  
**Task**: Implement Gaussian smoothing using nilearn  
**Method**: `smooth_image(self, img, fwhm=6.0)`

### Group 2: Skull Stripping 🟢
**Branch**: `feature/group-2-skullstrip`  
**Task**: Remove non-brain tissue  
**Method**: `skull_strip(self, img)`

### Group 3: Quality Assurance 🟡
**Branch**: `feature/group-3-qa`  
**Task**: Calculate tSNR and detect outliers  
**Method**: `quality_assurance(self, img)`

### Group 4: Visualization 🟣
**Branch**: `feature/group-4-visualization`  
**Task**: Create diagnostic plots  
**Method**: `create_visualization(self, img, subject_id)`

## 🔄 Workflow

### Step 1: Create Your Branch
```bash
git checkout -b feature/group-X-TASKNAME
```

### Step 2: Implement Your Task
- Open `src/run_analysis.py`
- Find your group's section
- Implement the method
- Test with `python src/run_analysis.py`

### Step 3: Commit & Push
```bash
git add src/run_analysis.py
git commit -m "Add [functionality]: [description]"
git push origin feature/group-X-TASKNAME
```

### Step 4: Create Pull Request
1. Go to GitHub.com
2. Click "Compare & pull request"
3. Set base: `INSTRUCTOR/neuroimaging-workshop` (main branch)
4. Fill out PR template
5. Request review

### Step 5: Code Review
- Address reviewer feedback
- Make requested changes
- Push updates (PR auto-updates)

### Step 6: Merge!
Once approved, instructor will merge your PR.

## 📋 Pull Request Template

When creating your PR, include:
```markdown
## Group X: [Task Name]

### Summary
[What does this PR implement?]

### Testing
- [ ] Tested with subject 01
- [ ] Outputs saved correctly
- [ ] No errors in console

### Dependencies
[Does this depend on other PRs?]
```

## ⚠️ Important Rules

### DO ✅
- Create a new branch for your task
- Write descriptive commit messages
- Test your code before pushing
- Ask for help if stuck
- Comment your code
- Use relative paths (`self.output_dir / "file.nii.gz"`)

### DON'T ❌
- Push directly to `main` branch
- Commit large data files
- Use absolute paths (`/home/yourname/...`)
- Delete others' code
- Force push to `main`
- Include passwords or tokens

## 🔧 Dependencies
```txt
nibabel>=5.0.0
nilearn>=0.10.0
numpy>=1.24.0
matplotlib>=3.7.0
scipy>=1.10.0
```

## 📚 Helpful Resources

- [Nilearn Documentation](https://nilearn.github.io/)
- [Git Branching Guide](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [BIDS Specification](https://bids-specification.readthedocs.io/)
- [VS Code Remote SSH](https://code.visualstudio.com/docs/remote/ssh)

## 🆘 Troubleshooting

### "Permission denied" when accessing data
```bash
# Check you're in the correct group
groups
# Contact instructor if not in 'workshop_users'
```

### "Module not found" errors
```bash
# Activate virtual environment
source venv/bin/activate
# Reinstall packages
pip install -r requirements.txt
```

### Git conflicts
```bash
# Fetch latest changes
git fetch upstream
git rebase upstream/main
# Resolve conflicts in VS Code
# Then: git rebase --continue
```

## 👨‍🏫 Instructor

**[Your Name]**  
Email: your.email@institution.edu  
Office Hours: [Time/Location]

## 📝 License

This workshop material is licensed under MIT License.

---

**Happy collaborating! 🧠**# github-workshop
