import os
import json
import urllib.request
import time
import sys
import re

# Configuration
API_URL = "http://nyx.local:8000/v1/chat/completions"
MODEL = "mlx-community/Qwen3.6-35B-A3B-4bit"
LANGUAGES = [
#    "en", "it", "es", "ru", "uk", "bg", "hi", "fr", "rm",
#    "ar", "arc", "he", "zh", "la", "grc", "el", "fa", "akk", "cop",
    "en", "it", "es", "ru", "uk", "bg", "hi", "fr", "ta", "pa",
    "la", "rm", "ro", "id", "zh-CN", "zh-TW", "th", "he"
]
LANG_NAMES = {
    "en": "English", "it": "Italian", "es": "Spanish",
    "ru": "Russian", "uk": "Ukrainian", "bg": "Bulgarian",
    "hi": "Hindi", "fr": "French", "ta": "Tamil", "pa": "Punjabi (Gurmukhi)",
    "la": "Latin", "rm": "Romansh Grischun", "ro": "Romanian",
    "id": "Indonesian", "zh-CN": "Simplified Chinese", "zh-TW": "Traditional Chinese",
    "th": "Thai", "he": "Hebrew",
#    "ar": "Arabic", "arc": "Aramaic",
#    "zh": "Mandarin Chinese",
#    "grc": "Ancient Greek", "el": "Modern Greek",
#    "fa": "Persian (Farsi)", "akk": "Akkadian", "cop": "Coptic",
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
    "zh-TW": {
        "Abb.:": "圖.:",
        "Bildquelle:": "圖片來源:",
        "Bildquelle.": "圖片來源.",
        "Bildquelle ": "圖片來源 ",
        "gemeinfrei": "公共領域",
        "Jhdt.": "世紀",
        "Zugriff am": "訪問日期",
        "Namensnennung": "署名",
        "keine kommerzielle Nutzung": "非商業性使用",
        "keine kommerzielle Nuttzung": "非商業性使用",
        "keine kommerzielle Bearbeitung": "非商業性使用，禁止演繹",
        "keine Bearbeitung": "禁止演繹",
        "GNU FDLizenz": "GNU FD許可證",
        "FDLicense": "FD License",
        "Creative  Commons Lizenz": "知識共享許可證",
        "Creative Commons Lizenz": "知識共享許可證",
        "Creative Commons lizenz": "知識共享許可證",
        "Unbekannt": "未知",
        "Beschriftung:": "說明:",
        "Lehrgangsmaterial": "課程材料",
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


def translate_text(text, target_lang):
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    _mark_skt = (target_lang == 'hi')
    protected, deva_registry = protect_devanagari(text)
    protected, iast_registry = protect_iast_lines(protected)
    protected = protect_br(protected)
    system = (
        f"You are a scholarly translator. Translate ALL German text in this Sanskrit-education markdown to {lang_name}. "
        "Rules: "
        "(1) Translate every German word — including captions, image descriptions, verse translations, and prose. "
        "(2) Preserve unchanged: Markdown syntax, VitePress containers (:::), IAST transliterations, YAML frontmatter keys, HTML comments, ⟨DEVA_N⟩ placeholders, ⟨IAST_L_N⟩ placeholders, and ⟨BR⟩ placeholders. "
        f"(3) Translate '# Lektion N' headings to the target-language equivalent (e.g. '# Lesson N' in English, '# Lezione N' in Italian, '# Lección N' in Spanish, '# Урок N' in Russian/Ukrainian/Bulgarian, '# पाठ N' in Hindi, '# Leçon N' in French, '# Lecziun N' in Romansh Grischun, '# பாடம் N' in Tamil, '# ਪਾਠ N' in Punjabi, '# الدرس N' in Arabic, '# ܡܠܦܢܘܬܐ N' in Aramaic, '# שיעור N' in Hebrew, '# 第N课' in Mandarin Chinese, '# บทที่ N' in Thai, '# Lectio N' in Latin, '# Μάθημα N' in Ancient Greek, '# Μάθημα N' in Modern Greek, '# درس N' in Persian, '# Ṭupšarru N' in Akkadian, '# ⲙⲁⲑⲏⲙⲁ N' in Coptic). "
        "(4) NEVER add TODO comments, fallback markers, or any annotations of your own. If unsure how to translate something, translate it as best you can. "
        "(5) Keep the scholarly editorial tone throughout. "
        "(6) CRITICAL: Preserve the exact line count of the source. Every source line must appear as exactly one output line. NEVER delete, merge, or collapse lines. "
        "(7) CRITICAL: Copy every ⟨DEVA_N⟩ and ⟨IAST_L_N⟩ placeholder character-for-character. They are replaced with Devanāgarī and IAST text after translation — do NOT interpret, transliterate, or remove them. "
        "(7a) CRITICAL: Lines consisting ONLY of ⟨DEVA_N⟩ tokens (and spaces/punctuation like ।  ॥) are Sanskrit verse lines. Copy every token on that line verbatim. NEVER transliterate Sanskrit verses into the target script — the placeholders will be restored to Devanāgarī automatically. "
        "(7b) CRITICAL: Preserve ALL Markdown image syntax exactly: ![alt](/path/to/image.jpg) — never drop the parentheses around the image path. "
        "(8) Numbered exercise sentences (e.g. '3. Śūdras erlangen...', '4. Die Kṣatriyas...') MUST be translated to the target language even when they begin with Sanskrit proper nouns in IAST notation. The IAST proper noun is preserved as-is; only the surrounding German words are translated."
    )
    best_result = None
    best_missing: list = list(deva_registry.keys())  # worst case: all missing

    max_ph_retries = 3
    for ph_attempt in range(max_ph_retries):
        # Bump temperature on retries so the model makes different choices.
        temperature = 0.3 if ph_attempt == 0 else 0.6
        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": protected}
            ],
            "temperature": temperature,
            "max_tokens": 4096
        }

        max_retries = 5
        got_response = False
        for attempt in range(max_retries):
            try:
                import subprocess as _sp
                start_time = time.time()
                _proc = _sp.run(
                    ['curl', '-s', '-X', 'POST', API_URL,
                     '-H', 'Content-Type: application/json',
                     '-d', json.dumps(data),
                     '--max-time', '1800'],
                    capture_output=True, text=True, timeout=1820
                )
                end_time = time.time()
                if _proc.returncode != 0:
                    raise OSError(f"curl exit {_proc.returncode}: {_proc.stderr[:200]}")
                res_data = json.loads(_proc.stdout)
                result = res_data['choices'][0]['message']['content']
                got_response = True

                # Performance Monitoring & Auto-Restart
                if 'usage' in res_data and 'completion_tokens' in res_data['usage']:
                    comp_tokens = res_data['usage']['completion_tokens']
                    elapsed = end_time - start_time
                    if elapsed > 0:
                        tps = comp_tokens / elapsed
                        sys.stdout.write(f"      [Speed: {tps:.1f} t/s | {comp_tokens} tokens in {elapsed:.1f}s]\n")
                        sys.stdout.flush()
                        if comp_tokens > 20 and tps < 5.0:
                            sys.stdout.write(f"\n[!] Performance kritisch ({tps:.1f} t/s). Führe automatischen Neustart aus...\n")
                            sys.stdout.flush()
                            try:
                                _sp.run(['ssh', 'marco@nyx.local', 'nohup ~/llm-benchmark/start > /dev/null 2>&1 &'], timeout=15)
                                sys.stdout.write("[!] Neustart-Befehl gesendet. Warte 25s auf den Server...\n")
                                sys.stdout.flush()
                                time.sleep(25)
                            except Exception as ssh_e:
                                sys.stdout.write(f"[!] SSH Neustart fehlgeschlagen: {ssh_e}\n")
                                sys.stdout.flush()

                missing = [k for k in deva_registry if k not in result]
                if len(missing) < len(best_missing):
                    best_result = result
                    best_missing = missing
                if not missing:
                    result = restore_devanagari(result, deva_registry, _mark_skt)
                    result = restore_iast_lines(result, iast_registry)
                    result = restore_br(result)
                    return result
                # Got a response but placeholders were dropped — retry outer loop.
                if ph_attempt < max_ph_retries - 1:
                    sys.stdout.write(
                        f"[{target_lang}] Placeholder drop ({len(missing)}): "
                        f"{missing[:3]}{'…' if len(missing) > 3 else ''} "
                        f"— retrying ({ph_attempt + 2}/{max_ph_retries}, T={0.6})...\n"
                    )
                    sys.stdout.flush()
                break  # break connection-retry loop; outer loop handles the rest
            except Exception as e:
                err_str = str(e)
                wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s, 40s, 80s
                
                # Auto-Restart bei Timeouts, HTTP 500 (Compute error) oder Absturz (Connection refused/exit 7)
                err_lower = err_str.lower()
                if "exit 28" in err_str or "timeout" in err_lower or "500" in err_str or "exit 7" in err_str or "refused" in err_lower or "choices" in err_lower:
                    sys.stdout.write(f"\n[!] Timeout/Absturz erkannt ({err_str}). Führe automatischen Neustart aus...\n")
                    sys.stdout.flush()
                    try:
                        import subprocess as _sp_err
                        _sp_err.run(['ssh', 'marco@nyx.local', 'nohup ~/llm-benchmark/start > /dev/null 2>&1 &'], timeout=15)
                        sys.stdout.write("[!] Neustart-Befehl gesendet. Warte 25s...\n")
                        sys.stdout.flush()
                        time.sleep(25)
                    except Exception:
                        pass

                msg = f"[{target_lang}] Connection failed (attempt {attempt+1}/{max_retries}): {err_str}. Retrying in {wait_time}s...\n"
                sys.stdout.write(msg)
                sys.stdout.flush()
                time.sleep(wait_time)

        if not got_response:
            return f"ERROR: Failed to translate after {max_retries} attempts."

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
    return result

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


