import requests

def is_spam(message, model_name='spamNS_v6', user_token=None): 
    """
    Проверяет, является ли сообщение спамом, и возвращает дополнительные параметры из API.
    
    :param message: Строка сообщения для анализа.
    :param model_name: Имя модели для использования (по умолчанию: 'spamNS_v6').
    :param user_token: Токен API для аутентификации.
    
    :return: Словарь с результатами анализа (включая is_spam, confidence, model_used, tokens_used, cost, api_key).
    """
    if not user_token:
        print("API token is required for authentication.")
        return {
            "is_spam": False,
            "confidence": 0.0,
            "model_used": None,
            "tokens_used": 0,
            "cost": 0.0,
            "api_key": None,
        }
    
    api_urls = [
        "https://sawfly-divine-rabbit.ngrok-free.app/api/check_spam",
        "https://neurospacex-modelhost.hf.space/api/check_spam"
    ]
    
    headers = {
        "api-key": user_token
    }
    data = {
        "message": message,
        "model_name": model_name
    }
    
    for api_url in api_urls:
        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"Response received from server: {api_url}")
                return {
                    "is_spam": result.get('is_spam', 0) == 1,
                    "confidence": result.get('confidence', 0.0),
                    "model_used": result.get('model_used', model_name),
                    "tokens_used": result.get('tokens_used', 0),
                    "cost": result.get('cost', 0.0),
                    "api_key": result.get('api_key', user_token),
                }
            else:
                print(f"Server at {api_url} failed with status code {response.status_code}.")
                if response.status_code == 400:
                    result = response.json()
                    if 'error' in result:
                        print(f"Error: {result['error']}")
        except requests.exceptions.RequestException as e:
            print(f"Network error while connecting to {api_url}: {e}")
    
    print("All servers failed to process the request.")
    return {
        "is_spam": False,
        "confidence": 0.0,
        "model_used": model_name,
        "tokens_used": 0,
        "cost": 0.0,
        "api_key": user_token,
    }
