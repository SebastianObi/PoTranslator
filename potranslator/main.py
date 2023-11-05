##############################################################################################################
#
# Copyright (c) 2023 Sebastian Obele  /  obele.eu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
##############################################################################################################


##############################################################################################################
# Include


#### System ####
import sys
import os
import time
import argparse
import shutil
from datetime import datetime

#### Polib ####
# Installation: pip install polib
import polib

#### ArgosTranslate ####
# Installation: pip install argostranslate

#### Deepl ####
# Installation: pip install deepl

#### Googletrans ####
# Installation: pip install googletrans

#### Translators ####
# Installation: pip install translators
import translators as ts

if sys.platform.startswith("win"):
    import vendor.umsgpack as umsgpack

    #### Version ####
    from _version import __version__, __version_variant__, __copyright_short__, __title__, __description__, __package_name__, __config__

else:
    from .vendor import umsgpack as umsgpack

    #### Version ####
    from ._version import __version__, __version_variant__, __copyright_short__, __title__, __description__, __package_name__, __config__


##############################################################################################################
# Globals


PATH = os.path.expanduser("~") + "/." + __package_name__
TRANSLATOR = None


##############################################################################################################
# Translate


def translate(text, lng_src, lng_dst, translator):
    if translator == "argostranslate":
        return argostranslate.translate.translate(text, lng_src, lng_dst)

    elif translator == "deepl-api":
        result = TRANSLATOR.translate_text(text, target_lang=lng_dst)
        return result.text

    elif translator == "googletrans":
        result = TRANSLATOR.translate(text, src=lng_src, dest=lng_dst)
        return result.text

    else:
        return ts.translate_text(query_text=text, translator=translator, from_language=lng_src, to_language=lng_dst)


##############################################################################################################
# Log


LOG_FORCE    = -1
LOG_CRITICAL = 0
LOG_ERROR    = 1
LOG_WARNING  = 2
LOG_NOTICE   = 3
LOG_INFO     = 4
LOG_VERBOSE  = 5
LOG_DEBUG    = 6
LOG_EXTREME  = 7

LOG_LEVEL         = LOG_NOTICE
LOG_LEVEL_SERVICE = LOG_NOTICE
LOG_TIMEFMT       = "%Y-%m-%d %H:%M:%S"
LOG_MAXSIZE       = 5*1024*1024
LOG_PREFIX        = ""
LOG_SUFFIX        = ""
LOG_FILE          = ""


def log(text, level=3, file=None):
    if not LOG_LEVEL:
        return

    if LOG_LEVEL >= level:
        name = "Unknown"
        if (level == LOG_FORCE):
            name = ""
        if (level == LOG_CRITICAL):
            name = "Critical"
        if (level == LOG_ERROR):
            name = "Error"
        if (level == LOG_WARNING):
            name = "Warning"
        if (level == LOG_NOTICE):
            name = "Notice"
        if (level == LOG_INFO):
            name = "Info"
        if (level == LOG_VERBOSE):
            name = "Verbose"
        if (level == LOG_DEBUG):
            name = "Debug"
        if (level == LOG_EXTREME):
            name = "Extra"

        if not isinstance(text, str):
            text = str(text)

        text = "[" + time.strftime(LOG_TIMEFMT, time.localtime(time.time())) +"] [" + name + "] " + LOG_PREFIX + text + LOG_SUFFIX

        if file == None and LOG_FILE != "":
            file = LOG_FILE

        if file == None:
            print(text)
        else:
            try:
                file_handle = open(file, "a")
                file_handle.write(text + "\n")
                file_handle.close()

                if os.path.getsize(file) > LOG_MAXSIZE:
                    file_prev = file + ".1"
                    if os.path.isfile(file_prev):
                        os.unlink(file_prev)
                    os.rename(file, file_prev)
            except:
                return


##############################################################################################################
# System


#### Panic #####
def panic():
    sys.exit(255)


#### Exit #####
def exit():
    sys.exit(0)


##############################################################################################################
# Setup/Start


