# translateEpub
Une démo pour traduire mes fichiers epub en français, via un client LLM générique
(compatible SDK OpenAI) qui peut pointer vers Socle AI, OpenAI, ou Anthropic.

## Configuration

Crée un fichier `.env` à la racine (utilisé via `python-decouple`) :

```
PROVIDER=socle       # socle | openai | anthropic
API_KEY=xxxxxxxxxxxxxxxxxx
MODEL_NAME=xxxxxxxxxxxxxxxxxx
# BASE_URL=...       # optionnel, pour surcharger l'URL du provider
```

Pour l'usage de Socle je vous conseille le modèle 'qwen3-235b-a22b-instruct-2507'

## Installation

```
pip install ebooklib beautifulsoup4 gtts python-decouple openai
```

## Utilisation

```
python main.py mon_livre.epub
```
