import re

with open("docs/.vitepress/theme/components/PayerLanguageSettings.vue", "r") as f:
    content = f.read()

# Update template
old_template = """    <div class="locale-grid">
      <label 
        v-for="locale in ALL_LOCALES" 
        :key="locale" 
        class="locale-item"
        :class="{ 'is-disabled': locale === currentLocale }"
      >
        <input
          type="checkbox"
          :value="locale"
          v-model="selected"
          :disabled="locale === currentLocale"
          @change="markDirty"
        />
        <span class="locale-name">{{ LOCALE_NAMES[locale] }}</span>
        <span class="locale-code">({{ locale }})</span>
        <span v-if="locale === currentLocale" class="locale-current">{{ t.currentBadge }}</span>
      </label>
    </div>"""

new_template = """    <div class="settings-group">
      <h3 class="locale-group-title">{{ t.activeLanguages || 'Aktive Sprachen' }}</h3>
      <div class="locale-grid">
        <label 
          v-for="locale in ALL_LOCALES.filter(l => selected.includes(l))" 
          :key="locale" 
          class="locale-item"
          :class="{ 'is-disabled': locale === currentLocale }"
        >
          <input
            type="checkbox"
            :value="locale"
            v-model="selected"
            :disabled="locale === currentLocale"
            @change="markDirty"
          />
          <span class="locale-name">
            <span v-if="locale === 'bg'" class="quality-warning" title="Beta / Translation Quality Warning">⚠</span>
            {{ LOCALE_NAMES[locale] }}
          </span>
          <span class="locale-code">({{ locale }})</span>
          <span v-if="locale === currentLocale" class="locale-current">{{ t.currentBadge }}</span>
        </label>
      </div>
    </div>

    <div class="settings-group" v-if="ALL_LOCALES.filter(l => !selected.includes(l)).length > 0">
      <h3 class="locale-group-title">{{ t.availableLanguages || 'Weitere Sprachen hinzufügen' }}</h3>
      <div class="locale-grid">
        <label 
          v-for="locale in ALL_LOCALES.filter(l => !selected.includes(l))" 
          :key="locale" 
          class="locale-item unselected-item"
        >
          <input
            type="checkbox"
            :value="locale"
            v-model="selected"
            @change="markDirty"
          />
          <span class="locale-name">
            <span v-if="locale === 'bg'" class="quality-warning" title="Beta / Translation Quality Warning">⚠</span>
            {{ LOCALE_NAMES[locale] }}
          </span>
          <span class="locale-code">({{ locale }})</span>
        </label>
      </div>
    </div>"""

if old_template in content:
    content = content.replace(old_template, new_template)
else:
    print("WARNING: old_template not found!")

# Add translations
translations = {
  'de': "    activeLanguages: 'Aktive Sprachen',\n    availableLanguages: 'Weitere Sprachen hinzufügen',",
  'en': "    activeLanguages: 'Active Languages',\n    availableLanguages: 'Add more languages',",
  'it': "    activeLanguages: 'Lingue attive',\n    availableLanguages: 'Aggiungi altre lingue',",
  'bg': "    activeLanguages: 'Активни езици',\n    availableLanguages: 'Добавяне на други езици',",
  'ru': "    activeLanguages: 'Активные языки',\n    availableLanguages: 'Добавить другие языки',",
  'uk': "    activeLanguages: 'Активні мови',\n    availableLanguages: 'Додати інші мови',",
  'hi': "    activeLanguages: 'सक्रिय भाषाएँ',\n    availableLanguages: 'अन्य भाषाएँ जोड़ें',",
  'fr': "    activeLanguages: 'Langues actives',\n    availableLanguages: 'Ajouter d\\'autres langues',",
  'es': "    activeLanguages: 'Idiomas activos',\n    availableLanguages: 'Añadir más idiomas',",
  'ta': "    activeLanguages: 'செயலிலுள்ள மொழிகள்',\n    availableLanguages: 'மேலும் மொழிகளைச் சேர்',",
  'pa': "    activeLanguages: 'ਸਰਗਰਮ ਭਾਸ਼ਾਵਾਂ',\n    availableLanguages: 'ਹੋਰ ਭਾਸ਼ਾਵਾਂ ਸ਼ਾਮਲ ਕਰੋ',",
  'la': "    activeLanguages: 'Linguae activae',\n    availableLanguages: 'Adde plures linguas',",
  'rm': "    activeLanguages: 'Linguas activas',\n    availableLanguages: 'Agiuntar autras linguas',",
  'ro': "    activeLanguages: 'Limbi active',\n    availableLanguages: 'Adăugați alte limbi',"
}

for lang, translation in translations.items():
    pattern = f"({lang}: {{.*?)(title: )"
    content = re.sub(pattern, rf"\1{translation}\n    \2", content, flags=re.DOTALL)

with open("docs/.vitepress/theme/components/PayerLanguageSettings.vue", "w") as f:
    f.write(content)

print("Settings updated.")
