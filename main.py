from terminal_ui import TerminalUI
from api.solar_system_api import SolarSystemAPI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
	raise RuntimeError(
		"API_KEY não foi encontrada."
	)

api = SolarSystemAPI(api_key)
#terminal.main_menu() 
print(api.get_bodies())