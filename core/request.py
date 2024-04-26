import requests
import random
import time
from fake_useragent import UserAgent


def connector(url):
    result = False
    ua = UserAgent()
    random_user_agent = ua.random
    user_agent = random_user_agent
    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        result = response.text
        retry = False
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        retry = False
    except requests.exceptions.Timeout as e:
        retry = True
        time.sleep(2)
    except requests.exceptions.HTTPError as err:
        retry = True
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        retry = True
    except KeyboardInterrupt as k:
        retry = False
        exit()
        raise SystemExit(k)
    finally:
        return result, retry
