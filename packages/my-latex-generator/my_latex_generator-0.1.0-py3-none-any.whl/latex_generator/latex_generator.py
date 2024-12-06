def generate_table(data):
    table = "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{|"
    table += " | ".join(["c"] * len(data[0]))
    table += "|}\n\\hline\n"

    for row in data:
        table += " & ".join(row) + " \\\\\n\\hline\n"

    table += "\\end{tabular}\n\\caption{Your table caption here}\n\\label{tab:your_label}\n\\end{table}"

    return table


if __name__ == "__main__":
    example_data = [
        ["Header1", "Header2", "Header3"],
        ["Row1Col1", "Row1Col2", "Row1Col3"],
        ["Row2Col1", "Row2Col2", "Row2Col3"]
    ]
    print(generate_table(example_data))