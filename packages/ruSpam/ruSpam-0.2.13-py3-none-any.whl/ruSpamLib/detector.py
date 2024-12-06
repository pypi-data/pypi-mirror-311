import requests

def is_spam(message, model_name='spamNS_v6', user_token=None): 
    if not user_token:
        print("API token is required for authentication.")
        return False, 0
    
    api_url = "https://sawfly-divine-rabbit.ngrok-free.app/api/check_spam"
    headers = {
        "Authorization": user_token
    }
    data = {
        "message": message,
        "model_name": model_name
    }
    
    response = requests.post(api_url, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        is_spam_result = result.get('is_spam', 0) == 1
        confidence = result.get('confidence', 0)
        return is_spam_result, confidence
    else:
        print(f"Ngrok server failed with status code {response.status_code}. Trying the second server.")
        api_url = "https://neurospacex-modelhost.hf.space/api/check_spam"
        headers = {
            "api-key": user_token
        }
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
