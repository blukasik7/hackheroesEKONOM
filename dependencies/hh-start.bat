@echo off
setlocal enabledelayedexpansion
color 2
cls

echo ---------------------------------------------
echo.
echo        Instalator zaleznosci UHUHU
echo.
echo        Zawiera:
echo        - Python 3.12
echo        - timedelta (Python (PIP^)^)
echo        - vulcan-api (Python (PIP^)^)
echo        - Vulcan (Python (PIP^)^)
echo        - g4f (Python (PIP^)^)
echo        - winotify (Python (PIP^)^)
echo.
echo        (C^) UHUHU 2023 Jakub Namyslak
echo                        Remigiusz Lukasik
echo                        Bartosz Lukasik
echo                        Lukasz Piechaczek
echo                        Jacek Dombrowski
echo                         All rights reserved
echo.
echo ---------------------------------------------
echo.
echo --INSTALACJA---------------------------------
echo.
echo Aby zapewnic poprawne dzialanie programu,
echo uzytkownik musi pobrac kazda z powyzszych
echo zaleznosci.
echo.
echo ---------------------------------------------
echo.
echo --PYTHON-------------------------------------
echo.
echo 1. Instalacja Pythona
echo.
echo Srodowisko wyzej wymienionego
echo programu jest wykorzystywane
echo w obrebie naszego projektu.
echo Jego obecnosc jest krytyczna.
:instalacja-python
echo.
echo Kontynuowac? (y/n^)
set /p "input=PYTHON >>"
if /i "%input%"=="y" (
	echo.
	echo Przejdz przez proces instalacyjny.
	echo W celu mozliwosci instalacji bibliotek,
	echo nie odznaczaj opcji `pip` (jesli
	echo jest dostepna^).
	echo.
	python-3.12.0-amd64.exe
	echo Czy chcesz sprobowac ponownie? (y/n^)
	set /p "input2=Python >>"
	echo.
	if /i "!input2!"=="y" (
		echo Reinstalowanie...
		goto instalacja-python
	)
)
if not "%input%"=="y" (
	echo.
	echo Python 3.12 nie zostanie zainstalowany.
)
echo.
echo ---------------------------------------------
echo.
echo --PIP----------------------------------------
echo.
echo 2. Instalacja bibliotek Pythona
echo.
echo Jesli Python i pip sa zainstalowane
echo na tym komputerze, nastepnym krokiem 
echo jest instalacja zewnetrzych bibliotek
echo wymaganych przez skrypt.
echo.
echo Kontynuowac? (y/n^)
set /p "input3=pip >>"
echo.
if /i "%input3%"=="y" (
	echo --LOGI---------------------------------------
	echo.
	pip install pip
	python.exe -m pip install --upgrade pip
	pip install timedelta
    	pip install vulcan-api
	pip install Vulcan
	pip install aiohttp==3.9.0b0
	pip install -U g4f
	pip install winotify
)
if not "%input3%"=="y" (
	echo Zaleznosci PIP nie zostana zainstalowane.
)
echo.
echo ---------------------------------------------
echo.
echo -KONIEC--------------------------------------
echo.
echo To juz wszystkie zaleznosci dotychczas
echo wykorzystane w tym projekcie.
echo Dziekujemy za cierpliwosc.
echo.
echo Czy chcesz uruchomic plik
echo startowy? (pierwsze-uruchomienie.py^)
echo (y/n^)
set /p "input6=>>"
if /i "%input6%"=="y" (
	echo.
	echo ---------------------------------------------
	echo.
	echo ---------------------------------------------
	echo.
	cd ..
	python pierwsze_uruchomienie.py
)
echo.
echo ----------------------------------------------
pause