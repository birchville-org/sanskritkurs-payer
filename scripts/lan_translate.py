import os
import json
import urllib.request
import time
import sys
import re
import datetime
import hashlib

# Configuration
API_URL = "http://nyx.local:8088/v1/chat/completions"
MODEL = "mlx-community--Qwen3.6-35B-A3B-4bit"
LANGUAGES = [
    "en", "it", "es", "ru", "uk", "bg", "hi", "fr", "ta", "pa",
    "la", "rm", "ro", "id", "zh-CN", "he", "ar", "arc",
    "th", "el", "cop", "grc", "fa", "nl", "af", "lt", "sh", "sq", "akk", "am", "gez"
]
LANG_NAMES = {
    "en": "English", "it": "Italian", "es": "Spanish",
    "ru": "Russian", "uk": "Ukrainian", "bg": "Bulgarian",
    "hi": "Hindi", "fr": "French", "ta": "Tamil", "pa": "Punjabi (Gurmukhi)",
    "la": "Latin", "rm": "Romansh Grischun", "ro": "Romanian",
    "id": "Indonesian", "zh-CN": "Simplified Chinese",
    "th": "Thai", "he": "Hebrew",
    "ar": "Arabic", "arc": "Aramaic",
#    "zh": "Mandarin Chinese",
    "grc": "Ancient Greek", "el": "Modern Greek", "am": "Amharic", "gez": "Ge\'ez",
    "fa": "Persian (Farsi)", "akk": "Akkadian", "cop": "Coptic",
}
LESSONS = list(range(1, 62))
MAIN_PAGES = ["index.md", "grammatik.md", "themen.md", "impressum.md"]

