from django.shortcuts import render

# Create your views here.
from datetime import date
from .utils import WeatherStation, CSV_READER, EXCEL_READER, ONLINEDATA

def home(request):
    return render(request, "app1/home.html")

def report(request):
    source = request.POST.get("source")
    ws = WeatherStation()
    today = date.today()

    if source == "csv":
        reader = CSV_READER("data.csv")
        ws.data = reader.read_data()

    elif source == "excel":
        reader = EXCEL_READER("data.xlsx")
        ws.data = reader.read_data()

    elif source == "api":
        cities = ["Mumbai", "Bangalore", "Delhi", "Chennai"]
        api = ONLINEDATA()
        ws.data = api.read_data(cities)

    context = {
        "source": source.upper(),
        "avg_temp": ws.avg_temp(),
        "avg_hum": ws.avg_hum(),
        "daily": ws.daily_summarize(today),
        "weekly": ws.weekly_summary(today),
    }

    return render(request, "app1/report.html", context)
