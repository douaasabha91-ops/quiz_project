@echo off
echo ========================================
echo Interactive Quiz System - Windows Setup
echo ========================================
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo.

echo Step 2: Installing dependencies...
echo Installing Streamlit...
pip install streamlit
echo.

echo Installing Python-dotenv...
pip install python-dotenv
echo.

echo Installing Pandas...
pip install pandas
echo.

echo Installing Plotly...
pip install plotly
echo.

echo Step 3: Installing PostgreSQL driver...
echo Trying psycopg2-binary first...
pip install psycopg2-binary
if %errorlevel% neq 0 (
    echo.
    echo psycopg2-binary failed. Trying psycopg3...
    pip install "psycopg[binary]"
    if %errorlevel% equ 0 (
        echo.
        echo SUCCESS: Installed psycopg3
        echo IMPORTANT: Run this command to use psycopg3:
        echo copy database_psycopg3.py database.py
        echo.
    ) else (
        echo.
        echo ERROR: Both psycopg2 and psycopg3 failed to install.
        echo Please see INSTALL_WINDOWS.md for alternative methods.
        echo.
        pause
        exit /b 1
    )
) else (
    echo SUCCESS: Installed psycopg2-binary
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Set up PostgreSQL database
echo 2. Copy .env.example to .env and configure
echo 3. Run: streamlit run app.py
echo.
echo For detailed instructions, see README.md
echo.
pause
