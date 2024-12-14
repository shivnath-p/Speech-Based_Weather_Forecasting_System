import requests
import speech_recognition as sr
import pyttsx3

API_KEY = '30e259f8809c41f0bcd171718240712'

def speak(text):
    """Speak the given text."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def fetch_weather(city):
    """Get weather details for the given city."""
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": city, "aqi": "no"}
    response = requests.get(url, params=params)
    return response.json()

def get_weather(city):
    """Process and display weather data."""
    data = fetch_weather(city)
    if "error" not in data:
        name = data["location"]["name"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        result = f"Weather in {name}: {temp}°C, {condition}."
        print(result)
        speak(result)
    else:
        speak("City not found. Please try again.")
        print("City not found. Please try again.")

def main():
    """Main function to get city name using voice and fetch weather."""
    recognizer = sr.Recognizer()
    speak("Say the name of the city you want the weather for.")
    
    while True:
        try:
            with sr.Microphone() as mic:
                print("Listening...")
                audio = recognizer.listen(mic)
                city = recognizer.recognize_google(audio)
                print(f"You said: {city}")
                get_weather(city)

                speak("Do you want to check another city? Say yes or no.")
                print("Listening for yes or no...")
                audio = recognizer.listen(mic)
                response = recognizer.recognize_google(audio).lower()

                if "no" in response:
                    speak("Goodbye!")
                    break
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please try again.")
            print("Sorry, I didn't understand. Please try again.")
        except Exception as e:
            speak("An error occurred.")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

