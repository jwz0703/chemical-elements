def load_elements(filename):
    elements = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            symbol, chinese_name, electron_config, row, col = line.strip().split(',')
            elements.append((symbol, chinese_name, electron_config, int(row), int(col)))
    return elements

def get_element_color(row, col):
    if row == 8:
        return "#FFC0CB, #FF69B4"
    if row == 9:
        return "#F08080, #CD5C5C"
    if col == 1 and row > 1:
        return "#FF6666, #FF0000"
    if col == 2 and row > 1:
        return "#FFDAB9, #FFB366"
    if col == 18:
        return "#E6E6FA, #9370DB"
    if col == 17 and row > 1:
        return "#FFFF00, #FFD700"
    if (row <= 2 and col > 13) or (row <= 3 and col >= 15) or (row <= 4 and col >= 16) or (row == 5 and col == 17):
        return "#90EE90, #32CD32"
    if (row == 2 and col == 13) or (row <= 4 and col == 14) or (row <= 5 and col == 15) or (row == 5 and col == 16):
        return "#97FFFF, #00CED1"
    if col in range(3, 13) and row > 3:
        return "#FFD700, #DAA520"
    if col in [13, 14, 15, 16] and row > 2:
        return "#BFC9CA, #95A5A6"
    if row == 1 and col == 1:
        return "#E6E6FA, #9370DB"
    return "#FFFFFF, #EEEEEE"

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
    <title>超華麗週期表</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(45deg, #1a1a2e, #16213e, #0f3460);
            color: #e94560;
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
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 30px;
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
            width: 60px;
            height: 60px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-radius: 8px;
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
            overflow: hidden;
        }
        .element::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                transparent, 
                rgba(255, 255, 255, 0.3), 
                transparent 30%
            );
            animation: rotate 4s linear infinite;
        }
        @keyframes rotate {
            100% {
                transform: rotate(1turn);
            }
        }
        .element:hover {
            transform: scale(1.2) rotate(5deg);
            z-index: 1;
            box-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        .atomic-number {
            position: absolute;
            top: 2px;
            left: 2px;
            font-size: 10px;
            font-weight: bold;
        }
        .symbol {
            font-size: 22px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .name {
            font-size: 8px;
            margin-top: 2px;
        }
        .electron-config {
            font-size: 6px;
            font-style: italic;
            opacity: 0.7;
        }
        .legend {
            margin-top: 30px;
            text-align: center;
        }
        .legend-item {
            display: inline-block;
            margin: 5px;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .legend-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .period-labels, .group-labels {
            position: absolute;
            display: flex;
            justify-content: space-around;
            width: 100%;
            font-weight: bold;
            color: #e94560;
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
        <h1>超華麗週期表</h1>
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
        ("鹼金屬", "#FF6666, #FF0000"),
        ("鹼土金屬", "#FFDAB9, #FFB366"),
        ("過渡金屬", "#FFD700, #DAA520"),
        ("其他金屬", "#BFC9CA, #95A5A6"),
        ("類金屬", "#97FFFF, #00CED1"),
        ("非金屬", "#90EE90, #32CD32"),
        ("鹵素", "#FFFF00, #FFD700"),
        ("稀有氣體", "#E6E6FA, #9370DB"),
        ("鑭系元素", "#FFC0CB, #FF69B4"),
        ("錒系元素", "#F08080, #CD5C5C")
    ]
    
    for name, color in legend_items:
        html += f'<span class="legend-item" style="background: linear-gradient(135deg, {color});">{name}</span>'
    
    html += """
        </div>
    </div>
    <script>
        document.querySelectorAll('.element').forEach(el => {
            el.addEventListener('mouseover', () => {
                el.style.animationPlayState = 'paused';
            });
            el.addEventListener('mouseout', () => {
                el.style.animationPlayState = 'running';
            });
        });
    </script>
</body>
</html>
    """
    
    return html

elements = load_elements('elements.txt')
periodic_table = create_periodic_table(elements)
html_content = generate_html(periodic_table)

with open("periodic_table.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("超華麗的週期表已成功保存到 periodic_table.html 檔案中。")