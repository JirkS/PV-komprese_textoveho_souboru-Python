# ALFA 2 | komprese textoveho souboru

### Funcionalita
- Program má za úkol zredukovat velikost textového souboru, tedy zkomprimovat textový soubor.
- Na začátku program vypíše nápovědu, jak používat program a ovládat ho pomocí konfiguračního souboru ve složce "config/config.ini".
- Na konci program vypíše logy z loggovacího souboru podle hodnot nastavených uživatelem v konfiguračním souboru.
- Při prvním zapnutí jsou v konfiguračním souboru nastaveny defaultní hodnoty.
- Zkompromovaný soubor má zachováný smysl a je stále k přečtení s využitím všech slovníků v output složce.

### Instalace a spuštění
- pro úspěšné zapnutí programu je zapotřebí mít na zařízení nainstalovaný python
- stáhneme si zip soubor a extrahujeme ho
- spustíme si windows cmd
- dojdeme pomocí příslušných příkazů do složky projektu (kompreseSouboruAlfa)
- poté program spustíme pomocí příkazu: "python main.py"

### Hlavní Třídy
#### Compressor
- Třída obsahuje metody pro kompletní kompresi textového souboru.
##### metody:
- compress() - spouští všechny metody pro kompresi
- count_num_of_words() - spočítá všechny slova v textovém souboru
- fill_dic_by_the_most_common_words() - naplní list slovy s největší četností - využití frekvenční analýzi
- fill_dic_of_two_word_phrases() - naplní dictionary dvěma nejčastějšími slovními spojeními o dvou slovech
- fill_dic_of_abbreviation() - naplní dictionary slovy společně s jejich zkratkami podle frekvenční anlýzi
- delete_short_sentences() - smaže nepodstatné, nedůležité a krátké nicneřikající věty
- delete_useless_words() - smaže nicneříkající, výplňová slova
- replace_words_with_abbreviations() - vymění slova za zkratky
- replace_words_of_coupling_synonyms() - vymění slova se stejným významem za nejkratší možnost
- replace_words_with_abbreviations_from_dictionary() - vymění slova za zkratky, které se vybraly
- fill_best_of_rest_of_the_most_common_words() - naplní list zbylými, nejvíce častými slovy
- replace_words_for_symbols() - vymění slova za vygenerované symboly
- write_csv_file() - zapíše slovník do csv souboru
- check_directory_path() - zkontroluje správnost cesty
- write_final_text_file() - zapíše finání verzi zkomprimovaného souboru
- Tato třída generuje různé verze rozvrhů pomocí náhodného vybírání předmětů. Pravděpodobnost, že se budou jakékoliv předměty totžné, je velmi mizivá. Každopádně i tyto varianty jsou bezpečně ohlídané, aby k nim nedocházelo. Třída slouží převážně pro vygenerování co nejvíce různých rozvrhů a nezáleží na tom, jak moc jsou kvalitní. Jde zkrátko o to, vygenerovat jich co nejvíce.
#### Loader
- Obsahuje metody pro načítání statických souborů ".json" a ".txt".
- Kontroluje správnost cest.
#### Template
- Tato třída obsahuje listy a dictionary, keteré obsahují načtené hodnoty ze statických souborů ".json".
#### Logger
- Tato třída slouží pro zapisování do log souborů (ingo.log a error.log ve složce log/) 
- Obsahuje metodu pro filtraci informací z informačního log souboru pro výpis před ukočením programu.