def translate_file(source_path, target_path, lang, post_process=None, force=False):
    """Translate a single file with mtime-based skip and chunking. Returns True on success."""
    filename = os.path.basename(source_path)
    if not force and os.path.exists(target_path) and os.path.getsize(target_path) > 500:
        if os.path.getmtime(target_path) > os.path.getmtime(source_path):
            print(f"[{lang}] Skipping {filename} (up to date).")
            return True
        print(f"[{lang}] Outdated {filename} — re-translating...")

    print(f"[{lang}] Translating {filename}...")
    with open(source_path, encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_content(content)
    translated_chunks = []
    for i, chunk in enumerate(chunks, 1):
        if not chunk.strip():
            translated_chunks.append(chunk)
            continue
        print(f"  -> section {i}/{len(chunks)}...")
        result = translate_text(chunk, lang)
        if result.startswith("ERROR:"):
            print(f"  [!] Failed chunk {i}: {result}")
            return False
        translated_chunks.append(result)

    translated = escape_angle_brackets_in_tables('\n\n'.join(translated_chunks))
    if post_process:
        translated = post_process(translated)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(translated)
    print(f"[{lang}] Done {filename}.")
    time.sleep(2)
    return True


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
        elif is_safe_break and current_chunk and current_size > 0:
            # Even if under MAX_CHUNK, break at safe boundaries to keep
            # chunks small and translation quality high.
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(line)
        current_size += len(line) + 1

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

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
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[{lang}] Generated licenses.md (static copy + phrase substitution).")


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
    """Extract --lang/-l, --force/-f, --pages/-p options from args. Returns (languages, force, pages_only, remaining_args)."""
    languages = list(LANGUAGES)
    force = False
    pages_only = False
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
        elif args[i] in ("--force", "-f"):
            force = True
            i += 1
        elif args[i] in ("--pages", "-p"):
            pages_only = True
            i += 1
        else:
            remaining.append(args[i])
            i += 1
    return languages, force, pages_only, remaining


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
        print("Usage: python3 scripts/lan_translate.py [--lang CODE[,CODE...]] [-f] [-p] <all | lesson_num | start-end | num1 num2 ...>")
        print("Options:")
        print("  --lang/-l CODE[,CODE...]  translate only the given language(s)")
        print("  --force/-f                skip mtime check and always retranslate")
        print("  --pages/-p                translate only site-level pages (index, grammatik, impressum…)")
        print("Examples:")
        print("  python3 scripts/lan_translate.py all")
        print("  python3 scripts/lan_translate.py 28")
        print("  python3 scripts/lan_translate.py 28-32")
        print("  python3 scripts/lan_translate.py 28 29 30")
        print("  python3 scripts/lan_translate.py --lang it 28")
        print("  python3 scripts/lan_translate.py --lang it,es all")
        print("  python3 scripts/lan_translate.py -l en -f 10")
        print("  python3 scripts/lan_translate.py --lang la --pages")
        sys.exit(1)

    active_languages, force, pages_only, remaining_args = parse_lang_args(args)

    if pages_only:
        print(f"Starting translation process using {MODEL} at {API_URL}...")
        if active_languages != list(LANGUAGES):
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
    if active_languages != list(LANGUAGES):
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
            for filename in ("wortliste.md", "inhaltsverzeichnis.md", "index.md"):
                src = os.path.join(SOURCE_DIR, filename)
                if os.path.exists(src):
                    translate_file(src, os.path.join(lesson_dir, filename), lang, force=force)

            # ── Hauptseiten ──────────────────────────────────────────────────
            translate_main_pages(lang, force=force)

        elapsed = time.time() - lang_start
        print(f"[{lang}] End:   {time.strftime('%H:%M:%S')} — {_fmt_elapsed(elapsed)}")


if __name__ == "__main__":
    main()
