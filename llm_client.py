"""
Client LLM générique basé sur le SDK OpenAI.

Fonctionne avec n'importe quel fournisseur qui expose une API compatible
OpenAI (Socle AI, OpenAI lui-même, ou Anthropic via sa couche de
compatibilité OpenAI) : on se contente de changer l'URL de base et la clé
d'API, le reste du code ne change pas.

Variables d'environnement (voir .env) :
    PROVIDER    socle | openai | anthropic   (défaut: socle)
    API_KEY     clé d'API du fournisseur choisi
    MODEL_NAME  nom du modèle à utiliser chez ce fournisseur
    BASE_URL    optionnel, surcharge l'URL par défaut du provider
"""

from openai import OpenAI
from decouple import config

# URL de base par défaut pour chaque fournisseur.
# Anthropic n'expose sa couche de compatibilité OpenAI que sur /v1/chat/completions
# (pas d'équivalent à client.responses.create) ; on utilise donc partout
# chat.completions.create, seule méthode disponible chez les trois fournisseurs.
PROVIDER_BASE_URLS = {
    "socle": "https://app.socle.ai/api/v1",
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com/v1",
}


def get_client() -> OpenAI:
    provider = config("PROVIDER", default="socle").lower()
    base_url = config("BASE_URL", default=PROVIDER_BASE_URLS.get(provider))

    if base_url is None:
        raise ValueError(
            f"Provider inconnu '{provider}'. Utilise PROVIDER=socle|openai|anthropic "
            "ou renseigne BASE_URL directement."
        )

    return OpenAI(
        api_key=config("API_KEY"),
        base_url=base_url,
    )


def chat(prompt: str, system: str | None = None) -> str:
    """Envoie un prompt au LLM configuré et renvoie le texte de la réponse."""
    client = get_client()
    model = config("MODEL_NAME")
    provider = config("PROVIDER", default="socle").lower()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    extra_body = {}
    if provider == "socle":
        # "reasoning.effort" est une extension propre à Socle AI (low/medium/high/
        # high_plan/exhaustive) : pas de champ équivalent chez OpenAI/Anthropic,
        # on ne l'envoie donc que pour ce provider.
        extra_body["reasoning"] = {"effort": config("REASONING_EFFORT", default="low")}

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # Limite les boucles de répétition ("in-in-in-...") auxquelles les
        # petits modèles sont sujets sur de longs passages.
        frequency_penalty=config("FREQUENCY_PENALTY", default=0.4, cast=float),
        presence_penalty=config("PRESENCE_PENALTY", default=0.4, cast=float),
        extra_body=extra_body or None,
    )
    return response.choices[0].message.content
