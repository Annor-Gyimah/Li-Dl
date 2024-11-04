@echo off
setlocal

REM Define paths
set TEMP_DIR=%USERPROFILE%\AppData\Local\Temp\AppUpdate
set UPDATE_ZIP=%TEMP_DIR%\update.zip
set APP_DIR=%USERPROFILE%\Desktop\App

REM Create TEMP_DIR if it doesn’t exist
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM Extract update.zip to TEMP_DIR
echo Extracting update package...
powershell -Command "Expand-Archive -Path '%UPDATE_ZIP%' -DestinationPath '%TEMP_DIR%' -Force"

REM Copy extracted files to APP_DIR, replacing old ones
echo Replacing application files...
xcopy /Y /E "%TEMP_DIR%\*" "%APP_DIR%"

REM Clean up TEMP_DIR
echo Cleaning up...
rmdir /S /Q "%TEMP_DIR%"

echo Update completed.
endlocal
exit
