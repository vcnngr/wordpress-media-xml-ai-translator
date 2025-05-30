# XML CDATA Translator

Applicazione web Docker per tradurre automaticamente il contenuto dei tag CDATA nei file XML utilizzando l'API di OpenAI.

In un sito Wordpress esportare i media tramite Tools -> Export.

Passare il file .xml che viene generato a questa APP che si occuperà per ogni lingua prescelta di tradurre tutti 
i dati delle singole immagini. A questo punto importare il file nel nuvo sito nella nuova lingua.


## 🚀 Avvio Rapido

1. Esegui questo script per generare tutti i file
2. Naviga nella cartella `xml-translator`
3. Esegui: `docker-compose up --build`
4. Apri: `http://localhost:5000`

## 📋 Requisiti

- Docker e Docker Compose
- API Key di OpenAI
- File XML con tag CDATA

## 🎯 Funzionalità

- ✅ Rilevamento automatico della lingua
- ✅ Traduzione in 5 lingue (EN, FR, ES, RU, IT)  
- ✅ Preserva struttura XML
- ✅ Interfaccia web moderna
- ✅ Containerizzato con Docker

## 📁 Struttura Generata

```
xml-translator/
├── xml_translator.py      # Motore di traduzione
├── app.py                 # Applicazione Flask  
├── requirements.txt       # Dipendenze Python
├── Dockerfile            # Configurazione Docker
├── docker-compose.yml    # Orchestrazione
├── templates/
│   └── index.html        # Interfaccia web
├── uploads/              # Upload temporanei
└── outputs/              # Output temporanei
```

## 💡 Utilizzo

1. Inserisci la tua API Key OpenAI
2. Seleziona la lingua di destinazione
3. Carica il file XML
4. Scarica il file tradotto

## 🔒 Sicurezza

- API Key non salvate permanentemente
- Validazione rigorosa dei file
- Pulizia automatica file temporanei
- Container non-root

## 📞 Supporto

Per problemi o miglioramenti, crea una issue nel repository.