#### Setup translate ####
def setup_translate(lng_src, lng_dst, translator="", translator_key=None):
    global TRANSLATOR

    if translator == "argostranslate":
        try:
            import argostranslate.package
            import argostranslate.translate
        except ImportError:
            log("The 'argostranslate' module is not installed.", LOG_ERROR)
            panic()
        try:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == lng_src and x.to_code == lng_dst, available_packages
                )
            )
            argostranslate.package.install_from_path(package_to_install.download())
        except Exception as e:
            log(str(e), LOG_ERROR)
            panic()

    elif translator == "deepl-api":
        try:
            import deepl
        except ImportError:
            log("The 'deepl' module is not installed.", LOG_ERROR)
            panic()
        try:
            TRANSLATOR = deepl.Translator(translator_key)
        except Exception as e:
            log(str(e), LOG_ERROR)
            panic()

    elif translator == "googletrans":
        try:
            from googletrans import Translator
        except ImportError:
            log("The 'googletrans' module is not installed.", LOG_ERROR)
            panic()
        try:
            TRANSLATOR = Translator()
        except Exception as e:
            log(str(e), LOG_ERROR)
            panic()

    else:
        try:
            import translators
            TRANSLATOR = translators
            if translator not in TRANSLATOR.translators_pool:
                log("Unknown translator '"+translator+"'", LOG_ERROR)
                panic()
        except ImportError:
            log("The 'translators' module is not installed.", LOG_ERROR)
            panic()


#### Setup file ####
def setup_file(path, lng_src, lng_dst, force=False):
    try:
        file_src = path+"/"+lng_src+"/LC_MESSAGES/base.po"
        file_dst = path+"/"+lng_dst+"/LC_MESSAGES/base.po"

        if not os.path.isfile(file_src):
            log("Source file '"+file_src+"' not found", LOG_ERROR)
            panic()

        if not os.path.exists(path+"/"+lng_dst+"/LC_MESSAGES"):
            os.makedirs(path+"/"+lng_dst+"/LC_MESSAGES")

        if force:
            if os.path.isfile(file_dst):
                os.remove(file_dst)

        if not os.path.isfile(file_dst):
            shutil.copyfile(file_src, file_dst)
            po = polib.pofile(file_dst)
            for entry in po:
                entry.msgstr = ""
            po.save()

        return file_src, file_dst
    except Exception as e:
        log(str(e), LOG_ERROR)
        panic()


