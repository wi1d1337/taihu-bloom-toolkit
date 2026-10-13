"""示例 3：CCM 因果检验——风速 → 水华（方案式 8）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taihu_toolkit.ccm import causal_direction, ccm_skill
from taihu_toolkit.synth import synth_taihu

df = synth_taihu(days=1095, seed=5)
z = df[df["zone"] == "西部沿岸"]
wind = z["wind"].to_numpy()
chla = z["chla"].to_numpy()

L, rho = ccm_skill(chla, wind, E=3, tau=8)
print("检验『风速 ⇒ 水华』：库长度 L 与预测技能 rho（上升 ⇒ 支持因果，式 8）")
for l, r in zip(L[::2], rho[::2]):
    bar = "█" * max(0, int((r + 0.05) * 40))
    print(f"  L={l:>5}  rho={r:+.3f}  {bar}")

res = causal_direction(chla, wind, E=3, tau=8)
print(f"\n方向判定（技能增幅对比）：{res['direction']}（wind=>chla 即风速驱动水华）")
print("生产使用建议换 rEDM / pyEDM（方案 4.2 节），本实现为教学级简化。")
