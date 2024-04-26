import time
import requests
from core import new
from fake_useragent import UserAgent
from colorama import Style , Fore


# base function

def base_func_pe(domain, number_of_urls, start_date, end_date, pyloded):
    start_time = time.time()
    desired_part_list = []
    list_url_not_vald = []
    archive = f"https://web.archive.org/cdx/search/cdx?url={domain}//*&output=txt&collapse=urlkey&fl=original&page=/"

    if start_date and end_date:
        archive += f"&from={start_date}&to={end_date}"

    ua = UserAgent()
    random_user_agent = ua.random
    user_agent = random_user_agent
    headers = {"User-Agent": user_agent}
    req = requests.get(archive , headers=headers)

    if req.status_code in [404, 403, 400, 500, 503]:
        print(f"Error web.archive.org {req.status_code}")
        exit()
    counter = 0
    valid_counter = 0
    print(f"{Fore.YELLOW}Number of urls:{Fore.BLUE} | {Fore.GREEN}{new.number_lines(req.text.splitlines())}{Style.RESET_ALL}")

    for line in req.text.splitlines():

        if "=" in line:
            counter += 1

            if counter <= int(number_of_urls):
                parts = line.split("=", 1)
                desired_part = parts[0] + "="

                if desired_part not in desired_part_list:
                    list_url_not_vald.append(desired_part)

                    if pyloded is not None:
                        if type(pyloded) == list:
                            for pylo in pyloded:
                                url = desired_part + pylo
                                success = new.test_response(url, pylo)
                                new.print_preosses_2(success ,url)
                                if success:
                                    valid_counter += 1
                                    parts = line.split("=", 1)
                                    desired_part = parts[0] + "="
                                    desired_part_list.append(desired_part)
                        else:
                            url = desired_part + pyloded
                            success = new.test_response(url, pyloded)
                            new.print_preosses_2(success ,url)
                            if success:
                                valid_counter += 1
                                parts = line.split("=", 1)
                                desired_part = parts[0] + "="
                                desired_part_list.append(desired_part)
                    else:
                        exit()

            else:
                break
    end_time = time.time()
    running_time = end_time - start_time
    return desired_part_list, counter, valid_counter, int(running_time), list_url_not_vald
