@echo off
echo ========================================
echo SHAMMAR SERVICES - Ecosysteme MABIPINT
echo ========================================
echo.

REM Activer l'environnement virtuel
if exist venv\Scripts\activate.bat (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
    echo.

    echo Demarrage du serveur Django...
    echo.
    echo L'application sera accessible sur: http://127.0.0.1:8000/
    echo.
    echo Appuyez sur Ctrl+C pour arreter le serveur
    echo.
    python manage.py runserver
) else (
    echo ERREUR: L'environnement virtuel n'existe pas!
    echo.
    echo Veuillez d'abord executer les commandes suivantes:
    echo   1. python -m venv venv
    echo   2. .\venv\Scripts\Activate
    echo   3. pip install -r requirements.txt
    echo   4. python manage.py migrate
    echo   5. python manage.py createsuperuser
    echo.
    pause
)
