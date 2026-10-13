# taihu-bloom-toolkit

太湖蓝藻水华预报与打捞调度的**最小可运行算法演示库**——把《太湖蓝藻水华预报与打捞调度优化系统技术实施方案》（无锡天垣视界科技有限公司）中的核心算法模块做成开箱即用的 Python 工具，供评估与试用。

> ⚠️ 本仓库内置数据为**合成演示数据**（`taihu_toolkit/synth.py`，模拟太湖风格的季节/营养盐/风场结构），**不是真实太湖观测值**。真实部署需要接入实测数据并重新率定参数（方法见方案第二章）。

## 快速开始

```bash
pip install -r requirements.txt
python examples/01_forecast_demo.py     # 预报基线 + POD/FAR/CSI 评测
python examples/02_indicators_demo.py   # 临界慢化指标（AR(1)/方差/排列熵）
python examples/03_ccm_demo.py          # CCM 因果检验（风速 → 水华）
python examples/04_dispatch_demo.py     # 打捞调度建议单生成
python -m tests.test_smoke              # 冒烟测试
```

## 模块与方案对应关系

| 模块 | 内容 | 对应方案 |
|---|---|---|
| `taihu_toolkit.growth` | 藻类生长率：温度 × 光（Steele）× 营养盐（Monod）联合限制 | 式 2 |
| `taihu_toolkit.ndci` | 遥感反演：NDCI 指数 → Chl-a 经验式（系数需同步实测标定） | 式 4、式 5 |
| `taihu_toolkit.indicators` | 临界慢化指标：滚动 AR(1)、滚动方差；排列熵（Bandt–Pompe） | 式 7 |
| `taihu_toolkit.ccm` | 收敛交叉映射（简化实现）：变量间因果方向检验 | 式 8 |
| `taihu_toolkit.forecast` | 预报基线（持续性 / 气候态 / 梯度提升）与 POD/FAR/CSI 事件检验 | 表 2、表 3 |
| `taihu_toolkit.dispatch` | 打捞调度：贪心构造 + 局部交换启发式（MIP 的降级可运行版） | 式 9、5.3 节 |
| `taihu_toolkit.synth` | 合成太湖风格多源日序列（水温/风速/TP/TN/辐射/Chl-a，六分区） | 第二章 |

各模块 docstring 中标注了对应公式与文献出处（同方案参考文献）。

## 设计原则

- **零重型依赖**：核心仅依赖 numpy / pandas；`scikit-learn`、`matplotlib` 为可选（缺失时自动降级）。
- **与方案同一套口径**：指标定义（POD/FAR/CSI）、调度目标结构（收藻量 − 航行成本）与方案正文一致，试用结论可直接对话。
- **可替换**：预报基线留出 CNN-LSTM（方案表 2）接入位——真实数据接入后按方案 3.2 节结构替换即可；调度留出 PuLP/CBC 精确求解接口位。

## License

MIT © 2026 无锡天垣视界科技有限公司
