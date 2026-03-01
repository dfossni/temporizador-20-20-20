@echo off
setlocal

echo ============================================
echo   Instalador - Temporizador 20-20-20
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Descargalo desde https://www.python.org/downloads/
    pause
    exit /b 1
)

set "DEST=%LOCALAPPDATA%\Timer202020"
set "SCRIPT=%DEST%\20_20_20_timer.py"
set "ICON=%DEST%\icono.ico"
set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Temporizador 20-20-20.lnk"
set "PS1=%DEST%\crear_acceso.ps1"

if not exist "%DEST%" mkdir "%DEST%"

copy /Y "%~dp020_20_20_timer.py" "%SCRIPT%" >nul
if errorlevel 1 (
    echo [ERROR] No se pudo copiar 20_20_20_timer.py
    echo Asegurate de que todos los archivos esten en la misma carpeta.
    pause
    exit /b 1
)

copy /Y "%~dp0icono.ico" "%ICON%" >nul
if errorlevel 1 (
    echo [ERROR] No se pudo copiar icono.ico
    echo Asegurate de que icono.ico este en la misma carpeta que este instalador.
    pause
    exit /b 1
)

(
echo $ws = New-Object -ComObject WScript.Shell
echo $s = $ws.CreateShortcut('%SHORTCUT%'^)
echo $s.TargetPath = 'pythonw.exe'
echo $s.Arguments = '"%SCRIPT%"'
echo $s.WorkingDirectory = '%DEST%'
echo $s.IconLocation = '%ICON%'
echo $s.Description = 'Temporizador 20-20-20 para el cuidado visual'
echo $s.Save(^)
) > "%PS1%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
if errorlevel 1 (
    echo [ERROR] No se pudo crear el acceso directo.
    pause
    exit /b 1
)

del "%PS1%" >nul 2>&1

echo.
echo [OK] Instalacion completada.
echo.
echo El acceso directo ya esta en tu menu de inicio.
echo Buscalo presionando Windows y escribiendo: Temporizador
echo.
pause
