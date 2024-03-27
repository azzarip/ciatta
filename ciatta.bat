@echo off
setlocal enabledelayedexpansion

rem Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Miniconda...
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
    start /wait "" miniconda.exe /InstallationType=JustMe /RegisterPython=1 /AddToPath=1 /S
    del miniconda.exe
)
echo Loading Python...
pip install --upgrade pip >nul
pip show ciatta > nul 2>&1
if not %errorlevel% == 0 (
    echo Package is not installed. Installing...
    pip install ciatta
)
echo Loading Package...
pip list --outdated | findstr /c:"ciatta"
if %errorlevel% == 0 (
    pip install --upgrade ciatta
) 
cls

echo Analyzing Files...
python -c "import ciatta; ciatta.start()"
echo Finished! 
pause