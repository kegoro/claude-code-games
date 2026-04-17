"""GA 進化回測引擎全域設定（契約 V2.0.0 — single source of truth）。

本檔是《GA 進化回測引擎 V2 契約》的唯一權威來源，涵蓋：
- A.1 PDE 微觀信號視窗
- A.2 庫存橋解封閾值
- A.3 適應度公式常數
- A.5 1-4-5 繁衍配比
- A.7 GA 超參常數表
- A.8 基因合法盒

所有模組禁止硬編碼契約參數，一律從此檔讀取。變更任何契約項必須 bump CONTRACT_VERSION。
對應文件：docs/CONTRACT.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ---------------------------------------------------------------------------
# 契約版本
# ---------------------------------------------------------------------------
CONTRACT_VERSION: str = "2.0.0"

# ---------------------------------------------------------------------------
# 資產與資料層（Q1, Q1b）
# ---------------------------------------------------------------------------
SYMBOL: str = "BTCUSDT"
BASE_CLOCK_MINUTES: int = 1
BACKTEST_START: str = "2016-01-01"
BACKTEST_END: str = "2026-01-01"
INITIAL_CAPITAL: float = 100_000.0  # USDT

DATA_CACHE_DIR: str = "data/cache"
EXCHANGE_SPECS_DIR: str = "data/specs"
BINANCE_VISION_BASE: str = "https://data.binance.vision/data/spot/monthly/klines"

BINANCE_BTCUSDT_FALLBACK_SPECS: dict[str, float] = {
    "step_size": 0.00001,
    "min_qty": 0.00001,
    "min_notional": 5.0,
    "tick_size": 0.01,
}

# ---------------------------------------------------------------------------
# A.3 適應度公式常數（LOCKED）
# ---------------------------------------------------------------------------
FITNESS_W_ALPHA: float = 1.0
FITNESS_W_PNL: float = 1.0
FITNESS_W_MDD: float = 2.0
FITNESS_K_MDD: float = 5.0
FITNESS_W_FRICTION: float = 1.0

TAKER_FEE_RATE: float = 0.001

MDD_SAMPLING: Literal["daily_close"] = "daily_close"

# ---------------------------------------------------------------------------
# A.1 PDE 視窗設定（Q-S1, Q-S2）
# ---------------------------------------------------------------------------
SIGMA_V_WINDOW_BARS: int = 240
SIGMA_A_WINDOW_BARS: int = 1440
VELOCITY_BARS: int = 5

# ---------------------------------------------------------------------------
# A.2 庫存橋觸發（LOCKED）
# ---------------------------------------------------------------------------
UNLOCK_SIGMA_MULT: float = 2.0

# ---------------------------------------------------------------------------
# A.7 GA 超參（LOCKED）
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GAHyperParams:
    """GA 跨 Epoch 不變的超參包。"""

    pop_size: int
    epochs: int
    generations_per_epoch: int
    elite_ratio: float = 0.05
    tournament_k: int = 3
    p_mut_init: float = 0.15
    p_mut_max: float = 0.55
    mutation_ramp_window: int = 5
    mutation_ramp_threshold: float = 0.005
    mutation_ramp_multiplier: float = 1.25


DEV_GA: GAHyperParams = GAHyperParams(pop_size=100, epochs=50, generations_per_epoch=20)
CLOUD_GA: GAHyperParams = GAHyperParams(pop_size=1000, epochs=200, generations_per_epoch=40)

INIT_ELITE_FRAC: float = 0.10
INIT_MUTANT_FRAC: float = 0.40
INIT_EXPLORER_FRAC: float = 0.50
INIT_MUTANT_SIGMA_AMP: float = 1.5

# ---------------------------------------------------------------------------
# 環境層（頂層 — 造物主法則，Q20）
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EnvironmentBounds:
    """Environment 合法區間與跨 Epoch 截斷常態抽樣配置。"""

    dead_reserve_ratio_min: float = 0.1
    dead_reserve_ratio_max: float = 0.8
    global_stop_loss_min: float = 0.1
    global_stop_loss_max: float = 0.4
    max_leverage: float = 1.0
    sigma_ratio: float = 0.10


ENV_BOUNDS: EnvironmentBounds = EnvironmentBounds()

# ---------------------------------------------------------------------------
# 季節層（中層 — 週期氣候，Q11）
# ---------------------------------------------------------------------------
SEASON_AGGR_TIERS: tuple[float, ...] = (0.5, 0.8, 1.2, 2.0)
SEASON_PRIOR: tuple[float, ...] = (0.25, 0.25, 0.25, 0.25)
SEASON_NAMES: tuple[str, ...] = ("winter", "spring", "summer", "autumn")
SEASON_COUNT: int = 4

# ---------------------------------------------------------------------------
# 坩堝多窗 Alpha 加權 + 蒙卡終審（Q8, Q17）
# ---------------------------------------------------------------------------
CRUCIBLE_WINDOWS: tuple[tuple[str, float], ...] = (
    ("all", 0.4),
    ("5y", 0.3),
    ("2y", 0.2),
    ("6m", 0.1),
)

MC_BLOCK_LEN_DAYS: int = 14
MC_BLOCK_LEN_BARS: int = MC_BLOCK_LEN_DAYS * 1440
MC_PATHS: int = 1000
MC_BANKRUPTCY_WARN: float = 0.05

# ---------------------------------------------------------------------------
# 月相壓力（Q14：虛擬正弦週期 29.53 天，起算日 = BACKTEST_START）
# ---------------------------------------------------------------------------
LUNAR_CYCLE_MINUTES: int = int(29.53 * 1440)

# ---------------------------------------------------------------------------
# A.8 基因 Registry（LOCKED — Q-S6 拆分後版本）
# ---------------------------------------------------------------------------
GeneDType = Literal["float", "int"]
GeneBlock = Literal[0, 1, 2, 3, 4]


@dataclass(frozen=True)
class GeneSpec:
    """單一基因的合法盒與突變配置。"""

    name: str
    dtype: GeneDType
    min_val: float
    max_val: float
    step: float | None
    mutation_sigma: float
    block_id: GeneBlock
    semantics: str


GENE_REGISTRY: tuple[GeneSpec, ...] = (
    # Block 0: 宏觀戰略
    GeneSpec("MaxDCAMonths", "int", 3, 48, 1, 3.0, 0, "最大定投月數（子彈消耗上限）"),
    GeneSpec("BetaThreshold", "float", 0.02, 0.30, None, 0.03, 0, "大盤偏離度觸發門檻"),
    GeneSpec("DeadlineForcePct", "float", 0.0, 1.0, None, 0.1, 0, "耐心耗盡強制動用比例"),
    GeneSpec("GCThresholdMonths", "int", 3, 24, 1, 2.0, 0, "長期閒置 GC 候選門檻月數"),
    GeneSpec("GCMaxRatio", "float", 0.0, 0.5, None, 0.05, 0, "GC 回收上限（相對 dead_btc）"),
    GeneSpec("MacroReserveRate", "float", 0.05, 0.50, None, 0.05, 0, "宏觀單次定投占現金比例"),
    # Block 1: 宏觀時鐘
    GeneSpec("TMacro", "int", 60, 1440, 1, 60.0, 1, "宏觀 tick 分鐘（1h–1d）"),
    GeneSpec("TMicro", "int", 1, 5, 1, 1.0, 1, "微觀 tick 分鐘（>=1m）"),
    GeneSpec("TDeadline", "int", 1440, 525600, 1, 10080.0, 1, "耐心截止分鐘（1d–1y）"),
    GeneSpec("EMAAnchor", "int", 20, 500, 1, 30.0, 1, "EMA / sigma_win 視窗 bar 數"),
    GeneSpec("MoonPhasePressure", "float", 0.0, 2.0, None, 0.2, 1, "月相壓力振幅"),
    # Block 2: 動力學感知
    GeneSpec("kp", "float", -2.0, 2.0, None, 0.25, 2, "位置權重 (Z-score)"),
    GeneSpec("kv", "float", -2.0, 2.0, None, 0.25, 2, "速度權重 (標準化對數收益)"),
    # Block 3: 開火/逃頂
    GeneSpec("ka", "float", -2.0, 2.0, None, 0.25, 3, "加速度權重（速度差分）"),
    GeneSpec("MinTradeThreshold", "float", 0.01, 0.30, None, 0.03, 3, "最小交易偏差閾值"),
    GeneSpec("MicroReserveRate", "float", 0.05, 0.50, None, 0.05, 3, "微觀開火 / 庫存橋解封比例"),
    # Block 4: 形狀參數
    GeneSpec("SigmoidScale", "float", 0.5, 5.0, None, 0.3, 4, "Sigmoid 壓縮陡峭度"),
    GeneSpec("Gamma", "float", 0.0, 1.0, None, 0.1, 4, "波動率折現因子"),
)

GENE_NAMES: tuple[str, ...] = tuple(g.name for g in GENE_REGISTRY)
GENE_SPEC_BY_NAME: dict[str, GeneSpec] = {g.name: g for g in GENE_REGISTRY}

BLOCK_NAMES: dict[GeneBlock, str] = {
    0: "Macro Strategy",
    1: "Macro Clock",
    2: "Dynamics Perception",
    3: "Fire / Escape",
    4: "Shape",
}


def genes_of_block(block_id: GeneBlock) -> tuple[str, ...]:
    """回傳指定 block 包含的基因名稱（正交交叉用）。"""
    return tuple(g.name for g in GENE_REGISTRY if g.block_id == block_id)


# ---------------------------------------------------------------------------
# 契約匯出（docs/CONTRACT.md 會引用）
# ---------------------------------------------------------------------------
DESIGN_CONTRACT: dict[str, object] = {
    "version": CONTRACT_VERSION,
    "symbol": SYMBOL,
    "initial_capital": INITIAL_CAPITAL,
    "fitness": {
        "w_alpha": FITNESS_W_ALPHA,
        "w_pnl": FITNESS_W_PNL,
        "w_mdd": FITNESS_W_MDD,
        "k_mdd": FITNESS_K_MDD,
        "w_friction": FITNESS_W_FRICTION,
        "taker_fee": TAKER_FEE_RATE,
        "mdd_sampling": MDD_SAMPLING,
    },
    "pde": {
        "sigma_v_window": SIGMA_V_WINDOW_BARS,
        "sigma_a_window": SIGMA_A_WINDOW_BARS,
        "velocity_bars": VELOCITY_BARS,
        "unlock_sigma_mult": UNLOCK_SIGMA_MULT,
    },
    "ga": {
        "dev": DEV_GA,
        "cloud": CLOUD_GA,
        "init_fractions": (INIT_ELITE_FRAC, INIT_MUTANT_FRAC, INIT_EXPLORER_FRAC),
        "mutant_sigma_amp": INIT_MUTANT_SIGMA_AMP,
    },
    "environment": ENV_BOUNDS,
    "season": {
        "tiers": SEASON_AGGR_TIERS,
        "prior": SEASON_PRIOR,
        "names": SEASON_NAMES,
    },
    "crucible": {
        "windows": CRUCIBLE_WINDOWS,
        "mc_block_len_days": MC_BLOCK_LEN_DAYS,
        "mc_paths": MC_PATHS,
        "mc_bankruptcy_warn": MC_BANKRUPTCY_WARN,
    },
    "lunar_cycle_minutes": LUNAR_CYCLE_MINUTES,
    "genes": GENE_REGISTRY,
}
