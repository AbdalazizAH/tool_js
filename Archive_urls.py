import argparse
import os
from datetime import datetime
from colorama import Style , Fore
from core import base_function_fix
from core import new


# Define color codes for console output
yellow_color_code = "\033[93m"
reset_color_code = "\033[0m"
# log_text = "Archive URLs extraction tool"
log_text = r"""


                             ____    _   _   _    ____    _   _   _    ____  
                            / ___|  | | | | | |  / ___|  | | | | | |  / ___| 
                            \___ \  | | | | | | | |  _   | |_| | | | | |  _  
                             ___) | | |_| | | | | |_| |  |  _  | | | | |_| | 
                            |____/   \___/  |_|  \____|  |_| |_| |_|  \____| 
                            
                            VERSION 1.0.1
"""


def main():
    """
    Main function to parse arguments, extract archived URLs, and display results.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console
    colored_log_text = f"{yellow_color_code}{log_text}{reset_color_code}"
    print(colored_log_text)

    try:
        # Parse command-line arguments
        args = parse_arguments()

        # Process domain and payload options
        if args.domain:
            domain = new.domens(args.domain)

            # Set default start and end dates if not provided
            start_date = args.start_date or new.date_one_year_ago()
            end_date = args.end_date or new.date_time_now()

            # Display search date range
            formatted_string = (
                f"{Style.RESET_ALL}{Fore.GREEN}[+] "
                f"{Style.RESET_ALL}{Fore.BLUE}resrsh date is from "
                f"{Fore.RED}{start_date}{Style.RESET_ALL}{Fore.BLUE} "
                f"to "
                f"{Style.RESET_ALL}{Fore.RED}{end_date}"
            )
            print(formatted_string)

            # Extract archived URLs based on payload type
            if args.list_of_pelod:
                payload_list = new.read_lines_to_list(args.list_of_pelod)
                list_url_vald, counter, vald, running_time, list_url_not_vald = (
                    base_function_fix.base_func_pe(
                        domain, args.number_of_urls, start_date, end_date, payload_list
                    )
                )
            else:
                list_url_vald, counter, vald, running_time, list_url_not_vald = (
                    base_function_fix.base_func_pe(
                        domain, args.number_of_urls, start_date, end_date, args.pyloded
                    )
                )

            # Format and display results
            new.format_string(counter, vald, running_time)

            # Prompt user for further actions
            prints = input(
                f"{Fore.YELLOW}[+]{Style.RESET_ALL} {Fore.RED}====> : {Style.RESET_ALL}"
            )
            if prints in ("y", "yes"):
                print(
                    f"\n{Fore.YELLOW}{"-" * 100}{Style.RESET_ALL}"
                )
                for i, url_ in enumerate(list_url_vald, 1):
                    print(
                        f"{Fore.YELLOW}[{Fore.YELLOW}{i}{Fore.YELLOW}] {Fore.BLUE}| {Fore.GREEN}{url_} {Style.RESET_ALL}"
                    )
                print(
                    f"{Fore.YELLOW}{"-" * 100}{Style.RESET_ALL}"
                )
            elif prints in ("s", "save"):
                new.save_file(domain, list_url_vald)
            elif prints in ("S", "NotValid"):
                new.save_file(domain, list_url_not_vald)

    except KeyboardInterrupt:
        exit()
    except TypeError:
        exit()
    except UnboundLocalError:
        print(
            """usage: main.py [-h] [-u DOMAIN] [-s START_DATE] [-e END_DATE] [-n NUMBER_OF_URLS] [-p PYLODED] [-l LIST_OF_DOMAINS]"""
        )
        exit()


def parse_arguments():
    """
    Parses command-line arguments using argparse.
    """
    parser = argparse.ArgumentParser(description="Archive URLs extraction tool")
    parser.add_argument("-u", "--domain", help="Domain name to extract archived URLs")
    parser.add_argument(
        "-s",
        "--start_date",
        type=lambda s: datetime.strptime(s, "%Y%m%d").date(),
        help="Start date of the range in YYYYMMDD format (default: one year ago)",
    )
    parser.add_argument(
        "-e",
        "--end_date",
        type=lambda s: datetime.strptime(s, "%Y%m%d").date(),
        help="End date of the range in YYYYMMDD format (default: today)",
    )
    parser.add_argument(
        "-n",
        "--number-of-urls",
        type=int,
        default=10,
        help="Number of URLs to check (default: 10)",
    )
    parser.add_argument(
        "-p",
        "--pyloded",
        default="hello<>helo",
        help="Pyloded string to search for (default: 'hello<>helo')",
    )
    parser.add_argument(
        "-lp",
        "--list_of_pelod",
        default="",
        help="File path containing a list of payloads (one per line)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
