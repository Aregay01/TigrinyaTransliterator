# ----------------------------------------------------------------------
# 2. Tigrinya Transliterator class
# ----------------------------------------------------------------------
class TigrinyaTransliterator:
    """
    A transliterator from Latin (English) characters to Tigrinya (Ge'ez) script.
    Uses a greedy, longest‑first matching algorithm to handle multi‑letter combinations.
    """

    def __init__(self):
        self.en_to_ti = {}          # Latin string -> Tigrinya character
        self._build_dictionaries()
        # Sort keys by length (longest first) for greedy matching
        self.sorted_en_keys = sorted(self.en_to_ti.keys(), key=len, reverse=True)

    def _build_dictionaries(self):
        """Build the Latin → Tigrinya mapping from consonant matrices."""
        # Vowel systems
        vowels_7 = {1: 'ä', 2: 'u', 3: 'i', 4: 'a', 5: 'e', 6: 'ə', 7: 'o'}
        vowels_8 = {**vowels_7, 8: 'wo'}
        vowels_gluetal = {1: 'wä', 3: 'wi', 4: 'wa', 5: 'we', 6: 'wə'}

        # Standard consonants (duplicate keys are overwritten by later entries)
        matrix_standard = {
            'h':   ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ', 'ሇ'],
            'l':   ['ለ', 'ሉ', 'ሊ', 'ላ', 'ሌ', 'ል', 'ሎ', 'ሏ'],
            'hh':  ['ሐ', 'ሑ', 'ሒ', 'ሓ', 'ሔ', 'ሕ', 'ሖ', 'ሗ'],
            'm':   ['መ', 'ሙ', 'ሚ', 'ማ', 'ሜ', 'ም', 'ሞ', 'ሟ'],
            's':   ['ሠ', 'ሡ', 'ሢ', 'ሣ', 'ሤ', 'ሥ', 'ሦ', 'ሧ'],   # archaic
            'r':   ['ረ', 'ሩ', 'ሪ', 'ራ', 'ሬ', 'ር', 'ሮ', 'ሯ'],
            's':   ['ሰ', 'ሱ', 'ሲ', 'ሳ', 'ሴ', 'ስ', 'ሶ', 'ሷ'],   # overwrites previous 's'
            'sh':  ['ሸ', 'ሹ', 'ሺ', 'ሻ', 'ሼ', 'ሽ', 'ሾ', 'ሿ'],
            'q':   ['ቀ', 'ቁ', 'ቂ', 'ቃ', 'ቄ', 'ቅ', 'ቆ', 'ቇ'],
            "q'":  ['ቐ', 'ቑ', 'ቒ', 'ቓ', 'ቔ', 'ቕ', 'ቖ', '\u1257'],
            'b':   ['በ', 'ቡ', 'ቢ', 'ባ', 'ቤ', 'ብ', 'ቦ', 'ቧ'],
            'v':   ['ቨ', 'ቩ', 'ቪ', 'ቫ', 'ቬ', 'ቭ', 'ቮ', 'ቯ'],
            't':   ['ተ', 'ቱ', 'ቲ', 'ታ', 'ቴ', 'ት', 'ቶ', 'ቷ'],
            'ch':  ['ቸ', 'ቹ', 'ቺ', 'ቻ', 'ቼ', 'ች', 'ቾ', 'ቿ'],
            'h':   ['ኀ', 'ኁ', 'ኂ', 'ኃ', 'ኄ', 'ኅ', 'ኆ', 'ኇ'],   # second 'h' overwrites first
            'n':   ['ነ', 'ኑ', 'ኒ', 'ና', 'ኔ', 'ን', 'ኖ', 'ኗ'],
            'ny':  ['ኘ', 'ኙ', 'ኚ', 'ኛ', 'ኜ', 'ኝ', 'ኞ', 'ኟ'],
            'ʼ':   ['አ', 'ኡ', 'ኢ', 'ኣ', 'ኤ', 'እ', 'ኦ', 'ኧ'],   # glottal stop
            'k':   ['ከ', 'ኩ', 'ኪ', 'ካ', 'ኬ', 'ክ', 'ኮ', 'ኯ'],
            'kh':  ['ኸ', 'ኹ', 'ኺ', 'ኻ', 'ኼ', 'ኽ', 'ኾ', '\u12bf'],
            'w':   ['ወ', 'ዉ', 'ዊ', 'ዋ', 'ዌ', 'ው', 'ዎ', 'ዏ'],
            'ʿ':   ['ዐ', 'ዑ', 'ዒ', 'ዓ', 'ዔ', 'ዕ', 'ዖ', '\u12d7'], # ayin
            'z':   ['ዘ', 'ዙ', 'ዚ', 'ዛ', 'ዜ', 'ዝ', 'ዞ', 'ዟ'],
            'zh':  ['ዠ', 'ዡ', 'ዢ', 'ዣ', 'ዤ', 'ዥ', 'ዦ', 'ዧ'],
            'y':   ['የ', 'ዩ', 'ዪ', 'ያ', 'ዬ', 'ይ', 'ዮ', 'ዯ'],
            'd':   ['ደ', 'ዱ', 'ዲ', 'ዳ', 'ዴ', 'ድ', 'ዶ', 'ዷ'],
            'dd':  ['ዸ', 'ዹ', 'ዺ', 'ዻ', 'ዼ', 'ዽ', 'ዾ', 'ዿ'],
            'j':   ['ጀ', 'ጁ', 'ጂ', 'ጃ', 'ጄ', 'ጅ', 'ጆ', 'ጇ'],
            'g':   ['ገ', 'ጉ', 'ጊ', 'ጋ', 'ጌ', 'ግ', 'ጎ', 'ጏ'],
            'ng':  ['ጘ', 'ጙ', 'ጚ', 'ጛ', 'ጜ', 'ጝ', 'ጞ', 'ጟ'],
            "t'":  ['ጠ', 'ጡ', 'ጢ', 'ጣ', 'ጤ', 'ጥ', 'ጦ', 'ጧ'],
            "ch'": ['ጨ', 'ጩ', 'ጪ', 'ጫ', 'ጬ', 'ጭ', 'ጮ', 'ጯ'],
            "p'":  ['ጰ', 'ጱ', 'ጲ', 'ጳ', 'ጴ', 'ጵ', 'ጶ', 'ጷ'],
            'ts':  ['ጸ', 'ጹ', 'ጺ', 'ጻ', 'ጼ', 'ጽ', 'ጾ', 'ጿ'],
            'ts':  ['ፀ', 'ፁ', 'ፂ', 'ፃ', 'ፄ', 'ፅ', 'ፆ', 'ፇ'],   # overwrites previous 'ts'
            'f':   ['ፈ', 'ፉ', 'ፊ', 'ፋ', 'ፌ', 'ፍ', 'ፎ', 'ፏ'],
            'p':   ['ፐ', 'ፑ', 'ፒ', 'ፓ', 'ፔ', 'ፕ', 'ፖ', 'ፗ'],
        }

        # Labialized consonants
        matrix_labial = {
            'qw':   ['ቈ', '', 'ቊ', 'ቋ', 'ቌ', 'ቍ'],
            "q'w":  ['ቘ', '', 'ቚ', 'ቛ', 'ቜ', 'ቝ'],
            'hw':   ['ኈ', '', 'ኊ', 'ኋ', 'ኌ', 'ኍ'],
            'kw':   ['ኰ', '', 'ኲ', 'ኳ', 'ኴ', 'ኵ'],
            'khw':  ['ዀ', '', 'ዂ', 'ዃ', 'ዄ', 'ዅ'],
            'gw':   ['ጐ', '', 'ጒ', 'ጓ', 'ጔ', 'ጕ'],
        }

        # Punctuation mapping (Ge'ez → Latin)
        punctuation_map = {
            '።': '.',
            '፣': ',',
            '፤': ';',
            '?': '?',
            '፨': ':',
        }

        # Build forward map (Ge'ez → Latin) first, then reverse it
        ti_to_en = {}

        # Standard consonants
        for cons, chars in matrix_standard.items():
            for i, char in enumerate(chars):
                order = i + 1
                if order in vowels_8:
                    ti_to_en[char] = cons + vowels_8[order]

        # Labialized consonants
        labial_indices = {0: 1, 2: 3, 3: 4, 4: 5, 5: 6}
        for cons, chars in matrix_labial.items():
            for list_idx, char in enumerate(chars):
                if char and list_idx in labial_indices:
                    v_order = labial_indices[list_idx]
                    suffix = vowels_gluetal[v_order]
                    clean_base = cons.replace('w', '')
                    ti_to_en[char] = clean_base + suffix

        # Punctuation
        for ti_char, en_char in punctuation_map.items():
            ti_to_en[ti_char] = en_char

        # Reverse to get Latin → Ge'ez (duplicate Latin keys are overwritten; last one wins)
        for ti_char, en_str in ti_to_en.items():
            self.en_to_ti[en_str] = ti_char

    def to_tigrinya(self, latin_text):
        """
        Convert a Latin (English) string to Tigrinya (Ge'ez) script.
        """
        if not latin_text:
            return ""
        text = latin_text.lower()
        result = []
        i = 0
        n = len(text)

        while i < n:
            matched = False
            for key in self.sorted_en_keys:
                if text.startswith(key, i):
                    result.append(self.en_to_ti[key])
                    i += len(key)
                    matched = True
                    break
            if not matched:
                # Keep original character (e.g., punctuation, numbers)
                result.append(latin_text[i])
                i += 1
        return ''.join(result)
