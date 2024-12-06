from latex_generator import generate_table


def save_to_tex(file_path, data):
    latex_code = generate_table(data)
    with open(file_path, "w") as file:
        file.write(r"\documentclass{article}" + "\n")
        file.write(r"\usepackage{amsmath}" + "\n")
        file.write(r"\usepackage{graphicx}" + "\n")
        file.write(r"\begin{document}" + "\n")
        file.write(latex_code + "\n")
        file.write(r"\end{document}")


if __name__ == "__main__":
    example_data = [
        ["Header1", "Header2", "Header3"],
        ["Row1Col1", "Row1Col2", "Row1Col3"],
        ["Row2Col1", "Row2Col2", "Row2Col3"]
    ]
    save_to_tex("HW_2_1/example_table.tex", example_data)
