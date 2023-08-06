
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m" # added magenta color
    CYAN = "\033[96m" # added cyan color
    WHITE = "\033[97m" # added white color
    END = "\033[00m"

def pause(_, v):
    input(">> ")

def lt(_, args):
    if not args: return False

    last = args[0]

    for v in args:
        if last >= v:
            return False

    return True

def red(_, s):
    return Colors.RED + s + Colors.END

def green(_, s):
    return Colors.GREEN + s + Colors.END

def yellow(_, s):
    return Colors.YELLOW + s + Colors.END

def blue(_, s):
    return Colors.BLUE + s + Colors.END

def magenta(_, s):
    return Colors.MAGENTA + s + Colors.END

def cyan(_, s):
    return Colors.CYAN + s + Colors.END

def white(_, s):
    return Colors.WHITE + s + Colors.END

def print_red(_, s):
    print(Colors.RED + s + Colors.END)

def print_green(_, s):
    print(Colors.GREEN + s + Colors.END)

def print_yellow(_, s):
    print(Colors.YELLOW + s + Colors.END)

def print_blue(_, s):
    print(Colors.BLUE + s + Colors.END)

def print_magenta(_, s):
    print(Colors.MAGENTA + s + Colors.END)

def print_cyan(_, s):
    print(Colors.CYAN + s + Colors.END)

def print_white(_, s):
    print(Colors.WHITE + s + Colors.END)
