# Onboarding-Prozess für neue Payer-Autoren

Da Authelia absichtlich keine öffentliche Registrierung ("Sign-up") anbietet, müssen neue Autoren-Konten vom Administrator manuell angelegt werden.

## 1. Nutzeranfrage
Der neue Mitarbeiter muss sich per E-Mail an [onboarding@birchville.org](mailto:onboarding@birchville.org) beim Administrator melden und um einen Zugang für das Autoren-Portal (`payer-author.birchville.cc`) bitten.

## 2. Initial-Passwort generieren
Loggen Sie sich auf der Synology per SSH ein.
Generieren Sie einen sicheren Passwort-Hash für das Startpasswort (z. B. `Start123!`) mit diesem Befehl:

```bash
docker run --rm authelia/authelia:latest authelia crypto hash generate pbkdf2 --password 'Start123!'
```

Kopieren Sie den erzeugten String, der mit `$pbkdf2-sha...` beginnt.

## 3. Nutzerkonto in der YAML-Datenbank anlegen
Öffnen Sie auf der Synology die Datei:
`/volume1/docker/authelia/config/users_database.yml`

Fügen Sie ganz unten den neuen Nutzer bündig (!) an. Achten Sie strikt auf die korrekte Einrückung (jeweils 4 Leerzeichen für die Felder unterhalb des Usernamen):

```yaml
  anna:
    displayname: "Anna Müller"
    password: "$pbkdf2-sha512...HIER_DEN_KOPIERTEN_HASH_EINFÜGEN..."
    email: "anna@birchville.org"
    groups:
      - authors
```

Speichern Sie die Datei ab. Authelia lädt die Datei im Regelfall im Hintergrund automatisch neu. Falls nicht, führen Sie `docker restart authelia` aus.

## 4. Nutzer informieren
Teilen Sie der Person ihren Username (`anna`) und das gewählte Initialpasswort (`Start123!`) mit. 

Sobald sich die Person das erste Mal einloggt, wird sie von Authelia aufgefordert, die Zwei-Faktor-Authentifizierung (2FA) einzurichten. Danach kann der Nutzer jederzeit über die "Passwort vergessen"-Funktion ein eigenes, geheimes Passwort vergeben (sofern SMTP konfiguriert ist).
