
from latex_gen import generate_latex_table

def save_latex_to_file(filename, latex_code):
    """
    Сохраняем LaTeX код в файл.
    
    Args:
        filename: Имя файла, в который будет сохранён LaTeX код.
        latex_code: Строка, содержащая код LaTeX.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(latex_code)

example_matrix = [
    ["Row1Col1", "Row1Col2", "Row1Col3"],
    ["Row2Col1", "Row2Col2", "Row2Col3"],
    ["Row3Col1", "Row3Col2", "Row3Col3"]
]

latex_code = generate_latex_table(example_matrix)

full_latex_document = f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}

\\begin{{document}}

{latex_code}

\\end{{document}}
"""

save_latex_to_file('artifacts/example_table.tex', full_latex_document)
