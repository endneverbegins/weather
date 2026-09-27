import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)

from PyQt5.QtCore import Qt


class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        # Create the widgets
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)

        # These labels will show the weather information
        self.temperature_label = QLabel("N/A", self)
        self.description_label = QLabel("N/A", self)

        # Set up the user interface
        self.initUI()

    def initUI(self):

        # Set the title of the window
        self.setWindowTitle("Weather Appie :3")

        # Create a vertical layout
        vbox = QVBoxLayout()

        # Add the widgets to the layout
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.description_label)

        # Apply the layout to the window
        self.setLayout(vbox)

        # Center the text inside the widgets
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Give each widget an object name so we can style it with CSS
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")

        # Apply some styling to the application
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }

            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }

            QLineEdit#city_input {
                font-size: 40px;
            }

            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                font-size: 75px;
            }

            QLabel#description_label {
                font-size: 30px;
            }
        """)

        # This is important:
        # It connects the button's clicked signal to get_weather().
        # Without this, clicking the button would do nothing.
        self.get_weather_button.clicked.connect(self.get_weather)

        # This allows the user to press Enter after typing a city
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):

        # Put your NEW OpenWeather API key here.
        # Do not post your API key publicly.
        api_key = "3532023faf645ec4de6962734c7bcb68"

        # Get the city entered by the user
        city = self.city_input.text().strip()

        # Check if the user entered a city
        if not city:
            self.display_error("Please enter a city.")
            return

        # OpenWeather API URL
        url = "https://api.openweathermap.org/data/2.5/weather"

        # Parameters sent to the API
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        try:
            # Send the request to OpenWeather
            response = requests.get(url, params=params, timeout=10)

            # Convert the response from JSON into a Python dictionary
            data = response.json()

            # A status code of 200 means the request was successful
            if response.status_code == 200:
                self.display_weather(data)

            else:
                # OpenWeather usually provides an error message
                # such as "city not found" or "invalid API key"
                error_message = data.get(
                    "message",
                    "Something went wrong."
                )

                self.display_error(error_message)

        # Handle problems such as no internet connection
        except requests.RequestException as e:
            self.display_error(f"Network error: {e}")

        # Handle unexpected JSON/API responses
        except ValueError:
            self.display_error("The server returned invalid data.")

    def display_weather(self, data):

        # Get the temperature from the API response
        temperature = data["main"]["temp"]

        # Get the weather description
        description = data["weather"][0]["description"]

        # Get some additional information
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        # Update the temperature label
        self.temperature_label.setText(
            f"{temperature:.1f}°C"
        )

        # Update the description label
        self.description_label.setText(
            f"{description.capitalize()}\n"
            f"Feels like: {feels_like:.1f}°C\n"
            f"Humidity: {humidity}%"
        )

    def display_error(self, message):

        # Show an error in the temperature label
        self.temperature_label.setText("Error")

        # Show the actual error message underneath
        self.description_label.setText(message)


# This code only runs when this file is executed directly
if __name__ == "__main__":

    # Create the PyQt application
    app = QApplication(sys.argv)

    # Create our weather application
    weather_app = WeatherApp()

    # Show the window
    weather_app.show()

    # Start the PyQt event loop
    sys.exit(app.exec_())