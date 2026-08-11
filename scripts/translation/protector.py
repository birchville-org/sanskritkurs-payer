"""
Protection and restoration functions for Devanāgarī, IAST lines, line breaks, and Markdown structural containers.
"""

import re
from .config import _DEVA_RE

_IAST_DIACRITICS_RE = re.compile(r'[āĀīĪūŪṛṚṝṜḷḶṭṬḍḌṇṆṣṢśŚñÑṅṄṃṂḥḤ]')
_IAST_LINE_RE = re.compile(r'^[a-zA-ZāĀīĪūŪṛṚṝṜḷḶṭṬḍḌṇṆṣṢśŚñÑṅṄṃṂḥḤ\s\|.,;:!\-]+$')
_GERMAN_CONNECTORS_RE = re.compile(r'\b(und|des|Abb)\b')

BR_PLACEHOLDER = '⟨BR⟩'

def protect_devanagari(text):
    """Replace every Devanāgarī run with a unique placeholder. Returns (protected_text, registry)."""
    # Merge adjacent Sanskrit ⟪...⟫ ⟪...⟫ tags into single blocks to prevent LLM placeholder explosion
    text = re.sub(r'⟫\s*⟪', ' ', text)
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
        if line.strip() == '---' or line.strip().startswith(':::'):
            key = f'⟨STRUCT_{counter[0]}⟩'
            registry[key] = line
            counter[0] += 1
            result_lines.append(key)
        else:
            result_lines.append(line)
    return '\n'.join(result_lines), registry

def restore_structure(text, registry):
    def replace_struct(m):
        idx = m.group(1)
        key = f'⟨STRUCT_{idx}⟩'
        return registry.get(key, m.group(0))
    
    text = re.sub(r'[⟨<〈]STRUCT_[^⟩>〉]*?(\d+)[⟩>〉]', replace_struct, text)
    
    for key, original in registry.items():
        text = text.replace(key, original)
    return text
