def generate_latex_image(image_path, caption="Image", label="fig:image"):
    return (
        "\\begin{figure}[h!]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.8\\textwidth]{{{image_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )
