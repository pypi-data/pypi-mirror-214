def convert_color(string, style):
    colors = {
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m'
    }
    return colors[style] + string
