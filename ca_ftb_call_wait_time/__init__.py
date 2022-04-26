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

    # Cron to call tool
    # */15 8-17 * * 1-5 /path/to/.virtualenvs/ca_ftb_call_wait_time/bin/check-ca-ftb-call-wait-time > /path/to/ca-ftb-call-wait-time.lastrun 2>&1

    selector_base = f"div#{accordian_id} > div.card-deck > div:nth-of-type({card_position}n) > div.card > div.card-footer"
    time_element = soup.select(f"{selector_base} > time > span")
    closed_element = soup.select(f"{selector_base} > span.text-body > span.text-primary")
    unavailable_element = soup.select(f"{selector_base} > p.text-primary > span")
    if time_element:
        time_value = str(time_element[0].contents[0]).strip()
        hours, minutes = [int(x) for x in time_value.split(':')]
        wait = timedelta(hours=hours, minutes=minutes)
        print(f"{now} : {wait}")
        if wait < timedelta(minutes=30):
            url = f"https://maker.ifttt.com/trigger/{config['ifttt_event_name']}/with/key/{config['ifttt_key']}"
            r = requests.post(url, json={'value1': f'CA FTB Wait time is {wait}'})
    elif closed_element and closed_element[0].contents == "Closed:":
        time_value = "closed"
    elif unavailable_element and 'Currently Unavailable' in unavailable_element[0].contents:
        time_value = "unavailable"
    else:
        raise Exception(f"Unable to find the right elements in the page\n{r.text}")

    history[now.isoformat()] = time_value
    with open(history_file, 'w') as f:
        yaml.dump(history, f)


if __name__ == '__main__':
    main()