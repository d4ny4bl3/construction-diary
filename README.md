# Construction Diary

Construction Diary je aplikace pro správu stavebního deníku. Umožňuje zaznamenávání jednotlivých projektů, včetně použitých materiálů, cen, odpracovaného času, popisu práce a fotografií.

## Funkcionality

- Správa projektů: Možnost přidávat, upravovat a mazat projekty.

- Záznam materiálů: Sledování použitých materiálů a jejich cen.

- Záznam práce: Možnost přidávat záznamy odpracovaného času a popis práce.

- Fotodokumentace: Ukládání fotografií jednotlivých prací.

Reporty: Export dat o jednotlivých projektech.
## Požadavky
- Python 3.9+

- Django 5.1.1

- Další knihovny specifikované v requirements.txt

## Instalace

1. Naklonujte repozitář:

``` git clone https://github.com/uzivatel/construction-diary.git ```

2. Přejděte do adresáře projektu:

``` cd construction_diary ```

3. Vytvořte a aktivujte virtuální prostředí:

``` python -m venv env ```
``` source venv/bin/activate ``` # na Windows: venv\Scripts\activate 

4. Nainstalujte požadované balíčky:

``` pip install -r requirements.txt ```

5. Proveďte migrace:

``` python manage.py migrate ```

6. Vytvořte superusera pro přístup do administračního rozhraní:

```python manage.py createsuperuser ```

8. Spusťte server:

``` python manage.py runserver ```

## Používání

Otevřete webový prohlížeč a přejděte na http://127.0.0.1:8000/.

Přihlaste se pomocí administrátorského účtu nebo vytvořte nový účet.

Pro správu produktů a lokalit použijte administrační rozhraní nebo zákaznické zóny aplikace.


## Plánované funkce

- Pokročilá analýza nákladů na jednotlivé projekty.

- Možnost generovat detailní reporty s grafy.

- Integrace s cloudovými úōložišti pro zálohu dat.