# licenses.md is handled by generate_licenses() — not via LLM — because it
# contains critical HTML anchors and image markdown that LLMs corrupt.
LICENSES_LABELS = {
    "en": {
        "title": "Image License Audit",
        "col1": "File", "col2": "Found Source Information", "col3": "Preview",
        "no_license": "No specific license/image source found in text",
    },
    "it": {
        "title": "Verifica delle licenze delle immagini",
        "col1": "File", "col2": "Informazione sulla fonte trovata", "col3": "Anteprima",
        "no_license": "Nessuna licenza specifica/fonte dell'immagine trovata nel testo",
    },
    "es": {
        "title": "Auditoría de licencias de imágenes",
        "col1": "Archivo", "col2": "Información de fuente encontrada", "col3": "Vista previa",
        "no_license": "No se encontró licencia específica/fuente de imagen en el texto",
    },
    "ru": {
        "title": "Аудит лицензий на изображения",
        "col1": "Файл", "col2": "Найденная информация об источнике", "col3": "Предпросмотр",
        "no_license": "В тексте не найдена конкретная лицензия/источник изображения",
    },
    "uk": {
        "title": "Аудит ліцензій на зображення",
        "col1": "Файл", "col2": "Знайдена інформація про джерело", "col3": "Перегляд",
        "no_license": "У тексті не знайдено конкретної ліцензії/джерела зображення",
    },
    "bg": {
        "title": "Одит на лицензите на изображенията",
        "col1": "Файл", "col2": "Намерена информация за източника", "col3": "Преглед",
        "no_license": "В текста не е намерен конкретен лиценз/източник на изображението",
    },
    "hi": {
        "title": "छवि लाइसेंस ऑडिट",
        "col1": "फ़ाइल", "col2": "पाई गई स्रोत जानकारी", "col3": "पूर्वावलोकन",
        "no_license": "पाठ में कोई विशिष्ट लाइसेंस/छवि स्रोत नहीं मिला",
    },
    "fr": {
        "title": "Audit des licences d'images",
        "col1": "Fichier", "col2": "Informations sur la source trouvées", "col3": "Aperçu",
        "no_license": "Aucune licence spécifique/source d'image trouvée dans le texte",
    },
    "rm": {
        "title": "Audit da licenzas d'immagins",
        "col1": "Datoteca", "col2": "Infurmaziun da la funtauna chattada", "col3": "Prevista",
        "no_license": "Nagina licenza speziala/funtauna d'immagina chattada en il text",
    },
    "ta": {
        "title": "படப் உரிம தணிக்கை",
        "col1": "கோப்பு", "col2": "கண்டறியப்பட்ட மூல தகவல்", "col3": "முன்னோட்டம்",
        "no_license": "உரையில் குறிப்பிட்ட உரிமம்/படத்தின் மூலம் காணப்படவில்லை",
    },
    "pa": {
        "title": "ਚਿੱਤਰ ਲਾਇਸੈਂਸ ਆਡਿਟ",
        "col1": "ਫ਼ਾਇਲ", "col2": "ਮਿਲੀ ਸਰੋਤ ਜਾਣਕਾਰੀ", "col3": "ਝਲਕ",
        "no_license": "ਪਾਠ ਵਿੱਚ ਕੋਈ ਖਾਸ ਲਾਇਸੈਂਸ/ਚਿੱਤਰ ਸਰੋਤ ਨਹੀਂ ਮਿਲਿਆ",
    },
    "ar": {
        "title": "تدقيق تراخيص الصور",
        "col1": "ملف", "col2": "معلومات المصدر الموجودة", "col3": "معاينة",
        "no_license": "لم يُعثر على ترخيص/مصدر صورة محدد في النص",
    },
    "arc": {
        "title": "ܒܘܩܪܐ ܕܙܕܩ̈ܐ ܕܨܘܪ̈ܐ",
        "col1": "ܣܕܪܐ", "col2": "ܡܘܕܥܢܘܬܐ ܕܡܩܘܪܐ ܕܐܫܬܟܚ", "col3": "ܚܙܝܐ",
        "no_license": "ܠܐ ܐܫܬܟܚ ܙܕܩܐ ܦܪܝܫܐ ܐܘ ܡܩܘܪܐ ܕܨܘܪܐ ܒܟܬܒܐ",
    },
    "he": {
        "title": "ביקורת רישיונות תמונות",
        "col1": "קובץ", "col2": "מידע מקור שנמצא", "col3": "תצוגה מקדימה",
        "no_license": "לא נמצא רישיון/מקור תמונה ספציפי בטקסט",
    },
    "zh-CN": {
        "title": "图片许可证审计",
        "col1": "文件", "col2": "找到的来源信息", "col3": "预览",
        "no_license": "文本中未找到特定许可证/图片来源",
    },
    "zh-TW": {
        "title": "圖片授權審計",
        "col1": "檔案", "col2": "找到的來源資訊", "col3": "預覽",
        "no_license": "文本中未找到特定授權/圖片來源",
    },
    "th": {
        "title": "การตรวจสอบใบอนุญาตภาพ",
        "col1": "ไฟล์", "col2": "ข้อมูลแหล่งที่มาที่พบ", "col3": "พรีวิว",
        "no_license": "ไม่พบใบอนุญาตเฉพาะ/แหล่งที่มาของภาพในข้อความ",
    },
    "ro": {
        "title": "Auditul licențelor imaginilor",
        "col1": "Fișier", "col2": "Informații despre sursă găsite", "col3": "Previzualizare",
        "no_license": "Nu s-a găsit nicio licență/sursă specifică de imagine în text",
    },
    "la": {
        "title": "Recognitio Licentiarium Imaginum",
        "col1": "Fasciculus", "col2": "Notitia Fontis Inventa", "col3": "Prospectus",
        "no_license": "Nulla licentia specialis nec fons imaginis in textu inventus",
    },
    "grc": {
        "title": "Ἔλεγχος Ἀδειῶν Εἰκόνων",
        "col1": "Ἀρχεῖον", "col2": "Εὑρεθεῖσα Πληροφορία Πηγῆς", "col3": "Προεπισκόπησις",
        "no_license": "Οὐδεμία εἰδικὴ ἄδεια οὐδὲ πηγὴ εἰκόνος εὑρέθη ἐν τῷ κειμένῳ",
    },
    "am": {
        "title": "የሳንስክሪት ኮርስ",
        "author": "Alois Payer",
        "description": "የሳንስክሪት ሰዋሰው መማሪያ መጽሐፍ",
        "lesson": "ትምህርት",
        "script": "ጽሑፍ",
        "exercise": "መልመጃ"
    },
    "gez": {
        "title": "ትምህርተ ሳንስክሪት",
        "author": "Alois Payer",
        "description": "መጽሐፈ ሰዋስው ዘሳንስክሪት",
        "lesson": "ትምህርት",
        "script": "ጽሑፍ",
        "exercise": "መልመጃ"
    },
    "el": {
        "title": "Έλεγχος Αδειών Εικόνων",
        "col1": "Αρχείο", "col2": "Βρέθηκαν πληροφορίες πηγής", "col3": "Προεπισκόπηση",
        "no_license": "Δεν βρέθηκε συγκεκριμένη άδεια/πηγή εικόνας στο κείμενο",
    },
    "fa": {
        "title": "ممیزی مجوزهای تصویر",
        "col1": "پرونده", "col2": "اطلاعات منبع یافت‌شده", "col3": "پیش‌نمایش",
        "no_license": "هیچ مجوز/منبع تصویر خاصی در متن یافت نشد",
    },
    "akk": {
        "title": "Bāru ša Lišānāt ṣalmī",
        "col1": "Ṭuppu", "col2": "Qibītu ša ašartu ša immarū", "col3": "Tamāru",
        "no_license": "Lā immarū lišānum pariṣtum ša ṣalmu ina ṭuppi",
    },
    "cop": {
        "title": "ⲡⲓⲉⲣⲏⲧ ⲛ̀ⲛⲓϩⲓⲥⲓ ⲛ̀ϩⲁⲛϩⲓⲕⲱⲛ",
        "col1": "ⲫⲁⲓ", "col2": "ⲫⲓⲙⲁ ⲉⲧⲁϥϭⲓ ⲛ̀ⲥⲱϥ", "col3": "ⲡⲓⲛⲓⲁⲩ",
        "no_license": "ⲙⲡⲉⲛϭⲓⲙⲓ ⲛ̀ⲟⲩⲛⲓϣϯ ⲛ̀ϩⲓⲥⲓ ⲉⲩⲁⲗⲏⲑⲉⲓⲁ ϩⲛ̀ ⲡⲓⲥϧⲁⲓ",
    },
    "id": {
        "title": "Audit Lisensi Gambar",
        "col1": "File", "col2": "Informasi Sumber yang Ditemukan", "col3": "Pratinjau",
        "no_license": "Tidak ada lisensi spesifik/sumber gambar yang ditemukan dalam teks",
    },
}
LICENSES_PHRASES = {
    "en": {
        "Abb.:": "Fig.:",
        "Bildquelle:": "Image source:",
        "Bildquelle.": "Image source.",
        "Bildquelle ": "Image source ",
        "gemeinfrei": "public domain",
        "Jhdt.": "cent.",
        "Zugriff am": "accessed",
        "Namensnennung": "Attribution",
        "keine kommerzielle Nutzung": "NonCommercial",
        "keine kommerzielle Nuttzung": "NonCommercial",
        "keine kommerzielle Bearbeitung": "NonCommercial NoDerivatives",
        "keine Bearbeitung": "NoDerivatives",
        "GNU FDLizenz": "GNU FD License",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Creative Commons License",
        "Creative Commons Lizenz": "Creative Commons License",
        "Creative Commons lizenz": "Creative Commons License",
        "Creative Commons lizenz": "Creative Commons License",
        "Unbekannt": "Unknown",
        "Beschriftung:": "Caption:",
        "Lehrgangsmaterial": "Course material",
    },
    "it": {
        "Abb.:": "Fig.:",
        "Bildquelle:": "Fonte:",
        "Bildquelle.": "Fonte.",
        "Bildquelle ": "Fonte ",
        "gemeinfrei": "pubblico dominio",
        "Jhdt.": "sec.",
        "Zugriff am": "consultato il",
        "Namensnennung": "Attribuzione",
        "keine kommerzielle Nutzung": "NonCommerciale",
        "keine kommerzielle Nuttzung": "NonCommerciale",
        "keine kommerzielle Bearbeitung": "NonCommerciale Senza opere derivate",
        "keine Bearbeitung": "Non opere derivate",
        "GNU FDLizenz": "Licenza GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Licenza Creative Commons",
        "Creative Commons Lizenz": "Licenza Creative Commons",
        "Creative Commons lizenz": "Licenza Creative Commons",
        "Unbekannt": "Sconosciuto",
        "Beschriftung:": "Didascalia:",
        "Lehrgangsmaterial": "Materiale del corso",
    },
    "es": {
        "Abb.:": "Fig.:",
        "Bildquelle:": "Fuente:",
        "Bildquelle.": "Fuente.",
        "Bildquelle ": "Fuente ",
        "gemeinfrei": "dominio público",
        "Jhdt.": "s.",
        "Zugriff am": "consultado el",
        "Namensnennung": "Atribución",
        "keine kommerzielle Nutzung": "NoComercial",
        "keine kommerzielle Nuttzung": "NoComercial",
        "keine kommerzielle Bearbeitung": "NoComercial SinDerivadas",
        "keine Bearbeitung": "SinDerivadas",
        "GNU FDLizenz": "Licencia GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Licencia Creative Commons",
        "Creative Commons Lizenz": "Licencia Creative Commons",
        "Creative Commons lizenz": "Licencia Creative Commons",
        "Unbekannt": "Desconocido",
        "Beschriftung:": "Leyenda:",
        "Lehrgangsmaterial": "Material del curso",
    },
    "ru": {
        "Abb.:": "Рис.:",
        "Bildquelle:": "Источник:",
        "Bildquelle.": "Источник.",
        "Bildquelle ": "Источник ",
        "gemeinfrei": "общественное достояние",
        "Jhdt.": "в.",
        "Zugriff am": "дата обращения:",
        "Namensnennung": "Указание авторства",
        "keine kommerzielle Nutzung": "некоммерческое использование",
        "keine kommerzielle Bearbeitung": "некоммерческое без производных",
        "keine kommerzielle Nuttzung": "некоммерческое использование",
        "keine Bearbeitung": "без производных",
        "GNU FDLizenz": "лицензия GNU FD",
        "FDLicense": "лицензия FD",
        "Creative  Commons Lizenz": "лицензия Creative Commons",
        "Creative Commons Lizenz": "лицензия Creative Commons",
        "Creative Commons lizenz": "лицензия Creative Commons",
        "Unbekannt": "Неизвестно",
        "Beschriftung:": "Подпись:",
        "Lehrgangsmaterial": "Учебные материалы",
    },
    "uk": {
        "Abb.:": "Рис.:",
        "Bildquelle:": "Джерело:",
        "Bildquelle.": "Джерело.",
        "Bildquelle ": "Джерело ",
        "gemeinfrei": "суспільне надбання",
        "Jhdt.": "ст.",
        "Zugriff am": "дата звернення:",
        "Namensnennung": "Зазначення авторства",
        "keine kommerzielle Nutzung": "некомерційне використання",
        "keine kommerzielle Nuttzung": "некомерційне використання",
        "keine kommerzielle Bearbeitung": "некомерційне без похідних",
        "keine Bearbeitung": "без похідних",
        "GNU FDLizenz": "ліцензія GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "ліцензія Creative Commons",
        "Creative Commons Lizenz": "ліцензія Creative Commons",
        "Creative Commons lizenz": "ліцензія Creative Commons",
        "Unbekannt": "Невідомо",
        "Beschriftung:": "Підпис:",
        "Lehrgangsmaterial": "Навчальні матеріали",
    },
    "bg": {
        "Abb.:": "Ил.:",
        "Bildquelle:": "Източник:",
        "Bildquelle.": "Източник.",
        "Bildquelle ": "Източник ",
        "gemeinfrei": "обществено достояние",
        "Jhdt.": "в.",
        "Zugriff am": "достъп на",
        "Namensnennung": "Признание",
        "keine kommerzielle Nutzung": "Некомерсиално",
        "keine kommerzielle Nuttzung": "Некомерсиално",
        "keine kommerzielle Bearbeitung": "Некомерсиално Без производни",
        "keine Bearbeitung": "Без производни",
        "GNU FDLizenz": "GNU FD лиценз",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Лиценз Creative Commons",
        "Creative Commons Lizenz": "Лиценз Creative Commons",
        "Creative Commons lizenz": "Лиценз Creative Commons",
        "Unbekannt": "Неизвестен",
        "Beschriftung:": "Надпис:",
        "Lehrgangsmaterial": "Учебен материал",
    },
    "hi": {
        "Abb.:": "चित्र.:",
        "Bildquelle:": "छवि स्रोत:",
        "Bildquelle.": "छवि स्रोत.",
        "Bildquelle ": "छवि स्रोत ",
        "gemeinfrei": "सार्वजनिक डोमेन",
        "Jhdt.": "शती.",
        "Zugriff am": "अभिगमन तिथि",
        "Namensnennung": "श्रेय",
        "keine kommerzielle Nutzung": "गैर-व्यावसायिक",
        "keine kommerzielle Nuttzung": "गैर-व्यावसायिक",
        "keine kommerzielle Bearbeitung": "गैर-व्यावसायिक, व्युत्पन्न नहीं",
        "keine Bearbeitung": "व्युत्पन्न नहीं",
        "GNU FDLizenz": "GNU FD लाइसेंस",
        "FDLicense": "FD लाइसेंस",
        "Creative  Commons Lizenz": "क्रिएटिव कॉमन्स लाइसेंस",
        "Creative Commons Lizenz": "क्रिएटिव कॉमन्स लाइसेंस",
        "Creative Commons lizenz": "क्रिएटिव कॉमन्स लाइसेंस",
        "Unbekannt": "अज्ञात",
        "Beschriftung:": "शीर्षक:",
        "Lehrgangsmaterial": "पाठ्यक्रम सामग्री",
    },
    "fr": {
        "Abb.:": "Fig.:",
        "Bildquelle:": "Source:",
        "Bildquelle.": "Source.",
        "Bildquelle ": "Source ",
        "gemeinfrei": "domaine public",
        "Jhdt.": "s.",
        "Zugriff am": "consulté le",
        "Namensnennung": "Attribution",
        "keine kommerzielle Nutzung": "NonCommercial",
        "keine kommerzielle Nuttzung": "NonCommercial",
        "keine kommerzielle Bearbeitung": "NonCommercial SansŒuvresDerivées",
        "keine Bearbeitung": "SansOeuvresDerivées",
        "GNU FDLizenz": "Licence GNU FD",
        "FDLicense": "Licence FD",
        "Creative  Commons Lizenz": "Licence Creative Commons",
        "Creative Commons Lizenz": "Licence Creative Commons",
        "Creative Commons lizenz": "Licence Creative Commons",
        "Unbekannt": "Inconnu",
        "Beschriftung:": "Légende:",
        "Lehrgangsmaterial": "Matériel pédagogique",
    },
    "rm": {
        "Abb.:": "Fig.:",
        "Bildquelle:": "Funtauna:",
        "Bildquelle.": "Funtauna.",
        "Bildquelle ": "Funtauna ",
        "gemeinfrei": "domini public",
        "Jhdt.": "sec.",
        "Zugriff am": "visità ils",
        "Namensnennung": "Attribuziun",
        "keine kommerzielle Nutzung": "NonCommercial",
        "keine kommerzielle Nuttzung": "NonCommercial",
        "keine kommerzielle Bearbeitung": "NonCommercial NingRielaboraziun",
        "keine Bearbeitung": "NingRielaboraziun",
        "GNU FDLizenz": "Licenza GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Licenza Creative Commons",
        "Creative Commons Lizenz": "Licenza Creative Commons",
        "Creative Commons lizenz": "Licenza Creative Commons",
        "Unbekannt": "Nunenconuschent",
        "Beschriftung:": "Descriziun:",
        "Lehrgangsmaterial": "Material da cors",
    },
    "ta": {
        "Abb.:": "படம்.:",
        "Bildquelle:": "படமூலம்:",
        "Bildquelle.": "படமூலம்.",
        "Bildquelle ": "படமூலம் ",
        "gemeinfrei": "பொது உரிமம்",
        "Jhdt.": "நூ.",
        "Zugriff am": "அணுகிய தேதி",
        "Namensnennung": "பங்களிப்பு",
        "keine kommerzielle Nutzung": "வணிகமற்றது",
        "keine kommerzielle Nuttzung": "வணிகமற்றது",
        "keine kommerzielle Bearbeitung": "வணிகமற்றது, வழித்தோன்றல் இல்லை",
        "keine Bearbeitung": "வழித்தோன்றல் இல்லை",
        "GNU FDLizenz": "GNU FD உரிமம்",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Creative Commons உரிமம்",
        "Creative Commons Lizenz": "Creative Commons உரிமம்",
        "Creative Commons lizenz": "Creative Commons உரிமம்",
        "Unbekannt": "தெரியாத",
        "Beschriftung:": "தலைப்பு:",
        "Lehrgangsmaterial": "பாட திட்ட பொருள்",
    },
    "pa": {
        "Abb.:": "ਚਿੱਤ.:",
        "Bildquelle:": "ਚਿੱਤਰ ਸਰੋਤ:",
        "Bildquelle.": "ਚਿੱਤਰ ਸਰੋਤ.",
        "Bildquelle ": "ਚਿੱਤਰ ਸਰੋਤ ",
        "gemeinfrei": "ਜਨਤਕ ਡੋਮੇਨ",
        "Jhdt.": "ਸਦੀ.",
        "Zugriff am": "ਪਹੁੰਚ ਦੀ ਮਿਤੀ",
        "Namensnennung": "ਨਾਮਕਰਨ",
        "keine kommerzielle Nutzung": "ਗੈਰ-ਵਪਾਰਕ",
        "keine kommerzielle Nuttzung": "ਗੈਰ-ਵਪਾਰਕ",
        "keine kommerzielle Bearbeitung": "ਗੈਰ-ਵਪਾਰਕ, ਕੋਈ ਡੈਰੀਵੇਟਿਵ ਨਹੀਂ",
        "keine Bearbeitung": "ਕੋਈ ਡੈਰੀਵੇਟਿਵ ਨਹੀਂ",
        "GNU FDLizenz": "GNU FD ਲਾਇਸੈਂਸ",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Creative Commons ਲਾਇਸੈਂਸ",
        "Creative Commons Lizenz": "Creative Commons ਲਾਇਸੈਂਸ",
        "Creative Commons lizenz": "Creative Commons ਲਾਇਸੈਂਸ",
        "Unbekannt": "ਅਣਜਾਣ",
        "Beschriftung:": "ਕੈਪਸ਼ਨ:",
        "Lehrgangsmaterial": "ਕੋਰਸ ਸਮੱਗਰੀ",
    },
    "ar": {
        "Abb.:": "شكل.:",
        "Bildquelle:": "مصدر الصورة:",
        "Bildquelle.": "مصدر الصورة.",
        "Bildquelle ": "مصدر الصورة ",
        "gemeinfrei": "نطاق عام",
        "Jhdt.": "ق.",
        "Zugriff am": "تاريخ الوصول",
        "Namensnennung": "نسب العمل",
        "keine kommerzielle Nutzung": "غير تجاري",
        "keine kommerzielle Nuttzung": "غير تجاري",
        "keine kommerzielle Bearbeitung": "غير تجاري بلا مشتقات",
        "keine Bearbeitung": "بلا مشتقات",
        "GNU FDLizenz": "رخصة GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "رخصة المشاع الإبداعي",
        "Creative Commons Lizenz": "رخصة المشاع الإبداعي",
        "Creative Commons lizenz": "رخصة المشاع الإبداعي",
        "Unbekannt": "مجهول",
        "Beschriftung:": "تسمية توضيحية:",
        "Lehrgangsmaterial": "مواد الدورة",
    },
    "arc": {
        "Abb.:": "ܨܘܪ.:",
        "Bildquelle:": "ܡܩܘܪܐ ܕܨܘܪܐ:",
        "Bildquelle.": "ܡܩܘܪܐ ܕܨܘܪܐ.",
        "Bildquelle ": "ܡܩܘܪܐ ܕܨܘܪܐ ",
        "gemeinfrei": "ܩܢܝܢܐ ܕܟܠܢ",
        "Jhdt.": "ܩ.",
        "Zugriff am": "ܡܛܝܬܐ ܒ",
        "Namensnennung": "ܝܗܒܬ ܫܡܐ",
        "keine kommerzielle Nutzung": "ܠܐ ܬܓܪܝܐ",
        "keine kommerzielle Nuttzung": "ܠܐ ܬܓܪܝܐ",
        "keine kommerzielle Bearbeitung": "ܠܐ ܬܓܪܝܐ ܒܠܐ ܦܪ̈ܥܐ",
        "keine Bearbeitung": "ܒܠܐ ܦܪ̈ܥܐ",
        "GNU FDLizenz": "ܙܕܩܐ GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "ܙܕܩܐ Creative Commons",
        "Creative Commons Lizenz": "ܙܕܩܐ Creative Commons",
        "Creative Commons lizenz": "ܙܕܩܐ Creative Commons",
        "Unbekannt": "ܠܐ ܝܕܝܥܐ",
        "Beschriftung:": "ܟܬܒܬܐ:",
        "Lehrgangsmaterial": "ܣܝܡ̈ܬܐ ܕܝܘܠܦܢܐ",
    },
    "he": {
        "Abb.:": "איור.:",
        "Bildquelle:": "מקור תמונה:",
        "Bildquelle.": "מקור תמונה.",
        "Bildquelle ": "מקור תמונה ",
        "gemeinfrei": "נחלת הכלל",
        "Jhdt.": "מאה",
        "Zugriff am": "תאריך גישה",
        "Namensnennung": "ייחוס",
        "keine kommerzielle Nutzung": "לא מסחרי",
        "keine kommerzielle Nuttzung": "לא מסחרי",
        "keine kommerzielle Bearbeitung": "לא מסחרי ללא נגזרות",
        "keine Bearbeitung": "ללא נגזרות",
        "GNU FDLizenz": "רישיון GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "רישיון Creative Commons",
        "Creative Commons Lizenz": "רישיון Creative Commons",
        "Creative Commons lizenz": "רישיון Creative Commons",
        "Unbekannt": "לא ידוע",
        "Beschriftung:": "כיתוב:",
        "Lehrgangsmaterial": "חומר לימוד",
    },
    "zh-CN": {
        "Abb.:": "图.:",
        "Bildquelle:": "图片来源:",
        "Bildquelle.": "图片来源.",
        "Bildquelle ": "图片来源 ",
        "gemeinfrei": "公共领域",
        "Jhdt.": "世纪",
        "Zugriff am": "访问日期",
        "Namensnennung": "署名",
        "keine kommerzielle Nutzung": "非商业性使用",
        "keine kommerzielle Nuttzung": "非商业性使用",
        "keine kommerzielle Bearbeitung": "非商业性使用，禁止演绎",
        "keine Bearbeitung": "禁止演绎",
        "GNU FDLizenz": "GNU FD许可证",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "知识共享许可证",
        "Creative Commons Lizenz": "知识共享许可证",
        "Creative Commons lizenz": "知识共享许可证",
        "Unbekannt": "未知",
        "Beschriftung:": "说明:",
        "Lehrgangsmaterial": "课程材料",
    },
    "th": {
        "Abb.:": "รูป.:",
        "Bildquelle:": "ที่มาของภาพ:",
        "Bildquelle.": "ที่มาของภาพ.",
        "Bildquelle ": "ที่มาของภาพ ",
        "gemeinfrei": "สาธารณสมบัติ",
        "Jhdt.": "ศตวรรษ",
        "Zugriff am": "วันที่เข้าถึง",
        "Namensnennung": "การแสดงที่มา",
        "keine kommerzielle Nutzung": "ไม่ใช้เพื่อการค้า",
        "keine kommerzielle Nuttzung": "ไม่ใช้เพื่อการค้า",
        "keine kommerzielle Bearbeitung": "ไม่ใช้เพื่อการค้า ห้ามดัดแปลง",
        "keine Bearbeitung": "ห้ามดัดแปลง",
        "GNU FDLizenz": "ใบอนุญาต GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "ใบอนุญาต Creative Commons",
        "Creative Commons Lizenz": "ใบอนุญาต Creative Commons",
        "Creative Commons lizenz": "ใบอนุญาต Creative Commons",
        "Unbekannt": "ไม่ทราบ",
        "Beschriftung:": "คำบรรยาย:",
        "Lehrgangsmaterial": "เอกสารประกอบการเรียน",
    },
    "la": {
        "Abb.:": "Fig.:",
        "Bildquelle:": "Fons imaginis:",
        "Bildquelle.": "Fons imaginis.",
        "Bildquelle ": "Fons imaginis ",
        "gemeinfrei": "in publico dominio",
        "Jhdt.": "saec.",
        "Zugriff am": "accessus die",
        "Namensnennung": "Attributio",
        "keine kommerzielle Nutzung": "usus non mercatorius",
        "keine kommerzielle Nuttzung": "usus non mercatorius",
        "keine kommerzielle Bearbeitung": "usus non mercatorius sine derivatis",
        "keine Bearbeitung": "sine derivatis",
        "GNU FDLizenz": "Licentia GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Licentia Creative Commons",
        "Creative Commons Lizenz": "Licentia Creative Commons",
        "Creative Commons lizenz": "Licentia Creative Commons",
        "Unbekannt": "Ignotum",
        "Beschriftung:": "Titulus:",
        "Lehrgangsmaterial": "Materia cursus",
    },
    "grc": {
        "Abb.:": "Εἰκ.:",
        "Bildquelle:": "Πηγὴ εἰκόνος:",
        "Bildquelle.": "Πηγὴ εἰκόνος.",
        "Bildquelle ": "Πηγὴ εἰκόνος ",
        "gemeinfrei": "δημόσιον κτῆμα",
        "Jhdt.": "αἰ.",
        "Zugriff am": "πρόσβασις τῇ",
        "Namensnennung": "Ἀπόδοσις",
        "keine kommerzielle Nutzung": "οὐκ ἐμπορική",
        "keine kommerzielle Nuttzung": "οὐκ ἐμπορική",
        "keine kommerzielle Bearbeitung": "οὐκ ἐμπορική, ἄνευ παραγώγων",
        "keine Bearbeitung": "ἄνευ παραγώγων",
        "GNU FDLizenz": "Ἄδεια GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Ἄδεια Creative Commons",
        "Creative Commons Lizenz": "Ἄδεια Creative Commons",
        "Creative Commons lizenz": "Ἄδεια Creative Commons",
        "Unbekannt": "Ἄγνωστον",
        "Beschriftung:": "Ἐπιγραφή:",
        "Lehrgangsmaterial": "Ὕλη μαθήματος",
    },
    "am": {
        "title": "የሳንስክሪት ኮርስ",
        "author": "Alois Payer",
        "description": "የሳንስክሪት ሰዋሰው መማሪያ መጽሐፍ",
        "lesson": "ትምህርት",
        "script": "ጽሑፍ",
        "exercise": "መልመጃ"
    },
    "gez": {
        "title": "ትምህርተ ሳንስክሪት",
        "author": "Alois Payer",
        "description": "መጽሐፈ ሰዋስው ዘሳንስክሪት",
        "lesson": "ትምህርት",
        "script": "ጽሑፍ",
        "exercise": "መልመጃ"
    },
    "el": {
        "Abb.:": "Εικ.:",
        "Bildquelle:": "Πηγή εικόνας:",
        "Bildquelle.": "Πηγή εικόνας.",
        "Bildquelle ": "Πηγή εικόνας ",
        "gemeinfrei": "δημόσιο κτήμα",
        "Jhdt.": "αι.",
        "Zugriff am": "πρόσβαση στις",
        "Namensnennung": "Αναφορά δημιουργού",
        "keine kommerzielle Nutzung": "Μη εμπορική χρήση",
        "keine kommerzielle Nuttzung": "Μη εμπορική χρήση",
        "keine kommerzielle Bearbeitung": "Μη εμπορική χρήση, Όχι παράγωγα",
        "keine Bearbeitung": "Όχι παράγωγα",
        "GNU FDLizenz": "Άδεια GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Άδεια Creative Commons",
        "Creative Commons Lizenz": "Άδεια Creative Commons",
        "Creative Commons lizenz": "Άδεια Creative Commons",
        "Unbekannt": "Άγνωστο",
        "Beschriftung:": "Λεζάντα:",
        "Lehrgangsmaterial": "Υλικό μαθήματος",
    },
    "fa": {
        "Abb.:": "شکل.:",
        "Bildquelle:": "منبع تصویر:",
        "Bildquelle.": "منبع تصویر.",
        "Bildquelle ": "منبع تصویر ",
        "gemeinfrei": "مالکیت عمومی",
        "Jhdt.": "ق.",
        "Zugriff am": "تاریخ دسترسی",
        "Namensnennung": "نسب‌دهی",
        "keine kommerzielle Nutzung": "غیرتجاری",
        "keine kommerzielle Nuttzung": "غیرتجاری",
        "keine kommerzielle Bearbeitung": "غیرتجاری بدون اشتقاق",
        "keine Bearbeitung": "بدون اشتقاق",
        "GNU FDLizenz": "مجوز GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "مجوز Creative Commons",
        "Creative Commons Lizenz": "مجوز Creative Commons",
        "Creative Commons lizenz": "مجوز Creative Commons",
        "Unbekannt": "ناشناخته",
        "Beschriftung:": "توضیح:",
        "Lehrgangsmaterial": "مواد دوره",
    },
    "akk": {
        "Abb.:": "ṣalmu:",
        "Bildquelle:": "Ašar ṣalmi:",
        "Bildquelle.": "Ašar ṣalmi.",
        "Bildquelle ": "Ašar ṣalmi ",
        "gemeinfrei": "mālik kalisunu",
        "Jhdt.": "ME.",
        "Zugriff am": "ūm kašādi",
        "Namensnennung": "Šuma zakāru",
        "keine kommerzielle Nutzung": "lā tamkārum",
        "keine kommerzielle Nuttzung": "lā tamkārum",
        "keine kommerzielle Bearbeitung": "lā tamkārum balu wârum",
        "keine Bearbeitung": "balu wârum",
        "GNU FDLizenz": "Lišān GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Lišān Creative Commons",
        "Creative Commons Lizenz": "Lišān Creative Commons",
        "Creative Commons lizenz": "Lišān Creative Commons",
        "Unbekannt": "lā idu",
        "Beschriftung:": "Šiṭru:",
        "Lehrgangsmaterial": "Mimma ša tāmartim",
    },
    "cop": {
        "Abb.:": "ϩⲓⲕⲱⲛ.:",
        "Bildquelle:": "ⲫⲓⲙⲁ ⲛ̀ⲧⲉ ϯϩⲓⲕⲱⲛ:",
        "Bildquelle.": "ⲫⲓⲙⲁ ⲛ̀ⲧⲉ ϯϩⲓⲕⲱⲛ.",
        "Bildquelle ": "ⲫⲓⲙⲁ ⲛ̀ⲧⲉ ϯϩⲓⲕⲱⲛ ",
        "gemeinfrei": "ⲫⲓϩⲱⲃ ⲛ̀ⲧⲉ ⲟⲩⲟⲛ ⲛⲓⲃⲉⲛ",
        "Jhdt.": "ⲁⲓ.",
        "Zugriff am": "ⲡⲓⲉϩⲟⲟⲩ ⲛ̀ⲧⲉ ⲡⲓϭⲓⲙⲓ",
        "Namensnennung": "ⲡⲓⲣⲁⲛ ⲉⲧⲁϥϭⲓ",
        "keine kommerzielle Nutzung": "ⲁⲛ ⲛ̀ⲧⲁⲙⲓⲟ",
        "keine kommerzielle Nuttzung": "ⲁⲛ ⲛ̀ⲧⲁⲙⲓⲟ",
        "keine kommerzielle Bearbeitung": "ⲁⲛ ⲛ̀ⲧⲁⲙⲓⲟ ⲭⲱⲣⲓⲥ ⲫⲓⲁⲗⲗⲟ",
        "keine Bearbeitung": "ⲭⲱⲣⲓⲥ ⲫⲓⲁⲗⲗⲟ",
        "GNU FDLizenz": "ⲡⲓϩⲓⲥⲓ GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "ⲡⲓϩⲓⲥⲓ Creative Commons",
        "Creative Commons Lizenz": "ⲡⲓϩⲓⲥⲓ Creative Commons",
        "Creative Commons lizenz": "ⲡⲓϩⲓⲥⲓ Creative Commons",
        "Unbekannt": "ⲙⲡⲉⲛⲥⲱⲟⲩⲛϥ",
        "Beschriftung:": "ⲡⲓⲥϧⲁⲓ:",
        "Lehrgangsmaterial": "ⲛⲓⲥⲓⲟⲩ ⲛ̀ⲧⲉ ⲡⲓⲙⲁⲑⲏⲙⲁ",
    },
    "id": {
        "Abb.:": "Gbr.:",
        "Bildquelle:": "Sumber gambar:",
        "Bildquelle.": "Sumber gambar.",
        "Bildquelle ": "Sumber gambar ",
        "gemeinfrei": "domain publik",
        "Jhdt.": "abad",
        "Zugriff am": "diakses tanggal",
        "Namensnennung": "Atribusi",
        "keine kommerzielle Nutzung": "NonKomersial",
        "keine kommerzielle Nuttzung": "NonKomersial",
        "keine kommerzielle Bearbeitung": "NonKomersial TanpaTurunan",
        "keine Bearbeitung": "TanpaTurunan",
        "GNU FDLizenz": "Lisensi GNU FD",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "Lisensi Creative Commons",
        "Creative Commons Lizenz": "Lisensi Creative Commons",
        "Creative Commons lizenz": "Lisensi Creative Commons",
        "Unbekannt": "Tidak diketahui",
        "Beschriftung:": "Keterangan:",
        "Lehrgangsmaterial": "Materi kursus",
    },
}

