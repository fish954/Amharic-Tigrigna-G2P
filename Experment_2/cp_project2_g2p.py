import re
from collections import Counter
from typing import List
import os

g2p_mapping = {
    "ሀ": "he", "ሁ": "hu", "ሂ": "hi", "ሃ": "ha", "ሄ": "hE", "ህ": "h", "ሆ": "ho",
    "ለ": "le", "ሉ": "lu", "ሊ": "li", "ላ": "la", "ሌ": "lE", "ል": "l", "ሎ": "lo",
    "ሐ": "He", "ሑ": "Hu", "ሒ": "Hi", "ሓ": "Ha", "ሔ": "HE", "ሕ": "H", "ሖ": "Ho",
    "መ": "me", "ሙ": "mu", "ሚ": "mi", "ማ": "ma", "ሜ": "mE", "ም": "m", "ሞ": "mo",
    "ሠ": "'se", "ሡ": "'su", "ሢ": "'si", "ሣ": "'sa", "ሤ": "'sE", "ሥ": "'s", "ሦ": "'so",
    "ረ": "re", "ሩ": "ru", "ሪ": "ri", "ራ": "ra", "ሬ": "rE", "ር": "r", "ሮ": "ro",
    "ሰ": "se", "ሱ": "su", "ሲ": "si", "ሳ": "sa", "ሴ": "sE", "ስ": "s", "ሶ": "so",
    "ሸ": "xe", "ሹ": "xu", "ሺ": "xi", "ሻ": "xa", "ሼ": "xE", "ሽ": "x", "ሾ": "xo",
    "ቀ": "qe", "ቁ": "qu", "ቂ": "qi", "ቃ": "qa", "ቄ": "qE", "ቅ": "q", "ቆ": "qo",
    "ቐ": "Qe", "ቑ": "Qu", "ቒ": "Qi", "ቓ": "Qa", "ቔ": "QE", "ቕ": "Q", "ቖ": "Qo",
    "በ": "be", "ቡ": "bu", "ቢ": "bi", "ባ": "ba", "ቤ": "bE", "ብ": "b", "ቦ": "bo",
    "ቨ":"ve", "ቩ":"vu", "ቪ":"vi", "ቫ":"va", "ቬ":"vE", "ቭ":"v", "ቮ":"vo",
    "ተ": "te", "ቱ": "tu", "ቲ": "ti", "ታ": "ta", "ቴ": "tE", "ት": "t", "ቶ": "to",
    "ቸ": "ce", "ቹ": "cu", "ቺ": "ci", "ቻ": "ca", "ቼ": "cE", "ች": "c", "ቾ": "co",
    "ኀ": "'he", "ኁ": "'hu", "ኂ": "'hi", "ኃ": "'ha", "ኄ": "'hE", "ኅ": "'h", "ኆ": "'ho",
    "ነ": "ne", "ኑ": "nu", "ኒ": "ni", "ና": "na", "ኔ": "nE", "ን": "n", "ኖ": "no",
    "ኘ": "Ne", "ኙ": "Nu", "ኚ": "Ni", "ኛ": "Na", "ኜ": "NE", "ኝ": "N", "ኞ": "No",
    "አ": "e", "ኡ": "u", "ኢ": "i", "ኣ": "a", "ኤ": "e", "እ": "I", "ኦ": "o",
    "ከ": "ke", "ኩ": "ku", "ኪ": "ki", "ካ": "ka", "ኬ": "kE", "ክ": "k", "ኮ": "ko",
    "ኸ": "Ke", "ኹ": "Ku", "ኺ": "Ki", "ኻ": "Ka", "ኼ": "KE", "ኽ": "K", "ኾ": "Ko",
    "ወ": "we", "ዉ": "wu", "ዊ": "wi", "ዋ": "wa", "ዌ": "wE", "ው": "w", "ዎ": "wo",
    "ዐ": "ʿe", "ዑ": "ʿu", "ዒ": "ʿi", "ዓ": "ʿa", "ዔ": "ʿE", "ዕ": "ʿe", "ዖ": "ʿo",
    "ዘ": "ze", "ዙ": "zu", "ዚ": "zi", "ዛ": "za", "ዜ": "zE", "ዝ": "z", "ዞ": "zo",
    "ዠ": "Ze", "ዡ": "Zu", "ዢ": "Zi", "ዣ": "Za", "ዤ": "ZE", "ዥ": "Z", "ዦ": "Zo",
    "የ": "ye", "ዩ": "yu", "ዪ": "yi", "ያ": "ya", "ዬ": "yE", "ይ": "y", "ዮ": "yo",
    "ደ": "de", "ዱ": "du", "ዲ": "di", "ዳ": "da", "ዴ": "dE", "ድ": "d", "ዶ": "do",
    "ዸ":"De", "ዹ":"Du", "ዺ":"Di", "ዻ":"Da", "ዼ":"DE", "ዽ":"D", "ዾ":"Do",
    "ጀ": "je", "ጁ": "ju", "ጂ": "ji", "ጃ": "ja", "ጄ": "jE", "ጅ": "j", "ጆ": "jo",
    "ገ": "ge", "ጉ": "gu", "ጊ": "gi", "ጋ": "ga", "ጌ": "gE", "ግ": "g", "ጎ": "go",
    "ጠ": "Te", "ጡ": "Tu", "ጢ": "Ti", "ጣ": "Ta", "ጤ": "TE", "ጥ": "T", "ጦ": "To",
    "ጨ": "Ce", "ጩ": "Cu", "ጪ": "Ci", "ጫ": "Ca", "ጬ": "CE", "ጭ": "C", "ጮ": "Co",
    "ጰ": "Pe", "ጱ": "Pu", "ጲ": "Pi", "ጳ": "Pa", "ጴ": "PE", "ጵ": "P", "ጶ": "Po",
    "ጸ": "Se", "ጹ": "Su", "ጺ": "Si", "ጻ": "Sa", "ጼ": "SE", "ጽ": "S", "ጾ": "So",
    "ፀ": "'Se", "ፁ": "'Su", "ፂ": "'Si", "ፃ": "'Sa", "ፄ": "'SE", "ፅ": "'S", "ፆ": "'So",
    "ፈ": "fe", "ፉ": "fu", "ፊ": "fi", "ፋ": "fa", "ፌ": "fE", "ፍ": "f", "ፎ": "fo",
    "ፐ": "pe", "ፑ": "pu", "ፒ": "pi", "ፓ": "pa", "ፔ": "pE", "ፕ": "p", "ፖ": "po",
    "ሇ":"hWa", "ሏ":"lWa", "ሗ":"HWa", "ሟ":"mWa", "ሧ":"'sWa", "ሯ":"rWa", "ሷ":"sWa",
    "ሿ":"xWa", "ቈ":"qWe", "ቊ":"qWi", "ቋ":"qWa", "ቌ":"qWe", "ቍ":"qW", "ቘ":"QWe", "ቚ":"QWi", 
    "ቛ":"QWa", "ቜ":"QWe", "ቝ":"QW", "ቧ":"bWa", "ቯ":"vWa", "ቷ":"tWa", "ቿ":"cWa",
    "ኈ":"hWe", "ኊ":"hWi", "ኋ":"hWa", "ኌ":"hWE", "ኍ":"hWu", "ኇ":"hW", "ኗ":"nWa", "ኟ":"NWa",
    "ኧ":"ea", "ኰ":"kWe", "ኲ":"kWu", "ኵ":"kWi", "ኳ":"kWa", "ኴ":"kWE", "ኯ":"kW", "ዀ":"KWe",
    "ዂ":"KWu", "ዅ": "KWi", "ዃ":"KWa", "ዄ":"KWE", "ዏ":"wWa", "ዟ":"zWa", "ዧ":"ZWa", "ዯ":"yWa",
    "ዷ":"dWa", "ዿ":"DWa", "ጇ":"jWa", "ጐ":"gWe", "ጕ":"gWu", "ጒ":"gWi", "ጓ":"gWa", "ጔ":"gWE", "ጏ":"gW",
    "ጧ":"TWa", "ጯ":"CWa", "ጷ":"PWa", "ጿ":"SWa", "ፏ":"fWa", "ፗ":"pWa", "ፇ":"'SWa", " ":" ", "\n":"\n"

    # Reads text from file
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
        
# Writes text to file
def write_output_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)
        