#### Setup #####
def setup(path=None, file=None, lng_src=None, lng_dst=None, translator=None, translator_key=None, cache=False, cache_read=False, cache_write=False, force=False, wait=0, autosave=50, loglevel=None, fuzzy_enable=False, fuzzy_disable=False, msgid_force=None, msgid_force_original=None):
    global LOG_LEVEL

    config = __config__

    if loglevel is not None:
        LOG_LEVEL = loglevel

    log("...............................................................................", LOG_INFO)
    log("        Name: " + __title__ + " - " + __description__, LOG_INFO)
    log("Program File: " + __file__, LOG_INFO)
    log("     Version: " + __version__ + " " + __version_variant__, LOG_INFO)
    log("   Copyright: " + __copyright_short__, LOG_INFO)
    log("...............................................................................", LOG_INFO)

    if (path == None and file == None) or lng_src == None or lng_dst == None or translator == None:
        log("Missing parameters", LOG_ERROR)
        panic()

    if lng_src == lng_dst:
        log("Source and target language are the same", LOG_ERROR)
        panic()

    if path.endswith("/"):
        path = src[:-1]

    if cache:
        cache_read = True
        cache_write = True

    log("           PO-File Path: " + path, LOG_INFO)
    log("             Translator: " + translator, LOG_INFO)
    log("        Source language: " + lng_src, LOG_INFO)
    log("Destination language(s): " + lng_dst, LOG_INFO)

    if msgid_force:
        msgid_force = msgid_force.split(',')
    else:
        msgid_force = []

    if msgid_force_original:
        msgid_force_original = msgid_force_original.split(',')
    else:
        msgid_force_original = []

    setup_translate(lng_src=lng_src, lng_dst=lng_dst, translator=translator, translator_key=translator_key)

    if cache_read or cache_write:
        cache = {}
        if cache_write and not os.path.exists(PATH):
            os.makedirs(PATH)
        if os.path.isfile(PATH+"/cache.data"):
            try:
                fh = open(PATH+"/cache.data", "rb")
                cache = umsgpack.unpackb(fh.read())
                fh.close()
            except Exception as e:
                cache = {}
        if not translator in cache:
            cache[translator] = {}
        if not lng_src+"_"+lng_dst in cache[translator]:
            cache[translator][lng_src+"_"+lng_dst] = {}

    log("", LOG_INFO)
    log("Translating '" + lng_src + "' to '" + lng_dst + "'. Please wait...", LOG_INFO)
    log("", LOG_INFO)

    if file:
        po_dict = {}
        if not os.path.isfile(file):
            log("File '"+file+"' not found", LOG_ERROR)
            panic()
        po_file_dst = file
    else:
        po_file_src, po_file_dst = setup_file(path=path, lng_src=lng_src, lng_dst=lng_dst, force=force)

        po_dict = {}
        po_src = polib.pofile(po_file_src)
        for entry in po_src:
            po_dict[entry.msgid] = entry.msgstr

    po_dst = polib.pofile(po_file_dst)

    current_datetime = datetime.now()
    po_dst.lang = lng_dst
    po_dst.metadata['Language'] = lng_dst
    po_dst.metadata['POT-Creation-Date'] = current_datetime.strftime('%Y-%m-%d %H:%M%z')
    po_dst.metadata['PO-Revision-Date'] = current_datetime.strftime('%Y-%m-%d %H:%M%z')
    po_dst.save()

    count = len(po_dst)
    count_current = 0
    count_skipped = 0
    count_forced = 0
    count_translated_cache = 0
    count_translated_online = 0
    count_error = 0
    count_chars = 0

    i = 0
    for entry in po_dst:
        try:
            count_current += 1

            if not entry.msgid:
                count_skipped += 1
                continue

            for value in msgid_force:
                if value in entry.msgid:
                    entry.msgstr = ""
                    entry.fuzzy = False
                    break

            forced = False
            for value in msgid_force_original:
                if value in entry.msgid:
                    if entry.msgid in po_dict and po_dict[entry.msgid] != "":
                        entry.msgstr = po_dict[entry.msgid]
                        entry.fuzzy = False
                    else:
                        entry.msgstr = entry.msgid
                        entry.fuzzy = False
                    count_forced += 1
                    forced = True
                    break
            if forced:
                continue

            if entry.msgstr != "":
                count_skipped += 1
                continue

            if entry.msgid in po_dict:
                if entry.msgid == po_dict[entry.msgid]:
                    count_skipped += 1
                    continue
                if po_dict[entry.msgid] != "":
                    text_src = po_dict[entry.msgid]
                else:
                    text_src = entry.msgid
            else:
                if entry.msgid == entry.msgstr:
                    count_skipped += 1
                    continue
                text_src = entry.msgid

            cached = False
            if cache_read:
                if text_src in cache[translator][lng_src+"_"+lng_dst]:
                    text_dst = cache[translator][lng_src+"_"+lng_dst][text_src]
                    cached = True

            if not cached:
                if wait:
                    time.sleep(wait/1000.0)
                text_dst = translate(text_src, lng_src, lng_dst, translator)

            if text_dst != "":
                if not cached and cache_write:
                    cache[translator][lng_src+"_"+lng_dst][text_src] = text_dst

                if text_src.startswith(('.', ',', ':', ';', '-', '_', '?', '!')):
                    text_src_char0 = text_src[0]
                else:
                    text_src_char0 = None
                if text_src.endswith(('.', ',', ':', ';', '-', '_', '?', '!')):
                    text_src_char1 = text_src[-1]
                else:
                    text_src_char1 = None
                if text_dst.startswith(('.', ',', ':', ';', '-', '_', '?', '!')):
                    text_dst_char0 = text_dst[0]
                else:
                    text_dst_char0 = None
                if text_dst.endswith(('.', ',', ':', ';', '-', '_', '?', '!')):
                    text_dst_char1 = text_dst[-1]
                else:
                    text_dst_char1 = None

                if text_src_char0 != text_dst_char0:
                    if text_dst_char0 == None:
                        text_dst = text_src_char0 + text_dst
                    elif text_src_char0 == None:
                        text_dst = text_dst[1:]
                    else:
                        text_dst = text_src_char0 + text_dst[1:]

                if text_src_char1 != text_dst_char1:
                    if text_dst_char1 == None:
                        text_dst = text_dst + text_src_char1
                    elif text_src_char1 == None:
                        text_dst = text_dst[:-1]
                    else:
                        text_dst = text_dst[:-1] + text_src_char1

                entry.msgstr = text_dst

                if fuzzy_enable:
                    entry.fuzzy = True
                elif fuzzy_disable:
                    entry.fuzzy = False

                i += 1
                if i >= autosave:
                    i = 0
                    po_dst.save()
                    if cache_write:
                        try:
                            fh = open(PATH+"/cache.data", "wb")
                            fh.write(umsgpack.packb(cache))
                            fh.close()
                        except Exception as e:
                            log(str(e), LOG_ERROR)

                if cached:
                    count_translated_cache += 1
                    log(str(count_current)+"/"+str(count)+": "+text_src+" -> "+text_dst+" [CACHE]", LOG_INFO)
                else:
                    count_translated_online += 1
                    count_chars += len(text_src)
                    log(str(count_current)+"/"+str(count)+": "+text_src+" -> "+text_dst+" [ONLINE]", LOG_INFO)

        except Exception as e:
            count_error += 1
            log(str(e), LOG_ERROR)

    po_dst.save()

    if cache_write:
        try:
            fh = open(PATH+"/cache.data", "wb")
            fh.write(umsgpack.packb(cache))
            fh.close()
        except Exception as e:
            log(str(e), LOG_ERROR)

    log("...............................................................................", LOG_NOTICE)
    log("          Translator: " + translator, LOG_NOTICE)
    log("         Translation: " + lng_src + " -> " + lng_dst, LOG_NOTICE)
    log("               Count: " + str(count), LOG_NOTICE)
    log("             Skipped: " + str(count_skipped), LOG_NOTICE)
    log("              Forced: " + str(count_forced), LOG_NOTICE)
    if cache_read:
        log("    Translated Cache: " + str(count_translated_cache), LOG_NOTICE)
        log("   Translated Online: " + str(count_translated_online), LOG_NOTICE)
    else:
        log("          Translated: " + str(count_translated_online), LOG_NOTICE)
    log("              Errors: " + str(count_error), LOG_NOTICE)
    log("    Translated chars: " + str(count_chars), LOG_NOTICE)
    log("  PO-File translated: " + str(po_dst.percent_translated())+"%", LOG_NOTICE)
    log("PO-File untranslated: " + str(len(po_dst.untranslated_entries())), LOG_NOTICE)
    log("       PO-File fuzzy: " + str(len(po_dst.fuzzy_entries())), LOG_NOTICE)
    log("    PO-File obsolete: " + str(len(po_dst.obsolete_entries())), LOG_NOTICE)
    log("...............................................................................", LOG_NOTICE)


