from browser import *


url = "https://google.com/"


def main():

    brws = browser(url)
    brws.browser_run()
    print("exit!!")

if __name__ == "__main__":
    main()