BASE_DIR = "/Volumes/SanDisk1TB/proj/Payer/docs"
SOURCE_DIR = os.path.join(BASE_DIR, "lektionen")

_DEVA_RE = re.compile(r'[ऀ-ॿ]+')

def protect_devanagari(text):
    """Replace every Devanāgarī run with a unique placeholder. Returns (protected_text, registry)."""
    registry = {}
    counter = [0]
    def _replace(m):
        key = f'⟨DEVA_{counter[0]}⟩'
        registry[key] = m.group(0)
        counter[0] += 1
        return key
    return _DEVA_RE.sub(_replace, text), registry

def restore_devanagari(text, registry, mark_sanskrit=False):
    for key, original in registry.items():
        replacement = f'⟪{original}⟫' if mark_sanskrit else original
        text = text.replace(key, replacement)
    return text

# IAST-specific diacritics that never appear in German text.
_IAST_DIACRITICS_RE = re.compile(r'[āĀīĪūŪṛṚṝṜḷḶṭṬḍḌṇṆṣṢśŚñÑṅṄṃṂḥḤ]')
# Charset for a line that is PURELY IAST (Latin letters, IAST diacritics, spaces, verse punctuation).
# Parentheses excluded so German translation examples like "Rāma isst (kaut)..." are never caught.
_IAST_LINE_RE = re.compile(r'^[a-zA-ZāĀīĪūŪṛṚṝṜḷḶṭṬḍḌṇṆṣṢśŚñÑṅṄṃṂḥḤ\s\|.,;:!\-]+$')
# German connector words/abbreviations that reveal a line is natural-language text mixed with
# IAST proper nouns (e.g. "Pārvatī und Śiva," or "Abb.: Gaṇeśa, Adamspeak, Sri Lanka").
# These never appear as standalone tokens in pure Sanskrit transliteration.
_GERMAN_CONNECTORS_RE = re.compile(r'\b(und|des|Abb)\b')

