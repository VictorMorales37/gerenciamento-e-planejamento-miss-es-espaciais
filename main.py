from terminal_ui import TerminalUI
from api.solar_system_api import SolarSystemAPI
from structures.tabela_hash import TabelaHash
from dotenv import load_dotenv

import os

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
	raise RuntimeError(
		"API_KEY não foi encontrada."
	)

api = SolarSystemAPI(api_key)
#terminal.main_menu() 

hashtable = TabelaHash()