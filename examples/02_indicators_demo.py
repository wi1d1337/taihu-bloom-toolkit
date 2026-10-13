"""示例 2：临界慢化指标——滚动 AR(1) 与方差（方案式 7）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from taihu_toolkit.indicators import permutation_entropy, rolling_ar1, rolling_var
from taihu_toolkit.synth import synth_taihu

df = synth_taihu(days=1095, seed=3)
z = df[df["zone"] == "梅梁湾"]["chla"].to_numpy()
ar1 = rolling_ar1(z, window=365)
var = rolling_var(z, window=365)
pe = permutation_entropy(z[-365:], order=4)

print("梅梁湾 Chl-a（合成序列，近三年）")
a1_first, a1_last = float(np.nanmean(ar1[365:730])), float(np.nanmean(ar1[730:]))
v_first, v_last = float(np.nanmean(var[365:730])), float(np.nanmean(var[730:]))
print(f"  滚动 AR(1)：首年 {a1_first:.3f} → 末年 {a1_last:.3f}")
print(f"  滚动方差  ：首年 {v_first:.1f} → 末年 {v_last:.1f}")
print(f"  近一年排列熵（4 阶归一）：{pe:.3f}")
if a1_last > a1_first and v_last > v_first:
    print("\n解读：AR(1) 与方差同步上升——系统恢复变慢（临界慢化特征，式 7）；")
else:
    print("\n解读：本合成序列未呈现 AR(1) 与方差同步上升，无临界慢化证据（式 7 为研究性监测量）。")
print("该指标为研究性监测量，不进入运行决策（方案 4.1 节边界说明）。")
