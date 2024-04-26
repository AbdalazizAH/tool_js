import os
import re
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
from colorama import Fore, Style


class JSFileExtractor:
    def __init__(
        self,
        base_url,
        download_dir="./output/js",
        output_file="./output/output_table.txt",
    ):
        self.base_url = base_url
        self.download_dir = download_dir
        self.output_file = output_file
        self.words = [
            "Apikey",
            "Api_key",
            "Access_token",
            "API/",
            "bearer",
            "admin",
            "administror",
            "config",
        ]

        self.num_files_found = 0
        self.num_files_downloaded = 0
        self.js_files = set()

        # Create the download directory if it doesn't exist
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)

    def extract_js_files(self):
        try:
            response = requests.get(self.base_url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            for script in soup.find_all("script", src=True):
                js_url = urljoin(self.base_url, script["src"])
                if js_url.endswith(".js"):
                    self.js_files.add(js_url)
                    print(
                        f"{Fore.CYAN}Found{Fore.RESET} {Fore.YELLOW} {js_url} {Fore.RESET}"
                    )
            self.num_files_found = len(self.js_files)
            logging.info(
                f"\n{Fore.GREEN}SUCCESS:{Fore.RESET} Found {self.num_files_found} JavaScript files\n"
            )
            return self.js_files
        except requests.exceptions.ReadTimeout as e:
            logging.error(
                f"\n{Fore.RED}ERROR:{Fore.RESET} Website connection timed out\n"
            )
            return set()
        except requests.exceptions.RequestException as e:
            logging.error(f"\n{Fore.RED}ERROR:{Fore.RESET} Error fetching website\n")
            return set()

    def download_js_files(self):
        try:
            for js_file in self.js_files:
                response = requests.get(js_file)
                response.raise_for_status()
                filename = js_file.split("/")[-1]
                filepath = os.path.join(self.download_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                self.num_files_downloaded += 1
                print(
                    f"{Fore.CYAN}Downloaded{Fore.RESET} {Fore.GREEN}{js_file}{Fore.RESET} to {filepath}"
                )
        except requests.exceptions.RequestException as e:
            logging.error(
                f"{Fore.RED}An error occurred while downloading {js_file}: {str(e)}{Fore.RESET}"
            )

    def search_words_in_js(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            matches = {
                word: len(re.findall(word, content, re.IGNORECASE))
                for word in self.words
            }
            return matches

    def search_in_js_files(self):
        with open(self.output_file, "w") as out_file:
            for dirpath, dirnames, filenames in os.walk(self.download_dir):
                js_files = [
                    filename for filename in filenames if filename.endswith(".js")
                ]
                for file in js_files:
                    file_path = os.path.join(dirpath, file)
                    matches = self.search_words_in_js(file_path)
                    if any(matches.values()):
                        if any(count > 0 for count in matches.values()):
                            out_file.write(
                                f"{Fore.GREEN}File:{Fore.RESET} {file_path}\n"
                            )
                            out_file.write("+---------------------+-------+\n")
                            out_file.write("| Word                | Count |\n")
                            out_file.write("+---------------------+-------+\n")
                            for word, count in matches.items():
                                if count > 0:
                                    out_file.write(
                                        f"| {word.ljust(20)} | {str(count).center(5)} |\n"
                                    )
                            out_file.write("+---------------------+-------+\n")
                            out_file.write("\n")
        print(
            f"\n{Fore.GREEN}Search completed.{Fore.RESET} Results saved in {self.output_file}"
        )

    def filter_results(self):
        output_file_filtered = r"./output/output_filtered.txt"
        with open(self.output_file, "r") as infile, open(
            output_file_filtered, "w"
        ) as outfile:
            for line in infile:
                if not line.strip().endswith("0"):
                    outfile.write(line)
        print(
            f"{Fore.GREEN}Results filtered.{Fore.RESET} Filtered results saved in {output_file_filtered}"
        )


import colorama

colorama.init()
text_logo = rf"""{Fore.YELLOW}
                         ___   _   _    ____   ___ 
                        |_ _| | | | |  / ___| |__ \
                         | |  | |_| | | |  _     ) |
                         | |  |  _  | | |_| |   / / 
                        |___| |_| |_|  \____|  /_/

                        {Fore.YELLOW}JSFileExtractor{Fore.WHITE} v.1.0
                        
                        {Fore.GREEN}@github.com
                        {Fore.RESET}
                            """

text_good_bye = f"""{Fore.YELLOW}

║ {Fore.WHITE}nise to se you again!{Fore.YELLOW} ║

{Fore.RESET}
"""


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")  # ?test
    print(text_logo)
    print(f"\n{Fore.BLUE}Extracting JavaScript files from website...")
    try:
        parser = argparse.ArgumentParser(description="JS File Extractor")
        parser.add_argument("-u", "--url", required=True, help="Target website URL")
        args = parser.parse_args()

        extractor = JSFileExtractor(args.url)
        extractor.extract_js_files()
        print(
            f"\n{Fore.BLUE}Number of JavaScript files found:{Fore.RESET} {extractor.num_files_found}"
        )
        confirmation = input(
            f"\n{Fore.YELLOW}Do you want to download {extractor.num_files_found} JavaScript files? {Fore.RED}(y/n): {Fore.RESET}"
        )
        if confirmation.lower() == "y":
            extractor.download_js_files()
            if extractor.num_files_found > 0:
                extractor.search_in_js_files()
                extractor.filter_results()
        else:
            exit()
    except KeyboardInterrupt:
        if extractor.num_files_found > 0:
            extractor.search_in_js_files()
            extractor.filter_results()
        print(f"\n \n{text_good_bye}")
