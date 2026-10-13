
import requests

url = "https://jezalyn-indic.onrender.com/course"

try:
    response = requests.get(url, timeout=30)

    print("Status Code:", response.status_code)
    response.raise_for_status()

    data = response.json()

    print("\nCOURSE INFORMATION")
    print("------------------")
    print("Course Code:", data["course_code"])
    print("Course Title:", data["course_title"])
    print("Instructor:", data["instructor"])
    print("Semester:", data["semester"])
    print("Academic Year:", data["academic_year"])

except requests.exceptions.RequestException as e:
    print("Request failed:", e)

except (ValueError, KeyError) as e:
    print("Error processing response:", e)