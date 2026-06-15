import os
import re

languages = {
    "en": """::: tip Version 1.4 — Offline-First PWA
**New in v1.4 (June 2026):**

- **Progressive Web App (PWA):** The course can now be installed as an app on your desktop and smartphone (iOS/Android).
- **Fully Offline:** All selected content is stored locally and can be used completely without an internet connection.
- **Dynamic Caching:** You can use the Settings to precisely control which of the 14 languages should be available offline at any time.
- **High Performance:** Massive reduction in loading times and data consumption thanks to highly compressed WebP images.

**Comments and bug reports:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "it": """::: tip Versione 1.4 — Offline-First PWA
**Novità nella v1.4 (Giugno 2026):**

- **Progressive Web App (PWA):** Il corso può ora essere installato come app su desktop e smartphone (iOS/Android).
- **Completamente Offline:** Tutti i contenuti selezionati vengono salvati localmente e sono utilizzabili senza connessione a internet.
- **Caching Dinamico:** Tramite le Impostazioni (Settings) è possibile gestire in modo preciso quali delle 14 lingue devono essere disponibili offline.
- **Alte Prestazioni:** Massiccia riduzione dei tempi di caricamento e del consumo dati grazie a immagini WebP altamente compresse.

**Commenti e segnalazioni di errori:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "es": """::: tip Versión 1.4 — Offline-First PWA
**Novedades en la v1.4 (Junio de 2026):**

- **Progressive Web App (PWA):** El curso ahora puede instalarse como aplicación en escritorio y teléfono inteligente (iOS/Android).
- **Completamente Offline:** Todos los contenidos seleccionados se almacenan localmente y pueden utilizarse sin conexión a Internet.
- **Caché Dinámico:** A través de la Configuración (Settings) se puede controlar con precisión en cualquier momento cuáles de los 14 idiomas deben estar disponibles sin conexión.
- **Alto Rendimiento:** Reducción masiva de los tiempos de carga y del consumo de datos mediante imágenes WebP altamente comprimidas.

**Comentarios y avisos de errores:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "fr": """::: tip Version 1.4 — Offline-First PWA
**Nouveautés de la v1.4 (Juin 2026):**

- **Progressive Web App (PWA):** Le cours peut désormais être installé sous forme d'application sur ordinateur et smartphone (iOS/Android).
- **Entièrement Hors Ligne:** Tout le contenu sélectionné est stocké localement et est utilisable sans connexion Internet.
- **Mise en cache dynamique:** Les paramètres (Settings) permettent de contrôler à tout moment quelles des 14 langues doivent être disponibles hors ligne.
- **Haute Performance:** Réduction massive des temps de chargement et de la consommation de données grâce aux images WebP hautement compressées.

**Remarques et rapports de bogues:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "ru": """::: tip Версия 1.4 — Offline-First PWA
**Новое в v1.4 (Июнь 2026):**

- **Progressive Web App (PWA):** Курс теперь можно установить как приложение на компьютер и смартфон (iOS/Android).
- **Полностью Офлайн:** Весь выбранный контент сохраняется локально и доступен без подключения к интернету.
- **Динамическое кэширование:** Через настройки (Settings) можно в любой момент точно настроить, какие из 14 языков должны быть доступны офлайн.
- **Высокая производительность:** Значительное сокращение времени загрузки и потребления данных благодаря сильно сжатым изображениям WebP.

**Комментарии и сообщения об ошибках:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "uk": """::: tip Версія 1.4 — Offline-First PWA
**Нове у v1.4 (Червень 2026):**

- **Progressive Web App (PWA):** Тепер курс можна встановити як додаток на комп'ютер та смартфон (iOS/Android).
- **Повністю Офлайн:** Весь обраний контент зберігається локально і доступний повністю без підключення до інтернету.
- **Динамічне кешування:** Через налаштування (Settings) можна в будь-який час точно керувати тим, які з 14 мов мають бути доступні офлайн.
- **Висока продуктивність:** Масове скорочення часу завантаження та споживання даних завдяки висококомпресованим зображенням WebP.

**Зауваження та повідомлення про помилки:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "bg": """::: tip Версия 1.4 — Offline-First PWA
**Ново във v1.4 (Юни 2026):**

- **Progressive Web App (PWA):** Курсът вече може да се инсталира като приложение на компютър и смартфон (iOS/Android).
- **Напълно Офлайн:** Цялото избрано съдържание се съхранява локално и може да се използва без интернет връзка.
- **Динамично кеширане:** Чрез Настройките (Settings) можете точно да контролирате по всяко време кои от 14-те езика да са достъпни офлайн.
- **Висока производителност:** Масивно намаляване на времето за зареждане и консумацията на данни чрез силно компресирани WebP изображения.

**Забележки и съобщения за грешки:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "hi": """::: tip संस्करण 1.4 — Offline-First PWA
**v1.4 में नया (जून 2026):**

- **Progressive Web App (PWA):** पाठ्यक्रम को अब डेस्कटॉप और स्मार्टफोन (iOS/Android) पर एक ऐप के रूप में स्थापित किया जा सकता है।
- **पूरी तरह से ऑफ़लाइन:** सभी चयनित सामग्री स्थानीय रूप से सहेजी जाती है और इंटरनेट कनेक्शन के बिना पूरी तरह से उपयोग की जा सकती है।
- **डायनेमिक कैशिंग:** सेटिंग्स (Settings) के माध्यम से आप किसी भी समय सटीक रूप से नियंत्रित कर सकते हैं कि 14 भाषाओं में से कौन सी ऑफ़लाइन उपलब्ध होनी चाहिए।
- **उच्च प्रदर्शन:** उच्च संपीड़ित WebP छवियों के कारण लोडिंग समय और डेटा खपत में भारी कमी।

**टिप्पणियाँ और बग रिपोर्ट:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "ta": """::: tip பதிப்பு 1.4 — Offline-First PWA
**v1.4 இல் புதியது (ஜூன் 2026):**

- **Progressive Web App (PWA):** இந்த பாடநெறியை இப்போது டெஸ்க்டாப் மற்றும் ஸ்மார்ட்போனில் (iOS/Android) ஒரு செயலியாக நிறுவ முடியும்.
- **முழுக்க ஆஃப்லைன்:** தேர்ந்தெடுக்கப்பட்ட அனைத்து உள்ளடக்கங்களும் உள்ளூரிலேயே சேமிக்கப்படுகின்றன, இணைய இணைப்பு இல்லாமலேயே பயன்படுத்தலாம்.
- **டைனமிக் கேச்சிங்:** அமைப்புகள் (Settings) மூலம் 14 மொழிகளில் எவை ஆஃப்லைனில் கிடைக்க வேண்டும் என்பதை எப்போது வேண்டுமானாலும் துல்லியமாக கட்டுப்படுத்தலாம்.
- **உயர் செயல்திறன்:** மிகவும் சுருக்கப்பட்ட WebP படங்களால் ஏற்றுதல் நேரம் மற்றும் தரவு நுகர்வு பெருமளவில் குறைக்கப்பட்டுள்ளது.

**கருத்துகள் மற்றும் பிழை அறிக்கைகள்:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "pa": """::: tip ਸੰਸਕਰਣ 1.4 — Offline-First PWA
**v1.4 ਵਿੱਚ ਨਵਾਂ (ਜੂਨ 2026):**

- **Progressive Web App (PWA):** ਕੋਰਸ ਨੂੰ ਹੁਣ ਡੈਸਕਟਾਪ ਅਤੇ ਸਮਾਰਟਫ਼ੋਨ (iOS/Android) 'ਤੇ ਇੱਕ ਐਪ ਵਜੋਂ ਸਥਾਪਤ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ।
- **ਪੂਰੀ ਤਰ੍ਹਾਂ ਔਫਲਾਈਨ:** ਸਾਰੀ ਚੁਣੀ ਗਈ ਸਮੱਗਰੀ ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਸੁਰੱਖਿਅਤ ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਅਤੇ ਇੰਟਰਨੈਟ ਕਨੈਕਸ਼ਨ ਤੋਂ ਬਿਨਾਂ ਵਰਤੀ ਜਾ ਸਕਦੀ ਹੈ।
- **ਡਾਇਨਾਮਿਕ ਕੈਚਿੰਗ:** ਸੈਟਿੰਗਾਂ (Settings) ਰਾਹੀਂ ਤੁਸੀਂ ਕਿਸੇ ਵੀ ਸਮੇਂ ਨਿਯੰਤਰਿਤ ਕਰ ਸਕਦੇ ਹੋ ਕਿ 14 ਭਾਸ਼ਾਵਾਂ ਵਿੱਚੋਂ ਕਿਹੜੀਆਂ ਔਫਲਾਈਨ ਉਪਲਬਧ ਹੋਣੀਆਂ ਚਾਹੀਦੀਆਂ ਹਨ।
- **ਉੱਚ ਪ੍ਰਦਰਸ਼ਨ:** ਉੱਚ ਸੰਕੁਚਿਤ WebP ਚਿੱਤਰਾਂ ਦੁਆਰਾ ਲੋਡਿੰਗ ਦੇ ਸਮੇਂ ਅਤੇ ਡੇਟਾ ਦੀ ਖਪਤ ਵਿੱਚ ਵੱਡੀ ਕਮੀ।

**ਟਿੱਪਣੀਆਂ ਅਤੇ ਬੱਗ ਰਿਪੋਰਟਾਂ:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "la": """::: tip Versio 1.4 — Offline-First PWA
**Nova in v1.4 (Iunio 2026):**

- **Progressive Web App (PWA):** Cursus nunc ut app in computatro et telephono gestabili (iOS/Android) institui potest.
- **Penitus Sine Reti:** Omnia argumenta selecta in disco servata sunt et sine interreti adhiberi possunt.
- **Caching Dynamicum:** Per praeferentias (Settings) semper accurate gubernare potes, quaenam ex 14 linguis sine reti praesto sint.
- **Praestantia Summa:** Reductio ingens temporis ad onerandum et consumptionis datorum propter imagines WebP compressissimas.

**Animadversiones et relationes mendorum:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "rm": """::: tip Versiun 1.4 — Offline-First PWA
**Nov en v1.4 (Zercladur 2026):**

- **Progressive Web App (PWA):** Il curs po uss vegnir installà sco app sin il desktop ed il smartphone (iOS/Android).
- **Tuttafatg Offline:** Tut ils cuntegns selecziunads vegnan memorisads localmain e pon vegnir duvrads senza connexiun d'internet.
- **Caching Dinamic:** Via las opziuns (Settings) pon ins controllar da tut temp precis, qualas da las 14 linguas che duain esser disponiblas offline.
- **Auta Prestaziun:** Reducziun massiva dal temp da chargiar e dal consum da datas grazia a maletgs WebP fitg cumpressads.

**Remartgas ed annunzias da sbagls:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::""",
    "ro": """::: tip Versiunea 1.4 — Offline-First PWA
**Nou în v1.4 (Iunie 2026):**

- **Progressive Web App (PWA):** Cursul poate fi acum instalat ca o aplicație pe desktop și smartphone (iOS/Android).
- **Complet Offline:** Tot conținutul selectat este salvat local și poate fi utilizat complet fără conexiune la internet.
- **Caching Dinamic:** Prin Setări (Settings) se poate controla precis în orice moment care dintre cele 14 limbi să fie disponibile offline.
- **Performanță Înaltă:** Reducere masivă a timpilor de încărcare și a consumului de date prin imagini WebP extrem de comprimate.

**Comentarii și raportări de erori:** [webmaster@birchville.cc](mailto:webmaster@birchville.cc)
:::"""
}

base_dir = "/Volumes/SanDisk1TB/proj/Payer/docs"
for lang, new_tip in languages.items():
    file_path = os.path.join(base_dir, lang, "index.md")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the old tip block with the new tip block
        content = re.sub(
            r'::: tip Version 1\.3.*?:::', 
            new_tip, 
            content, 
            flags=re.DOTALL
        )
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {lang}/index.md")

