# Copyright (c) 2021 Garvit Joshi <garvitjoshi9@gmail.com>


# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
from os import system, path, name
from time import sleep, ctime
import kompiler.constants as C


def clear_screen():
    system('cls' if name == 'nt' else 'clear')


def version():
    print(C.VERSION)


def about():
    print(C.ABOUT)


def help():
    print(C.HELP)


def main():
    argv = sys.argv
    args_len = len(argv)
    if args_len == 1:
        print("Please give a file name to watch")
        help()
        sys.exit()
    elif args_len == 2:
        if argv[1] in ("--version", "-v"):
            version()
            sys.exit()
        elif argv[1] in ("--help", "-h"):
            help()
            sys.exit()
        elif argv[1] in ("--about", "-a"):
            about()
            sys.exit()
        command = "g++ " + argv[1]
    else:
        command = "g++ " + (" ".join(argv[2:]))
    print("Command used for compiling:", command)
    try:
        timer = ctime(path.getmtime(argv[1]))
    except FileNotFoundError:
        print("File:", argv[1], "Not Found")
        sys.exit()
    last_timer = 0
    system(command)
    while True:
        try:
            if last_timer == 0:
                last_timer = timer
                timer = ctime(path.getmtime(argv[1]))
            if timer != last_timer:
                clear_screen()
                system(command)
                print(f"\n\nSuccess!! Last Compiled at: {timer} \n")
            last_timer = timer
            timer = ctime(path.getmtime(argv[1]))
            sleep(0.5)
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    sys.exit(main())
