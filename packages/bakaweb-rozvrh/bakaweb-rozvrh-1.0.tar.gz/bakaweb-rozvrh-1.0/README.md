<div align="center">

  <h1>Bakaweb Rozvrh</h1>

  ![GitHub License](https://img.shields.io/github/license/MortikCZ/bakaweb-rozvrh)
  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/MortikCZ/Bakaweb-Rozvrh)
  ![GitHub last commit](https://img.shields.io/github/last-commit/MortikCZ/Bakaweb-Rozvrh)

  <p>Jednoduchý nástroj pro extrakci rozvrhu z modulu Timetable Bakawebu. Data jsou získavána v HTML formátu a následně zpracována do JSON formátu.</p>
  
</div>

<h2 align = "center">Instalace</h2>

Tento nástroj je dostupný jako [PyPi balíček](https://pypi.org/project/bakaweb-rozvrh/). Pro instalaci je zapotřebí použít následující příkaz:
```bash
pip install bakawebrozvrh
```

<h2 align = "center">Použití</h2>

Funkce `get_timetable` má dva povinné parametry:
- `url` - URL adresa rozvrhu
- `output_file` - název souboru, do kterého se uloží rozvrh.

Vrací rozvrh ve formátu JSON.

Funkce `get_substitutions` má dva povinné parametry:
- `url` - URL adresa rozvrhu
- `output_file` - název souboru, do kterého se uloží změny.

Vrací změny v rozvrhu ve formátu JSON.

### Příklad použití
```python
import bakawebrozvrh

url = "https://bakalari.skola.cz/bakaweb/Timetable/Public/Permanent/Class/4U"
output_file = "timetable.json"
bakawebrozvrh.get_timetable(url, output_file)
```





