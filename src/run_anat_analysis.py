"""
Collaborative Structural MRI Processing Pipeline
"""

import os
from pathlib import Path
import nibabel as nib
from nilearn import datasets, plotting, image
import numpy as np
import matplotlib.pyplot as plt


class StructuralPipeline:
    """Modular structural MRI processing pipeline"""

    def __init__(self, output_dir):
        """
        Initialize structural processing pipeline

        Parameters
        ----------
        output_dir : str or Path
            Path to save outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, subject_idx=0):
        """
        Load structural MRI data from local Haxby dataset

        Parameters
        ----------
        subject_idx : int
            Subject index (0-based, max 2 for 3 subjects)

        Returns
        -------
        img : Nifti1Image
            T1-weighted structural MRI image
        """
        print(f"Loading subject {subject_idx+1} from local Haxby dataset...")

        # Check if data exists, download if needed
        data_path = Path("data/haxby2001")
        subject_dirs = ["subj1", "subj2", "subj3"]

        if subject_idx >= len(subject_dirs):
            raise ValueError(f"Subject index {subject_idx} out of range. Max: {len(subject_dirs)-1}")

        img_path = data_path / subject_dirs[subject_idx] / "anat.nii.gz"

        # Auto-download if data doesn't exist
        if not img_path.exists():
            print("📥 Dataset not found locally. Downloading Haxby dataset...")
            self._download_dataset()

            # Check again after download
            if not img_path.exists():
                raise FileNotFoundError(f"Download failed. Data not found at {img_path}")

        img = nib.load(str(img_path))

        print(f"✓ Loaded anatomical data: {img.shape}")
        print(f"✓ Voxel size: {img.header.get_zooms()[:3]} mm")
        return img

    def _download_dataset(self):
        """Download Haxby dataset if not already present"""
        try:
            from nilearn import datasets
            print("Downloading Haxby dataset (3 subjects)...")
            dataset = datasets.fetch_haxby(subjects=[1, 2, 3], data_dir="data/")
            print("✅ Download complete!")
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print("Manual download option:")
            print("Run: python scripts/download_workshop_data.py")
            raise
        return img

    # GROUP 1: IMPLEMENT SKULL STRIPPING METHOD HERE
    def skull_strip(self, img):
        """
        Remove skull and non-brain tissue

        Extracts brain tissue by computing a binary brain mask and applying
        it to the structural image.

        Parameters
        ----------
        img : Nifti1Image
            Input T1-weighted structural image (3D)

        Returns
        -------
        brain_img : Nifti1Image
            Brain-only structural image

        Notes
        -----
        Uses nilearn's compute_brain_mask which employs intensity thresholding
        and morphological operations to identify brain voxels.
        """
        from nilearn import masking

        print("  → Computing brain mask...")

        # TODO: Compute brain mask
        mask = masking.compute_brain_mask(img)

        # TODO: Get mask data and calculate statistics
        mask_data = mask.get_fdata()
        n_brain_voxels = int(mask_data.sum())
        n_total_voxels = mask_data.size
        brain_fraction = n_brain_voxels / n_total_voxels
        print(f"    Brain voxels: {n_brain_voxels:,} / {n_total_voxels:,} ({brain_fraction*100:.1f}%)")

        # TODO: Apply mask to extract brain
        brain_data = img.get_fdata()
        brain_data[mask_data == 0] = 0  # Set non-brain to zero
        brain_img = nib.Nifti1Image(brain_data, img.affine, img.header)

        # TODO: Save outputs
        mask_file = self.output_dir / "brain_mask.nii.gz"
        brain_file = self.output_dir / "brain.nii.gz"
        nib.save(mask, mask_file)
        nib.save(brain_img, brain_file)
        print(f"    Saved: {mask_file.name}, {brain_file.name}")

        print("  ✓ Skull stripping complete")
        return brain_img

    # GROUP 2: IMPLEMENT BIAS FIELD CORRECTION METHOD HERE

    def bias_field_correction(self, img):
        """
        Correct intensity inhomogeneity (bias field)

        Uses N4 bias field correction algorithm to remove smooth intensity
        variations caused by scanner hardware.

        Parameters
        ----------
        img : Nifti1Image
            Input brain-extracted T1 image (3D)

        Returns
        -------
        corrected_img : Nifti1Image
            Bias-corrected T1 image

        Notes
        -----
        N4ITK (N4 bias field correction) is the standard algorithm for
        removing intensity inhomogeneities from MRI. Implementation uses
        SimpleITK library.

        References
        ----------
        Tustison et al. (2010) N4ITK: Improved N3 Bias Correction.
        IEEE Trans Med Imaging.
        """
        import SimpleITK as sitk

        print("  → Running N4 bias field correction...")

        # TODO: Convert nibabel to SimpleITK format
        data = img.get_fdata()
        sitk_img = sitk.GetImageFromArray(np.transpose(data, (2, 1, 0)))
        # Convert numpy types to Python floats for SimpleITK
        spacing = [float(x) for x in img.header.get_zooms()[:3]]
        sitk_img.SetSpacing(spacing)

        # TODO: Run N4 bias field correction
        corrector = sitk.N4BiasFieldCorrectionImageFilter()
        corrector.SetMaximumNumberOfIterations([50, 50, 50, 50])
        corrected_sitk = corrector.Execute(sitk_img)

        # TODO: Get bias field
        bias_field_sitk = sitk.Divide(sitk_img, corrected_sitk)

        # TODO: Convert back to nibabel format
        corrected_data = np.transpose(sitk.GetArrayFromImage(corrected_sitk), (2, 1, 0))
        bias_field_data = np.transpose(sitk.GetArrayFromImage(bias_field_sitk), (2, 1, 0))

        # Ensure proper data types and handle invalid values
        corrected_data = corrected_data.astype(np.float32)
        bias_field_data = bias_field_data.astype(np.float32)
        
        # Replace any invalid values
        corrected_data = np.nan_to_num(corrected_data, nan=0.0, posinf=0.0, neginf=0.0)
        bias_field_data = np.nan_to_num(bias_field_data, nan=1.0, posinf=1.0, neginf=1.0)

        corrected_img = nib.Nifti1Image(corrected_data, img.affine, img.header)
        bias_field_img = nib.Nifti1Image(bias_field_data, img.affine, img.header)

        # TODO: Print statistics
        orig_mean = data[data > 0].mean()
        corr_mean = corrected_data[corrected_data > 0].mean()
        print(f"    Mean intensity: {orig_mean:.1f} → {corr_mean:.1f}")

        # TODO: Save outputs
        corrected_file = self.output_dir / "corrected.nii.gz"
        bias_file = self.output_dir / "bias_field.nii.gz"
        nib.save(corrected_img, corrected_file)
        nib.save(bias_field_img, bias_file)
        print(f"    Saved: {corrected_file.name}, {bias_file.name}")

        print("  ✓ Bias correction complete")
        return corrected_img

    # GROUP 3: IMPLEMENT TISSUE SEGMENTATION METHOD HERE

    def tissue_segmentation(self, img):
        """
        Segment brain into gray matter, white matter, and CSF

        Uses intensity-based clustering to classify each voxel into
        one of three tissue types.

        Parameters
        ----------
        img : Nifti1Image
            Bias-corrected brain image (3D)

        Returns
        -------
        segmentation : dict
            Dictionary containing:
            - 'gm': Gray matter probability map (Nifti1Image)
            - 'wm': White matter probability map (Nifti1Image)
            - 'csf': CSF probability map (Nifti1Image)
            - 'volumes_ml': Tissue volumes in milliliters

        Notes
        -----
        Uses a simple k-means clustering approach on intensity values.
        For production use, consider FSL FAST or SPM segmentation.
        """
        from sklearn.cluster import KMeans
        import numpy as np

        print("  → Segmenting tissues (GM, WM, CSF)...")

        # TODO: Get image data and mask
        data = img.get_fdata()
        brain_mask = data > 0
        brain_voxels = data[brain_mask].reshape(-1, 1)

        # TODO: Normalize intensities to 0-1
        brain_voxels_norm = (brain_voxels - brain_voxels.min()) / (brain_voxels.max() - brain_voxels.min())

        # TODO: K-means clustering (3 clusters)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        labels = kmeans.fit_predict(brain_voxels_norm)

        # TODO: Sort clusters by intensity (CSF=0, GM=1, WM=2)
        cluster_means = [brain_voxels[labels == i].mean() for i in range(3)]
        sorted_clusters = np.argsort(cluster_means)  # Sort: darkest to brightest

        # TODO: Create probability maps
        gm_prob = np.zeros(data.shape)
        wm_prob = np.zeros(data.shape)
        csf_prob = np.zeros(data.shape)

        csf_prob[brain_mask] = (labels == sorted_clusters[0]).astype(float)
        gm_prob[brain_mask] = (labels == sorted_clusters[1]).astype(float)
        wm_prob[brain_mask] = (labels == sorted_clusters[2]).astype(float)

        # TODO: Create NIfTI images
        gm_img = nib.Nifti1Image(gm_prob, img.affine, img.header)
        wm_img = nib.Nifti1Image(wm_prob, img.affine, img.header)
        csf_img = nib.Nifti1Image(csf_prob, img.affine, img.header)

        # TODO: Calculate volumes
        voxel_volume_ml = np.prod(img.header.get_zooms()) / 1000  # mm³ to ml
        gm_volume = gm_prob.sum() * voxel_volume_ml
        wm_volume = wm_prob.sum() * voxel_volume_ml
        csf_volume = csf_prob.sum() * voxel_volume_ml

        print(f"    GM volume:  {gm_volume:.1f} ml")
        print(f"    WM volume:  {wm_volume:.1f} ml")
        print(f"    CSF volume: {csf_volume:.1f} ml")

        # TODO: Save outputs
        nib.save(gm_img, self.output_dir / "gm_prob.nii.gz")
        nib.save(wm_img, self.output_dir / "wm_prob.nii.gz")
        nib.save(csf_img, self.output_dir / "csf_prob.nii.gz")
        print(f"    Saved: gm_prob.nii.gz, wm_prob.nii.gz, csf_prob.nii.gz")

        segmentation = {
            'gm': gm_img,
            'wm': wm_img,
            'csf': csf_img,
            'volumes_ml': {
                'gm': gm_volume,
                'wm': wm_volume,
                'csf': csf_volume
            }
        }

        print("  ✓ Tissue segmentation complete")
        return segmentation

    # GROUP 4: IMPLEMENT VISUALIZATION METHOD HERE
    def create_visualization(self, img, segmentation, subject_idx):
        """
        Create comprehensive diagnostic visualization

        Generates multi-panel figure showing all processing stages and
        tissue segmentation results.

        Parameters
        ----------
        img : Nifti1Image
            Final processed (bias-corrected) image
        segmentation : dict
            Segmentation results from tissue_segmentation()
        subject_idx : int
            Subject index for labeling

        Returns
        -------
        None
            Saves figure to outputs directory

        Notes
        -----
        Creates a 2x3 figure:
        - Top row: Processing stages (brain extraction, bias correction)
        - Bottom row: Tissue segmentation overlays (GM, WM, CSF)
        """
        from nilearn import plotting
        import matplotlib.pyplot as plt
        from pathlib import Path

        print("  → Creating diagnostic visualization...")

        # TODO: Load intermediate results
        brain_img = nib.load(self.output_dir / "brain.nii.gz")
        mask_img = nib.load(self.output_dir / "brain_mask.nii.gz")

        # TODO: Create figure with 2x3 subplots
        fig = plt.figure(figsize=(15, 10))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

        # TODO: Row 1, Col 1 - Brain mask overlay
        ax1 = fig.add_subplot(gs[0, 0])
        plotting.plot_roi(mask_img, bg_img=brain_img, axes=ax1,
                          title='Brain Extraction', alpha=0.4, cmap='autumn')

        # TODO: Row 1, Col 2 - Bias corrected
        ax2 = fig.add_subplot(gs[0, 1])
        plotting.plot_anat(img, axes=ax2, title='Bias Corrected')

        # TODO: Row 1, Col 3 - All tissues composite
        ax3 = fig.add_subplot(gs[0, 2])
        # Create RGB composite of tissues
        gm_data = segmentation['gm'].get_fdata()
        wm_data = segmentation['wm'].get_fdata()
        csf_data = segmentation['csf'].get_fdata()
        composite = np.stack([gm_data, wm_data, csf_data], axis=-1)
        # ... plot composite

        # TODO: Row 2 - Individual tissue overlays
        ax4 = fig.add_subplot(gs[1, 0])
        plotting.plot_roi(segmentation['gm'], bg_img=img, axes=ax4,
                          title='Gray Matter', cmap='Reds', alpha=0.5)

        ax5 = fig.add_subplot(gs[1, 1])
        plotting.plot_roi(segmentation['wm'], bg_img=img, axes=ax5,
                          title='White Matter', cmap='Blues', alpha=0.5)

        ax6 = fig.add_subplot(gs[1, 2])
        plotting.plot_roi(segmentation['csf'], bg_img=img, axes=ax6,
                          title='CSF', cmap='Greens', alpha=0.5)

        # TODO: Add text summary of volumes
        volumes = segmentation['volumes_ml']
        summary_text = (
            f"Subject {subject_idx}\n"
            f"GM:  {volumes['gm']:.1f} ml\n"
            f"WM:  {volumes['wm']:.1f} ml\n"
            f"CSF: {volumes['csf']:.1f} ml\n"
            f"Total: {sum(volumes.values()):.1f} ml"
        )
        fig.text(0.98, 0.02, summary_text, fontsize=10,
                 verticalalignment='bottom', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # TODO: Save figure
        output_file = self.output_dir / f"sub-{subject_idx}_diagnostic.png"
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"    Saved: {output_file.name}")

        print("  ✓ Visualization complete")

    def run_full_pipeline(self, subject_idx=0):
        """
        Execute complete structural processing pipeline

        Parameters
        ----------
        subject_idx : int
            Subject index

        Returns
        -------
        img : Nifti1Image
            Final processed image
        """
        print(f"\n{'='*60}")
        print(f"Processing Subject: {subject_idx}")
        print(f"{'='*60}\n")

        # Load data
        img = self.load_data(subject_idx)

        # GROUP 1: Uncomment after skull stripping PR merged
        img_brain = self.skull_strip(img)

        # GROUP 2: Uncomment after bias correction PR merged
        img_corrected = self.bias_field_correction(img_brain)

        # GROUP 3: Uncomment after segmentation PR merged
        segmentation = self.tissue_segmentation(img_corrected)

        # GROUP 4: Uncomment after visualization PR merged
        self.create_visualization(img_corrected, segmentation, subject_idx)

        print("\n✓ Pipeline complete!")
        return img


if __name__ == "__main__":
    # Example usage
    pipeline = StructuralPipeline(output_dir="./outputs")

    # Process first subject
    result = pipeline.run_full_pipeline(subject_idx=0)