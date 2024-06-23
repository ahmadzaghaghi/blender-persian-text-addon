@echo off
:: This script was written by Ahmad Zaghaghi.
:: It installs the necessary Python libraries for Persian text conversion in Blender.
:: The script checks if the default Blender Python bin directory is correct and if not, prompts the user to enter a new path.
:: All rights reserved by Ahmad Zaghaghi. Any copying or redistribution without permission is prohibited.

echo This script installs the prerequisite libraries for writing in Persian in Blender.
echo.
echo All rights reserved by Ahmad Zaghaghi. Any copying or redistribution without permission is prohibited.
echo.

setlocal

echo Is the default path "C:\Program Files\Blender Foundation\Blender 4.1\4.1\python\bin" correct? (yes/no)
set /p use_default_path=

if /I "%use_default_path%"=="yes" (
    set "bin_path=C:\Program Files\Blender Foundation\Blender 4.1\4.1\python\bin"
) else (
    echo Please enter the path to your Blender Python bin directory:
    set /p bin_path=
)

cd "%bin_path%"
if %errorlevel% neq 0 (
    echo Invalid path.
    pause
    exit /b 1
)

python.exe -m ensurepip
python.exe -m pip install arabic_reshaper python-bidi

if %errorlevel% neq 0 (
    echo Error installing libraries.
    pause
    exit /b 1
)

echo Libraries installed successfully.
pause
endlocal
