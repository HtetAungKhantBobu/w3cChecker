import os
import requests
import sys

W3C_CHECKER_API = "https://validator.w3.org/nu/"


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def post_request(file):
    headers = {"Content-type": "text/html"}
    response = requests.post(
        W3C_CHECKER_API,
        data=open(file, "rb").read(),
        headers=headers,
        params={"out": "json"},
    )
    if response.status_code != 200:
        print(
            f"""{Colors.FAIL}An error occured while sending request to w3c api.{Colors.ENDC}"""
        )
        print(
            f"""{Colors.FAIL}Status: {response.status_code}\nContents:\n{response.content}{Colors.ENDC}"""
        )
        sys.exit()

    response_json = response.json()
    return {
        "file": file,
        "response": response_json,
    }


def validate(files):
    for f in files:
        res = post_request(f)
        if len(res["response"]["messages"]) != 0:
            errors = res["response"]["messages"]
            print(
                f"""{Colors.FAIL}File {f} did not pass the check.Found {len(errors)} errors\nHere are the errors:{Colors.ENDC}"""
            )
            for err in errors:
                print(
                    f"""{Colors.FAIL}
        first line : {err["firstLine"]}
        last line : {err["lastLine"]}
        message : {err["message"]}
        {Colors.ENDC}"""
                )
        elif len(res["response"]["messages"]) == 0:
            print(f"""{Colors.OKGREEN}File {f} >> passed.{Colors.ENDC}""")


def get_files(path):
    files = [
        f
        for f in os.scandir(path)
        if os.path.isfile(f) and f.name.split(".")[-1] == "html"
    ]
    return [f.path for f in files]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            f"""{Colors.FAIL}Please provide the path to the folder using the format : python3 __init__.py [PATH/TO/FOLDER].{Colors.ENDC}"""
        )
        sys.exit()

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"""{Colors.FAIL}Invalid file path.{Colors.ENDC}""")
        sys.exit()

    files = get_files(folder_path)

    if len(files) <= 0:
        print(
            f"""{Colors.WARNING}No html file found in the folder: {folder_path}{Colors.ENDC}"""
        )

    validate(files)
