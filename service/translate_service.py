from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI("https://libretranslate.de")


def translate_text(text: str, source="ko", target="en"):

    try:
        translated = lt.translate(text, source, target)
        return translated

    except Exception as e:
        print(f"Translation error: {e}")
        return None