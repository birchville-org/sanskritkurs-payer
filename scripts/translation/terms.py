"""
Shared German & Grammar Terminology Library for Quality Control and QA checks.
Single Source of Truth across the translation pipeline.
"""
import re

DE_FALLBACK_ALLOWED = {"rm", "grc", "el", "la"}

LATIN_TOLERANT_LANGS = {"en", "fr", "it", "es", "pt", "rm", "nl", "ro", "la", "tr", "vi", "id", "af"}

EXCLUDE_META = {
    "licenses.md", "AUTHORS_GUIDE.md", "settings.md", "impressum.md", 
    "grammatik.md", "themen.md", "qa_help.md"
}

LATIN_GRAMMAR_TERMS = {
    "Nominativ", "Akkusativ", "Genetiv", "Instrumentalis", "Vokativ", 
    "Ablativ", "Passiv", "Infinitiv", "Dativ", "Lokativ", "Komposita"
}

STRICT_DE_GRAMMAR_KEYWORDS = [
    "Präsensklasse", "Verschlusslaut", "stimmhaft", "stimmlose", "stimmlosem",
    "Wiederholungsübung", "Bildungen auf", "wird durch", "bleiben unverändert",
    "bei Maskulina", "bei Neutra", "außer j", "entsprechenden", "Ersetzung durch",
    "mit direktem Objekt", "Passivsatz", "Doppelter Akkusativ", "Fragepronomina",
    "Glückbringender Anfang", "Konsonantenzeichen", "Materialien zum Sanskrit",
    "Zusätzliche Übung", "Verehrung des", "Laute des Sanskrit", "Bildquelle:",
    "Lautlehre", "Wortkunde", "Satzlehre", "Substantive und Adjektive", 
    "Pronomina", "Konjugation",
    # Instruction phrases & exercise patterns
    "Übersetzen Sie ins Sanskrit", "Übersetzen Sie ins Deutsche", "Übersetzen Sie:", "Übersetzen Sie",
    "Bilden Sie das Ātmanepada", "Bilden Sie das Femininum", "Bilden Sie:", "Bilden Sie",
    "Setzen Sie in den Plural", "Setzen Sie:", "Setzen Sie",
    "Formt das Ātmanepada", "Formt das Femininum", "Formt das",
    "Ergänzen Sie:", "Ergänzen Sie", "Bestimmen Sie:", "Bestimmen Sie",
    "Verwandeln Sie:", "Verwandeln Sie", "Deklinieren Sie:", "Deklinieren Sie",
    "Konjugieren Sie:", "Konjugieren Sie", "Schreiben Sie in Devanāgarī",
    "Zweimalgeborene sind", "Zweimalgeborene", "Opferherr",
    "ist eine Göttin", "ist ein Gott", "ist ein Heiliger", "ist ein Meister", "ist eine Gottheit",
    "sind verwirrt", "treten ein", "lässt emanieren", "besonders zu merken",
    "steht am Beginn", "Zusammengestellt aus den Wortlisten", "Möglichkeiten)", "Möglichkeit)"
]

GERMAN_KEYWORDS = [
    "Die Laute des Sanskrit", "Verehrung des", "Schriftübung", "Glückbringender Anfang", 
    "Bildquelle:", "Jedes Konsonantenzeichen", "Materialien zum Sanskrit", "Zusätzliche Übung", 
    "Auslautendes", "wird es zu", "Ersetzung durch", "mit direktem Objekt",
    "Der Passivsatz", "Doppelter Akkusativ", "Fragepronomina",
    "Übersetzen Sie", "Bilden Sie", "Setzen Sie", "Formt das"
]

# Distinct German grammatical expressions that indicate untranslated German text
RAW_RESIDUE_TERMS = [
    "d.h.", "usw.", "vgl.", "z.B.", "Stammabstufung", "auslautend", "Formgleich", 
    "mehrsilbig", "entweder", "Dehnstufe", "Hochstufe", "Tiefstufe", "Normalstufe", 
    "Schwundstufe", "Merke:", "Beachte:", "Anmerkung:", "Hinweis:", "Beispiel:", 
    "Beispiele:", "Präsensklasse", "Aoristklasse", "Perfektstamm", "Desiderativstamm", 
    "Kausativstamm", "Verbalwurzel", "Kasusendung", "Kasussystem", "Deklinationsklasse", 
    "Konjugationsklasse", "Sandhi-Regel", "Lautgesetz", "Stammvokal",
    "er, sie, es; der, die, das", "dieser, diese, dieses", "dem Sprechenden sehr Nahe"
]

ALL_TERMS = sorted(list(set(STRICT_DE_GRAMMAR_KEYWORDS + GERMAN_KEYWORDS + RAW_RESIDUE_TERMS)), key=len, reverse=True)

# Pre-compiled regex for fast residue scanning (strict word boundaries supporting punctuation)
DE_RESIDUE_REGEX = re.compile(
    r'(?<!\w)(' + '|'.join(re.escape(t) for t in ALL_TERMS) + r')(?!\w)',
    re.IGNORECASE
)

