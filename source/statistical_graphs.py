from tui_utilities import menu, confirm_exit, decimal_format, clear_console, wait_for_key
from constants import DATA_BASE_PATH
import os
import pandas
import matplotlib.pyplot as pyplot
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
import numpy

def generate_statistical_graphs_menu():
    while True:
        selection = menu(
            options = {
                "1": "Edad",
                "2": "Experiencia",
                "3": "Género",
                "4": "País de nacimiento",
                "5": "Salario",
                "6": "Carga laboral",
                "7": "Empresa",
                "8": "Lenguaje con mayor experiencia",
                "9": "Área",
                "0": "Proyectos activos",
                "A": "Atrás",
                "S": "Salir"
            },
            title = "Variable del gráfico estadístico"
        )
        match selection:
            case "1": show_statistical_graph("Edad", "Histogram")
            case "2": show_statistical_graph("Experiencia", "Frequency polygon")
            case "3": show_statistical_graph("Género", "Pie chart")
            case "4": show_statistical_graph("País de nacimiento", "Bar chart")
            case "5": show_statistical_graph("Salario", "Histogram")
            case "6": show_statistical_graph("Carga laboral", "Histogram")
            case "7": show_statistical_graph("Empresa", "Bar chart")
            case "8": show_statistical_graph("Lenguaje con mayor experiencia", "Bar chart")
            case "9": show_statistical_graph("Área", "Pie chart")
            case "0": show_statistical_graph("Proyectos activos", "Bar chart")
            case "A": break
            case "S": confirm_exit()

def show_statistical_graph(variable, graph_type):
    clear_console()
    dataframe = pandas.read_csv(DATA_BASE_PATH)
    dataframe = dataframe.rename(columns = {
        "Genero": "Género",
        "Nacionalidad": "País de nacimiento",
        "Salario_USD": "Salario",
        "Horas_Semanales": "Carga laboral",
        "Lenguaje": "Lenguaje con mayor experiencia",
        "Area": "Área",
        "Proyectos_Activos": "Proyectos activos"
    })
    data = dataframe[variable]
    pyplot.style.use("dark_background")
    figure, axes = pyplot.subplots(figsize = (16, 9))
    axes.margins(x = 0, y = 0)
    axes.tick_params(axis = "both", which = "both", length = 0, pad = 10)
    axes.grid(True, axis = "y", linestyle = "--", alpha = 0.5)

    def format_axis(number, pos = None): return decimal_format(number)

    formatter = FuncFormatter(format_axis)
    axes.yaxis.set_major_formatter(formatter)
    match graph_type:
        case "Pie chart":
            counts = data.value_counts()
            base_color = "#00bfff"
            h, s, v = colors.rgb_to_hsv(colors.to_rgb(base_color))
            color_list = [colors.to_hex(colors.hsv_to_rgb((h, 1.0 - (i / len(counts)) * 0.25, 0.25 + (i / len(counts)) * 0.5))) for i in range(len(counts))]
            axes.pie(counts, labels = counts.index, autopct = lambda percentage: f"{decimal_format(percentage, 2)}%", colors = color_list)
            axes.set_title(f"Distribución de {variable.lower()} de los Ingenieros en Informática", fontweight = "bold", fontsize = 16, pad = 25)
        case "Bar chart":
            counts = data.value_counts().sort_index()
            x_labels = [decimal_format(label) if isinstance(label, (int, float)) else str(label) for label in counts.index]
            axes.bar(x_labels, counts.values, color = "#00bfff", alpha = 0.75)
            axes.set_title(f"Distribución de {variable.lower()} de los Ingenieros en Informática", fontweight = "bold", fontsize = 16, pad = 25)
            axes.set_xlabel(variable, fontweight = "bold", fontsize = 14, labelpad = 15)
            axes.set_ylabel("Frecuencia absoluta", fontweight = "bold", fontsize = 14, labelpad = 15)
        case "Histogram":
            bins_count = 10
            minimum_value, maximum_value = int(numpy.floor(data.min())), int(numpy.ceil(data.max()))
            bin_edges = numpy.linspace(minimum_value, maximum_value, bins_count + 1).round().astype(int)
            counts, bins_edges = pandas.cut(data, bins = bin_edges, include_lowest = True, retbins = True)
            interval_counts = counts.value_counts().sort_index()
            
            def format_label(bottom_edge, top_edge, index):
                formatted_bottom_edge = decimal_format(int(bottom_edge))
                formatted_top_edge = decimal_format(int(top_edge))
                if variable == "Salario":
                    formatted_bottom_edge = f"${formatted_bottom_edge}"
                    formatted_top_edge = f"${formatted_top_edge}"
                label = f"[{formatted_bottom_edge}; {formatted_top_edge}]" if index == 0 else f"({formatted_bottom_edge}; {formatted_top_edge}]"
                match variable:
                    case "Edad": label += " años"
                    case "Salario": label += " USD"
                    case "Carga laboral": label += " horas"
                return label
            
            labels = [format_label(bins_edges[i], bins_edges[i + 1], i) for i in range(len(bins_edges) - 1)]
            axes.bar(
                labels, 
                interval_counts.values, 
                color = "#00bfff", 
                edgecolor = "#ffffff", 
                alpha = 0.75, 
                width = 1.0
            )
            axes.set_title(
                f"Distribución de {variable.lower()} de los Ingenieros en Informática", 
                fontweight = "bold", 
                fontsize = 16, 
                pad = 25
            )
            axes.set_xlabel(variable, fontweight = "bold", fontsize = 14, labelpad = 15)
            axes.set_ylabel("Frecuencia", fontweight = "bold", fontsize = 14, labelpad = 15)
            if variable == "Salario": pyplot.xticks(rotation = 45)
        case "Frequency polygon":
            bins_count = 10
            minimum_value, maximum_value = int(numpy.floor(data.min())), int(numpy.ceil(data.max()))
            bin_edges = numpy.linspace(minimum_value, maximum_value, bins_count + 1).round().astype(int)
            counts, bins_edges = pandas.cut(data, bins = bin_edges, include_lowest = True, retbins = True)
            interval_counts = counts.value_counts().sort_index()
            mid_points = [(bins_edges[i] + bins_edges[i + 1]) / 2 for i in range(len(bins_edges) - 1)]
            
            def format_midpoint(value):
                formatted_value = decimal_format(int(value))
                suffix = ""
                if variable == "Experiencia": suffix = " años" if value != 1 else " año"
                formatted_mid_point = f"{formatted_value}{suffix}"
                return formatted_mid_point
            
            labels = [format_midpoint(mid_point) for mid_point in mid_points]
            axes.plot(labels, interval_counts.values, marker = "o", color = "#00bfff", linewidth = 2)
            axes.fill_between(labels, interval_counts.values, alpha = 0.25, color = "#00bfff")
            axes.set_title(
                f"Distribución de {variable.lower()} de los Ingenieros en Informática", 
                fontweight = "bold", 
                fontsize = 16, 
                pad = 25
            )
            axes.set_xlabel(variable, fontweight = "bold", fontsize = 14, labelpad = 15)
            axes.set_ylabel("Frecuencia", fontweight = "bold", fontsize = 14, labelpad = 15)
    pyplot.tight_layout(pad = 2.5)
    pyplot.show()
    wait_for_key()