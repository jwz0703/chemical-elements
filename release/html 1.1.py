def load_elements(filename):
    elements = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            symbol, chinese_name, electron_config, row, col = line.strip().split(',')
            elements.append((symbol, chinese_name, electron_config, int(row), int(col)))
    return elements

def get_element_color(row, col):
    if row == 8:
        return "#F06292, #EC407A"  # 淺粉紅到中粉紅
    if row == 9:
        return "#BA68C8, #AB47BC"  # 淺紫到中紫
    if col == 1 and row > 1:
        return "#EF5350, #E53935"  # 淺紅到中紅
    if col == 2 and row > 1:
        return "#FF7043, #F4511E"  # 淺橙到深橙
    if col == 18:
        return "#5C6BC0, #3F51B5"  # 淺靛藍到靛藍
    if col == 17 and row > 1:
        return "#FFEE58, #FDD835"  # 淺黃到中黃
    if (row <= 2 and col > 13) or (row <= 3 and col >= 15) or (row <= 4 and col >= 16) or (row == 5 and col == 17):
        return "#66BB6A, #43A047"  # 淺綠到中綠
    if (row == 2 and col == 13) or (row <= 4 and col == 14) or (row <= 5 and col == 15) or (row == 5 and col == 16):
        return "#26C6DA, #00ACC1"  # 淺青到中青
    if col in range(3, 13) and row > 3:
        return "#FFA726, #FB8C00"  # 淺橙到深橙
    if col in [13, 14, 15, 16] and row > 2:
        return "#78909C, #546E7A"  # 淺藍灰到藍灰
    if row == 1 and col == 1:
        return "#42A5F5, #2196F3"  # 淺藍到藍
    return "#E0E0E0, #BDBDBD"  # 淺灰到中灰

def create_periodic_table(elements):
    table = [[" " for _ in range(18)] for _ in range(10)]
    
    for index, (symbol, chinese_name, electron_config, row, col) in enumerate(elements, start=1):
        if row == 8 or row == 9:
            col -= 1
        if row > 10 or col > 18:
            print(f"Error: Element {symbol} has row {row} or column {col} out of range.")
            continue
        
        bg_color = get_element_color(row, col)
        table[row-1][col-1] = f"""
        <div class="element" style="background: linear-gradient(135deg, {bg_color});">
            <div class="atomic-number">{index}</div>
            <div class="symbol">{symbol}</div>
            <div class="name">{chinese_name}</div>
            <div class="electron-config">{electron_config}</div>
        </div>
        """
    
    return table

def generate_html(table):
    html = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>精美週期表</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap');
        body {
            font-family: 'Noto Sans TC', sans-serif;
            background: linear-gradient(45deg, #1a237e, #283593, #303f9f, #3949ab);
            color: #FFFFFF;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            color: #FFF;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .periodic-table {
            display: grid;
            grid-template-columns: repeat(18, 1fr);
            gap: 3px;
            max-width: 1200px;
            margin: auto;
        }
        .element {
            width: 62px;
            height: 62px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-radius: 5px;
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .element:hover {
            transform: scale(1.1);
            z-index: 1;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .atomic-number {
            position: absolute;
            top: 2px;
            left: 2px;
            font-size: 10px;
            font-weight: bold;
            color: rgba(0, 0, 0, 0.7);
        }
        .symbol {
            font-size: 22px;
            font-weight: bold;
            color: rgba(0, 0, 0, 0.9);
        }
        .name {
            font-size: 8px;
            margin-top: 2px;
            color: rgba(0, 0, 0, 0.8);
        }
        .electron-config {
            font-size: 6px;
            color: rgba(0, 0, 0, 0.6);
        }
        .legend {
            margin-top: 30px;
            text-align: center;
        }
        .legend-item {
            display: inline-block;
            margin: 5px;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .legend-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .period-labels, .group-labels {
            position: absolute;
            display: flex;
            justify-content: space-around;
            width: 100%;
            font-weight: bold;
            color: #FFF;
        }
        .period-labels {
            flex-direction: column;
            height: 100%;
            left: -30px;
            top: 0;
        }
        .group-labels {
            top: -30px;
            left: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>精美週期表</h1>
        <div style="position: relative;">
            <div class="period-labels">
                <div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div>
            </div>
            <div class="group-labels">
                <div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div><div>9</div><div>10</div><div>11</div><div>12</div><div>13</div><div>14</div><div>15</div><div>16</div><div>17</div><div>18</div>
            </div>
            <div class="periodic-table">
    """
    
    for row_num, row in enumerate(table, start=1):
        for col_num, cell in enumerate(row, start=1):
            if cell == " ":
                html += "<div></div>"
            else:
                html += cell
    
    html += """
            </div>
        </div>
        <div class="legend">
            <h3>圖例</h3>
    """
    
    legend_items = [
        ("鹼金屬", "#EF5350, #E53935"),
        ("鹼土金屬", "#FF7043, #F4511E"),
        ("過渡金屬", "#FFA726, #FB8C00"),
        ("其他金屬", "#78909C, #546E7A"),
        ("類金屬", "#26C6DA, #00ACC1"),
        ("非金屬", "#66BB6A, #43A047"),
        ("鹵素", "#FFEE58, #FDD835"),
        ("稀有氣體", "#5C6BC0, #3F51B5"),
        ("鑭系元素", "#F06292, #EC407A"),
        ("錒系元素", "#BA68C8, #AB47BC")
    ]
    
    for name, color in legend_items:
        html += f'<span class="legend-item" style="background: linear-gradient(135deg, {color});">{name}</span>'
    
    html += """
        </div>
    </div>
</body>
</html>
    """
    
    return html

elements = load_elements('elements.txt')
periodic_table = create_periodic_table(elements)
html_content = generate_html(periodic_table)

with open("periodic_table.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("精美的週期表已成功保存到 periodic_table.html 檔案中。")