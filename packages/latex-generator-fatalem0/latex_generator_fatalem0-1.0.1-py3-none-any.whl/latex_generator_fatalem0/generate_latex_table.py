from functools import reduce
from typing import Optional


def generate_latex_table(data: list[list[str]]):
    if not data:
        raise ValueError('Передан пустой список')

    num_columns = len(data[0])
    for row in data:
        if num_columns != len(row):
            raise ValueError('Все строки таблицы должны быть одинаковой длины')

    def row_to_latex(rows: list[str]):
        reduced_str = reduce(lambda a, b: f"{a} & {b}", rows)
        return f" {reduced_str} \\\\"

    def make_res(header: str):
        def res(rows: Optional[str]):
            rows_str = f"{rows}\n \\hline\n" if rows else None

            table = f"\\begin{{tabular}}{{ |{column_format}| }}\n" \
                    " \\hline\n" \
                    f"{header}\n" \
                    f" \\hline\n" \
                    f"{rows_str}" \
                    "\\end{tabular}\n" \

            return table

        return res

    header = data[0]
    rows = data[1:]
    column_format = "|".join(["c"] * num_columns)
    latexed_header = row_to_latex(header)

    if not rows:
        return make_res(latexed_header)(None)

    def rows_to_latex(rows: list[list[str]]):
        def go(acc: str, rows: list[list[str]]):
            if not rows:
                return acc
            return go(f'{acc}\n{row_to_latex(rows[0])}', rows[1:])

        return go(f"{row_to_latex(rows[0])}", rows[1:])

    latexed_rows = rows_to_latex(rows)

    return make_res(latexed_header)(latexed_rows)
