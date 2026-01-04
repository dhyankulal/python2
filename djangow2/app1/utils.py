import pandas as pd
import numpy as np
import requests
from datetime import date, timedelta

API="b2febde596b24c579d273828250312"

class WeatherStation:
    def __init__(self):
        self.data = None

    def csv_sum(self):
        return self.data.describe().to_string()
    
    def avg_temp(self):
        if self.data is None or self.data.empty or "Temperature_C" not in self.data:
            return "No API data"
        return float(np.average(self.data["Temperature_C"]))

    def avg_hum(self):
        if self.data is None or self.data.empty or "Humidity_%" not in self.data:
            return "No API data"
        return float(np.average(self.data["Humidity_%"]))

    
    def daily_summarize(self, current_date):
        if self.data is None or self.data.empty:
            return None

        today = self.data[self.data["Date"] == current_date.strftime("%Y-%m-%d")]
        if today.empty:
            return None

        return {
            "Temperature_C": {
                "count": int(today["Temperature_C"].count()),
                "mean": round(float(today["Temperature_C"].mean()), 2),
                "std": round(float(today["Temperature_C"].std()), 2),
                "min": round(float(today["Temperature_C"].min()), 2),
                "max": round(float(today["Temperature_C"].max()), 2),
            },
            "Humidity_%": {
                "count": int(today["Humidity_%"].count()),
                "mean": round(float(today["Humidity_%"].mean()), 2),
                "std": round(float(today["Humidity_%"].std()), 2),
                "min": int(today["Humidity_%"].min()),
                "max": int(today["Humidity_%"].max()),
            }
        }

    
    def weekly_summary(self, current_date):
        if self.data is None or self.data.empty:
            return None

        self.data["Date"] = pd.to_datetime(self.data["Date"])
        start_date = current_date - timedelta(days=6)

        week = self.data[
            (self.data["Date"].dt.date >= start_date) &
            (self.data["Date"].dt.date <= current_date)
        ]

        if week.empty:
            return None

        return {
            "Temperature_C": {
                "mean": round(float(week["Temperature_C"].mean()), 2),
                "min": round(float(week["Temperature_C"].min()), 2),
                "max": round(float(week["Temperature_C"].max()), 2),
            },
            "Humidity_%": {
                "mean": round(float(week["Humidity_%"].mean()), 2),
                "min": int(week["Humidity_%"].min()),
                "max": int(week["Humidity_%"].max()),
            }
        }

class CSV_READER(WeatherStation):
    def __init__(self, file):
        super().__init__()
        self.file = file

    def read_data(self):
        self.file = r"D:\Coding\combine learning\python Lkg\whether\data.csv"
        self.data = pd.read_csv(self.file)
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data.ffill(inplace=True)
        return self.data


class EXCEL_READER(WeatherStation):
    def __init__(self, file):
        super().__init__()
        self.file = file

    def read_data(self):
        self.file = r"D:\Coding\combine learning\python Lkg\whether\data.xlsx"
        self.data = pd.read_excel(self.file)
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data.ffill(inplace=True)
        return self.data


class ONLINEDATA(WeatherStation):
    def read_data(self, cities):
        rows = []
        for city in cities:
            try:
                url = f"http://api.weatherapi.com/v1/current.json?key={API}&q={city}"
                data = requests.get(url).json()
                rows.append({
                    "City": city,
                    "Temperature_C": data["current"]["temp_c"],
                    "Humidity_%": data["current"]["humidity"],
                    "Date": data["location"]["localtime"][:10]
                })
            except Exception as e:
                print(f"Failed for {city}:", e)
            
        self.data = pd.DataFrame(rows)
        return self.data
    '''
25
    def avg_temp(self):
        return float(np.average(self.data["Temperature_C"]))

    def avg_hum(self):
        return float(np.average(self.data["Humidity_%"]))
    '''
    '''
    def daily_summarize(self, current_date):
        today = self.data[self.data['Date'] == current_date.strftime("%Y-%m-%d")]
        if today.empty:
            return "No data found for today"
        return today.describe().to_string()
    '''
    '''
    51
    def weekly_summary(self, current_date):
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        start_date = current_date - timedelta(days=6)
        week_data = self.data[
            (self.data["Date"].dt.date >= start_date) &
            (self.data["Date"].dt.date <= current_date)
        ]
        return week_data.describe().to_string()
    '''