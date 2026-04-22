import io
import base64
import matplotlib
import matplotlib.pyplot as plt

# 全局配置深色模式与中文字体支持
matplotlib.use('Agg') # 无头环境必须开启 Agg 模式
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

def generate_gold_trend_base64(data_list: list) -> tuple[str, dict]:
    """生成金价三十天跨平台走势图，返回基于 Base64 的图片序列和统计字典"""
    if not data_list:
        return "", {}
        
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
    fig.patch.set_facecolor('#1a1a2e')  # 背景颜色
    ax.set_facecolor('#1a1a2e')
    
    platforms = {
        'tieba': ('贴吧', '#FF5722'),
        'wanbaolou': ('万宝楼', '#00BCD4'),
        'dd373': ('DD373', '#FFC107'),
        'uu898': ('UU898', '#9C27B0'),
        '5173': ('5173', '#8BC34A'),
        '7881': ('7881', '#E91E63')
    }
    
    import datetime
    from datetime import timedelta
    import numpy as np
    from scipy.interpolate import make_interp_spline
    
    today = datetime.datetime.now().date()
    date_range_str = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
    x_labels = [d[5:] for d in date_range_str]
    
    data_dict = {item.get('date', ''): item for item in data_list if item.get('date')}
    all_valid_prices = []
    max_price = {"val": 0, "platform": "", "date": ""}
    min_price = {"val": 999999, "platform": "", "date": ""}
    
    # 动态渲染平滑折线
    for p_key, (p_name, color) in platforms.items():
        valid_x = []
        valid_y = []
        for idx, date_str in enumerate(date_range_str):
            item = data_dict.get(date_str)
            if item:
                try:
                    val = float(item.get(p_key, 0))
                except:
                    val = 0
                if val > 0:
                    valid_x.append(idx)
                    valid_y.append(val)
                    all_valid_prices.append(val)
                    if val > max_price["val"]:
                        max_price = {"val": val, "platform": p_name, "date": date_str[5:]}
                    if val < min_price["val"]:
                        min_price = {"val": val, "platform": p_name, "date": date_str[5:]}
                        
        if len(valid_x) > 3:  # 超过3个点才能使用平滑的三次样条插值
            from scipy.interpolate import PchipInterpolator
            pchip = PchipInterpolator(valid_x, valid_y)
            x_smooth = np.linspace(min(valid_x), max(valid_x), 300)
            y_smooth = pchip(x_smooth)
            ax.plot(x_smooth, y_smooth, linestyle='-', linewidth=2, color=color, label=p_name, alpha=0.9)
            # 给源点单独打上一层散点标记以便确认
            ax.scatter(valid_x, valid_y, color=color, s=15, alpha=0.8, zorder=5)
        elif len(valid_x) > 0:
            ax.plot(valid_x, valid_y, marker='o', markersize=3, linestyle='-', linewidth=2, color=color, label=p_name, alpha=0.9)
            
    # 配置横轴自定义刻度体系
    ax.set_xticks(range(30))
    ax.set_xticklabels(x_labels)
    ax.tick_params(axis='x', rotation=45, colors='#a0a0a0', labelsize=9)
    ax.tick_params(axis='y', colors='#a0a0a0', labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#404040')
    
    ax.grid(axis='y', linestyle='--', alpha=0.2)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(platforms), frameon=False)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    b64_img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    avg_val = round(sum(all_valid_prices) / len(all_valid_prices), 2) if all_valid_prices else 0
    if min_price["val"] == 999999:
        min_price["val"] = 0
        
    stats = {
        "max": max_price,
        "min": min_price,
        "avg": avg_val
    }
    
    return b64_img, stats
