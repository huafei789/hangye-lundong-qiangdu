import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_excel('基础数据.xlsx', index_col=0, parse_dates=True, header=1)
def calculate_rotation_intensity(df, window=5):
    """计算行业轮动强度指数"""
    returns_5d = df.pct_change(periods=window) * 100
    rotation_intensity = []
    dates = []
    for i in range(window, len(df)):
        date = df.index[i]
        current_returns = returns_5d.iloc[i]
        prev_returns = returns_5d.iloc[i-1]
        if current_returns.isna().any() or prev_returns.isna().any():
            continue
        current_rank = current_returns.rank(ascending=False, method='average')
        prev_rank = prev_returns.rank(ascending=False, method='average')
        rank_change = (current_rank - prev_rank).abs()
        intensity = rank_change.mean()
        rotation_intensity.append(intensity)
        dates.append(date)
    return pd.Series(rotation_intensity, index=dates)
rotation_series = calculate_rotation_intensity(df, window=5)
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(rotation_series.index, rotation_series.values, 
        color='darkblue', linewidth=2, label='行业轮动强度指数')
ax.set_title('行业轮动强度指数', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('轮动强度', fontsize=12)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('行业轮动强度指数.png', dpi=300, bbox_inches='tight')
plt.show()