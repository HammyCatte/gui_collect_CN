@echo off
setlocal enabledelayedexpansion

rem 检查是否安装了 py 命令
py --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=2 delims= " %%A in ('py --version 2^>^&1') do set "ver=%%A"
    call :run_script py
    goto end
)

rem 检查是否安装了 python 命令
python --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=2 delims= " %%A in ('python --version 2^>^&1') do set "ver=%%A"
    call :run_script python
    goto end
)

echo 未找到 Python！
pause
goto end

:run_script
rem 解析 Python 版本号
for /f "tokens=1,2 delims=." %%A in ("%ver%") do (
    set "major=%%A"
    set "minor=%%B"
)

rem 判断是否为 Python 3.9 及以上版本
if !major! EQU 3 if !minor! GTR 8 (
    %1 --version
    %1 ./collect.py
    goto :eof
) else (
    echo 您必须至少安装 Python 3.9！
    pause
)

:end
