# Наборы символов
NUMBERS = "0123456789"
LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIAL_SYMBOLS = "!#$%&()*+,-./|:;<=>?@[]^_{}~"
AMBIGUOUS_SYMBOLS = "lIi10oO8,.;:"

# Cловари для работы с пресетами в UI
PRESET_DISPLAY_NAMES = {
    "fullstrong": "Полная защита",
    "easytoread": "Легко читается",
    "easytosay": "Легко сказать",
    "pincode": "PIN-код",
    "custom": "Свой"
}

# Словарь для обратного преобразования (из имени в UI в ключ)
REVERSE_PRESET_DISPLAY_NAMES = {v: k for k, v in PRESET_DISPLAY_NAMES.items()}

# Настройки пресетов
PRESETS_CONFIG = {
    "fullstrong": {
        "numbers": True, "lowercase": True, "uppercase": True, "special": True,
        "unique": True, "no_ambiguous": False, "start_with_letter": True,
        "length": 36
    },
    "easytoread": {
        "numbers": True, "lowercase": True, "uppercase": True, "special": False,
        "unique": True, "no_ambiguous": True, "start_with_letter": True,
        "length": 18
    },
    "easytosay": {
        "numbers": False, "lowercase": True, "uppercase": True, "special": False,
        "unique": False, "no_ambiguous": True, "start_with_letter": False,
        "length": 12
    },
    "pincode": {
        "numbers": True, "lowercase": False, "uppercase": False, "special": False,
        "unique": False, "no_ambiguous": False, "start_with_letter": False,
        "length": 4
    }
}