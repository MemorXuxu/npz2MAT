@echo off
echo 正在安装依赖...
pip install numpy scipy pyinstaller

echo.
echo 请确保 A.ico 图标文件在当前目录中
echo.
echo 正在打包程序...
pyinstaller --onefile --windowed --name="NPZtoMATConverter" --icon=A.ico npz_to_mat_converter.py

echo.
echo 打包完成！可执行文件在 dist 文件夹中
echo 如果找不到图标文件，请手动添加 --icon=图标路径.ico 参数
pause