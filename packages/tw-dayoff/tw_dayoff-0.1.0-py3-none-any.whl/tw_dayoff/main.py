import requests

__all__ = ("TyphoonDayOff", "CityCountyNotFoundError")

class CityCountyNotFoundError(Exception):
    pass

class TyphoonDayOff:
    """
    Get the typhoon day off status of a city or county in Taiwan

    Args:
        city_county_name (str): The code of the city or county in Taiwan(Like kh(高雄市), tp(台北市), ntpc(新北市), etc.)

    Functions:
        get_dayoff(): Get the typhoon day off status of the city or county
    """
    def __init__(self, city_county_name: str):
        self.api_url = "https://twdayoff-api.vercel.app/api/dayoff"
        self.city_county_name = city_county_name

    def get_dayoff(self):
        """
        Get the typhoon day off status of the city or county
        :return:
            str: The typhoon day off status of the city or county
        """
        response = requests.get(self.api_url)
        data = response.json()
        for county in data:
            if county["cityName"] == self.city_county_name:
                return county["status"]
        raise CityCountyNotFoundError(f"{self.city_county_name} not found")