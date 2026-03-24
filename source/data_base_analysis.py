from tui_utilities import confirmation_menu, header, decimal_format, table, wait_for_key, menu, confirm_exit
from constants import DATA_BASE_PATH
import pandas
import numpy

def select_variable(title):
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
        title = title
    )
    match selection:
        case "1": return "Edad"
        case "2": return "Experiencia"
        case "3": return "Género"
        case "4": return "País de nacimiento"
        case "5": return "Salario"
        case "6": return "Carga laboral"
        case "7": return "Empresa"
        case "8": return "Lenguaje con mayor experiencia"
        case "9": return "Área"
        case "0": return "Proyectos activos"
        case "A": return None
        case "S": confirm_exit()

def interval_option():
    selection = confirmation_menu("¿Desea agrupar por intervalos?")
    return selection == "1"

def view_data_base():
    header("Base de datos")
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
    columns = [{"header": column, "justify": "center"} for column in dataframe.columns]
    dataframe["Edad"] = dataframe["Edad"].apply(lambda x: f"{decimal_format(x)} años")
    dataframe["Experiencia"] = dataframe["Experiencia"].apply(lambda x: f"{decimal_format(x)} años")
    dataframe["Salario"] = dataframe["Salario"].apply(lambda x: f"${decimal_format(x, 2)} USD")
    dataframe["Carga laboral"] = dataframe["Carga laboral"].apply(lambda x: f"{decimal_format(x)} horas")
    dataframe["Proyectos activos"] = dataframe["Proyectos activos"].apply(lambda x: decimal_format(x, 0))
    rows = dataframe.values.tolist()
    rows = [[str(item) for item in row] for row in rows]
    table(columns, rows, title = "Ingenieros en Informática")
    wait_for_key()

def analyze_variables():
    header("Análisis de variables")
    columns = [
        {"header": "Variable", "justify": "center"},
        {"header": "Tipo", "justify": "center", "color": "#00ff00"}
    ]
    rows = [
        ["Edad", "[#007f00]Cuantitativa[/] [#0000ff](Continua)[/]"],
        ["Experiencia", "[#007f00]Cuantitativa[/] [#0000ff](Continua)[/]"],
        ["Género", "[#ff0000]Cualitativa[/] [#ffff00](Nominal)[/]"],
        ["País de nacimiento", "[#ff0000]Cualitativa[/] [#ffff00](Nominal)[/]"],
        ["Salario", "[#007f00]Cuantitativa[/] [#1e90ff](Continua)[/]"],
        ["Carga laboral", "[#007f00]Cuantitativa[/] [#1e90ff](Continua)[/]"],
        ["Empresa", "[#ff0000]Cualitativa[/] [#ffff00](Nominal)[/]"],
        ["Lenguaje con mayor experiencia", "[#ff0000]Cualitativa[/] [#ffff00](Nominal)[/]"],
        ["Área", "[#ff0000]Cualitativa[/] [#ffff00](Nominal)[/]"],
        ["Proyectos activos", "[#007f00]Cuantitativa[/] [#00bfff](Discreta)[/]"]
    ]
    table(columns, rows, title = "Clasificación de variables")
    wait_for_key()

def frequencies_distribution_table_variable():
    while True:
        variable = select_variable("Variable de la tabla de distribución de frecuencias")
        match variable:
            case "Género" | "País de nacimiento" | "Empresa" | "Lenguaje con mayor experiencia" | "Área":
                use_interval = False
            case "Edad" | "Experiencia" | "Salario" | "Carga laboral" | "Proyectos activos":
                use_interval = interval_option()
            case None: break
        frequencies_distribution_table(variable, use_interval)

