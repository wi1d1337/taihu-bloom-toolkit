"""示例 1：预报基线与 POD/FAR/CSI 评测（方案表 2 基线 + 表 3 指标）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taihu_toolkit.forecast import climatology_forecast, event_metrics, persistence_forecast
from taihu_toolkit.synth import synth_taihu

df = synth_taihu(days=730, seed=7)
zone = "梅梁湾"
z = df[df["zone"] == zone]["chla"]
train, test = z[:-72], z[-72:]
thr = float(train.quantile(0.85))  # 事件阈值（演示口径，真实口径由共建评测集定义）

print(f"分区：{zone} ｜ 事件阈值 Chl-a ≥ {thr:.1f} ug/L（P85）")
print(f"{'模型':<14}{'POD':>8}{'FAR':>8}{'CSI':>8}")
for name, preds in [
    ("持续性", [persistence_forecast(train[: -3 * i], 3).tolist() for i in range(24, 0, -1)]),
    ("气候态", [climatology_forecast(train, test.index[3 * i:3 * i + 3], 3).tolist() for i in range(24)]),
]:
    flat = [v for p in preds for v in p]
    m = event_metrics(test.to_numpy()[: len(flat)], flat, thr)
    print(f"{name:<14}{m['POD']:>8.2f}{m['FAR']:>8.2f}{m['CSI']:>8.2f}")
print("\n说明：CNN-LSTM 主模型（方案表 2）接入真实数据后替换 forecast 接口即可。")
