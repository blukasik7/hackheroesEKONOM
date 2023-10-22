@echo off
setlocal enabledelayedexpansion
cls

echo ---------------------------------------------
echo        Instalator zaleznosci HHEkonom
echo.
echo        Zawiera:
echo        - Python 3.12
echo        - timedelta (Python (PIP^)^)
echo        - Node.js
echo.
echo        (C^) HHEkonom 2023 Jakub Namyslak
echo                           Remigiusz Lukasik
echo                           Bartosz Lukasik
echo                           Lukasz Piechaczek
echo                           Jacek Dombrowski
echo                           All rights reserved
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
	echo Czy chcesz sprobowac ponownie?
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
echo ---------------------------------------------
echo.
echo --PIP----------------------------------------
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
	pip install pip
	python.exe -m pip install --upgrade pip
	pip install timedelta
	echo ---------------------------------------------
)
if not "%input3%"=="y" (
	echo Zaleznosci PIP nie zostana zainstalowane.
)
echo ---------------------------------------------
echo.
echo --NODE.JS------------------------------------
echo.
echo Node.js z kolei znalazl u nas
echo zastosowanie w interakcjach
echo plik-strona. Wykorzystasz
echo go w trakcie podawania
echo swoich poswiadczen do
echo e-dziennika VULCAN.
echo.
echo Kontynuowac? (y/n^)
set /p "input4=Node.js >>"
if /i "%input4%"=="y" (
	:instalacja-node
	echo.
	echo Przejdz przez proces instalacyjny.
	echo Opcja 'Tools for Native Modules'
	echo nie jest wymagana.
	echo.
	node-v21.0.0-x64.msi
	echo Czy chcesz sprobowac ponownie?
	set /p "input5=Node.js >>"
	echo.
	if /i "%input5%"=="y" (
		echo Reinstalowanie...
		goto instalacja-node
	)
)
echo ---------------------------------------------
echo.
echo -KONIEC-------------------------------------
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
	cd ..
	python pierwsze_uruchomienie.py
)
echo.
echo ---------------------------------------------
pause