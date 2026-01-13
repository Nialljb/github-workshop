# Collaborative Neuroimaging Workshop

A hands-on workshop teaching version control, collaborative development, and structural MRI processing using Git, GitHub, and modern neuroimaging tools.

## Overview

This workshop teaches neuroimaging researchers how to:

- Use VS Code Remote-SSH for HPC development
- Collaborate using Git branches and Pull Requests
- Build modular structural MRI processing pipelines
- Apply professional software development practices

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Nialljb/github-workshop.git
cd neuroimaging-workshop
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Test Installation
```bash
python -c "from nilearn import datasets; print('✓ Installation successful!')"
```

### 5. Run Example
```bash
python src/run_analysis.py
```

## Dataset

We'll use the **Haxby Dataset** - a classic visual object recognition fMRI dataset
that includes both anatomical and functional data.

- **No manual download required** - automatically fetched via nilearn
- **Format**: NIfTI T1-weighted anatomical + BOLD functional images
- **Subjects**: 3 subjects (perfect for 3-4 workshop groups)
- **Anatomical**: 124×256×256 voxels at ~1mm resolution
- **Functional**: 40×64×64×1452 timepoints (visual task data)
- **Extras**: Pre-computed ROI masks for visual cortex regions

**Citation:**
```
Haxby, J.V., Gobbini, M.I., Furey, M.L., Ishai, A., Schouten, J.L.,
   and Pietrini, P. (2001). Distributed and overlapping representations
   of faces and objects in ventral temporal cortex. Science 293, 2425-2430.
```

## Processing Pipeline

The complete pipeline includes:

1. **Brain Extraction** (Group 1) - Remove skull and non-brain tissue
2. **Bias Field Correction** (Group 2) - Correct intensity inhomogeneities
3. **Tissue Segmentation** (Group 3) - Classify gray matter, white matter, CSF
4. **Visualization** (Group 4) - Create diagnostic figures

## Documentation

Full documentation available at: [\[Read the Docs link\]](https://nialljb.github.io/github-workshop/challenge/overview.html)

Or build locally:
```bash
cd docs
make setup           # First time only
source venv/bin/activate
make html
make show
```

## Workshop Structure
```
neuroimaging-workshop/
├── src/
│   ├── __init__.py
│   └── run_analysis.py          # Main pipeline
├── outputs/                      # Generated results (git-ignored)
├── tests/                        # Unit tests
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Group Tasks

| Group | Task | Method |
|-------|------|--------|
| 🔵 Group 1 | Skull Stripping | `skull_strip()` |
| 🟢 Group 2 | Bias Correction | `bias_field_correction()` |
| 🟡 Group 3 | Tissue Segmentation | `tissue_segmentation()` |
| 🟣 Group 4 | Visualization | `create_visualization()` |

## Example Usage
```python
from src.run_analysis import StructuralPipeline

# Initialize pipeline
pipeline = StructuralPipeline(output_dir="./outputs")

# Process a subject
result = pipeline.run_full_pipeline(subject_idx=0)

# Outputs saved to ./outputs/
```

## Requirements

- Python 3.8+
- 8GB+ RAM
- ~2GB disk space for dataset

## HPC Usage

For running on HPC clusters:
```bash
# Load modules
module load python/3.9

# Submit job
sbatch scripts/run_pipeline.sh
```

See `docs/` for detailed HPC setup instructions.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/group-X-taskname`)
3. Make your changes
4. Commit (`git commit -m "Add feature"`)
5. Push to your fork (`git push origin feature/group-X-taskname`)
6. Create a Pull Request

## Troubleshooting

**Common Issues:**

- **Module not found**: Ensure virtual environment is activated
- **Data download fails**: Check internet connection, clear nilearn cache
- **Out of memory**: Process one subject at a time
- **SimpleITK import error**: Reinstall with `pip install --force-reinstall SimpleITK`

See [Troubleshooting Guide](docs/source/reference/troubleshooting.rst) for more help.

## Resources

- [Workshop Documentation](docs/)
- [Git Tutorial](https://learngitbranching.js.org/)
- [Nilearn Documentation](https://nilearn.github.io/)
- [VS Code Remote-SSH](https://code.visualstudio.com/docs/remote/ssh)

## License

MIT License - see LICENSE file for details.

## Citation

If you use this workshop material:
```
Collaborative Neuroimaging Workshop Materials
https://github.com/Nialljb/github-workshop
```

## Contact

- **Instructor**: [Niall Bourke]
- **Email**: [niall.bourke@kcl.ac.uk]
- **Issues**: [GitHub Issues](https://github.com/Nialljb/github-workshop/issues)

---

**Happy collaborating! 🧠**