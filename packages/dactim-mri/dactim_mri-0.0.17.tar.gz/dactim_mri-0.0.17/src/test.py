from dactim_mri.sorting import sort_dicom
from dactim_mri.conversion import convert_dicom_to_nifti
from dactim_mri.transformation import Dactim

dactim = Dactim()
dactim.skull_stripping(r"F:\Dev\taima-2022\data\nifti\AX_T1_MPRAGE.nii.gz", model_path=r"C:\Users\467355\Documents\HD-BET-master\HD_BET\hd-bet_params", mask=True)