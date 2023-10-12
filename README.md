# PoTranslator
This program automatically translate .po files into one or more languages.

At the moment only a few translation services are supported (see features). There will be further developement in the future.


### Features
- Simple translation from a .po file into another language
- Use of the whole locale folder without specifying individual files
- Use one or more target languages at once (Currently only one target language at once)
- Various parameters to define exactly what should be translated and several setting options
- Cache translations
- Supports the following translator modules (paramater `-t`)
  - ArgosTranslate: `argostranslate`
  - Deepl: `deepl-api`
  - Googletrans: `googletrans`
  - Translators: `alibaba, apertium, argos, baidu, bing, caiyun, cloudTranslation, deepl, elia, google, iciba, iflytek, iflyrec, itranslate, judic, languageWire, lingvanex, niutrans, mglip, mirai, modernMt, myMemory, papago, qqFanyi, qqTranSmart, reverso, sogou, sysTran, tilde, translateCom, translateMe, utibet, volcEngine, yandex, yeekit, youdao`
  - ...


## Current Status
It should currently be considered beta software and still work in progress.

All core features are implemented and functioning, but additions will probably occur as real-world use is explored.

There may be errors or the compatibility after an update is no longer guaranteed.

The full documentation is not yet available. Due to lack of time I can also not say when this will be further processed.


## Installation manual

### Linux

Download the file `potranslator-x.x.x-py3-none-any.whl`.

Install the dependencies. (CentOS)
```
yum -y install epel-release.noarch
yum -y install python3-pip
pip3 install pip --upgrade
pip3 install wheel --upgrade
```

Install the dependencies. (Debian/Mint/Raspi OS/Ubuntu)
```
apt install python3-pip
pip3 install pip --upgrade
```

Install the dependencies. (Fedora)
```
yum -y install make gcc
yum -y install python3-pip
pip3 install pip --upgrade
pip3 install wheel --upgrade
```

Install the dependencies. (Manjaro)
```
pacman -Sy python-pip
pip3 install pip --upgrade
```

Install the dependencies. (openSUSE)
```
zypper install python310 python310-pip
pip3 install pip --upgrade
```

Install the translation provider modules.
It depends on which translation providers are to be used later. 
```
pip install argostranslate

pip install deepl

pip install googletrans

pip install translators
apt install nodejs
```

Install the application.
`pip3 install potranslator-x.x.x-py3-none-any.whl`

Done. Launch the application (as user).
`potranslator`
or in case of an error
`./local/bin/potranslator`

### Windows
Download the file `potranslator-x.x.x.exe`.

Launch it.

### Startup parameters:
```bash
usage: potranslator [-h] [-p PATH] [-s LNG_SRC] [-d LNG_DST] [-t TRANSLATOR] [-tk TRANSLATOR_KEY] [-c] [-cr] [-cw] [-f] [-w WAIT] [-a AUTOSAVE] [-l LOGLEVEL]
               [--msgid_force_original MSGID_FORCE_ORIGINAL]

PoTranslator - Automatically translate .po files into one or more languages

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Option 1: Path to locales directory (source and target language folders are in this folder)
  -f FILE, --file FILE  Option 2: .po file (direct editing of the file)
  -s LNG_SRC, --lng_src LNG_SRC
                        Source language (2 digit locales code)
  -d LNG_DST, --lng_dst LNG_DST
                        Destination language (2 digit locales code) (comma separated)
  -t TRANSLATOR, --translator TRANSLATOR
                        Translation service provider
  -tk TRANSLATOR_KEY, --translator_key TRANSLATOR_KEY
                        API key for the translation service provider
  -c, --cache           Use an internal translation cache (read and write)
  -cr, --cache_read     Use an internal translation cache (read)
  -cw, --cache_write    Use an internal translation cache (write)
  -fo, --force          Forcing a new translation
  -w WAIT, --wait WAIT  Waiting time in milliseconds between translations
  -a AUTOSAVE, --autosave AUTOSAVE
                        Automatic saving after x-translations
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Log level
  --fuzzy_enable        Enable the 'fuzzy' flag on all translated entries
  --fuzzy_disable       Disable the 'fuzzy' flag on all translated entries
  --msgid_force MSGID_FORCE
                        Force a new translation for the following msgid's (comma separated)
  --msgid_force_original MSGID_FORCE_ORIGINAL
                        Force original translation for the following msgid's (comma separated)

```

### Example:
The following command translates the locales inside the folder `/root/locales` from `en` to `de` with the `deepl-api` translator.
  ```bash
  potranslator -p /root/locales -s en -d de -t deepl-api -tk <YOUR DEEPL API KEY>
  ```
The following command translates the locales inside the folder `/root/locales` from `en` to `de` with the `deepl-api` translator and display all translations with the log level setting `4`.
  ```bash
  potranslator -p /root/locales -s en -d de -t deepl-api -tk <YOUR DEEPL API KEY> -l 4
  ```
The following command translates the locales inside the folder `/root/locales` from `en` to `de,it,es,dk,pl` with the `deepl-api` translator.
  ```bash
  potranslator -p /root/locales -s en -d de,it,es,dk,pl -t deepl-api -tk <YOUR DEEPL API KEY>
  ```

## Support / Donations
You can help support the continued development by donating via one of the following channels:

- PayPal: https://paypal.me/SebastianObi
- Liberapay: https://liberapay.com/SebastianObi/donate


## Support in another way?
You are welcome to participate in the development. Just create a pull request. Or just contact me for further clarifications.


## Do you need a special function or customization?
Then feel free to contact me. Customizations or tools developed specifically for you can be realized.


## FAQ

### How do I start with the software?
You should read the `Installation manual` section. There everything is explained briefly. Just work through everything from top to bottom :)