def protect_iast_lines(text):
    """Replace lines that are purely IAST transliteration with placeholders.

    Runs AFTER protect_devanagari so mixed IAST+Devanagari lines already have
    ⟨DEVA_N⟩ tokens in them and won't accidentally match as pure-IAST.
    """
    registry = {}
    counter = [0]
    result_lines = []
    for line in text.split('\n'):
        core = line.strip().strip('*').strip()
        if (core
                and _IAST_DIACRITICS_RE.search(core)
                and _IAST_LINE_RE.match(core)
                and '⟨' not in line
                and not _GERMAN_CONNECTORS_RE.search(core)):
            key = f'⟨IAST_L_{counter[0]}⟩'
            registry[key] = line
            counter[0] += 1
            result_lines.append(key)
        else:
            result_lines.append(line)
    return '\n'.join(result_lines), registry

def restore_iast_lines(text, registry):
    for key, original in registry.items():
        text = text.replace(key, original)
    return text

BR_PLACEHOLDER = '⟨BR⟩'

def protect_br(text):
    """Replace [[br]] with a placeholder so the LLM never sees the token boundary."""
    return text.replace('[[br]]', BR_PLACEHOLDER)

def restore_br(text):
    return text.replace(BR_PLACEHOLDER, '[[br]]')

def protect_structure(text):
    """Replace VitePress containers (:::) and horizontal rules (---) with placeholders."""
    registry = {}
    counter = [0]
    result_lines = []
    for line in text.split('\n'):
        # Protect lines that are exactly '---' or start with ':::'
        if line.strip() == '---' or line.strip().startswith(':::'):
            key = f'⟨STRUCT_{counter[0]}⟩'
            registry[key] = line
            counter[0] += 1
            result_lines.append(key)
        else:
            result_lines.append(line)
    return '\n'.join(result_lines), registry

def restore_structure(text, registry):
    import re
    def replace_struct(m):
        idx = m.group(1)
        key = f'⟨STRUCT_{idx}⟩'
        return registry.get(key, m.group(0))
    
    text = re.sub(r'[⟨<〈]STRUCT_[^⟩>〉]*?(\d+)[⟩>〉]', replace_struct, text)
    
    for key, original in registry.items():
        text = text.replace(key, original)
    return text


