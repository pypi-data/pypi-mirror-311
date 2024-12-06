import base64
import gzip
import os
import json
import logging

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Prompt
from rich.table import Table
from rich.logging import RichHandler


# handler.setFormatter(colorlog.ColoredFormatter(
#     "%(log_color)s%(asctime)s %(levelname)-8s %(message)s",
#     datefmt='%Y-%m-%d %H:%M:%S',
#     log_colors={
#         'DEBUG': 'cyan',
#         'INFO': 'green',
#         'WARNING': 'yellow',
#         'ERROR': 'red,bg_white',
#         'CRITICAL': 'red,bg_white',
#     },
# ))
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", 
    handlers=[RichHandler(markup=True, show_path=False)]
)

logger = logging.getLogger("lumeo")
logger.setLevel(logging.INFO)

urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.WARNING)
docker_logger = logging.getLogger("docker")
docker_logger.setLevel(logging.WARNING)

console = Console()
progress = None
progress_tasks = {}
    
OUTPUT_FORMAT = 'text'
DEBUG_MODE = False

def set_debug_mode(debug):
    global DEBUG_MODE
    DEBUG_MODE = debug
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
def set_output_format(format):
    global OUTPUT_FORMAT
    OUTPUT_FORMAT = 'json' if format in ['json', True] else 'text'
    
def lumeo_logo():
    encoded_data = "H4sIACZdkGMCA8WUMQ7AIAhFd07hURkcHBicPKAnaUxqqy1qVbTNnxr8L5APSt2fd1pEkBmaZYqgxRgG6Z3dRQySg2KiZjFF7iArTRYOMbD0EvPAVihlf+JmSkz11YSd8W6PkqkYIFRCQl2EEHd+t/hpY8FpIkVaPc+TEfW/QScrJurLVvxwAtRGJEFzeaW7S3gCyky5e5H8gFelnZhYZzMAB0lpiLmGBwAA"
    decoded_data = base64.b64decode(encoded_data)
    decompressed_data = gzip.decompress(decoded_data)
    return decompressed_data.decode('utf-8')
    
def print_header(text, title=None, subtitle=None):
    if os.getenv('NO_PROMPT', False):
        return
    if title:
        console.print(Panel(text, title=title, subtitle=subtitle, style="cyan"))
    else:
        console.print(Panel(text, style="cyan"))
    
def print_text(text):
    console.print(text)

def output_message(message, status='info', title=''):
    global DEBUG_MODE
    if OUTPUT_FORMAT == 'json':
        if status != 'debug' or DEBUG_MODE:
            output = {'status': status, 'message': message}
            print_text(json.dumps(output))
    else:
        if status == 'debug':
            logger.debug(message)
        elif status == 'warning':
            logger.warning(message)
        elif status == 'error':
            logger.error(message)
        else:
            logger.info(message)
        #print_text(title)
        #print_text(message)        

def output_data(headers, rows, title, expand=True):
    if OUTPUT_FORMAT == 'json':
        # Convert headers and rows into a list of dictionaries
        output = {'status': 'success', 'data': []}
        headers_fixed = [header.replace(" ", "_").lower() for header in headers]
        for row in rows:
            output['data'].append(dict(zip(headers_fixed, row)))
        print(json.dumps(output))
    else:
        table = generate_table(headers, rows, title, expand)
        console.print(table)
        
def get_progress(reset=False):
    global progress, progress_tasks
    if reset or not progress:
        progress = Progress()
        progress_tasks = {}
        progress.start()
    return progress

def stop_progress():
    global progress, progress_tasks
    progress.stop()
    progress_tasks = {}

def add_progress_task(task_key, description, total=100):
    progress_tasks[task_key] = (get_progress().add_task(description, total=total), total)
    return progress_tasks[task_key]

def update_progress_task(task_key, advance=1, completed=None):
    if completed and progress_tasks[task_key][1] is None:
        get_progress().update(progress_tasks[task_key][0], total=completed)
    get_progress().update(progress_tasks[task_key][0], advance=advance, completed=completed)
    
        
def generate_table(headers, rows, title, expand=True):
    table = Table(title=title, expand=expand, style="cyan")
    for header in headers:
        table.add_column(header, style="cyan", no_wrap=False)
    for row in rows:
        table.add_row(*row)
    return table

def prompt_yes_no(msg, default_value):
    """Prompt for yes/no input with a default value."""
    while True:
        if os.getenv('NO_PROMPT', False):
            console.print(f"{msg} (using default: {default_value})")
            return default_value.lower() == 'y'

        response = prompt_input(msg, default=default_value.lower(), choices=['y', 'n'])
        if response in ['y', 'n']:
            return response == 'y'
        elif response == '':
            return default_value.lower() == 'y'
        else:
            print("Please enter 'y' for Yes, 'n' for No, or press Enter for the default value.")            

def prompt_input(msg, default=None, choices=None):
    """Prompt for input with a default value."""
    if os.getenv('NO_PROMPT', False):
        console.print(f"{msg} (using default: {default})")
        return default
    try:
        return Prompt.ask(f"[bold]{msg}[/bold]", default=default, choices=choices)
    except KeyboardInterrupt:
        exit(1)
    except EOFError:
        exit(1)