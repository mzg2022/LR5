import requests
from xml.etree import ElementTree as ET
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Currencies(metaclass=Singleton):
    def __init__(self, request_interval=1):
        self.valutes = []
        self.request_interval = request_interval
        self.last_request_time = 0

    def get_currencies(self, currencies_ids_lst: list) -> list:
        """Метод для получения курсов валют с сайта ЦБ РФ."""
        current_time = time.time()

        # Контроль частоты запросов
        if current_time - self.last_request_time < self.request_interval:
            raise Exception(f"Запрос можно отправлять не чаще, чем раз в {self.request_interval} секунд.")

        self.last_request_time = current_time
        result = []
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        valutes = root.findall("Valute")

        for currency_id in currencies_ids_lst:
            valute = next((v for v in valutes if v.get('ID') == currency_id), None)
            if valute is not None:
                valute_cur_name, valute_cur_val = valute.find('Name').text, valute.find('Value').text
                valute_charcode = valute.find('CharCode').text
                result.append({valute_charcode: (valute_cur_name, valute_cur_val)})
            else:
                # Если валюты с данным ID нет, возвращаем None
                result.append({currency_id: None})
        return result

    def visualize_currencies(self, currencies_lst, show_plot=False, save_fig=False):
        """Визуализация списка валют в виде графика."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        names = []
        values = []

        for currency in currencies_lst:
            for code, (name, value) in currency.items():
                names.append(code)
                values.append(float(value.replace(',', '.')))

        ax.bar(names, values)
        ax.set_ylabel('Курсы валют')
        ax.set_title('Курсы валют ЦБ РФ')

        if save_fig:
            plt.savefig('currencies.jpg')

        if show_plot:
            plt.show()  # Показываем график только если show_plot=True
        else:
            plt.close()  # Закрываем график, если не нужно показывать

if __name__ == "__main__":
    cur = Currencies()
    currencies_ids = ['R01035', 'R01335', 'R01700J']  # Замените на нужные вам ID валют
    result = cur.get_currencies(currencies_ids)
    print(result)

    # Если вы хотите также визуализировать курсы валют:
    cur.visualize_currencies(result, show_plot=True, save_fig=True)
