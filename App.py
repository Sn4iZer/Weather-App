import streamlit as st
import requests
import datetime 

st.title("Weather App 🌥️")
#listofcities = ["Rabat", "Kenitra", "Tiflet"]
# city = st.selectbox("Chose a city", listofcities)
city = st.text_input("Enter a City name : ", value="Kenitra")

API_KEY = "your_api_key_here"

if city:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        st.write(f"### Weather in {data['name']}")

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        country = data["sys"]["country"]
        icon = data["weather"][0]["icon"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        pressure = data["main"]["pressure"]

        col1, col2 = st.columns([1, 3])

        with col1:
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            st.image(icon_url, caption=description)

        with col2:
            st.success(f"📍 {city}, {country}")
            st.text(f"🌡️ Temperature: {temp}°C")
            st.text(f"☁️ Condition: {description.capitalize()}")

        st.markdown("---")
        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric(label="💧 Humidity", value=f"{humidity}%")
        with m2:
            st.metric(label="🌬️ Wind Speed", value=f"{wind} m/s")
        with m3:
            st.metric(label="⏱️ Pressure", value=f"{pressure} hPa")

        st.markdown("## 📅 5-Day Forecast")
        
        url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response_forecast = requests.get(url_forecast)
        
        if response_forecast.status_code == 200:
            forecast_data = response_forecast.json()
            forecasts = forecast_data["list"]
            
            daily_forecasts = {}
            for forecast in forecasts:
                date = forecast["dt_txt"].split(" ")[0]
                time = forecast["dt_txt"].split(" ")[1]
                if time == "12:00:00": 
                    daily_forecasts[date] = forecast
            
            cols = st.columns(5)
            for i, (date, forecast) in enumerate(daily_forecasts.items()):
                with cols[i]:
                    day = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%a %d")
                    temp = forecast["main"]["temp"]
                    desc = forecast["weather"][0]["description"].title()
                    icon = forecast["weather"][0]["icon"]
                    icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
                    
                    st.write(f"**{day}**")
                    st.image(icon_url)
                    st.write(f"{temp}°C")
                    st.write(desc)
        else:
            st.error("Forecast data not available")

    else:

        st.error("City not found! Please try again.")