def frequencies_distribution_table(variable, use_interval):
    header(f"Tabla de distribución de frecuencias de {variable.lower()}")
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
    column = variable
    if use_interval:
        bins_count = 10
        data = dataframe[variable]
        minimum_value, maximum_value = int(numpy.floor(data.min())), int(numpy.ceil(data.max()))
        bin_edges = numpy.unique(numpy.linspace(minimum_value, maximum_value, bins_count + 1).round().astype(int))
        dataframe[f"{variable}_interval"] = pandas.cut(data, bins = bin_edges, include_lowest = True)
        column = f"{variable}_interval"
    counts = dataframe[column].value_counts().reset_index()
    counts.columns = [column, "absolute_frequency"]
    counts = counts.sort_values(by = column)
    counts["absolute_frequency_accumulated"] = counts["absolute_frequency"].cumsum()
    counts["relative_frequency"] = counts["absolute_frequency"] / len(dataframe)
    counts["relative_frequency_accumulated"] = counts["relative_frequency"].cumsum()
    columns = [
        {"header": variable, "justify": "center"},
        {"header": "Frecuencia absoluta", "justify": "center"},
        {"header": "Frecuencia absoluta acumulada", "justify": "center"},
        {"header": "Frecuencia relativa", "justify": "center"},
        {"header": "Frecuencia relativa acumulada", "justify": "center"}
    ]
    rows = []
    for i, (_, row) in enumerate(counts.iterrows()):
        value = row[column]
        if use_interval and column.endswith("_interval"):
            bottom_edge, top_edge = int(value.left), int(value.right)
            formatted_bottom_edge = decimal_format(bottom_edge)
            formatted_top_edge = decimal_format(top_edge)
            if variable == "Salario":
                formatted_bottom_edge = f"${formatted_bottom_edge}"
                formatted_top_edge = f"${formatted_top_edge}"
            label = f"[{formatted_bottom_edge}; {formatted_top_edge}]" if i == 0 else f"({formatted_bottom_edge}; {formatted_top_edge}]"
            match variable:
                case "Edad" | "Experiencia": label += " años"
                case "Salario": label += " USD"
                case "Carga laboral": label += " horas"
            value = label
        else:
            match variable:
                case "Edad" | "Experiencia":
                    value = f"{decimal_format(value)} años" if value != 1 else f"{decimal_format(value)} año"
                case "Salario": value = f"${decimal_format(value, 2)} USD"
                case "Carga laboral":
                    value = f"{decimal_format(value)} horas" if value != 1 else f"{decimal_format(value)} hora"
                case "Proyectos activos": value = decimal_format(value, 0)
        absolute_frequency = decimal_format(row["absolute_frequency"])
        accumulated_absolute_frequency = decimal_format(row["absolute_frequency_accumulated"])
        relative_frequency = decimal_format(row["relative_frequency"], 2)
        accumulated_relative_frequency = decimal_format(row["relative_frequency_accumulated"], 2)
        rows.append([
            str(value), 
            absolute_frequency, 
            accumulated_absolute_frequency, 
            relative_frequency, 
            accumulated_relative_frequency
        ])
    total_absolute_frequency = decimal_format(counts["absolute_frequency"].sum())
    total_relative_frequency = decimal_format(counts["relative_frequency"].sum(), 2)
    rows.append([
        "Total", 
        total_absolute_frequency, 
        total_absolute_frequency, 
        total_relative_frequency, 
        total_relative_frequency
    ])
    table(columns, rows, title = f"{variable} de los Ingenieros en Informática")
    wait_for_key()

def compare_frequencies_distribution_tables():
    while True:
        header("Selección de variables a comparar")
        variable_1 = select_variable("Primera variable de la tabla de distribución de frecuencias")
        match variable_1:
            case "Género" | "País de nacimiento" | "Empresa" | "Lenguaje con mayor experiencia" | "Área":
                use_interval_1 = False
            case "Edad" | "Experiencia" | "Salario" | "Carga laboral" | "Proyectos activos":
                use_interval_1 = interval_option()
            case None: break
        variable_2 = select_variable("Segunda variable de la tabla de distribución de frecuencias")
        match variable_2:
            case "Género" | "País de nacimiento" | "Empresa" | "Lenguaje con mayor experiencia" | "Área":
                use_interval_2 = False
            case "Edad" | "Experiencia" | "Salario" | "Carga laboral" | "Proyectos activos":
                use_interval_2 = interval_option()
            case None: continue
        compare_variables(variable_1, variable_2, use_interval_1, use_interval_2)

