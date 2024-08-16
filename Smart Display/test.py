import requests

i = 0  # Initialize i

while True:  # Infinite loop or add condition to exit as needed
    if i == 6:
        i = 0
    else:
        with open('stocks.txt', 'r') as file:
            lines = file.readlines()
            if i < len(lines):  # Ensure index is within bounds
                ticker = lines[i].strip()
                print(ticker)
        
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

        i+=1

        print(today_close_value)
        print(yesterday_close_value)
        print(percentage)