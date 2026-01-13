# Neuroimaging Datasets Available for Workshop

This document summarizes the neuroimaging datasets available through nilearn for the collaborative neuroimaging workshop.

## Dataset Summary

### ✅ Recommended: Haxby Dataset
**Best choice for multi-subject anatomical + functional analysis**

- **Subjects**: 6 available (we use 3)
- **Anatomical**: T1-weighted structural images (124×256×256 voxels, ~1mm resolution)
- **Functional**: BOLD fMRI during visual object recognition task (40×64×64×1452 timepoints)
- **Extras**: Pre-computed masks for visual cortex regions (faces, houses, etc.)
- **Use case**: Perfect for all workshop challenges - anatomical processing and functional analysis

**Download code:**
```python
from nilearn import datasets
dataset = datasets.fetch_haxby(subjects=[1, 2, 3], data_dir="data/")
```

### ✅ SPM Auditory Dataset  
**High-quality single subject for detailed examples**

- **Subjects**: 1
- **Anatomical**: T1-weighted (256×256×54 voxels, 1×1×3mm)
- **Functional**: BOLD fMRI during auditory task (64×64×64×84 timepoints)
- **Extras**: Event files with stimulus timing
- **Use case**: Instructor demonstrations, detailed walkthroughs

### ⚠️ Development fMRI Dataset
**Functional only - no anatomical data**

- **Subjects**: 155 (ages 3-39)
- **Data**: Pre-processed functional data only (already in MNI space)
- **Task**: Movie watching (Pixar films)
- **Limitation**: No raw anatomical scans available through nilearn
- **Use case**: Age prediction, large cohort analysis (functional only)

### ⚠️ ADHD Dataset
**Resting-state functional only**

- **Subjects**: Multiple available
- **Data**: Resting-state fMRI only
- **Limitation**: No anatomical data
- **Use case**: Resting-state connectivity analysis

## Workshop Data Structure

After downloading, your data directory will contain:

```
data/
├── haxby2001/                    # Main dataset for workshop
│   ├── subj1/
│   │   ├── anat.nii.gz          # Anatomical T1
│   │   ├── bold.nii.gz          # Functional BOLD
│   │   └── masks/               # ROI masks
│   ├── subj2/
│   └── subj3/
├── spm_auditory/                 # Single subject for demos
│   └── sub-01/
│       ├── anat/sub-01_T1w.nii  # High-quality T1
│       └── func/sub-01_bold.nii # Functional data
└── development_fmri/             # Functional only
    └── (155 preprocessed files)
```

## Group Assignment Recommendation

**For anatomical challenges (skull stripping, bias correction, segmentation, visualization):**

- **Group 1**: Haxby Subject 1 (`subj1/anat.nii.gz`)
- **Group 2**: Haxby Subject 2 (`subj2/anat.nii.gz`) 
- **Group 3**: Haxby Subject 3 (`subj3/anat.nii.gz`)
- **Group 4**: SPM Auditory Subject (`sub-01_T1w.nii`)

**For functional challenges:**
- Use corresponding functional data from same subjects
- Development fMRI dataset for large cohort examples

## Data Characteristics

| Dataset | Anat Resolution | Func Resolution | Subjects | Task |
|---------|----------------|-----------------|----------|------|
| Haxby | 1.2×0.94×0.94mm | 3.5×3.75×3.75mm | 3/6 | Visual objects |
| SPM Auditory | 1×1×3mm | 3×3×3mm | 1 | Auditory stimuli |
| Development | N/A | 4×4×4mm | 155 | Movie watching |
| ADHD | N/A | 3×3×3mm | Multiple | Resting state |

## Quick Start

```python
from nilearn import datasets
import nibabel as nib
from pathlib import Path

# Set up data directory
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Download main dataset for workshop
dataset = datasets.fetch_haxby(subjects=[1, 2, 3], data_dir=str(data_dir))

# Check what was downloaded
print(f"Anatomical files: {len(dataset.anat)}")
print(f"Functional files: {len(dataset.func)}")

# Load first subject's data
anat_img = nib.load(dataset.anat[0])
func_img = nib.load(dataset.func[0])

print(f"Anatomical shape: {anat_img.shape}")
print(f"Functional shape: {func_img.shape}")
```