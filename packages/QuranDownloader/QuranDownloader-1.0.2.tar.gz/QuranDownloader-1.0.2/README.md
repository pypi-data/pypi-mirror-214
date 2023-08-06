# test
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install QuranDownloader lib.

```bash
pip install QuranDownloader
```

## usage

to import the library type:
```python
import QuranDownloader
```

Get all reciters names
```python
print(QuranDownloader.RECITERS)
```

### download_word

```python
(function) def download_word(
    verses_keys: list,
    export_dir: str = './export/words'
) -> None
```
#### Example 1: download all word in the 7th verse from surah al-fatiha

```python
QuranDownloader.download_word(['1:7'])
```

### download_verse

```python
(function) def download_verse(
    reciter_name: str,
    verse_key: str,
    export_dir: str = './export',
    chapter_number: int,
    juz_number: int,
    page_number: int
) -> None
```

#### Example 2: download the 7th verse from surah al-fatiha with 'Alafasy' voice

```python
QuranDownloader.download_verse('Alafasy', '1:7')
```

## License

[MIT](https://choosealicense.com/licenses/mit/)