# Formats Counter into string
def counter_to_string(counter):
    return '\n'.join([f'{k}:{v}' for k, v in counter.items()])
    
# Clean and preprocess text
def preprocess_text(text: str):
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = text.strip()
    return text
    
# Word frequency
def word_frequency(text: str):
    words = text.split()
    return Counter(words)
    
# Overlap score for words
def word_overlap(freq1: Counter, freq2: Counter):
    common_words = set(freq1.keys()) & set(freq2.keys())
    total_words = set(freq1.keys()) | set(freq2.keys())
    if not total_words:
        return 0.0
    return len(common_words) / len(total_words)

# Grapheme-to-phoneme conversion (space-separated for accurate phoneme splitting)
def g2p(text: str):
    phonemes = []
    for char in text:
        phonemes.append(g2p_mapping.get(char, char))
    return ' '.join(phonemes)  # Use space to preserve phoneme boundaries

# Count full phoneme units
def phoneme_distribution(phoneme_str: str):
    return Counter(phoneme_str.split())

# Overlap score for phonemes
def phoneme_overlap(dist1: Counter, dist2: Counter):
    common_phonemes = set(dist1.keys()) & set(dist2.keys())
    total_phonemes = set(dist1.keys()) | set(dist2.keys())
    if not total_phonemes:
        return 0.0
    return len(common_phonemes) / len(total_phonemes)

# === File paths ===
assets_dir = r'CP_Project\Experiment_2\assets2'

amharic_file_path = os.path.join(assets_dir, 'amharic2.txt')
tigrinya_file_path = os.path.join(assets_dir, 'tigrinya2.txt')
