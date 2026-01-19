from cx_Freeze import setup, Executable

setup(
    name="NPZtoMATConverter",
    version="1.0",
    description="NPZ to MAT File Converter",
    executables=[Executable("npz_to_mat_converter.py")]
)