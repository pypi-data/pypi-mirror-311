def _table_template(table_data, cols_size):
    return f"""
    \\begin{{table}}[ht]
        \\centering
        \\begin{{tabular}}{{ | {" | ".join(["c"] * cols_size)} | }}
        \\hline
        {table_data} 
        \\hline
        \\end{{tabular}}
    \\end{{table}}
    """


def generate_table(pure_table: list[list[str]]) -> str:
    """
    Генерирует LaTeX-код таблицы.

    :param pure_table: двойной список, представляющий содержимое таблицы
    :return: строка с LaTeX-кодом таблицы
    """
    rows = len(pure_table)
    cols = len(pure_table[0]) if rows > 0 else 0

    table_rows = (" & ".join(str(item) for item in row) + " \\\\\n" for row in pure_table)

    table_data = "\\hline\n".join(table_rows)

    return _table_template(table_data, cols)


def generate_image(image_path, caption="Sample Image", label="fig:sample"):
    """
    Генерирует LaTeX-код для вставки изображения.

    :param image_path: путь к изображению
    :param caption: подпись к изображению
    :param label: метка для ссылки
    :return: строка с LaTeX-кодом для изображения
    """
    return f"""
\\begin{{figure}}[ht]
    \\centering
    \\includegraphics[width=0.8\\textwidth]{{{image_path}}}
    \\caption{{{caption}}}
    \\label{{{label}}}
\\end{{figure}}
"""
