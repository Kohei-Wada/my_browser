from urllib.request import urlopen, urlretrieve
from urllib.parse   import urljoin
from bs4            import BeautifulSoup
from commands       import *

import getopt
import os
import sys




class browser:
    ###########################################################################
    def __init__(self, url):

        self.start_url       = url
        self.current         = url
        self.urls_history    = []
        self.next_urls       = []
        self.browser_active  = True
        self.commands        = commands


        self.urls_history.append(url)

        self._err = lambda msg: sys.stderr.write("<browser_err> " + msg + "\n")
        self._log = lambda msg: None#sys.stderr.write("<browser_log> " + msg + "\n")


        self._log(f"first url is {self.start_url}")
        self.next_urls = self.get_all_urls(url)


    ###########################################################################
    def browser_run(self):

        #self._log("inside browser_run()")


        #This loop is main loop
        while (self.browser_active):
            print(f"\033[34mmy_browser\033[0m:\033[32m{self.current}\033[0m$", end="")
            self.do_command()



    ###########################################################################
    def browser_cat(self, args):
        #self._log("inside browser_cat()")
        url = self.current


        html = self.open_url(url, True)
        bs = BeautifulSoup(html, "html.parser")

        for script in bs(["script", "style"]):
            script.decompose()

        text = bs.get_text()
        lines = [line.strip() for line in text.splitlines()]

        text = "\n".join(line for line in lines if line)

        print("")
        print(text)
        print("")


    ###########################################################################
    def browser_quit(self, args):
        #self._log("inside browser_quit()")
        self.browser_active = False


    ##########################################################################
    def to_abs_url(self, url):

        return urljoin(self.current, url)


    ###########################################################################
    def browser_cd(self, _args):
        self._log("inside browser_cd()")

        url = ""

        try:
            opts, args = getopt.getopt(_args,
                            "n:h:u:",
                            ["number=", "history=", "url="])
        except getopt.GetoptError as e:
            self._err(str(e))
            return


        for o, a in opts:
            if o in ("-u", "--url"):
                url = a

            elif o in ("-n", "--number"):
                #fixme
                index = int(a)
                url = self.next_urls[index]
                url = self.to_abs_url(url)
                break;

            elif o in ("-h", "--history"):
                index = int(a)
                if int(a) <= len(self.urls_history):
                    url = self.urls_history[int(a)]
                    break;
                else:
                    self._err("out of range")
                    return

            else:
                self._err("invalid flag")
                return


        if not url:
            if _args:
                url = _args[0]
            else:
                url = self.start_url


        if not self.open_url(url):
            self._err("could not find such url")
            return

        self.current = url
        self.next_urls = self.get_all_urls(url)

        if not url in self.urls_history:
            self.urls_history.append(url)


        self._log(f"current is changed to {url}")


    ###########################################################################
    def browser_clear(self, args):
        self._log("inside browser_clear()")

        os.system("clear")


    ###########################################################################
    def browser_ls(self, args):
        self._log("inside browser_ls()")

        links = []
        index = 0
        extention = ""
        url   = self.current
        links = self.next_urls


        if args:
            try:
                opts, args = getopt.getopt(args,
                                "he:",
                                ["history", "extention="])
            except getopt.GetoptError as e:
                self._err(str(e))
                return

            for o, a in opts:
                if o in ("-h", "--history"):
                    links = self.urls_history
                elif o in ("-e", "--extention"):
                    extention = a
                else:
                    self._err("invalid flag")
                    return


        if extention:
            for url in links:
                if (url.endswith(extention)):
                    print(f"{index} : {url}")
                index += 1

        else:
            for url in links:
                print(f"{index} : {url}")
                index += 1



    ###########################################################################
    def open_url(self, url, return_html=False):
        self._log("inside open_url()")

        self._log(f"\turl = {url}")
        try:
            html = urlopen(url)
        except:
            return False

        if return_html:
            return html

        return True


    ###########################################################################
    def browser_help(self, args):
        self._log("inside browser_help()")

        alias = False


        if args:
            try:
                opts, args = getopt.getopt(args,
                                "a",
                                ["alias"])
            except getopt.GetoptError as e:
                pass

            for o, a in opts:
                if o in ("-a", "--alias"):
                    alias = True

                else:
                    self._err("invalid flag")
                    return


        if not alias:
            print("")
            print("<my_browser Usage>")
            print("")
            print("[Commands]")
            print("   cd     : change current url. if no operand current change to start_url")
            print("   cat    : display current html.")
            print("   ls     : show all urls in current.")
            print("   quit   : quit this program.")
            print("   status : show current and urls_history.")
            print("   help   : show this help.")
            print("   clear  : clear screen.")
            print("   get    : get file.")

            print("")

            print("[Flags]")
            print("   cd [-h | -n] [number]")
            print("     -h  : change current  by urls_history number")
            print("     -n  : change current by next_urls number")
            print("")
            print("   ls [-h | -e:] [extention]")
            print("     -h : show urls_history")
            print("     -e : show all url ends with specified extention")
            print("")
            print("   help [-a]")
            print("     -a : show alias")
            print("")
            print("   get [-n | -e | -a] [extenion]")
            print("      -n : specified by file number. if this flage specified flag -a is ignored")
            print("      -a : get all file ends with specified extenion")
            print("      -e : extenion")

            print("")

            print("[Exmaples]")
            print("    cd -n 0")
            print("    cd -h 20")
            print("    ls -h ")
            print("    get -n 34 -e pdf")
            print("    get -a -e pdf")
            print("")


        elif alias:
            print("")
            print("<my_browser alias>")
            print("")
            print("    quit  :  q, exit ")
            print("    help  :  h")
            print("    ls    :  l")
            print("    cat   :  show")
            print("")


    ###########################################################################
    def browser_status(self, args):
        self._log("inside browser_status()")

        print("")

        print(f"current : {self.current}")
        print("history : ")
        index = 0
        for url in self.urls_history:
            print(f"  {index} : {url}")
            index += 1

        print("")


    ###########################################################################
    def browser_get(self, args):
        self._log("inside browser get")


        extention = ""
        all       = False
        number    = None
        urls      = self.next_urls
        path      = os.getcwd()


        if not args:
            self._err("There are syntax errors in command")
            return
        try:
            opts, args = getopt.getopt(args,
                            "e:an:p:",
                            ["extention=", "all", "number=", "path="])
        except getopt.GetoptError as e:
            self._err(str(e))
            return


        for o, a in opts:
            if o in ("-e", "--extention"):
                extention = a

            elif o in ("-a", "--all"):
                all = True

            elif o in ("-n", "--number"):
                number = int(a)

            elif o in ("-p", "--path"):
                path = a

            else:
                self._err("invalid flag detcted")
                return


        if number is not None:
            file = self.to_abs_url(urls[number])
            file_name = os.path.basename(file)
            path = os.path.join(path, file_name)
            self.save_file(file, path)
            return


        if not extention:
            self._err("There is not extenion")
            return

        if not all:
            self._err("There are syntax errors in command")
            return


        for url in urls:
            if url.endswith(extention):
                file = self.to_abs_url(url)
                file_name = os.path.basename(file)
                file_path = os.path.join(path, file_name)

                self.save_file(file, file_path)



    ###########################################################################
    def save_file(self, url, path):
        self._log("inside save_file()")

        try:
            urlretrieve(url, path)
        except:
            self._err("failed to save file")
            self._err(f"url = {url}, path = {path}")



    ###########################################################################
    def do_command(self):

        command = list(map(str, input().split()))

        if command:
            if command[0] in self.commands:
                eval("self.browser_" + commands[command[0]] + "(command[1:])")

            else:
                self._err("invalid command")
                return
        else:
            return


    ###########################################################################
    def get_all_urls(self, url):
        #get all links in current url
        self._log("inside get_all_urls()")

        next_all_links = []
        html = urlopen(url)
        bs = BeautifulSoup(html, "html.parser")

        for link in bs.find_all("a"):
            if "href" in link.attrs:
                next_all_links.append(link.attrs["href"])

        return next_all_links
