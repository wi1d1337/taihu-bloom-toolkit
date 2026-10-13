"""冒烟测试：python -m tests.test_smoke（pytest 亦可）。"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taihu_toolkit.ccm import causal_direction
from taihu_toolkit.dispatch import greedy_dispatch
from taihu_toolkit.forecast import event_metrics, persistence_forecast
from taihu_toolkit.growth import growth_rate
from taihu_toolkit.indicators import permutation_entropy, rolling_ar1
from taihu_toolkit.ndci import chla_from_ndci, ndci
from taihu_toolkit.synth import fleet, separation_stations, synth_taihu, zonal_loads


def test_growth_and_ndci():
    mu = growth_rate(temp=25.0, rad=220.0, N=1.5, P=0.05)
    assert 0 < mu <= 1.7, mu
    x = ndci(0.12, 0.08)
    assert -1 < x < 1
    assert chla_from_ndci(x) > 0


def test_synth_and_indicators():
    from taihu_toolkit.synth import ZONES
    df = synth_taihu(days=400, seed=1)
    assert set(df["zone"].unique()) == set(ZONES)
    z = df[df["zone"] == "贡湖"]["chla"].to_numpy()
    ar1 = rolling_ar1(z, window=180)
    assert np.isfinite(np.nanmean(ar1[180:]))
    assert 0 <= permutation_entropy(z[-200:], order=3) <= 1


def test_ccm_direction():
    # Sugihara 2012 经典单向耦合：X 驱动 Y（非线性混沌，CCM 可分辨方向）
    n, burn = 900, 200
    x = np.zeros(n + burn)
    y = np.zeros(n + burn)
    x[0], y[0] = 0.4, 0.2
    for k in range(n + burn - 1):
        x[k + 1] = x[k] * (3.8 - 3.8 * x[k])
        y[k + 1] = y[k] * (3.5 - 3.5 * y[k]) + 0.32 * x[k]
        if not (0.0 < y[k + 1] < 1.0):   # 越界重置（保序列有界）
            y[k + 1] = 0.35
    x, y = x[burn:], y[burn:]  # 去暂态
    res = causal_direction(y, x, E=3, tau=1)   # a=Y（响应）, b=X（驱动）
    assert res["direction"] == "b=>a", res      # X ⇒ Y


def test_event_metrics():
    m = event_metrics([10, 10, 2, 2], [10, 2, 10, 2], threshold=5)
    assert m["hits"] == 1 and m["misses"] == 1 and m["false_alarms"] == 1
    assert abs(m["POD"] - 0.5) < 1e-9 and abs(m["FAR"] - 0.5) < 1e-9


def test_dispatch():
    r = greedy_dispatch(fleet(), zonal_loads(), separation_stations(), quantile="q50", key_zone="贡湖")
    assert r["collected_tons"] > 0
    assert all(v <= separation_stations()[k] + 1e-6 for k, v in r["station_load"].items())
    boats_used = set(r["assignment"])
    assert len(boats_used) == len(r["assignment"])  # 单船单任务
    assert "贡湖" in r["assignment"].values()       # 重点水域保底


def test_persistence():
    p = persistence_forecast(__import__("pandas").Series([1, 2, 3]), 3)
    assert np.allclose(p, 3.0)


if __name__ == "__main__":
    for name, fn in sorted({k: v for k, v in globals().items() if k.startswith("test_")}.items()):
        fn()
        print(f"PASS {name}")
    print("all smoke tests passed")