def translate_text(text, target_lang):
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    _mark_skt = (target_lang == 'hi')
    protected, deva_registry = protect_devanagari(text)
    protected, iast_registry = protect_iast_lines(protected)
    protected = protect_br(protected)
    protected, struct_registry = protect_structure(protected)
    system = (
        f"You are a scholarly translator. Translate ALL German text in this Sanskrit-education markdown to {lang_name}. "
        "Rules: "
        "(1) Translate every German word — including captions, image descriptions, verse translations, and prose. "
        "(2) Preserve unchanged: Markdown syntax, IAST transliterations, YAML frontmatter keys, HTML comments, ⟨DEVA_N⟩ placeholders, ⟨IAST_L_N⟩ placeholders, ⟨BR⟩ placeholders, and ⟨STRUCT_N⟩ placeholders. "
        f"(3) Translate '# Lektion N' headings to the target-language equivalent (e.g. '# Lesson N' in English, '# Lezione N' in Italian, '# Lección N' in Spanish, '# Урок N' in Russian/Ukrainian/Bulgarian, '# पाठ N' in Hindi, '# Leçon N' in French, '# Lecziun N' in Romansh Grischun, '# பாடம் N' in Tamil, '# ਪਾਠ N' in Punjabi, '# الدرس N' in Arabic, '# ܡܠܦܢܘܬܐ N' in Aramaic, '# שיעור N' in Hebrew, '# 第N课' in Mandarin Chinese, '# บทที่ N' in Thai, '# Lectio N' in Latin, '# Μάθημα N' in Ancient Greek, '# Μάθημα N' in Modern Greek, '# درس N' in Persian, '# Ṭupšarru N' in Akkadian, '# ⲙⲁⲑⲏⲙⲁ N' in Coptic). "
        "(4) NEVER add TODO comments, fallback markers, or any annotations of your own. If unsure how to translate a word or sentence into the target language, translate it into English as a fallback (NEVER leave it in German). "
        "(5) Keep the scholarly editorial tone throughout. "
        "(6) CRITICAL: Preserve the exact line count of the source. Every source line must appear as exactly one output line. NEVER delete, merge, or collapse lines. "
        "(6a) CRITICAL: Each non-empty line of the input is prefixed with a bracketed identifier like [L0], [L1], [L2]... You MUST preserve these identifiers exactly at the start of each translated line. Do not translate, modify, or remove them. "
        "(7) CRITICAL: Copy every ⟨DEVA_N⟩ and ⟨IAST_L_N⟩ placeholder character-for-character. They are replaced with Devanāgarī and IAST text after translation — do NOT interpret, transliterate, or remove them. "
        "(7a) CRITICAL: Lines consisting ONLY of ⟨DEVA_N⟩ tokens (and spaces/punctuation like ।  ॥) are Sanskrit verse lines. Copy every token on that line verbatim. NEVER transliterate Sanskrit verses into the target script — the placeholders will be restored to Devanāgarī automatically. "
        "(7b) CRITICAL: Preserve ALL Markdown image syntax exactly: ![alt](/path/to/image.jpg) — never drop the parentheses around the image path. "
        "(8) Numbered exercise sentences (e.g. '3. Śūdras erlangen...', '4. Die Kṣatriyas...') MUST be translated to the target language even when they begin with Sanskrit proper nouns in IAST notation. The IAST proper noun is preserved as-is; only the surrounding German words are translated."
    )
    import uuid
    system = system + f"\n\n[Session Key: {uuid.uuid4()}]"
    best_result = None
    best_missing: list = list(deva_registry.keys())  # worst case: all missing
    is_fallback = False  # FIX: was undefined, causing NameError on retry attempts

    max_ph_retries = 4
    for ph_attempt in range(max_ph_retries):
        # 3-Tier Fallback Hierarchy: Qwen (local) -> Sonnet (cloud) -> Gemini 2.5 Pro (cloud)
        current_api_url = API_URL
        current_model = MODEL
        is_fallback = False
        
        if ph_attempt == 2:
            current_api_url = "https://openrouter.ai/api/v1/chat/completions"
            current_model = "anthropic/claude-sonnet-5"
            is_fallback = True
        elif ph_attempt >= 3:
            current_api_url = "https://openrouter.ai/api/v1/chat/completions"
            current_model = "google/gemini-2.5-pro"
            is_fallback = True

        # Bump temperature and repetition_penalty on retries so the model makes different choices.
        temperature = 0.1 if ph_attempt == 0 else 0.3
        repetition_penalty = 1.15 if ph_attempt == 0 else 1.25
        
        # Prepare indexed prompt
        source_lines = protected.split('\n')
        indexed_lines = []
        for idx, l in enumerate(source_lines):
            if l.strip():
                indexed_lines.append(f"[L{idx}] {l}")
            else:
                indexed_lines.append(l)
        indexed_protected = '\n'.join(indexed_lines)

        user_prompt = indexed_protected
        if ph_attempt > 0 and 'qc_reason' in locals():
            if is_fallback:
                sys.stdout.write(f"\n[{target_lang}] FALLBACK TRIGGERED: Switching to OpenRouter ({current_model}) for this chunk due to persistent QC failures.\n")
                sys.stdout.flush()
            user_prompt = f"CRITICAL CORRECTION REQUIRED:\nYour previous translation failed Quality Control for this reason: {qc_reason}\n\nYou MUST fix this error. If you failed to translate sentences, translate EVERY single word now. If you dropped lines, preserve line count strictly. Translate the following text:\n\n{indexed_protected}"

        data = {
            "model": current_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": 8192,
            "repetition_penalty": repetition_penalty
        }

        max_retries = 100
        got_response = False
        for attempt in range(max_retries):
            try:
                import subprocess as _sp
                start_time = time.time()
                curl_cmd = ['curl', '-s', '-X', 'POST', current_api_url, '-H', 'Content-Type: application/json']
                api_key = os.environ.get('OPENROUTER_API_KEY', 'local') if 'openrouter.ai' in current_api_url else 'local'
                curl_cmd.extend(['-H', f"Authorization: Bearer {api_key}"])
                curl_cmd.extend(['-d', json.dumps(data), '--max-time', '1800', '--keepalive-time', '15'])
                
                _proc = _sp.run(
                    curl_cmd,
                    capture_output=True, text=True, timeout=1820
                )
                end_time = time.time()
                if _proc.returncode != 0:
                    raise OSError(f"curl exit {_proc.returncode}: {_proc.stderr[:200]}")
                res_data = json.loads(_proc.stdout)
                if 'error' in res_data:
                    raise RuntimeError(f"API Error: {res_data['error']}")
                raw_result = res_data['choices'][0]['message']['content']
                got_response = True

                # Parse and restore lines based on prefixes
                import re
                result_lines = raw_result.split('\n')
                restored_lines = [None] * len(source_lines)
                unmatched_lines = []
                for r_line in result_lines:
                    m = re.match(r'^\s*\[[LЛlл]?(\d+)\]\s*(.*)$', r_line)
                    if m:
                        idx = int(m.group(1))
                        content = m.group(2)
                        if 0 <= idx < len(source_lines):
                            restored_lines[idx] = content
                        else:
                            unmatched_lines.append(r_line)
                    else:
                        if r_line.strip():
                            unmatched_lines.append(r_line)
                
                # Fill missing non-empty lines sequentially
                unmatched_idx = 0
                for idx, src_l in enumerate(source_lines):
                    if src_l.strip():
                        if restored_lines[idx] is None:
                            if unmatched_idx < len(unmatched_lines):
                                clean_line = re.sub(r'^\s*\[[LЛlл]?\d+\]\s*', '', unmatched_lines[unmatched_idx])
                                restored_lines[idx] = clean_line
                                unmatched_idx += 1
                            else:
                                restored_lines[idx] = src_l
                    else:
                        restored_lines[idx] = ''
                
                result = '\n'.join(restored_lines)
                got_response = True

                # Performance Monitoring & Auto-Restart
                if 'usage' in res_data and 'completion_tokens' in res_data['usage']:
                    comp_tokens = res_data['usage']['completion_tokens']
                    elapsed = end_time - start_time
                    if elapsed > 0:
                        tps = comp_tokens / elapsed
                        ts = time.strftime('%H:%M:%S')
                        sys.stdout.write(f"[{ts}]      [Speed: {tps:.1f} t/s | {comp_tokens} tokens in {elapsed:.1f}s]\n")
                        sys.stdout.flush()
                        if comp_tokens > 20 and tps < 1.0:
                            sys.stdout.write(f"\n[{ts}] [!] Performance kritisch ({tps:.1f} t/s). Führe automatischen oMLX-Neustart aus...\n")
                            sys.stdout.flush()
                            try:
                                # Old CLI restart method (commented out):
                                # _sp.run(['ssh', 'marco@nyx.local', 'pkill -f "mlx_lm server"; sleep 2; cd ~/llm-benchmark && nohup ./start > /dev/null 2>&1 &'], timeout=15)
                                # time.sleep(60)
                                
                                # New oMLX App restart method:
                                _sp.run(['ssh', 'marco@nyx.local', 'osascript -e \'quit app "oMLX"\' || pkill -9 -f oMLX'], timeout=15)
                                time.sleep(3)
                                _sp.run(['ssh', 'marco@nyx.local', 'open -a oMLX'], timeout=15)
                                sys.stdout.write(f"[{ts}] [!] oMLX-Neustart-Befehl gesendet. Warte 40s auf den Server...\n")
                                sys.stdout.flush()
                                time.sleep(40)
                            except Exception as ssh_e:
                                sys.stdout.write(f"[{ts}] [!] SSH oMLX-Neustart fehlgeschlagen: {ssh_e}\n")
                                sys.stdout.flush()

                # --- QUALITY CONTROL (QC) ---
                source_lines = protected.split('\n')
                result_lines = result.split('\n')
                qc_failed = False
                qc_reason = ""
                
                if len([l for l in source_lines if l.strip()]) != len([l for l in result_lines if l.strip()]):
                    qc_failed = True
                    qc_reason = f"Line count mismatch (Expected non-empty: {len([l for l in source_lines if l.strip()])}, Got: {len([l for l in result_lines if l.strip()])})"
                else:
                    missing_struct = [k for k in struct_registry if k not in result]
                    if missing_struct:
                        qc_failed = True
                        qc_reason = f"Missing structure placeholders: {len(missing_struct)} dropped"
                
                if not qc_failed and target_lang != 'de':
                    import re
                    safe_german_words = ['und', 'oder', 'nicht', 'sich', 'wird', 'werden', 'auch', 'dass', 'auf', 'für']
                    ger_pattern = re.compile(r'\b(' + '|'.join(safe_german_words) + r')\b', re.IGNORECASE)
                    ger_result_count = len(ger_pattern.findall(result))
                    if ger_result_count >= 3:
                        ger_source_count = len(ger_pattern.findall(protected))
                        if ger_result_count >= (ger_source_count * 0.2):
                            qc_failed = True
                            qc_reason = f"Untranslated German detected ({ger_result_count} marker words found)"
                            
                # English Leak Detection (Fallback catch)
                if not qc_failed and target_lang not in ('de', 'en'):
                    safe_english_words = ['the', 'is', 'to', 'and', 'that', 'of', 'for', 'this', 'are', 'with']
                    en_pattern = re.compile(r'\b(' + '|'.join(safe_english_words) + r')\b', re.IGNORECASE)
                    en_result_count = len(en_pattern.findall(result))
                    if en_result_count >= 3:
                        en_source_count = len(en_pattern.findall(protected))
                        # Only flag if there are significantly more English words than in the source text
                        if en_result_count > en_source_count + 2:
                            qc_failed = True
                            qc_reason = f"English fallback leak detected ({en_result_count} English marker words found)"

                if qc_failed:
                    if ph_attempt < max_ph_retries - 1:
                        sys.stdout.write(f"[{target_lang}] QC failed: {qc_reason} — retrying ({ph_attempt + 2}/{max_ph_retries}, T={temperature})...\n")
                        sys.stdout.flush()
                        break  # break connection loop to retry generation outer loop
                    else:
                        sys.stdout.write(f"[{target_lang}] WARNING: QC failed on all retries. Reason: {qc_reason}. Proceeding with latest attempt.\n")
                        sys.stdout.flush()
                        if best_result is None:
                            best_result = result
                        break
                # --- END QC ---

                missing = [k for k in deva_registry if k not in result]
                if len(missing) < len(best_missing):
                    best_result = result
                    best_missing = missing
                if not missing:
                    result = restore_devanagari(result, deva_registry, _mark_skt)
                    result = restore_iast_lines(result, iast_registry)
                    result = restore_br(result)
                    result = restore_structure(result, struct_registry)
                    return result, ph_attempt
                # Got a response but placeholders were dropped — retry outer loop.
                if ph_attempt < max_ph_retries - 1:
                    sys.stdout.write(
                        f"[{target_lang}] Placeholder drop ({len(missing)}): "
                        f"{missing[:3]}{'…' if len(missing) > 3 else ''} "
                        f"— retrying ({ph_attempt + 2}/{max_ph_retries}, T={temperature})...\n"
                    )
                    sys.stdout.flush()
                break  # break connection-retry loop; outer loop handles the rest
            except Exception as e:
                err_str = str(e)
                wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s, 40s, 80s
                
                # Auto-Restart bei Timeouts, HTTP 500 (Compute error) oder Absturz (Connection refused/exit 7, exit 56)
                err_lower = err_str.lower()
                is_local = 'localhost' in current_api_url or '127.0.0.1' in current_api_url
                if is_local and ("exit 28" in err_str or "timeout" in err_lower or "500" in err_str or "exit 7" in err_str or "exit 56" in err_str or "exit 52" in err_str or "refused" in err_lower or "choices" in err_lower):
                    ts = time.strftime('%H:%M:%S')
                    sys.stdout.write(f"\n[{ts}] [!] Timeout/Absturz erkannt ({err_str}). Führe automatischen oMLX-Neustart aus...\n")
                    sys.stdout.flush()
                    try:
                        import subprocess as _sp_err
                        # Old CLI restart method (commented out):
                        # _sp_err.run(['ssh', 'marco@nyx.local', 'pkill -f "mlx_lm server"; sleep 2; cd ~/llm-benchmark && nohup ./start > /dev/null 2>&1 &'], timeout=15)
                        # time.sleep(60)
                        
                        # New oMLX App restart method:
                        _sp_err.run(['ssh', 'marco@nyx.local', 'osascript -e \'quit app "oMLX"\' || pkill -9 -f oMLX'], timeout=15)
                        time.sleep(3)
                        _sp_err.run(['ssh', 'marco@nyx.local', 'open -a oMLX'], timeout=15)
                        sys.stdout.write(f"[{ts}] [!] oMLX-Neustart-Befehl gesendet. Warte 40s...\n")
                        sys.stdout.flush()
                        time.sleep(40)
                    except Exception:
                        pass

                if "API Error" in err_str:
                    if "'code': 404" in err_str or "'code': 400" in err_str:
                        sys.stdout.write(f"\n[!] API Error 400/404 (Bad Request/Model not found): {err_str}\nSkipping to next fallback tier...\n")
                        sys.stdout.flush()
                        break
                    if "'code': 402" in err_str or "'code': 401" in err_str:
                        sys.stdout.write(f"\n[FATAL] Unrecoverable Auth/Credit API Error encountered: {err_str}\nAborting translation completely.\n")
                        sys.stdout.flush()
                        sys.exit(1)

                msg = f"[{time.strftime('%H:%M:%S')}] [{target_lang}] Connection failed (attempt {attempt+1}/{max_retries}): {err_str}. Retrying in {wait_time}s...\n"
                sys.stdout.write(msg)
                sys.stdout.flush()
                time.sleep(wait_time)

        if not got_response:
            if is_fallback and ph_attempt < max_ph_retries - 1:
                sys.stdout.write(f"[{target_lang}] WARNING: API failed. Escalating to next fallback tier (attempt {ph_attempt + 2})...\n")
                sys.stdout.flush()
                continue
            sys.stdout.write(f"[{target_lang}] FATAL: Maximum inner connection retries reached and no more fallback tiers available.\n")
            sys.stdout.flush()
            return f"ERROR: Failed to translate after {max_retries} attempts.", ph_attempt

    # All placeholder-retry attempts exhausted — use the best partial result.
    sys.stdout.write(
        f"[{target_lang}] WARNING: LLM dropped {len(best_missing)} Devanāgarī "
        f"placeholder(s) after {max_ph_retries} attempts: "
        f"{best_missing[:5]}{'…' if len(best_missing) > 5 else ''}\n"
    )
    sys.stdout.flush()
    # Fallback: if all retries produced None, use the protected text to avoid crash
    if best_result is None:
        best_result = protected
    result = restore_devanagari(best_result, deva_registry, _mark_skt)
    result = restore_iast_lines(result, iast_registry)
    result = restore_br(result)
    result = restore_structure(result, struct_registry)
    return result, max_ph_retries - 1