def compare_variables(variable_1, variable_2, use_interval_1, use_interval_2):
    header(f"Comparación de {variable_1.lower()} contra {variable_2.lower()}")
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

    def process_variable(dataframe, variable, use_interval):
        if use_interval:
            bins_count = 10
            data = dataframe[variable]
            minimum_value, maximum_value = int(numpy.floor(data.min())), int(numpy.ceil(data.max()))
            bin_edges = numpy.unique(numpy.linspace(minimum_value, maximum_value, bins_count + 1).round().astype(int))
            dataframe[f"{variable}_interval"] = pandas.cut(data, bins = bin_edges, include_lowest = True)
            return f"{variable}_interval"
        return variable
    
    column_1 = process_variable(dataframe, variable_1, use_interval_1)
    column_2 = process_variable(dataframe, variable_2, use_interval_2)
    column_1_unique_values = sorted(dataframe[column_1].unique())
    is_variable_2_numeric = variable_2 in ["Edad", "Experiencia", "Salario", "Carga laboral", "Proyectos activos"]
    results = []
    for value in column_1_unique_values:
        subset = dataframe[dataframe[column_1] == value]
        count = len(subset)
        variable_2_counts = subset[column_2].value_counts()
        if not variable_2_counts.empty:
            max_frequency = variable_2_counts.max()
            mode_values = variable_2_counts[variable_2_counts == max_frequency].index.tolist()
            percentage = (max_frequency / count) * 100
        else: mode_values, max_frequency, percentage = [], 0, 0
        if column_1.endswith("_interval"):
            bottom_edge, top_edge = int(value.left), int(value.right)
            formatted_bottom_edge = decimal_format(bottom_edge)
            formatted_top_edge = decimal_format(top_edge)
            if variable_1 == "Salario":
                formatted_bottom_edge = f"${formatted_bottom_edge}"
                formatted_top_edge = f"${formatted_top_edge}"
            is_first = (value == column_1_unique_values[0])
            formatted_value = f"[{formatted_bottom_edge}; {formatted_top_edge}]" if is_first else f"({formatted_bottom_edge}; {formatted_top_edge}]"
            match variable_1:
                case "Edad" | "Experiencia": formatted_value += " años"
                case "Salario": formatted_value += " USD"
                case "Carga laboral": formatted_value += " horas"
        else:
            match variable_1:
                case "Edad" | "Experiencia":
                    formatted_value = f"{decimal_format(value)} años" if value != 1 else f"{decimal_format(value)} año"
                case "Salario": formatted_value = f"${decimal_format(value, 2)} USD"
                case "Carga laboral":
                    formatted_value = f"{decimal_format(value)} horas" if value != 1 else f"{decimal_format(value)} hora"
                case "Proyectos activos": formatted_value = decimal_format(value, 0)
                case _: formatted_value = str(value)
        formatted_modes = []
        for mode in mode_values:
            if column_2.endswith("_interval"):
                bottom_edge, top_edge = int(mode.left), int(mode.right)
                formatted_bottom_edge = decimal_format(bottom_edge)
                formatted_top_edge = decimal_format(top_edge)
                if variable_2 == "Salario":
                    formatted_bottom_edge = f"${formatted_bottom_edge}"
                    formatted_top_edge = f"${formatted_top_edge}"
                formatted_mode = f"[{formatted_bottom_edge}; {formatted_top_edge}]"
                match variable_2:
                    case "Edad" | "Experiencia": formatted_mode += " años"
                    case "Salario": formatted_mode += " USD"
                    case "Carga laboral": formatted_mode += " horas"
            else:
                match variable_2:
                    case "Edad" | "Experiencia":
                        formatted_mode = f"{decimal_format(mode)} años" if mode != 1 else f"{decimal_format(mode)} año"
                    case "Salario": formatted_mode = f"${decimal_format(mode, 2)} USD"
                    case "Carga laboral":
                        formatted_mode = f"{decimal_format(mode)} horas" if mode != 1 else f"{decimal_format(mode)} hora"
                    case "Proyectos activos": formatted_mode = decimal_format(mode, 0)
                    case _: formatted_mode = str(mode)
            formatted_modes.append(formatted_mode)
        modes = " / ".join(formatted_modes) if formatted_modes else "N/A"
        if max_frequency > 0:
            modes += f" ({decimal_format(max_frequency)} - {decimal_format(percentage, 2)}%)"
        row = [formatted_value, str(count), modes]
        if is_variable_2_numeric:
            mean = subset[variable_2].mean()
            formatted_mean = decimal_format(mean, 2)
            match variable_2:
                case "Edad" | "Experiencia": formatted_mean += " años"
                case "Salario": formatted_mean = f"${formatted_mean} USD"
                case "Carga laboral": formatted_mean += " horas"
            row.append(formatted_mean)
        results.append(row)
    columns = [
        {"header": variable_1, "justify": "center"},
        {"header": "Cantidad", "justify": "center"},
        {"header": f"Moda de {variable_2.lower()}", "justify": "center"}
    ]
    if is_variable_2_numeric:
        columns.append({"header": f"Promedio de {variable_2.lower()}", "justify": "center"})
    table(columns, results, title = f"Relación entre {variable_1.lower()} y {variable_2.lower()}")
    wait_for_key()