def generate_latex_table(data):
    latex_code = (
        "\documentclass{article}\n"
        "\\begin{document}\n"
        "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{" + " | ".join(["c"] * len(data[0])) + "}\n"
        "\\hline\n"
    )

    for row in data:
        latex_code += " & ".join(map(str, row)) + " \\\\\n\\hline\n"
    
    latex_code += "\\end{tabular}\n\\caption{Generated Table}\n\\end{table}"
    latex_code += "\n\\end{document}"
    return latex_code

def generate_latex_image(image_path, caption="Generated Image", label="fig:image"):
    latex_code = (
        "\documentclass{article}\n"
        "\\usepackage{graphicx}\n"
        "\\begin{document}\n"
        "\\begin{figure}[h!]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.8\\textwidth]{{{image_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}\n"
        "\n\\end{document}"
    )
    return latex_code

