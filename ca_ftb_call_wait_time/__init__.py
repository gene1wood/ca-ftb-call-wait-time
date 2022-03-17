from datetime import datetime, timedelta
import yaml
import requests
from xdg import xdg_data_home, xdg_config_home
from bs4 import BeautifulSoup

def main():
    history_file = xdg_data_home() / 'ca-ftb-call-wait-time.yaml'
    config_file = xdg_config_home() / 'ca-ftb-call-wait-time.yaml'
    if history_file.exists():
        with open(history_file) as f:
            history = yaml.load(f, Loader=yaml.SafeLoader)
    else:
        history = {}

    if config_file.exists():
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
    else:
        raise Exception(f'Config file {config_file} is missing')

    now = datetime.now()
    r = requests.get('https://www.ftb.ca.gov/help/time-frames/')
    soup = BeautifulSoup(r.text, 'html.parser')
    accordian_id = 'A3'  # Business Collections
    card_position = 4  # Phone
    selector = f"div#{accordian_id} > div.card-deck > div:nth-of-type({card_position}n) > div.card > div.card-footer > time > span"
    time_element = soup.select(selector)
    time_value = str(time_element[0].contents[0])
    hours, minutes = [int(x) for x in time_value.split(':')]
    wait = timedelta(hours=hours, minutes=minutes)
    history[now.isoformat()] = time_value
    with open(history_file, 'w') as f:
        yaml.dump(history, f)
    print(f"{now} : {wait}")
    if wait < timedelta(minutes=30):
        url = f"https://maker.ifttt.com/trigger/{config['ifttt_event_name']}/with/key/{config['ifttt_key']}"
        r = requests.post(url, json={'value1': f'CA FTB Wait time is {wait}'})


if __name__ == '__main__':
    main()