def escape_angle_brackets_in_tables(text):
    # LLMs sometimes convert &lt;form&gt; → <form>, breaking Vue (HTML is forbidden).
    # Fix: re-escape raw <...> on all lines, skipping already-escaped entities.
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.replace('&lt;', '\x00LT\x00').replace('&gt;', '\x00GT\x00')
        line = re.sub(r'<([^>\s][^>]*)>', r'&lt;\1&gt;', line)
        line = line.replace('\x00LT\x00', '&lt;').replace('\x00GT\x00', '&gt;')
        result.append(line)
    return '\n'.join(result)

def fix_home_links(content, lang):
    """Prefix bare absolute links in index.md YAML frontmatter with /lang/.
    Also restore URL paths the LLM may have translated (e.g. /lessons/ → /lektionen/)."""
    content = re.sub(r'/lessons/', '/lektionen/', content)
    content = re.sub(r'/lesson(\d+)', r'/lektion\1', content)
    content = re.sub(r'/grammar\b', '/grammatik', content)
    def replace_link(m):
        path = m.group(1)
        if path.startswith(f'/{lang}/'):
            return m.group(0)
        return f'link: /{lang}{path}'
    return re.sub(r'link:\s*(/[^\s\n]+)', replace_link, content)

def fix_lesson_links(content, lang):
    """Rewrite bare /licenses links in translated lessons to /{lang}/licenses."""
    def replace(m):
        path = m.group(1)
        if path.startswith(f'/{lang}/'):
            return f'({path})'
        return f'(/{lang}{path})'
    return re.sub(r'\((/licenses[^)]*)\)', replace, content)


def get_tm_path(lang):
    tm_dir = os.path.join(BASE_DIR, ".zennotes", "tm")
    os.makedirs(tm_dir, exist_ok=True)
    return os.path.join(tm_dir, f"{lang}.json")

def load_tm(lang):
    p = get_tm_path(lang)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

def save_tm(lang, tm):
    p = get_tm_path(lang)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(tm, f, ensure_ascii=False, indent=2)

def hash_chunk(chunk):
    return hashlib.md5(chunk.encode('utf-8')).hexdigest()

def translate_file(source_path, target_path, lang, post_process=None, force=False):
    """Translate a single file with mtime-based skip and chunking. Returns True on success."""
    filename = os.path.basename(source_path)
    is_fallback_mode = False
    has_fallback = False
    
    if not force and os.path.exists(target_path) and os.path.getsize(target_path) > 200:
        with open(target_path, 'r', encoding='utf-8') as tf:
            target_content = tf.read()
        has_fallback = "Fallback translation" in target_content
        source_mtime = os.path.getmtime(source_path)
        target_mtime = os.path.getmtime(target_path)

        if not has_fallback and source_mtime <= target_mtime:
            print(f"[{lang}] Skipping {filename} (up to date, no fallback tags).")
            return True
        
        if has_fallback:
            print(f"[{lang}] Fallback tags detected in {filename} — resolving fallbacks only...")
            is_fallback_mode = True
        else:
            print(f"[{lang}] Outdated {filename} — re-translating completely...")
    else:
        print(f"[{lang}] Translating {filename}...")

    total_retries = 0

    if is_fallback_mode:
        # SURGICAL FALLBACK MODE
        # Extract blocks from target file, translate adjacent ones in groups to optimize API requests
        blocks = target_content.split('\n\n')
        
        # Group adjacent fallback blocks
        groups = []
        i = 0
        n = len(blocks)
        while i < n:
            if "TODO: Fallback translation" in blocks[i]:
                group = []
                while i < n and "TODO: Fallback translation" in blocks[i]:
                    group.append((i, blocks[i]))
                    i += 1
                groups.append(group)
            else:
                i += 1
                
        fallbacks_found = 0
        for group in groups:
            # Split large groups into sub-chunks of max 4 blocks
            chunk_size = 4
            for j in range(0, len(group), chunk_size):
                sub_group = group[j:j+chunk_size]
                success = False
                
                if len(sub_group) > 1:
                    cleaned_sources = []
                    for idx, block in sub_group:
                        src = re.sub(r'\s*(?:&lt;|<)!--\s*TODO:\s*Fallback\s*translation\s*[^\n]*', '', block)
                        cleaned_sources.append(src)
                    
                    group_source = '\n\n'.join(cleaned_sources)
                    ts = time.strftime('%H:%M:%S')
                    print(f"[{ts}]  -> surgical group translation of {len(sub_group)} blocks...")
                    
                    result_tuple = translate_text(group_source, lang)
                    result = result_tuple[0]
                    total_retries += result_tuple[1]
                    
                    if not result.startswith("ERROR:"):
                        # Split by double newline to recover individual block translations
                        translated_parts = result.split('\n\n')
                        translated_parts = [p.strip() for p in translated_parts if p.strip()]
                        
                        if len(translated_parts) == len(sub_group):
                            for k, (idx, _) in enumerate(sub_group):
                                blocks[idx] = translated_parts[k]
                            success = True
                            fallbacks_found += len(sub_group)
                            print(f"       -> Successfully translated group of {len(sub_group)} blocks in one run!")
                        else:
                            print(f"       [!] Group translation QC failed (Block count mismatch: expected {len(sub_group)}, got {len(translated_parts)}). Falling back to block-by-block...")
                
                if not success:
                    # Individual fallback block-by-block
                    for idx, block in sub_group:
                        fallbacks_found += 1
                        source_text = re.sub(r'\s*(?:&lt;|<)!--\s*TODO:\s*Fallback\s*translation\s*[^\n]*', '', block)
                        if not source_text.strip():
                            blocks[idx] = source_text
                            continue
                            
                        ts = time.strftime('%H:%M:%S')
                        print(f"[{ts}]  -> surgical fallback {fallbacks_found} (block-by-block)...")
                        result_tuple = translate_text(source_text, lang)
                        result = result_tuple[0]
                        total_retries += result_tuple[1]
                        
                        if result.startswith("ERROR:"):
                            print(f"  [!] Failed fallback {fallbacks_found}: {result}")
                            return False
                        
                        blocks[idx] = result.strip()
                        
        translated = '\n\n'.join(blocks)
        
    else:
        # FULL FILE TRANSLATION MODE
        with open(source_path, encoding="utf-8") as f:
            content = f.read()

        yaml_block = ""
        if content.startswith("---\n"):
            end_idx = content.find("\n---\n", 4)
            if end_idx != -1:
                yaml_block = content[:end_idx+5]
                content = content[end_idx+5:]
                ts = time.strftime('%H:%M:%S')
                print(f"[{ts}]  -> translating YAML frontmatter safely...")
                yaml_block = translate_yaml_frontmatter(yaml_block, lang)

        chunks = chunk_content(content)
        translated_chunks = []
        
        if yaml_block:
            translated_chunks.append(yaml_block)
            
        tm_cache = load_tm(lang)
        tm_updated = False
        
        for i, chunk in enumerate(chunks, 1):
            if not chunk.strip():
                translated_chunks.append(chunk)
                continue
                
            chunk_hash = hash_chunk(chunk)
            if chunk_hash in tm_cache:
                ts = time.strftime('%H:%M:%S')
                print(f"[{ts}]  -> section {i}/{len(chunks)}... (TM CACHE HIT)")
                translated_chunks.append(tm_cache[chunk_hash])
                continue
                
            ts = time.strftime('%H:%M:%S')
            print(f"[{ts}]  -> section {i}/{len(chunks)}... (LLM API)")
            
            result_tuple = translate_text(chunk, lang)
            result = result_tuple[0]
            total_retries += result_tuple[1]
            
            if result.startswith("ERROR:"):
                print(f"  [!] Failed chunk {i}: {result}")
                return False
                
            tm_cache[chunk_hash] = result
            tm_updated = True
            translated_chunks.append(result)

        if tm_updated:
            save_tm(lang, tm_cache)

        translated = '\n\n'.join(translated_chunks)

    translated = escape_angle_brackets_in_tables(translated)
    if post_process:
        translated = post_process(translated)

    # FIX: Guard against empty translation result — never write an empty file.
    if not translated or not translated.strip():
        print(f"  [!] ABORT: Translation result for {filename} is empty — refusing to overwrite existing file.")
        return False

    # FIX: Atomic write — use a temp file + os.replace()
    import tempfile
    target_dir = os.path.dirname(target_path) or '.'
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(dir=target_dir, suffix='.tmp')
        try:
            with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
                f.write(translated)
            os.replace(tmp_path, target_path)  # atomic on POSIX
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
    except Exception as write_err:
        print(f"  [!] FATAL: Could not write {target_path}: {write_err}")
        return False

    # FIX: Warn if the written file is suspiciously small compared to source.
    source_size = os.path.getsize(source_path)
    written_size = os.path.getsize(target_path)
    if not is_fallback_mode and source_size > 200 and written_size < source_size * 0.3:
        print(f"  [!] WARNING: {filename} looks too small ({written_size} B written vs {source_size} B source). Review output!")

    # ── POST-TRANSLATION RESIDUE SCAN ────────────────────────────────────────
    # Only run on lesson files (lektion*.md) — not on structural pages.
    if filename.startswith('lektion') and lang != 'de':
        with open(target_path, encoding='utf-8') as _f:
            _written_content = _f.read()
        _flagged = scan_german_residues(_written_content)
        if _flagged:
            ts_now = time.strftime('%H:%M:%S')
            sys.stdout.write(
                f"[{ts_now}] [{lang}] ⚠ RESIDUE SCAN: {len(_flagged)} German term(s) in {filename}:\n"
            )
            for _li, _lt in _flagged[:5]:
                sys.stdout.write(f"   L{_li}: {_lt[:120]}\n")
            if len(_flagged) > 5:
                sys.stdout.write(f"   ... and {len(_flagged) - 5} more\n")
            sys.stdout.flush()

            # Sonnet fallback: patch the flagged lines
            sys.stdout.write(f"  → Sending {len(_flagged)} line(s) to Sonnet for targeted patch...\n")
            sys.stdout.flush()
            _patched = sonnet_patch_residues(_written_content, _flagged, lang)

            # Verify the patch improved things
            _flagged_after = scan_german_residues(_patched)
            if len(_flagged_after) < len(_flagged):
                # Write the patched version atomically
                import tempfile as _tf
                _td = os.path.dirname(target_path) or '.'
                _tmp_fd, _tmp_p = _tf.mkstemp(dir=_td, suffix='.tmp')
                with os.fdopen(_tmp_fd, 'w', encoding='utf-8') as _wf:
                    _wf.write(_patched)
                os.replace(_tmp_p, target_path)
                resolved = len(_flagged) - len(_flagged_after)
                sys.stdout.write(
                    f"  ✓ Sonnet patched {resolved}/{len(_flagged)} residue(s). "
                    f"{len(_flagged_after)} remaining.\n"
                )
                sys.stdout.flush()
                if _flagged_after:
                    log_failure(lang, filename, 'RESIDUE',
                                _flagged_after,
                                f"After Sonnet patch: {len(_flagged_after)} unresolved")
            else:
                sys.stdout.write(
                    f"  [!] Sonnet patch did not improve result "
                    f"({len(_flagged_after)} residues remain). Keeping Qwen3.6 output.\n"
                )
                sys.stdout.flush()
                log_failure(lang, filename, 'RESIDUE', _flagged,
                            f"Sonnet patch ineffective ({len(_flagged_after)} remain)")
        else:
            ts_now = time.strftime('%H:%M:%S')
            sys.stdout.write(f"[{ts_now}] [{lang}] ✓ Residue scan clean: {filename}\n")
            sys.stdout.flush()
    # ── END RESIDUE SCAN ─────────────────────────────────────────────────────

    retry_msg = f" (Total QC retries: {total_retries})" if total_retries > 0 else " (Flawless run)"
    mode_msg = " (Surgical)" if is_fallback_mode else ""
    print(f"[{lang}] Done {filename}{mode_msg}.{retry_msg}")
    time.sleep(2)
    return True


