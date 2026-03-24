from tui_utilities import menu, confirm_exit
from data_base_analysis import view_data_base, analyze_variables, frequencies_distribution_table_variable, compare_frequencies_distribution_tables
from statistical_graphs import generate_statistical_graphs_menu

def main():
    while True:
        selection = menu(
            options = {
                "1": "Comenzar",
                "S": "Salir"
            },
            title = "Análisis de las características laborales de los Ingenieros en Informática"
        )
        main_menu() if selection == "1" else confirm_exit()

def main_menu():
    while True:
        selection = menu(
            options = {
                "1": "Visualizar base de datos",
                "2": "Analizar variables",
                "3": "Visualizar tablas de distribución de frecuencias",
                "4": "Comparar tablas de distribución de frecuencias",
                "5": "Generar gráficos estadísticos",
                "A": "Atrás",
                "S": "Salir"
            },
            title = "Menú principal"
        )
        match selection:
            case "1": view_data_base()
            case "2": analyze_variables()
            case "3": frequencies_distribution_table_variable()
            case "4": compare_frequencies_distribution_tables()
            case "5": generate_statistical_graphs_menu()
            case "A": break
            case "S": confirm_exit()

main()