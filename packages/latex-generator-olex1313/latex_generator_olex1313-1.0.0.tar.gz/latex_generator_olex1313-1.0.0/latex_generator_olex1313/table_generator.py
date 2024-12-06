def generate_latex_table(data):
    """
    Генерирует LaTeX-код для таблицы на основе двойного списка.

    :param data: Двойной список с данными для таблицы.
    :return: Строка с валидным кодом LaTeX.
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a non-empty list of lists.")

    num_columns = len(data[0])
    if any(len(row) != num_columns for row in data):
        raise ValueError("All rows must have the same number of columns.")

    table_latex = "\\begin{tabular}{" + "|".join(["c"] * num_columns) + "}\n\\hline\n"
    for row in data:
        table_latex += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
    table_latex += "\\end{tabular}"
    return table_latex
