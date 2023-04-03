from fake_useragent import UserAgent

import requests
import json


class Controller:
    def __init__(self):
        pass

    @staticmethod
    def save_all_vac():
        print("preparing data")
        fua = UserAgent().random
        try:
            query = "https://api.hh.ru/vacancies?text=&area=154&" \
                    "search_period=2&" \
                    "order_by=publication_time&" \
                    "per_page=50&no_magic=true&"
            response = requests.get(query, headers={
                "user-agent": fua
            }).json()
            pages = response["pages"]

            this_page = response["page"]
            for page_num in range(this_page, round(pages/2)):
                query = "https://api.hh.ru/vacancies?" \
                        "text=&area=154&" \
                    "search_period=2&" \
                    "order_by=publication_time&" \
                    "per_page=50&no_magic=true&" \
                        f"page={page_num}"
                response = requests.get(query).json()["items"]
                for vac in response:
                    with open("data/data.json", "r", encoding="utf-8") as file:
                        data = json.load(file)
                        data.append(vac)
                    with open("data/data.json", "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
            print("data created")

        except Exception as ex:
            print(ex)

    @staticmethod
    def get_vac():
        with open("data/data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        vacancies = []
        for item in data:
            currency = ""
            sal_from_to = ""
            address = "Не указан"
            geo = None
            responsibility = "Не указан"
            if "salary" in item and isinstance(item["salary"], dict) and isinstance(item["salary"]["currency"], str):
                currency = f"{item['salary']['currency']}"
                if isinstance(item["salary"]["from"], int) and isinstance(item["salary"]["to"], int):
                    sal_from_to = f"{item['salary']['from']} - {item['salary']['to']} {currency}💰"
                elif isinstance(item["salary"]["from"], int) and not isinstance(item["salary"]["to"], int):
                    sal_from_to = f'{item["salary"]["from"]} {currency}💰'
                elif isinstance(item["salary"]["from"], int) and isinstance(item["salary"]["to"], int):
                    sal_from_to = f'{item["salary"]["to"]} {currency}💰'

            if isinstance(item["address"], dict) and "address" in item and isinstance(item["address"]["street"], str):
                street = f'#{item["address"]["street"]}'.replace(" ", "").replace("-", "_").replace("-", "_")
                address = f'{street}, {item["address"]["building"]}'
                if isinstance(item["address"]["lat"], float):
                    geo = [item["address"]["lat"], item["address"]["lng"]]

            if isinstance(item["snippet"], dict) and isinstance(item["snippet"]["responsibility"], str):
                responsibility = item["snippet"]["responsibility"]

            roles = item["professional_roles"][0]["name"]
            vacancy = {
                "name": item["name"],
                "salary": sal_from_to,
                "employer": item["employer"]["name"],
                "responsibility": responsibility,
                "address": address,
                "role": f"{roles}",
                "link": item["alternate_url"],
                "geo": geo
            }
            vacancies.append(vacancy)
            print(vacancy["address"])
        print("Vacs send!")
        return vacancies

    @staticmethod
    def clear_data():
        with open("data/data.json", "w", encoding="utf-8") as file:
            arr = []
            json.dump([], file)
            print("data cleared")


if __name__ == '__main__':
    c = Controller()
    # c.clear_data()
    # c.save_all_vac()
    vacs = c.get_vac()
