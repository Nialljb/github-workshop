from nilearn import plotting
import matplotlib.pyplot as plt
import nibabel as nib

# Load data
img = nib.load("outputs/corrected.nii.gz")
gm = nib.load("outputs/gm_prob.nii.gz")
wm = nib.load("outputs/wm_prob.nii.gz")
csf = nib.load("outputs/csf_prob.nii.gz")

# Create comparison figure
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Background image
plotting.plot_anat(img, axes=axes[0, 0], title="Original")

# Tissue overlays
plotting.plot_roi(gm, bg_img=img, axes=axes[0, 1],
                  title="Gray Matter", colorbar=True, cmap='Reds')
plotting.plot_roi(wm, bg_img=img, axes=axes[1, 0],
                  title="White Matter", colorbar=True, cmap='Blues')
plotting.plot_roi(csf, bg_img=img, axes=axes[1, 1],
                  title="CSF", colorbar=True, cmap='Greens')

plt.tight_layout()
plt.savefig("outputs/segmentation_qa.png", dpi=150)
print("Saved: outputs/segmentation_qa.png")