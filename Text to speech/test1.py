import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set the properties of the engine
engine.setProperty('rate', 150)   # Set the speaking rate (words per minute)
engine.setProperty('volume', 1)   # Set the volume (min: 0, max: 1)

# Define the text to be spoken
text = "Hello, world! This is an example of text-to-speech conversion in Python."

# Convert the text to speech
engine.say(text)

# Run the TTS engine
engine.runAndWait()
