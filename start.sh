#!/bin/bash
# Script di setup rapido per XML Translator

echo "🐳 Avvio XML Translator..."
# cd wordpress-media-xml-ai-translator

echo "📦 Build del container..."
docker-compose up --build -d

echo "✅ Applicazione avviata!"
echo "🌐 Accedi a: http://localhost:3000"
echo "📋 Per fermare: docker-compose down"
