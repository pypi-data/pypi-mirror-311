def generate_latex_image(image_path, caption="Image", label="fig:image"):
    """
    Генерирует LaTeX-код для вставки картинки.

    :param image_path: Путь к картинке.
    :param caption: Подпись к картинке.
    :param label: Метка для картинки.
    :return: Строка с валидным кодом LaTeX.
    """
    return (
        "\\begin{figure}[h!]\n"
        "\\centering\n"
        f"\\includegraphics[width=0.8\\textwidth]{{{image_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )
