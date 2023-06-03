
import os
from typing import Callable


clear: Callable[[], int] = (lambda: os.system('cls')) if os.name == 'nt' else (lambda: os.system('clear'))