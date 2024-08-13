def load_elements(filename):
    elements = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            symbol, chinese_name, electron_config, row, col = line.strip().split(',')
            elements.append((symbol, chinese_name, electron_config, int(row), int(col)))
    return elements

def get_element_color(row, col):
    if row == 8:
        return "#FF00FF, #8A2BE2"  # 鮮豔的粉紅色到藍紫色
    if row == 9:
        return "#FF1493, #C71585"  # 深粉色到中紫紅色
    if col == 1 and row > 1:
        return "#FF4500, #FF0000"  # 橙紅色到純紅色
    if col == 2 and row > 1:
        return "#FFA500, #FF8C00"  # 橙色到深橙色
    if col == 18:
        return "#00FFFF, #00CED1"  # 青色到深青色
    if col == 17 and row > 1:
        return "#FFFF00, #FFD700"  # 黃色到金色
    if (row <= 2 and col > 13) or (row <= 3 and col >= 15) or (row <= 4 and col >= 16) or (row == 5 and col == 17):
        return "#00FF00, #32CD32"  # 亮綠色到檸檬綠
    if (row == 2 and col == 13) or (row <= 4 and col == 14) or (row <= 5 and col == 15) or (row == 5 and col == 16):
        return "#1E90FF, #4169E1"  # 道奇藍到皇家藍
    if col in range(3, 13) and row > 3:
        return "#FFD700, #FFA07A"  # 金色到淺鮭色
    if col in [13, 14, 15, 16] and row > 2:
        return "#C0C0C0, #A9A9A9"  # 銀色到深灰色
    if row == 1 and col == 1:
        return "#FF69B4, #FF1493"  # 熱粉紅到深粉紅
    return "#FFFFFF, #F8F8FF"  # 純白到幽靈白

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
    <title>超炫酷週期表</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        body {
            font-family: 'Orbitron', sans-serif;
            background: linear-gradient(45deg, #000000, #1a1a2e, #16213e, #0f3460);
            color: #00FFFF;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            overflow-x: hidden;
        }
        .container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            position: relative;
        }
        .container::before {
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            background: linear-gradient(45deg, #ff00ff, #00ff00, #ff00ff, #00ff00);
            z-index: -1;
            filter: blur(20px);
            opacity: 0.7;
            animation: glowing 20s linear infinite;
        }
        @keyframes glowing {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        h1 {
            text-align: center;
            font-size: 3.5em;
            margin-bottom: 30px;
            text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 30px #00FFFF;
            animation: pulsate 2s infinite alternate;
        }
        @keyframes pulsate {
            0% { text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 30px #00FFFF; }
            100% { text-shadow: 0 0 20px #00FFFF, 0 0 30px #00FFFF, 0 0 40px #00FFFF, 0 0 50px #00FFFF, 0 0 60px #00FFFF; }
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
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
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
            transform: scale(1.3) rotate(10deg);
            z-index: 1;
            box-shadow: 0 0 30px rgba(255,255,255,0.8);
        }
        .atomic-number {
            position: absolute;
            top: 2px;
            left: 2px;
            font-size: 10px;
            font-weight: bold;
            color: rgba(255, 255, 255, 0.8);
        }
        .symbol {
            font-size: 22px;
            font-weight: bold;
            text-shadow: 0 0 5px rgba(255,255,255,0.5);
        }
        .name {
            font-size: 8px;
            margin-top: 2px;
            color: rgba(255, 255, 255, 0.9);
        }
        .electron-config {
            font-size: 6px;
            font-style: italic;
            opacity: 0.7;
            color: rgba(255, 255, 255, 0.7);
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
            box-shadow: 0 0 10px rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }
        .legend-item:hover {
            transform: translateY(-3px) scale(1.1);
            box-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        .period-labels, .group-labels {
            position: absolute;
            display: flex;
            justify-content: space-around;
            width: 100%;
            font-weight: bold;
            color: #00FFFF;
            text-shadow: 0 0 5px #00FFFF;
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
        <h1>超炫酷週期表</h1>
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
        ("鹼金屬", "#FF4500, #FF0000"),
        ("鹼土金屬", "#FFA500, #FF8C00"),
        ("過渡金屬", "#FFD700, #FFA07A"),
        ("其他金屬", "#C0C0C0, #A9A9A9"),
        ("類金屬", "#1E90FF, #4169E1"),
        ("非金屬", "#00FF00, #32CD32"),
        ("鹵素", "#FFFF00, #FFD700"),
        ("稀有氣體", "#00FFFF, #00CED1"),
        ("鑭系元素", "#FF00FF, #8A2BE2"),
        ("錒系元素", "#FF1493, #C71585")
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

print("超炫酷的週期表已成功保存到 periodic_table.html 檔案中。")