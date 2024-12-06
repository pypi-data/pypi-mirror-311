import requests

def is_spam(message, model_name='spamNS_v6', user_token=None, server_choice=1, api_key=None): 
    if server_choice == 1:
        if not api_key:
            print("API key is required for authentication.")
            return False, 0
        api_url = "https://neurospacex-modelhost.hf.space/api/check_spam"
        headers = {
            "api-key": api_key
        }
        data = {
            "message": message,
            "model_name": model_name
        }
    elif server_choice == 2:
        api_url = "https://sawfly-divine-rabbit.ngrok-free.app/api/check_spam"
        
        if not user_token:
            print("API token is required for authentication.")
            return False, 0
        
        headers = {
            "Authorization": user_token
        }
        data = {
            "message": message,
            "model_name": model_name
        }
    else:
        print("Invalid server choice. Choose either 1 or 2.")
        return False, 0

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        is_spam_result = result.get('is_spam', 0) == 1
        confidence = result.get('confidence', 0)
        return is_spam_result, confidence
    else:
        print(f"Error with API request: {response.status_code}")
        if response.status_code == 400:
            result = response.json()
            if 'error' in result:
                print("Error:", result['error'])
        return False, 0
