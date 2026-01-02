@echo off
echo ========================================
echo PostgreSQL Database Setup
echo ========================================
echo.

set PSQL="C:\Program Files\PostgreSQL\18\bin\psql.exe"

echo Creating database 'quiz_system'...
echo You will be prompted for the PostgreSQL password.
echo.

%PSQL% -U postgres -c "CREATE DATABASE quiz_system;"

if %errorlevel% equ 0 (
    echo.
    echo Database created successfully!
    echo.
    echo Now loading schema...
    echo.
    %PSQL% -U postgres -d quiz_system -f schema.sql

    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo SUCCESS! Database is ready!
        echo ========================================
        echo.
        echo Next steps:
        echo 1. Create .env file: copy .env.example .env
        echo 2. Edit .env and set your PostgreSQL password
        echo 3. Run: python -m streamlit run app.py
        echo.
    ) else (
        echo.
        echo ERROR: Failed to load schema
        echo Please check schema.sql file
    )
) else (
    echo.
    echo Note: Database might already exist. Trying to load schema anyway...
    echo.
    %PSQL% -U postgres -d quiz_system -f schema.sql

    if %errorlevel% equ 0 (
        echo.
        echo Schema loaded successfully!
    )
)

echo.
pause
