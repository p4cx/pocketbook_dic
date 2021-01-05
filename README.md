# CREATE POCKETBOOK DICTIONARY

A few years ago I bought a Pocketbook Lux 4 e-book reader and discovered that it had a lousy dictionary. As a non-native speaker, I enjoy reading English books, so I occasionally need a translation of a word. The standard dictionaries on this device only provide basic vocabulary and are therefore of no help to me. Based on this problem, I looked around a bit and at that time only found expensive dictionaries that were not big enough for my taste.

Here I decided that I would try to build my own dictionary based on data provided by dict.cc.   
Excerpts from the ["About dict.cc" page](https://www.dict.cc/?s=about%3A&l=e):   
```
[...]
To guarantee that the users' work is not lost in case something happens to the maintainer of dict.cc (Paul Hemetsberger), the resulting vocabulary database can be downloaded anytime.
[...]
Terms of Use

All services offered by dict.cc can be used in the web browser for free, both for private and business purposes. All other ways of usage, particularly automated requests (parsing) require express permission.
[...]
```

The status of these instructions is from January 5th, 2021 and it's only developed and tested for the EN-DE (English to German) data. If this does not work, then unfortunately you are unlucky. If I have the time and inclination, I will answer requests for help, but no guarantee for this. Feel free to add new languages to this script or improve it elsewhere.

### How To Create a (Translation) Dictionary for Pocketbook eBook Readers:
(These instructions have only been tested with the Pocketbook Touch 3, but the new created dictionaries should work on all Pocketbook devices)

1. Download translation text file from [dict.cc](https://www1.dict.cc/translation_file_request.php) (for private usage only, therefore, you cannot download the finished dictionary in this repository)
    - if you don't want to bother around with this tool or these instructions, [download](https://www1.dict.cc/download/pocketbook-dict-cc-en-de.zip) the finished dictionary by dict.cc and install it on your e-book reader as described from step 5 (but keep in mind, that this dictionary will be outdated)
2. Unzip the downloaded archive and place the text file next to the python file (after cloning this repo 🤓) and rename it to `lex.txt`
4. Run `python3 ./parser.py` in the dictionary, where the `lex.txt` and `parser.py` are
    - you will need the python package `sqlite3`, get it before using the tool 
5. Get some coffee, read a book or clean your kitchen - it will take some time

https://www.dict.cc/?s=about%3Awordlist

https://github.com/soshial/xdxf_makedict/blob/master/format_standard/xdxf_description.md
