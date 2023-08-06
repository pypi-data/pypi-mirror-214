import pandas as pd
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

if __name__ == "__main__":

    class fourcast:
        
        """
        Object for weather prediction 
        Nt= number of hourly time steps
        Area of interest is defined by minlat,minlon,maxlat,maxlon
        mintime = time now
        maxtime = time now + Nt number of hours
        """

        def __init__(self, lat, lon):

            self.lat = lat
            self.lon = lon

        def json2df(url_current):

            """
            Convert to DataFrame
            """

            dfcur = pd.read_json(url_current)
            df = dfcur.daily.to_frame().T
            arr = []
            Nrows = len(df.time[0])
            for i in range(Nrows):
                col = []
                for column in df.columns:
                    col.append(df[column][0][i])
                arr.append(col)
            data = pd.DataFrame(columns=df.columns, data=arr)
            data.time = (data['time']).apply(lambda d: pd.to_datetime(str(d)))

            return data
        
        def day_cast(self, model):

            """
            Method for weather prediction at a point 
            with coordinates lat,lon.

            model:  best_match
                    ecmwf_ifs04
                    gfs_seamless
                    gfs_global
                    icon_seamless
                    gem_seamless
                    jma_seamless
                    meteofrance_seamless
            """
            url = f'https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&models={model}&forecast_days=1&timezone=Europe%2FMoscow'
            data = fourcast.json2df(url)

            # Translate wmo codes
            wmo_codes = {0:'Clear sky',
                        1:'Mainly clear',
                        2:'Partly cloudy',
                        3:'Overcast',
                        45:'Fog',
                        48:'Depositing rime fog',
                        51:'Drizzle light intensity',
                        53:'Drizzle moderate intensity',
                        55:'Drizzle dense intensity',
                        56:'Freezing Drizzle light intensity',
                        57:'Freezing Drizzle dense intensity',
                        61:'Rain slight intensity',
                        63:'Rain moderate intensity',
                        65:'Rain heavy intensity',
                        66:'Freezing rain light intensity',
                        67:'Freezing rain heavy intensity',
                        71:'Snow fall slight intensity',
                        73:'Snow fall moderate intensity',
                        75:'Snowfall heavy intensity',
                        77:'Snow grains',
                        80:'Rain showers slight',
                        81:'Rain showers moderate',
                        82:'Rain showers violent',
                        85:'Snow showers slight',
                        86:'Snow showers heavy',
                        95:'Thunderstorm slight or moderate',
                        96:'Thunderstorm with slight hail',
                        99:'Thunderstorm with heavy hail'}
            
            for code in wmo_codes.keys():
                data.weathercode = data.weathercode.apply(lambda x: wmo_codes.get(code) if x==code else x)
            data = data.rename(columns={'time':'date'})

            return data.T
        
        def flood_cast(self):

            url = f'https://flood-api.open-meteo.com/v1/flood?latitude={self.lat}&longitude={self.lon}&daily=river_discharge&start_date=2023-01-01&end_date=2023-06-30&forecast_days=1'
            data = fourcast.json2df(url)
            data = data.rename(columns={'time':'date'})
            
            return data
