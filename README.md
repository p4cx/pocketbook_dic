# CREATE POCKETBOOK DICTIONARY

A few years ago I bought a Pocketbook Lux 4 e-book reader and discovered that it had a lousy lexicon. As a non-native speaker, I enjoy reading English books, so I occasionally need a translation of a word. The standard lexicons on this device only provide basic vocabulary and are therefore of no help to me. Based on this problem, I looked around a bit and at that time only found expensive lexicons that were not big enough for my taste.

Here I decided that I would try to build my own dictionary based on data provided by dict.cc.   
Excerpts from the ["About dict.cc" page](https://www.dict.cc/?s=about%3A&l=e):   
[...]
To guarantee that the users' work is not lost in case something happens to the maintainer of dict.cc (Paul Hemetsberger), the resulting vocabulary database can be downloaded anytime.
[...]
Terms of Use

All services offered by dict.cc can be used in the web browser for free, both for private and business purposes. All other ways of usage, particularly automated requests (parsing) require express permission.
[...]

The status of these instructions is from January 5th, 2021. If this does not work, then unfortunately we are unlucky. If I have the time and inclination, I will answer requests for help, but no guarantee for this.

#### How To Create a (Translation) Lexicon for Pocketbook eBook Readers:
(These instructions have only been tested with the Pocketbook Touch 3)

1. Download translation text file from [dict.cc](https://www1.dict.cc/translation_file_request.php) (for private usage only, therefore, you cannot download the finished dictionary in this repository)
    - if you don't want to bother around with this tool or the instructions, [download](https://www1.dict.cc/download/pocketbook-dict-cc-en-de.zip) the finished dictionary by dict.cc and install it on your e-book reader as described from step 5 
2. Unzip the downloaded archive
3. Place the downloaded text file next to the python file (after cloning this repo 🤓) and rename it to `lex.txt`
4. Run `python3 ./parser.py` in the dictionary, where the `lex.txt` and `parser.py` files are
    - you will need the python package `sqlite3`, install it before using the tool 
5. Get some coffee, read a book or clean your kitchen - it will take some time

https://www.dict.cc/?s=about%3Awordlist

https://github.com/soshial/xdxf_makedict/blob/master/format_standard/xdxf_description.md
