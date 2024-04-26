import re
import os
import time
from core import request
from datetime import datetime, timedelta
from colorama import Fore, Style
def print_preosses(value):
    print(f"{Fore.BLUE}{value}")


def print_preosses_2(value :bool ,url : str):
    if value :
        print(f"{Fore.GREEN}ok : {Fore.BLUE}{url} | {Fore.YELLOW}[{Fore.GREEN}200{Fore.YELLOW}] {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error : {Fore.BLUE}{url} | {Fore.YELLOW}[{Fore.RED}404{Fore.YELLOW}] {Style.RESET_ALL}")


def print_preosses_vald(value):
    print(f"{Fore.RED}{value}")


def persint(total_operations, completed_operations):
    completion_percentage = (completed_operations / total_operations) * 100
    formatted_percentage = f"{completion_percentage:.0f}"
    percentage = f" {formatted_percentage.zfill(2)}%"
    return percentage


def get_valid_input(prompt, default):
    while True:
        user_input = input(prompt).strip()
        if user_input.isdigit() and len(user_input) == 4:
            return user_input
        elif not user_input:
            return default
un = []


def test_response(url, pyloded):
    c= 0 
    if url not in un or c == 0:
        c+=1
        content, status = request.connector(url )

        if status == False:
            matches = len(re.findall(str(pyloded), content, re.IGNORECASE))
            if matches != 0:
                return True
            else:
                return False
        else:
            return False


def read_lines_to_list(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found - {filename}")
        return []


def save_file(domain, list_url):
    file_name = f"{domain}.txt"
    with open(file_name, "w") as f:
        for line in list_url:
            if "=" in line:
                parts = line.split("=", 1)
                desired_part = parts[0] + "="
                f.write(desired_part + "\n")
    print(f"{Fore.GREEN}Extracted parts saved to {domain}.txt{Style.RESET_ALL}")

def domens(domen):
    if domen.startswith("https://") or domen.startswith("http://"):
        domen = domen.replace("https://", "") or domen.replace("http://", "")
        print(f"{Style.RESET_ALL}{Fore.BLUE}\nThis your link{Style.RESET_ALL}{Fore.GREEN} |{domen}|\n{Style.RESET_ALL}")
    else:
        domen = domen
        print(f"{Style.RESET_ALL}{Fore.BLUE}\nThis your link{Style.RESET_ALL}{Fore.GREEN} |{domen}|\n{Style.RESET_ALL}")
    return domen


def date_time_now():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d")
    return formatted_datetime
def date_one_year_ago():
    current_datetime = datetime.now()
    one_year_ago = current_datetime - timedelta(days=365)
    formatted_one_year_ago = one_year_ago.strftime("%Y%m%d")
    return formatted_one_year_ago


def format_string(counter, vald, running_time):
    formatted_string = (
        f"\n"
        f"{Fore.YELLOW}[-]{Style.RESET_ALL} {Fore.GREEN}Do you want to print the URLs? (y/yes)\n"
        f"{Fore.YELLOW}[-]{Style.RESET_ALL} {Fore.GREEN}Do you want to save the valid URLs? (s/save)\n"
        f"{Fore.YELLOW}[-]{Style.RESET_ALL} {Fore.GREEN}Do you want to save the invalid URLs? (S/NotValid)\n"
        f"{Fore.YELLOW}[+]{Style.RESET_ALL} {Fore.GREEN}Number of desired URLs: ({counter})\n"
        f"{Fore.YELLOW}[+]{Style.RESET_ALL} {Fore.GREEN}Number of valid URLs: ({vald})\n"
        f"{Fore.YELLOW}[+]{Style.RESET_ALL} {Fore.GREEN}Execution time (in seconds): ({running_time})"
    )
    print (formatted_string)


def number_lines(text):
    c = 0
    for linn in text:
        if "=" in linn :
            c+=1
    return c
