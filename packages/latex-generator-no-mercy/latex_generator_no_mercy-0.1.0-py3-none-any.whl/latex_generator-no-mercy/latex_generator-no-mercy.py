def generate_latex_table(data):
    return (
        "\\begin{tabular}{" + 'c' * len(data[0]) + "}\n" +
        "\n".join(map(lambda row: ' & '.join(map(str, row)) + ' \\\\', data)) +
        "\n\\end{tabular}"
    )

def generate_latex_image(image_path, width="0.8\\textwidth"):
    return (
        f"""
        \\begin{{figure}}[h!]
            \\centering
            \\includegraphics[width={width}]{{{image_path}}}
            \\caption{{Example image}}
        \\end{{figure}}
        """
    )
