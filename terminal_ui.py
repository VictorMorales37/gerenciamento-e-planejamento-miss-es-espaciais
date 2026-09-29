from enum import Enum

class TerminalUI:

    def __init__(self):
        self.input = 0

    def main_menu(self):
        self.input = 0
        while (self.input != 4):
            print("SOLARHELPER - PLANEJE E GERENCIE SUAS MISSÕES NO SISTEMA SOL")
            print("###############################################")
            print("1 - Missões")
            print("2 - Veículos")
            print("3 - Sistema Solar")
            print("4 - Sair")
            self.input = input("INPUT: ")
            match self.input:
                case "1":
                    self.mission_menu()
                case "2":
                    self.ship_menu()
                case "3":
                    self.system_menu()
                case "4":
                    return

    def mission_menu(self):
        self.input = 0
        while self.input != 3: 
            print("SOLARHELPER - PLANEJE E GERENCIE SUAS MISSÕES NO SISTEMA SOL")
            print("###############################################")
            print("1 - Missões Ativas")
            print("2 - Planejar Missão")
            print("3 - Voltar <-")
            self.input = input("INPUT: ")
            match self.input:
                case "1":
                    print("WIP")
                case "2":
                    print("WIP")
                case "3":
                    return

    def ship_menu(self):
        self.input = 0
        while self.input != 3: 
            print("SOLARHELPER - PLANEJE E GERENCIE SUAS MISSÕES NO SISTEMA SOL")
            print("###############################################")
            print("1 - Meus veículos")
            print("2 - Adicionar veículo")
            print("3 - Voltar <-")
            self.input = input("INPUT: ")
            match self.input:
                case "1":
                    print("WIP")
                case "2":
                    print("WIP")
                case "3":
                    return
            
    def system_menu(self):
        self.input = 0
        while self.input != 2: 
            print("SOLARHELPER - PLANEJE E GERENCIE SUAS MISSÕES NO SISTEMA SOL")
            print("###############################################")
            print("1 - Pesquisar planeta")
            print("2 - Voltar <-")
            self.input = input("INPUT: ")
            match self.input:
                case "1":
                    print("WIP")
                case "2":
                    print("WIP")
                case "3":
                    return
