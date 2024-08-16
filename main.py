import customtkinter as ctk
import requests
import datetime

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Smart Display")
        self.geometry("1920x1080")

        # Create frames for each screen
        self.stock_frame = self.create_stock_frame()
        self.weather_frame = self.create_weather_frame()
        self.time_frame = self.create_time_frame()

        # Add frames to a list for easy cycling
        self.frames = [self.stock_frame, self.weather_frame, self.time_frame]
        self.current_frame = 0

        # Show the first screen
        self.show_frame(self.current_frame)

        # Start cycling through the screens
        self.cycle_screens()

    def create_stock_frame(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True)

        self.stock_ticker = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=250, weight="bold"))
        self.stock_ticker.pack(anchor="w", padx=80, pady=10)

        self.stock_price_today = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=200, weight="bold"))
        self.stock_price_today.pack(anchor="w", padx=80, pady=10)

        self.stock_percentage = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=150))
        self.stock_percentage.pack(anchor="w", padx=80, pady=10)

        self.update_stock_data()
        return frame

    def create_weather_frame(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True)

        self.weather_location = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=250))
        self.weather_location.pack(anchor="w", padx=80, pady=10)

        self.weather_condition = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=150))
        self.weather_condition.pack(anchor="w", padx=80, pady=10)

        self.weather_temperature = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=150))
        self.weather_temperature.pack(anchor="sw", padx=80, pady=10)

        #self.weather_humidity = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=100))
        #self.weather_humidity.pack(anchor="sw", padx=80, pady=10)
       
        self.update_weather_data()
        return frame

    def create_time_frame(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True)

        self.time_info_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=250))
        self.time_info_label.pack(pady=440)

        self.update_time()
        return frame

    def show_frame(self, index):
        for i, frame in enumerate(self.frames):
            if i == index:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def cycle_screens(self):
        self.show_frame(self.current_frame)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(5000, self.cycle_screens)  # Switch screens every 5000 milliseconds (5 seconds)

    def update_stock_data(self): 
        """if i == 6: #cycle mech
            i = 0
        else:
            with open('stocks.txt', 'r') as file:
                lines = file.readlines()
            ticker = lines[i].strip()
            print ticker
        i+=1"""

        with open('stocks.txt', 'r') as file:
            lines = file.readlines()
            ticker = lines[0].strip()
        

        url = "https://api.twelvedata.com/time_series?"    
        querystring = {"symbol": ticker, "interval": "1day", "apikey": "a405777a469a49a09a6410ff350c595a"}
        response = requests.get(url, params=querystring) #Making the request to the API

        if response.status_code == 200: #Checking if the request was successful
            data = response.json()
        
            today_close_value = data['values'][0]['close']
            yesterday_close_value = data['values'][1]['close']

            today_close_value = float(today_close_value)
            yesterday_close_value = float(yesterday_close_value)        
        
            percentage = (today_close_value - yesterday_close_value)/yesterday_close_value*100

        else:
            print("Stock API Error")

        self.stock_ticker.configure(text=f"{ticker}")
        self.stock_price_today.configure(text=f"{today_close_value}")

        if percentage > 0:
            self.stock_percentage.configure(text=f"{percentage:.2f}%", text_color="green")
        else:
            self.stock_percentage.configure(text=f"{percentage:.2f}%", text_color="red")

    def update_weather_data(self):
        city = "Boston"
        url = "https://api.openweathermap.org/data/2.5/weather"    
        querystring = {"q": city, "appid": "fce8f922f1d10ee82680f0c9fa17b7e8", "units": "imperial"}
        response = requests.get(url, params=querystring) #Making the request to the API

        if response.status_code == 200: #Checking if the request was successful
            data = response.json()
            main = data['main']
            weather = data['weather'][0]
            
            # Extracting and printing the data
            temperature = main['temp']
            humidity = main['humidity']
            description = weather['description']
            description = description.title()
        else:
            print("City not found or an error occurred.")

        self.weather_location.configure(text=f"{city}")
        self.weather_temperature.configure(text=f"{temperature}°F")
        self.weather_condition.configure(text=f"{description}")
        #self.weather_humidity.configure(text=f"{humidity}%")


    def update_time(self):
        # Update the time every second
        now = datetime.datetime.now().strftime("%I:%M:%S %p")
        
        self.time_info_label.configure(text=now)
        self.after(1000, self.update_time)  # Update time every 1000 milliseconds (1 second)

if __name__ == "__main__":
    app = App()
    app.mainloop()
