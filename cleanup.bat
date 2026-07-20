@echo off
REM ATLAS Cleanup Script - Organizes documentation

echo Creating docs/archive folder...
if not exist "docs\archive" mkdir "docs\archive"

echo Moving historical documentation files...
if exist "FIX_SUMMARY.md" move /Y "FIX_SUMMARY.md" "docs\archive\" >nul 2>&1
if exist "IMPLEMENTATION_SUMMARY.md" move /Y "IMPLEMENTATION_SUMMARY.md" "docs\archive\" >nul 2>&1
if exist "UPGRADE_SUMMARY.md" move /Y "UPGRADE_SUMMARY.md" "docs\archive\" >nul 2>&1

if exist "docs\BUGFIX_APP_LAUNCHER.md" move /Y "docs\BUGFIX_APP_LAUNCHER.md" "docs\archive\" >nul 2>&1
if exist "docs\BUGFIX_FILE_VS_APP.md" move /Y "docs\BUGFIX_FILE_VS_APP.md" "docs\archive\" >nul 2>&1
if exist "docs\BUGFIX_SELF_LISTENING.md" move /Y "docs\BUGFIX_SELF_LISTENING.md" "docs\archive\" >nul 2>&1

if exist "docs\PHASE1_FIXES.md" move /Y "docs\PHASE1_FIXES.md" "docs\archive\" >nul 2>&1
if exist "docs\PHASE2_COMPLETE.md" move /Y "docs\PHASE2_COMPLETE.md" "docs\archive\" >nul 2>&1
if exist "docs\PHASE3_COMPLETE.md" move /Y "docs\PHASE3_COMPLETE.md" "docs\archive\" >nul 2>&1

if exist "docs\REFACTOR_SUMMARY.md" move /Y "docs\REFACTOR_SUMMARY.md" "docs\archive\" >nul 2>&1
if exist "docs\COMPLETE_REFACTOR_SUMMARY.md" move /Y "docs\COMPLETE_REFACTOR_SUMMARY.md" "docs\archive\" >nul 2>&1
if exist "docs\MIGRATION_NOTE.md" move /Y "docs\MIGRATION_NOTE.md" "docs\archive\" >nul 2>&1
if exist "docs\CONFIRMATION_SYSTEM.md" move /Y "docs\CONFIRMATION_SYSTEM.md" "docs\archive\" >nul 2>&1
if exist "docs\FUZZY_MATCHING_IMPLEMENTATION.md" move /Y "docs\FUZZY_MATCHING_IMPLEMENTATION.md" "docs\archive\" >nul 2>&1
if exist "docs\ROOT_CAUSE_ANALYSIS_SELF_LISTENING.md" move /Y "docs\ROOT_CAUSE_ANALYSIS_SELF_LISTENING.md" "docs\archive\" >nul 2>&1

echo.
echo Cleanup complete!
echo - Historical docs moved to docs/archive/
echo - Project structure improved
echo.
pause
