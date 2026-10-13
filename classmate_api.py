
import requests

url = "https://distura-kate-ashley.onrender.com/student"

try:
    response = requests.get(url, timeout=30)

    print("Status Code:", response.status_code)
    response.raise_for_status()

    try:
        data = response.json()

        print("\nCLASSMATE API RESPONSE")
        print("----------------------")

        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print(data)

    except ValueError:
        print("Response is not JSON:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)