"""示例 4：打捞调度建议单生成（方案式 9 启发式降级版，5.3 节）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taihu_toolkit.dispatch import greedy_dispatch, print_dispatch
from taihu_toolkit.synth import fleet, separation_stations, zonal_loads

boats = fleet()
zones = zonal_loads()
stations = separation_stations()

print("【常规方案】q50 分位预报口径")
r1 = greedy_dispatch(boats, zones, stations, quantile="q50", key_zone="贡湖")
print_dispatch(r1)

print("\n【保守方案】q25 分位预报口径（机会约束的保守取值，方案 5.2 节）")
r2 = greedy_dispatch(boats, zones, stations, quantile="q25", key_zone="贡湖")
print_dispatch(r2)

print("\n说明：真实系统按式 9 走 MIP 滚动求解（CBC/SCIP），本例为其降级启发式；")
print("调度单为建议值，由调度人员确认执行（旁路红线，方案 1.1 节）。")