def translate_yaml_frontmatter(yaml_content, target_lang):
    """Safely translates only string values in a YAML frontmatter block."""
    translatable_keys = {'name', 'text', 'tagline', 'title', 'details'}
    lines = yaml_content.split('\n')
    
    indices = []
    values = []
    
    for i, line in enumerate(lines):
        m = re.match(r'^(\s*[a-zA-Z0-9_-]+:\s*)(.+)$', line)
        if m:
            key_str = m.group(1).strip().strip(':')
            val_str = m.group(2).strip().strip('"').strip("'")
            if key_str in translatable_keys and val_str and not val_str.startswith('/'):
                indices.append(i)
                values.append(val_str)
                
    if not values:
        return yaml_content
        
    source_text = "\n\n".join(values)
    res_tuple = translate_text(source_text, target_lang)
    translated_text = res_tuple[0]
    
    if translated_text.startswith("ERROR:"):
        return yaml_content
        
    translated_vals = [p.strip() for p in translated_text.split('\n\n') if p.strip()]
    if len(translated_vals) == len(values):
        for idx, new_val in zip(indices, translated_vals):
            m = re.match(r'^(\s*[a-zA-Z0-9_-]+:\s*)(.+)$', lines[idx])
            prefix = m.group(1)
            lines[idx] = f'{prefix}"{new_val}"'
            
    return '\n'.join(lines)


def chunk_content(content):
    # Splits content into safe, manageable chunks of max ~3000 characters.
    # Prefers breaking at markdown boundaries (empty lines, container markers,
    # table lines, headers) to preserve translation quality.  If a chunk
    # exceeds 3000 characters without hitting such a boundary, it is split
    # anyway — a hard cap prevents server overload.
    lines = content.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
    MAX_CHUNK = 3000

    for line in lines:
        is_header = line.startswith('## ') or line.startswith('### ')
        is_safe_break = (not line.strip() or line.startswith(':::') or line.startswith('|'))

        if (is_header or is_safe_break) and current_chunk and current_size >= MAX_CHUNK:
            # Chunk is large enough — break at this safe boundary.
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(line)
        current_size += len(line) + 1

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks


# ══════════════════════════════════════════════════════════════════════════════
# HYBRID STRATEGY: Post-scan → Sonnet Fallback → Failure Log
# ══════════════════════════════════════════════════════════════════════════════

# German patterns that should never appear in a translated file.
# Only surface-level lexical markers — no Sanskrit/IAST terms.
_DE_RESIDUE_PATTERNS = re.compile(
    r'\b(d\.h\.|usw\.|vgl\.|z\.B\.|Bildung|Stamm[^s]|Stämme|Stammabstufung'
    r'|auslautend|Formgleich|mehrsilbig|entweder|Dehnstufe|Hochstufe'
    r'|Tiefst(?:ufe|\.)|Normalst(?:ufe|\.)|Schwundstufe|Merke:|Beachte:'
    r'|Anmerkung:|Hinweis:|Beispiel:|Beispiele:|Präsensklasse|Aoristklasse'
    r'|Perfektstamm|Desiderativstamm|Kausativstamm|Verbalwurzel'
    r'|Kasusendung|Kasussystem|Deklinationsklasse|Konjugationsklasse'
    r'|Sandhi-Regel|Lautgesetz|Stammvokal|Endung(?:en)?\b'
    r')'
)
# (Unused placeholder — pure-IAST line detection handled inline in scan_german_residues)

FAILURE_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "qa", "translation_failures.md"
)


def scan_german_residues(content: str) -> list:
    """Scan translated content for remaining German terms.

    Returns a list of (line_index, line_text) tuples where residues were found.
    Ignores lines inside ::: deleteme-box containers and YAML frontmatter.
    """
    flagged = []
    in_frontmatter = False
    in_deleteme = False
    frontmatter_count = 0

    for i, line in enumerate(content.split('\n')):
        stripped = line.strip()

        # Track YAML frontmatter (first --- block)
        if stripped == '---' and i < 5:
            frontmatter_count += 1
            in_frontmatter = frontmatter_count == 1
            if frontmatter_count == 2:
                in_frontmatter = False
            continue
        if in_frontmatter:
            continue

        # Track ::: deleteme-box containers
        if '::: deleteme-box' in stripped or ':::deleteme-box' in stripped:
            in_deleteme = True
        if in_deleteme and stripped == ':::':
            in_deleteme = False
            continue
        if in_deleteme:
            continue

        # Skip lines that are purely Devanāgarī, IAST, or URLs
        if not stripped or stripped.startswith('http') or stripped.startswith('<!--'):
            continue

        # Skip lines in grammar-box headers / structural markers
        if stripped.startswith(':::') or stripped == '---':
            continue

        if _DE_RESIDUE_PATTERNS.search(line):
            flagged.append((i, line))

    return flagged


SONNET_API_URL = "https://openrouter.ai/api/v1/chat/completions"
SONNET_MODEL = "anthropic/claude-sonnet-5"


def sonnet_patch_residues(content: str, flagged_lines: list, target_lang: str) -> str:
    """Send ONLY the flagged lines (with context) to Sonnet for targeted patching.

    Returns the full content with residues replaced.
    Uses OpenRouter with OPENROUTER_API_KEY env variable.
    """
    api_key = os.environ.get('OPENROUTER_API_KEY', '')
    if not api_key:
        sys.stdout.write("  [!] SONNET FALLBACK: OPENROUTER_API_KEY not set — skipping patch.\n")
        sys.stdout.flush()
        return content

    lang_name = LANG_NAMES.get(target_lang, target_lang)
    lines = content.split('\n')
    flagged_indices = {i for i, _ in flagged_lines}

    # Build a context window: flagged lines ± 2 lines of context
    context_indices = set()
    for i in flagged_indices:
        for j in range(max(0, i - 2), min(len(lines), i + 3)):
            context_indices.add(j)

    # Format the snippet with line markers
    snippet_lines = []
    for i in sorted(context_indices):
        marker = ">>" if i in flagged_indices else "  "
        snippet_lines.append(f"[L{i}]{marker} {lines[i]}")
    snippet = '\n'.join(snippet_lines)

    system = (
        f"You are a scholarly translator fixing German residues in a {lang_name} Sanskrit-education text. "
        "Lines marked with >> contain German words that were not translated. "
        "Rules: "
        "(1) Translate ONLY the German words on lines marked >>. "
        "(2) Preserve all Markdown syntax, IAST, Devanāgarī (⟪...⟫), and container syntax exactly. "
        "(3) Return ONLY the corrected lines in the format [LN] corrected_text — one per line. "
        "(4) Do NOT return context lines (without >>). "
        "(5) Keep the scholarly editorial tone."
    )
    data = {
        "model": SONNET_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": snippet}
        ],
        "temperature": 0.1,
        "max_tokens": 2048,
    }

    import subprocess as _sp
    curl_cmd = [
        'curl', '-s', '-X', 'POST', SONNET_API_URL,
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'HTTP-Referer: https://sanskritkurs-payer.ch',
        '-d', json.dumps(data), '--max-time', '120'
    ]

    try:
        proc = _sp.run(curl_cmd, capture_output=True, text=True, timeout=125)
        if proc.returncode != 0:
            raise OSError(f"curl exit {proc.returncode}: {proc.stderr[:200]}")
        res = json.loads(proc.stdout)
        if 'error' in res:
            raise RuntimeError(f"API Error: {res['error']}")
        patched_text = res['choices'][0]['message']['content']
    except Exception as e:
        err_str = str(e)
        if "API Error" in err_str and ("'code': 402" in err_str or "'code': 404" in err_str or "'code': 401" in err_str):
            sys.stdout.write(f"\n[FATAL] Unrecoverable OpenRouter API Error in patcher: {err_str}\nAborting immediately.\n")
            sys.stdout.flush()
            sys.exit(1)
        sys.stdout.write(f"  [!] SONNET FALLBACK API error: {e}\n")
        sys.stdout.flush()
        return content

    # Parse Sonnet's response and apply corrections
    patched_lines = list(lines)  # copy
    for resp_line in patched_text.split('\n'):
        m = re.match(r'^\[[LЛlл]?(\d+)\](?:>>)?\s*(.*)', resp_line.strip())
        if m:
            idx = int(m.group(1))
            corrected = m.group(2)
            if 0 <= idx < len(patched_lines):
                patched_lines[idx] = corrected

    return '\n'.join(patched_lines)


