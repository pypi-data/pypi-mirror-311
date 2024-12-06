
def generate_latex_table(matrix):
    """
    Генерация LaTeX кода таблицы из двойного списка (matrix).
    
    Args:
        matrix: Двойной список значений, которые должны быть включены в таблицу.

    Returns:
        str: Строка с кодом LaTeX для таблицы.
    """
    def format_row(row):
        return ' & '.join(map(str, row)) + ' \\\\'

    table_header = '\\begin{tabular}{' + 'c' * len(matrix[0]) + '}'
    table_footer = '\\end{tabular}'
    formatted_rows = map(format_row, matrix)
    table_body = '\n'.join(formatted_rows)

    return '\n'.join([table_header, '\\hline', table_body, '\\hline', table_footer])

def generate_latex_image(image_path, width='\\textwidth'):
    """
    Генерация LaTeX кода для вставки изображения.

    Args:
        image_path: Путь к файлу изображения.
        width: Ширина изображения в LaTeX (например, '\\textwidth').

    Returns:
        str: Строка с LaTeX кодом для изображения.
    """
    return f"""
\\begin{{figure}}[h!]
    \\centering
    \\includegraphics[width={width}]{{{image_path}}}
    \\caption{{Image example}}
    \\label{{fig:sample_image}}
\\end{{figure}}
    """