#### Start ####
def main():
    try:
        description = __title__ + " - " + __description__
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument("-p", "--path", action="store", type=str, default=None, help="Option 1: Path to locales directory (source and target language folders are in this folder)")
        parser.add_argument("-f", "--file", action="store", type=str, default=None, help="Option 2: .po file (direct editing of the file)")

        parser.add_argument("-s", "--lng_src", action="store", type=str, default=None, help="Source language (2 digit locales code)")
        parser.add_argument("-d", "--lng_dst", action="store", type=str, default=None, help="Destination language (2 digit locales code) (comma separated)")

        parser.add_argument("-t", "--translator", action="store", type=str, default=None, help="Translation service provider")
        parser.add_argument("-tk", "--translator_key", action="store", type=str, default=None, help="API key for the translation service provider")

        parser.add_argument("-c", "--cache", action="store_true", default=False, help="Use an internal translation cache (read and write)")
        parser.add_argument("-cr", "--cache_read", action="store_true", default=False, help="Use an internal translation cache (read)")
        parser.add_argument("-cw", "--cache_write", action="store_true", default=False, help="Use an internal translation cache (write)")

        parser.add_argument("-fo", "--force", action="store_true", default=False, help="Forcing a new translation")
        parser.add_argument("-w", "--wait", action="store", type=int, default=0, help="Waiting time in milliseconds between translations")
        parser.add_argument("-a", "--autosave", action="store", type=int, default=50, help="Automatic saving after x-translations")
        parser.add_argument("-l", "--loglevel", action="store", type=int, default=LOG_LEVEL, help="Log level")

        parser.add_argument("--fuzzy_enable", action="store_true", default=False, help="Enable the 'fuzzy' flag on all translated entries")
        parser.add_argument("--fuzzy_disable", action="store_true", default=False, help="Disable the 'fuzzy' flag on all translated entries")
        parser.add_argument("--msgid_force", action="store", type=str, default=None, help="Force a new translation for the following msgid's (comma separated)")
        parser.add_argument("--msgid_force_original", action="store", type=str, default=None, help="Force original translation for the following msgid's (comma separated)")

        params = parser.parse_args()

        setup(path=params.path, file=params.file, lng_src=params.lng_src, lng_dst=params.lng_dst, translator=params.translator, translator_key=params.translator_key, cache=params.cache, cache_read=params.cache_read, cache_write=params.cache_write, force=params.force, wait=params.wait, autosave=params.autosave, loglevel=params.loglevel, fuzzy_enable=params.fuzzy_enable, fuzzy_disable=params.fuzzy_disable, msgid_force=params.msgid_force, msgid_force_original=params.msgid_force_original)

    except KeyboardInterrupt:
        print("Terminated by CTRL-C")
        exit()


##############################################################################################################
# Init


if __name__ == "__main__":
    main()