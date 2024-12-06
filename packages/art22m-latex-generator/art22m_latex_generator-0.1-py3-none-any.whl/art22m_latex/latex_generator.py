def generate_table(data):
    columns_count = len(data[0]) if data else 0

    column_format = '|' + 'c|' * columns_count

    table_latex = "\\begin{tabular}{" + column_format + "}\n\\hline\n"
    for row in data:
        table_latex += " & ".join(str(cell) for cell in row) + " \\\\\n\\hline\n"
    table_latex += "\\end{tabular}"
    return table_latex


def generate_image(path, caption, label):
    return (
        "\\begin{figure}[h!]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.8\\textwidth]{{{path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )
