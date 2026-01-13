from nilearn import plotting
import matplotlib.pyplot as plt
import nibabel as nib


# Load outputs
img = nib.load("outputs/brain.nii.gz")
mask = nib.load("outputs/brain_mask.nii.gz")

# Create comparison figure
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Original with mask overlay
plotting.plot_roi(mask, bg_img=img, axes=axes[0],
                  title="Brain Mask Overlay", alpha=0.4)

# Brain extracted
plotting.plot_anat(img, axes=axes[1], title="Brain Extracted")

plt.tight_layout()
plt.savefig("outputs/skull_strip_qa.png", dpi=150)
print("Saved: outputs/skull_strip_qa.png")