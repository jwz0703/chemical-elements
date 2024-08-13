def load_elements(filename):
    elements = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            symbol, chinese_name, electron_config, row, col = line.strip().split(',')
            elements.append((symbol, chinese_name, electron_config, int(row), int(col)))
    return elements
def get_element_color(row, col):
    # 鑭系元素
    if row == 8:
        return "#FFC0CB"  # 粉紅色
    # 錒系元素
    if row == 9:
        return "#F08080"  # 淺珊瑚色
    # 鹼金屬
    if col == 1 and row > 1:
        return "#FF6666"  # 紅色
    # 鹼土金屬
    if col == 2 and row > 1:
        return "#FFDAB9"  # 淺橙色
    # 稀有氣體
    if col == 18 :
        return "#E6E6FA"  # 淺紫色
    # 鹵素
    if col == 17 and row > 1:
        return "#FFFF00"  # 黃色
    # 非金屬
    if (row <= 2 and col > 13) or (row <= 3 and col >= 15) or (row <= 4 and col >= 16) or (row == 5 and col == 17):
        return "#90EE90"  # 淺綠色
    # 半金屬
    if (row == 2 and col == 13) or (row <= 4 and col == 14) or (row <= 5 and col == 15) or (row == 5 and col == 16):
        return "#97FFFF"  # 淺青色
    # 過渡金屬
    if col in range(3, 13) and row > 3:
        return "#FFD700"  # 金色
    # 其他金屬
    if col in [13, 14, 15, 16] and row > 2:
        return "#BFC9CA"  # 淺灰色
    # 氫
    if row == 1 and col == 1:
        return "#E6E6FA"  # 淺紫色

# 為了測試，可以添加以下代碼：
for row in range(1, 10):
    for col in range(1, 19):
        print(f"Row {row}, Col {col}: {get_element_color(row, col)}")
def create_periodic_table(elements):
    table = [[" " for _ in range(18)] for _ in range(10)]
    
    for index, (symbol, chinese_name, electron_config, row, col) in enumerate(elements, start=1):
        if row == 8 or row == 9:
            col -= 1
        if row > 10 or col > 18:
            print(f"Error: Element {symbol} has row {row} or column {col} out of range.")
            continue
        
        bg_color = get_element_color(row, col)
        atomic_number = f"<div style='font-size: 10px; position: absolute; top: 2px; left: 2px;'>{index}</div>"
        colored_symbol = f"<div style='font-size: 18px; font-weight: bold; margin-bottom: 2px;'>{symbol}</div>"
        colored_name = f"<div style='font-size: 8px; color: #333; margin-bottom: 1px;'>{chinese_name}</div>"
        electron_config = f"<div style='font-size: 6px; color: #666; font-style: italic;'>{electron_config}</div>"
        
        table[row-1][col-1] = f"""<div style='
            background-color: {bg_color};
            padding: 2px;
            border-radius: 4px;
            width: 50px;
            height: 50px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
        '>
            {atomic_number}
            {colored_symbol}
            {colored_name}
            {electron_config}
        </div>"""
    
    return table
def print_periodic_table(table, file):
    file.write("<table style='border-collapse: separate; border-spacing: 1px; margin: auto;'>\n")
    
    # Write header
    file.write("<tr><td style='width: 50px; height: 50px;'></td>")
    for i in range(1, 19):
        file.write(f"<td style='text-align: center; font-weight: bold; width: 50px; height: 50px; padding: 0; font-size: 12px;'>{i}</td>")
    file.write("</tr>\n")
    
    # Write body
    for row_num, row in enumerate(table, start=1):
        file.write(f"<tr><td style='text-align: center; font-weight: bold; width: 50px; height: 50px; padding: 0; font-size: 12px;'>{row_num}</td>")
        for cell in row:
            if cell == " ":
                file.write("<td style='width: 50px; height: 50px;'></td>")
            else:
                file.write(f"<td style='width: 50px; height: 50px; padding: 0;'>{cell}</td>")
        file.write("</tr>\n")
    
    file.write("</table>\n")

    # Add legend
    file.write("<div style='margin-top: 20px; text-align: center;'>\n")
    file.write("<h3>圖例</h3>\n")
    legend_items = [
        ("鹼金屬", "#FF6666"),
        ("鹼土金屬", "#FFDAB9"),
        ("過渡金屬", "#FFD700"),
        ("其他金屬", "#BFC9CA"),
        ("類金屬", "#97FFFF"),
        ("非金屬", "#90EE90"),
        ("鹵素", "#FFFF00"),
        ("稀有氣體", "#E6E6FA"),
        ("鑭系元素", "#FFC0CB"),
        ("錒系元素", "#F08080")
    ]
    for name, color in legend_items:
        file.write(f"<span style='display: inline-block; margin: 5px; padding: 5px 10px; background-color: {color}; border-radius: 4px;'>{name}</span>\n")
    file.write("</div>\n")

elements = load_elements('elements.txt')
periodic_table = create_periodic_table(elements)

# Write results to file
with open("periodic_table.md", "w", encoding="utf-8") as file:
    file.write("# 週期表\n\n")
    file.write("<style>\n")
    file.write("body { font-family: Arial, sans-serif; background-color: #f0f0f0; }\n")
    file.write("table { background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }\n")
    file.write("td > div { transition: all 0.3s ease; }\n")
    file.write("td > div:hover { transform: scale(1.1); box-shadow: 0 2px 6px rgba(0,0,0,0.2); z-index: 1; }\n")
    file.write("</style>\n\n")
    print_periodic_table(periodic_table, file)

print("週期表已成功保存到 periodic_table.md 檔案中。")