from nilearn import plotting
import matplotlib.pyplot as plt

import nibabel as nib
# Load data
original = nib.load("outputs/brain.nii.gz")
corrected = nib.load("outputs/corrected.nii.gz")
bias_field = nib.load("outputs/bias_field.nii.gz")

# Create comparison figure
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

plotting.plot_anat(original, axes=axes[0], title="Original")
plotting.plot_anat(corrected, axes=axes[1], title="Bias Corrected")
plotting.plot_anat(bias_field, axes=axes[2], title="Bias Field",
                   cmap='coolwarm', vmin=0.8, vmax=1.2)

plt.tight_layout()
plt.savefig("outputs/bias_correction_qa.png", dpi=150)
print("Saved: outputs/bias_correction_qa.png")