def log_failure(
    lang: str,
    filename: str,
    failure_code: str,
    flagged_lines: list,
    note: str = ""
) -> None:
    """Append a structured entry to docs/qa/translation_failures.md."""
    os.makedirs(os.path.dirname(FAILURE_LOG_PATH), exist_ok=True)

    # Initialize file with header if it doesn't exist
    if not os.path.exists(FAILURE_LOG_PATH):
        with open(FAILURE_LOG_PATH, 'w', encoding='utf-8') as f:
            f.write("# Translation Failure Log\n\n")
            f.write("Automatically generated. Do not edit manually.\n\n")
            f.write("| Timestamp | Language | File | Code | Lines | Note |\n")
            f.write("|-----------|----------|------|------|-------|------|\n")

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    line_refs = ', '.join(str(i) for i, _ in flagged_lines[:10])
    if len(flagged_lines) > 10:
        line_refs += f' (+{len(flagged_lines) - 10} more)'
    note_clean = note.replace('|', '\\|').replace('\n', ' ')

    entry = f"| {ts} | {lang} | {filename} | `{failure_code}` | {line_refs} | {note_clean} |\n"
    with open(FAILURE_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(entry)

    sys.stdout.write(f"  [LOG] Failure logged: {lang}/{filename} [{failure_code}] — {len(flagged_lines)} residues\n")
    sys.stdout.flush()

def generate_licenses(lang):
    """Copy DE licenses.md verbatim, substituting only fixed UI phrases. No LLM."""
    labels = LICENSES_LABELS.get(lang)
    if not labels:
        return
    src_path = os.path.join(BASE_DIR, "licenses.md")
    out_path = os.path.join(BASE_DIR, lang, "licenses.md")
    if not os.path.exists(src_path):
        return
    if os.path.exists(out_path) and os.path.getmtime(out_path) > os.path.getmtime(src_path):
        print(f"[{lang}] Skipping licenses.md (up to date).")
        return
    with open(src_path, encoding="utf-8") as f:
        content = f.read()
    content = content.replace("# Bild-Lizenzen Audit", f"# {labels['title']}")
    content = content.replace(
        "| Stamm | Gefundene Quell-Angabe | Vorschau |",
        f"| {labels['col1']} | {labels['col2']} | {labels['col3']} |"
    )
    content = content.replace(
        "Keine spezielle Lizenz/Bildquelle im Text gefunden",
        labels["no_license"]
    )
    for de_phrase, trans in LICENSES_PHRASES.get(lang, {}).items():
        content = content.replace(de_phrase, trans)

    import glob
    captions = {}
    for lekt_file in glob.glob(os.path.join(BASE_DIR, lang, "lektionen", "*.md")):
        try:
            with open(lekt_file, "r", encoding="utf-8") as lf:
                lekt_content = lf.read()
            matches = re.finditer(r'!\[(.*?)\]\(/images/([^/.]+)\.(?:webp|jpg|png)\)', lekt_content)
            for m in matches:
                cap = m.group(1).strip()
                img_id = m.group(2)
                if cap and cap != img_id + ".jpg" and cap != img_id + ".webp":
                    captions[img_id] = cap
        except FileNotFoundError:
            pass
            
    if captions:
        updated_lines = []
        for line in content.split('\n'):
            m = re.match(r'^\|\s*<a id="([^"]+)">', line)
            if m:
                img_id = m.group(1)
                if img_id in captions:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        parts[2] = f" {captions[img_id]} "
                        line = "|".join(parts)
            updated_lines.append(line)
        content = '\n'.join(updated_lines)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[{lang}] Generated licenses.md (static copy + phrase substitution + dynamic caption sync).")


def parse_lesson_args(args):
    """Parse lesson number arguments. Returns (lesson_nums, translate_all)."""
    if not args or args[0] == "all":
        return LESSONS, True
    nums = []
    for a in args:
        if "-" in a and not a.startswith("-"):
            parts = a.split("-", 1)
            try:
                start, end = int(parts[0]), int(parts[1])
                nums.extend(range(start, end + 1))
            except ValueError:
                print(f"Warning: ignoring invalid range '{a}'")
        else:
            try:
                nums.append(int(a))
            except ValueError:
                print(f"Warning: ignoring non-numeric argument '{a}'")
    return nums, False


def parse_lang_args(args):
    """Extract --lang/-l, --force/-f, --pages/-p, --api, --model options from args."""
    languages = []
    force = False
    pages_only = False
    api_url = None
    model_id = None
    remaining = []
    i = 0
    while i < len(args):
        if args[i] in ("--lang", "-l") and i + 1 < len(args):
            codes = [c.strip() for c in args[i + 1].split(",")]
            invalid = [c for c in codes if c not in LANGUAGES]
            if invalid:
                print(f"Error: unknown language code(s): {', '.join(invalid)}")
                print(f"Valid codes: {', '.join(LANGUAGES)}")
                sys.exit(1)
            languages = codes
            i += 2
        elif args[i] == "--api" and i + 1 < len(args):
            api_url = args[i + 1]
            i += 2
        elif args[i] == "--model" and i + 1 < len(args):
            model_id = args[i + 1]
            i += 2
        elif args[i] in ("--force", "-f"):
            force = True
            i += 1
        elif args[i] in ("--pages", "-p"):
            pages_only = True
            i += 1
        else:
            remaining.append(args[i])
            i += 1
    return languages, force, pages_only, api_url, model_id, remaining


def translate_main_pages(lang, force=False):
    """Translate only the site-level main pages (index, grammatik, themen, impressum, licenses)."""
    lang_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    for filename in MAIN_PAGES:
        source_path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(source_path):
            continue
        def make_post(fname, l=lang):
            def post(t):
                # Unescape Vue component tags escaped by LLM
                t = t.replace('&lt;PayerTopicIndex /&gt;', '<PayerTopicIndex />')
                t = t.replace('&lt;style&gt;', '<style>').replace('&lt;/style&gt;', '</style>')
                if fname == "index.md":
                    t = fix_home_links(t, l)
                return t
            return post
        translate_file(source_path, os.path.join(lang_dir, filename), lang, post_process=make_post(filename), force=force)
    generate_licenses(lang)


def _fmt_elapsed(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s}s" if m else f"{s}s"


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 scripts/lan_translate.py --lang CODE[,CODE...] [-f] [-p] <all | lesson_num | start-end | num1 num2 ...>")
        print("Options:")
        print("  --lang/-l CODE[,CODE...]  (REQUIRED) translate only the given language(s)")
        print("  --force/-f                skip mtime check and always retranslate")
        print("  --pages/-p                translate only site-level pages (index, grammatik, impressum…)")
        print("Examples:")
        print("  python3 scripts/lan_translate.py --lang he all")
        print("  python3 scripts/lan_translate.py --lang he 28")
        print("  python3 scripts/lan_translate.py --lang it,es 28-32")
        print("  python3 scripts/lan_translate.py --lang it,es 28 29 30")
        print("  python3 scripts/lan_translate.py -l en -f 10")
        print("  python3 scripts/lan_translate.py --lang la --pages")
        sys.exit(1)

    active_languages, force, pages_only, new_api, new_model, remaining_args = parse_lang_args(args)

    if new_api:
        global API_URL
        API_URL = new_api
    if new_model:
        global MODEL
        MODEL = new_model

    if not active_languages:
        print("Error: You must explicitly specify languages using --lang/-l (e.g., --lang he).")
        sys.exit(1)

    if pages_only:
        print(f"Starting translation process using {MODEL} at {API_URL}...")
        print(f"Language filter: {', '.join(active_languages)}")
        print("Pages-only mode: translating site-level pages only.")
        for lang in active_languages:
            lang_start = time.time()
            print(f"[{lang}] Start: {time.strftime('%H:%M:%S')}")
            translate_main_pages(lang, force=force)
            elapsed = time.time() - lang_start
            print(f"[{lang}] End:   {time.strftime('%H:%M:%S')} — {_fmt_elapsed(elapsed)}")
        return

    lesson_nums, translate_all = parse_lesson_args(remaining_args)

    print(f"Starting translation process using {MODEL} at {API_URL}...")
    print(f"Language filter: {', '.join(active_languages)}")
    if force:
        print("Force mode: mtime check disabled.")
    for lang in active_languages:
        lang_start = time.time()
        print(f"[{lang}] Start: {time.strftime('%H:%M:%S')}")
        lesson_dir = os.path.join(BASE_DIR, lang, "lektionen")
        os.makedirs(lesson_dir, exist_ok=True)

        # ── Lektionen ────────────────────────────────────────────────────────
        for l_num in lesson_nums:
            filename = f"lektion{l_num:02d}.md"
            source_path = os.path.join(SOURCE_DIR, filename)
            if not os.path.exists(source_path):
                print(f"Source not found: {source_path}")
                continue
            post = lambda t, l=lang: fix_lesson_links(t, l)
            translate_file(source_path, os.path.join(lesson_dir, filename), lang, post_process=post, force=force)

        if translate_all:
            # ── Schriften & Übungen ──────────────────────────────────────────
            for filename in sorted(os.listdir(SOURCE_DIR)):
                if not (filename.startswith('schrift') or filename.startswith('uebung')):
                    continue
                if not filename.endswith('.md'):
                    continue
                source_path = os.path.join(SOURCE_DIR, filename)
                translate_file(source_path, os.path.join(lesson_dir, filename), lang, force=force)

            # ── Sonderdateien in lektionen/ ──────────────────────────────────
            for filename in ("wortliste.md", "inhaltsverzeichnis.md", "index.md", "glossar.md"):
                src = os.path.join(SOURCE_DIR, filename)
                if os.path.exists(src):
                    def make_post_process(fname):
                        if fname == "inhaltsverzeichnis.md":
                            def post(t):
                                # Fix misplaced backslashes in lesson headings (e.g. 1\0.1. -> 10\.1.)
                                return re.sub(r'(\d+)\\(\d+)\.(\d+)', r'\1\2\\.\3', t)
                            return post
                        return None
                    translate_file(src, os.path.join(lesson_dir, filename), lang, post_process=make_post_process(filename), force=force)

            # ── Hauptseiten ──────────────────────────────────────────────────
            translate_main_pages(lang, force=force)

        elapsed = time.time() - lang_start
        print(f"[{lang}] End:   {time.strftime('%H:%M:%S')} — {_fmt_elapsed(elapsed)}")


if __name__ == "__main__":
    main()
