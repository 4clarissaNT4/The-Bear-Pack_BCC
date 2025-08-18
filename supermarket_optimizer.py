# Sistem Promosi Otomatis untuk Supermarket Jack

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple
import csv, os, random

random.seed(42)

# =========================
# DATA TOKO (Exhibit 1)
# =========================
STORES = [
    {"store_id": 1, "open_year": 2015, "size_m2": 180, "sku_count": 6843,  "employees": 4},
    {"store_id": 2, "open_year": 2017, "size_m2": 193, "sku_count": 12311, "employees": 5},
    {"store_id": 3, "open_year": 2018, "size_m2": 220, "sku_count": 14501, "employees": 6},
    {"store_id": 4, "open_year": 2020, "size_m2": 195, "sku_count": 13122, "employees": 5},
    {"store_id": 5, "open_year": 2022, "size_m2": 175, "sku_count": 7372,  "employees": 3},
    {"store_id": 6, "open_year": 2024, "size_m2": 230, "sku_count": 14983, "employees": 6},
    {"store_id": 7, "open_year": 2025, "size_m2": 320, "sku_count": 18374, "employees": 7},
]

# ======================================
# DATA KATEGORI (Exhibit 4)
# Kolom: kategori, sku, merek, penjualan_mingguan, promosi_mingguan
# ======================================
CATEGORIES = [
    ("Susu Bubuk",        86, 14, 567, 15),
    ("Biskuit",           37, 27, 362, 8),
    ("Sirup",             29, 11, 782, 7),
    ("Soda",              53, 7,  624, 9),
    ("Cokelat",           67, 21, 449, 6),
    ("Roti",              64, 15, 341, 9),
    ("Sereal",            107,11, 972, 20),
    ("Mie Instan",        186,8,  765, 25),
    ("Kopi Bubuk",        165,9,  378, 18),
    ("Sarden Kaleng",     86, 5,  246, 5),
    ("Jus Kemasan",       109,15, 289, 13),
    ("Buah Kering",       172,21, 480, 15),
    ("Beras",             134,19, 290, 7),
    ("Teh",               184,23, 580, 6),
    ("Pasta",             152,25, 732, 6),
    ("Mayones",           180,13, 665, 18),
    ("Kecap",             165,8,  238, 10),
    ("Penyedap Rasa",     79, 3,  138, 8),
    ("Saos",              194,20, 456, 20),
    ("Garam",             139,10, 304, 6),
    ("Gula",              168,13, 478, 16),
    ("Kaldu Jamur",       98, 11, 386, 14),
    ("Selai",             186,22, 467, 13),
    ("Permen",            179,18, 348, 5),
    ("Gulali",            65, 5,  276, 5),
    ("Makaroni",          162,8,  568, 15),
    ("Marshmallow",       132,10, 397, 9),
    ("Kuaci",             73, 3,  238, 8),
    ("Yogurt",            195,8,  369, 22),
    ("Keju",              168,12, 679, 13),
    ("Nugget",            175,13, 789, 15),
    ("Air Mineral",       195,8,  923, 20),
    ("Minuman Isotonik",  164,17, 685, 18),
    ("Keripik",           172,20, 876, 18),
    ("Susu Kemasan",      154,12, 687, 13),
    ("Kopi Kemasan",      189,11, 389, 15),
    ("Kacang",            165,10, 478, 17),
    ("Buah-Buahan",       179,13, 567, 8),
    ("Sayur-Sayuran",     196,11, 267, 11),
    ("Ice Cream",         174,16, 465, 6),
    ("Kornet",            136,9,  585, 9),
    ("Daging Segar",      184,8,  765, 21),
    ("Minyak Goreng",     179,13, 568, 8),
    ("Kentang Goreng",    163,7,  349, 13),
    ("Telur",             193,9,  465, 15),
    ("Seafood Segar",     136,18, 675, 20),
    ("Mentega",           120,15, 367, 6),
    ("Krim",              42, 10, 209, 8),
    ("Bihun",             113,13, 549, 7),
]

# =======================================================
# PARAMETER: HARGA, MARGIN, ELASTISITAS (berdasarkan harga rata-rata pasar Indonesia)
# =======================================================
def avg_price(category: str) -> int:
    mapping = {
        "Beras": 18000, "Gula": 13000, "Garam": 2500, "Minyak Goreng": 15000, "Bihun": 7000,
        "Air Mineral": 3000, "Soda": 7000, "Minuman Isotonik": 9000, "Jus Kemasan": 8000,
        "Teh": 8000, "Kopi Bubuk": 22000, "Kopi Kemasan": 12000,
        "Biskuit": 8000, "Keripik": 8000, "Permen": 2500, "Gulali": 1500, "Cokelat": 10000,
        "Kuaci": 4000, "Marshmallow": 5000, "Makaroni": 8000, "Roti": 5000, "Sereal": 25000,
        "Sirup": 15000, "Pasta": 12000, "Saos": 10000, "Kecap": 8000, "Penyedap Rasa": 6000,
        "Kaldu Jamur": 8000, "Mayones": 15000, "Selai": 18000, "Kacang": 10000,
        "Sarden Kaleng": 12000, "Kornet": 15000, "Buah Kering": 20000, "Mie Instan": 3000,
        "Susu Bubuk": 25000, "Susu Kemasan": 6000, "Yogurt": 8000, "Keju": 20000,
        "Mentega": 15000, "Krim": 15000, "Ice Cream": 15000,
        "Nugget": 35000, "Kentang Goreng": 25000,
        "Daging Segar": 35000, "Seafood Segar": 45000, "Sayur-Sayuran": 8000, 
        "Buah-Buahan": 12000, "Telur": 25000,
    }
    return mapping.get(category, 12000)

def realistic_margins(category: str) -> float:
    # Struktur margin
    margins = {
        "Beras": 0.08, "Gula": 0.10, "Garam": 0.12, "Minyak Goreng": 0.15,
        "Air Mineral": 0.18, "Mie Instan": 0.20,
        "Soda": 0.22, "Minuman Isotonik": 0.25, "Jus Kemasan": 0.24, 
        "Teh": 0.20, "Kopi Kemasan": 0.28, "Kopi Bubuk": 0.30,
        "Sirup": 0.32, "Pasta": 0.28, "Saos": 0.30, "Kecap": 0.25,
        "Mayones": 0.35, "Selai": 0.38, "Sarden Kaleng": 0.22,
        "Kornet": 0.25, "Penyedap Rasa": 0.35, "Kaldu Jamur": 0.32,
        "Biskuit": 0.35, "Keripik": 0.40, "Permen": 0.45, "Cokelat": 0.38,
        "Sereal": 0.32, "Gulali": 0.50, "Kuaci": 0.42, "Marshmallow": 0.40,
        "Makaroni": 0.30, "Roti": 0.30, "Kacang": 0.38,
        "Susu Bubuk": 0.28, "Susu Kemasan": 0.20, "Keju": 0.30,
        "Yogurt": 0.25, "Ice Cream": 0.35, "Mentega": 0.28, "Krim": 0.30,
        "Nugget": 0.28, "Kentang Goreng": 0.25,
        "Daging Segar": 0.25, "Seafood Segar": 0.30, 
        "Sayur-Sayuran": 0.35, "Buah-Buahan": 0.32,
        "Telur": 0.18,
        "Buah Kering": 0.42, "Bihun": 0.25
    }
    return margins.get(category, 0.25)

def realistic_elasticity(category: str, brands: int) -> float:
    # Kategori elastisitas berdasarkan perilaku kategori
    base_elasticity = {
        "Beras": 0.3, "Gula": 0.35, "Garam": 0.25, "Minyak Goreng": 0.4,
        "Mie Instan": 0.6, "Bihun": 0.5,
        "Air Mineral": 0.7, "Soda": 0.9, "Teh": 0.6, "Kopi Kemasan": 0.8,
        "Jus Kemasan": 1.0, "Minuman Isotonik": 1.1, "Kopi Bubuk": 0.8,
        "Biskuit": 1.2, "Keripik": 1.3, "Permen": 1.4, "Cokelat": 1.1,
        "Sereal": 0.9, "Gulali": 1.3, "Kuaci": 1.2, "Marshmallow": 1.1,
        "Makaroni": 1.0, "Roti": 0.8, "Kacang": 1.0,
        "Nugget": 0.8, "Ice Cream": 1.2, "Kentang Goreng": 0.9,
        "Susu Bubuk": 0.7, "Keju": 0.8, "Yogurt": 0.6, "Susu Kemasan": 0.5,
        "Mentega": 0.6, "Krim": 0.7,
        "Seafood Segar": 0.9, "Daging Segar": 0.7, "Sayur-Sayuran": 1.0,
        "Buah-Buahan": 0.9, "Telur": 0.4,
        "Sirup": 0.8, "Mayones": 0.6, "Saos": 0.7, "Kecap": 0.5,
        "Penyedap Rasa": 0.4, "Kaldu Jamur": 0.6, "Selai": 0.8,
        "Sarden Kaleng": 0.6, "Kornet": 0.7, "Buah Kering": 1.0,
    }
    base = base_elasticity.get(category, 0.8)
    if brands > 20:
        brand_multiplier = 1.15
    elif brands > 15:
        brand_multiplier = 1.10
    elif brands > 10:
        brand_multiplier = 1.05
    else:
        brand_multiplier = 1.0
    return min(base * brand_multiplier, 1.5)

def realistic_trade_support(category: str, discount: float) -> float:
    # Trade support  berdasarkan kategori dan perilaku pemasok
    high_support = {"Sereal", "Biskuit", "Cokelat", "Susu Bubuk", 
                   "Kopi Bubuk", "Minuman Isotonik", "Soda", "Ice Cream"}
    medium_support = {"Sirup", "Jus Kemasan", "Keripik", "Pasta", 
                     "Mayones", "Saos", "Selai", "Buah Kering", "Permen"}
    low_support = {"Nugget", "Seafood Segar", "Daging Segar", "Keju",
                  "Beras", "Gula", "Minyak Goreng", "Air Mineral"}
    if category in high_support:
        return 0.35 if discount >= 0.25 else 0.30
    elif category in medium_support:
        return 0.25 if discount >= 0.25 else 0.20
    elif category in low_support:
        return 0.15 if discount >= 0.25 else 0.10
    else:
        return 0.20

def trade_eligible(category: str, brands: int) -> bool:
    # Menentukan apakah sebuah kategori eligible untuk trade promotion
    return (brands >= 8) or (category in {
        "Soda", "Minuman Isotonik", "Jus Kemasan", "Keripik", "Biskuit", "Cokelat",
        "Sereal", "Susu Kemasan", "Yogurt", "Kopi Kemasan", "Kopi Bubuk", "Teh",
        "Ice Cream", "Buah Kering", "Selai", "Sirup"
    })

# =======================================================
# KALENDER PROMOSI TOKO BERDASARKAN KALENDAR INDONESIA
# =======================================================
@dataclass
class Event:
    name: str
    day: date
    boost: float
    focus: Tuple[str, ...]     

def build_event_calendar(year: int) -> List[Event]:
    ev = []
    for m in range(1, 13):
        ev.append(Event("Payday", date(year, m, 25), 1.15, ("All",)))
    for m in range(1, 13):
        d = min(m, 28)
        ev.append(Event(f"{m:02d}.{m:02d} Twin Date", date(year, m, d), 1.08, ("All",)))
    ev += [
        Event("New Year",          date(year, 1, 1),   1.18, ("All",)),
        Event("Chinese New Year",  date(year, 2, 1 if year==2025 else 10), 1.12, ("Cokelat","Ice Cream","Permen")),
        Event("Independence Day",  date(year, 8, 17),  1.15, ("All",)),
        Event("Singles Day 11.11", date(year, 11, 11), 1.25, ("All",)),
        Event("Christmas",         date(year, 12, 25), 1.20, ("All",)),
        Event("New Year's Eve",    date(year, 12, 31), 1.12, ("All",)),
    ]
    if year == 2025:
        start_r, end_r, lebaran = date(2025,3,1), date(2025,4,1), date(2025,4,2)
    elif year == 2026:
        start_r, end_r, lebaran = date(2026,4,1), date(2026,5,1), date(2026,5,2)
    else:
        start_r, end_r, lebaran = date(year,3,1), date(year,4,1), date(year,4,2)
    d = start_r
    while d <= end_r:
        ev.append(Event("Ramadan", d, 1.25, ("Sirup","Teh","Pasta","Biskuit")))
        d += timedelta(days=1)
    ev += [
        Event("Lebaran",   lebaran,                   1.3,  ("All",)),
        Event("Lebaran+1", lebaran+timedelta(days=1), 1.25, ("All",)),
        Event("Lebaran+2", lebaran+timedelta(days=2), 1.15, ("All",)),
    ]
    for m in [6, 7]:
        for dd in [5,12,19,26]:
            ev.append(Event("School Holiday Boost", date(year,m,dd), 1.08,
                            ("Ice Cream","Nugget","Keripik","Permen","Minuman Isotonik")))
    return ev

def event_boost_for_day(events: List[Event], day: date) -> Tuple[float, Tuple[str,...]]:
    boost = 1.0; focus=[]
    for e in events:
        if e.day == day:
            boost *= e.boost
            focus += list(e.focus)
    return boost, tuple(focus) if focus else tuple()

# =======================================================
# LOGIKA REKOMENDASI PROMOSI 
# =======================================================
@dataclass
class PromoOption:
    category: str
    promo_type: str           # "Trade" / "In-Store"
    discount: float           # 0.1 = 10%
    trade_support: float      # porsi diskon yang ditanggung pemasok (Trade)
    display_cost: int         # biaya display (Trade)
    expected_units: float
    base_units: float
    price: float
    margin: float
    base_profit: float
    promo_profit: float
    discount_cost_net: float  # biaya diskon setelah trade rebate
    invest_cost: float        # investasi (discount_net + display + overhead)
    incremental_profit: float
    roi: float

def store_scale(store: dict, all_stores: List[dict]) -> float:
    # Menghitung faktor skala toko berdasarkan ukuran, jumlah SKU, dan karyawan
    avg_size = sum(s["size_m2"] for s in all_stores) / len(all_stores)
    avg_sku  = sum(s["sku_count"] for s in all_stores) / len(all_stores)
    avg_emp  = sum(s["employees"] for s in all_stores) / len(all_stores)
    size_idx = (store["size_m2"] / avg_size) ** 0.3
    sku_idx  = (store["sku_count"] / avg_sku) ** 0.3
    emp_idx  = (store["employees"] / avg_emp) ** 0.2
    return size_idx * sku_idx * emp_idx

def cap(v, lo, hi):
    return max(lo, min(hi, v))

def compute_options_for_category(day: date, store: dict, cat_row, events, target_store:int) -> List[PromoOption]:
    category, sku, brands, wk_sales, wk_promos = cat_row
    price  = avg_price(category)
    margin = realistic_margins(category)
    elas   = realistic_elasticity(category, brands)
    base_daily_units = (wk_sales / 7.0) * store_scale(store, STORES)
    boost, focus = event_boost_for_day(events, day)
    elas_focus = 0.15 if (focus and (("All" in focus) or (category in focus))) else 0.0
    traffic_base = 1.02
    in_store_discounts = [0.10, 0.15, 0.20]
    trade_discounts    = [0.15, 0.20, 0.25] if trade_eligible(category, brands) else []
    options: List[PromoOption] = []
    OPERATIONAL_OVERHEAD = 50_000

    def eval_option(discount: float, promo_type: str, trade_support_ratio: float, display_cost: int):
        uplift = (elas + elas_focus) * discount * 0.85
        units  = cap(base_daily_units * (1.0 + uplift) * boost * traffic_base,
                     base_daily_units*0.95, base_daily_units*2.0)
        new_price = price * (1.0 - discount)
        base_profit  = base_daily_units * price * margin
        trade_support_amount = realistic_trade_support(category, discount) if promo_type == "Trade" else 0.0
        trade_rebate = units * price * (trade_support_amount * discount)
        promo_profit = (units * new_price * margin) + trade_rebate - display_cost
        incr = promo_profit - base_profit
        discount_cost_net = (units * price * discount) - trade_rebate
        invest_cost = max(1.0, discount_cost_net + display_cost + OPERATIONAL_OVERHEAD)
        roi = incr / invest_cost
        return PromoOption(category, promo_type, discount, trade_support_amount, display_cost,
                           units, base_daily_units, price, margin,
                           base_profit, promo_profit, discount_cost_net, invest_cost, incr, roi)

    for d in in_store_discounts:
        options.append(eval_option(d, "In-Store", 0.0, 0))
    for d in trade_discounts:
        sup  = realistic_trade_support(category, d)
        disp = 120_000 if d >= 0.25 else (100_000 if d >= 0.20 else 80_000)
        options.append(eval_option(d, "Trade", sup, disp))
    day_boost, _ = event_boost_for_day(events, day)
    min_roi = 0.08 if day_boost >= 1.2 else 0.12
    options = [o for o in options if o.incremental_profit > 0 and o.roi >= min_roi]
    options.sort(key=lambda x: (x.incremental_profit, x.roi), reverse=True)
    return options

def format_idr(x: float) -> str:
    return "Rp{:,.0f}".format(x).replace(",", ".")

# =======================================================
# PERHITUNGAN PEMILIHAN RENCANA HARIAN PROMOSI
# =======================================================
def pick_daily_plan(day: date, target_per_store: int):
    events = build_event_calendar(day.year)
    plan_rows: List[Dict] = []
    sum_rows: List[Dict]  = []
    chosen_by_store: Dict[int, List[PromoOption]] = {}

    for store in STORES:
        base_promos = 3 + store["employees"] * 1.5
        max_promos = min(12, int(base_promos))
        candidates: List[PromoOption] = []
        for cat in CATEGORIES:
            opts = compute_options_for_category(day, store, cat, events, target_per_store)
            if opts: candidates.append(opts[0])
        candidates.sort(key=lambda x: (x.incremental_profit, x.roi), reverse=True)
        def group_of(cat: str) -> str:
            if cat in {"Beras","Gula","Garam","Minyak Goreng","Bihun","Pasta","Mie Instan"}: return "Staples"
            if cat in {"Air Mineral","Soda","Minuman Isotonik","Jus Kemasan","Teh","Kopi Bubuk","Kopi Kemasan"}: return "Beverage"
            if cat in {"Biskuit","Keripik","Permen","Gulali","Cokelat","Kuaci","Marshmallow","Makaroni","Roti","Sereal","Kacang"}: return "Snack"
            if cat in {"Susu Bubuk","Susu Kemasan","Yogurt","Keju","Mentega","Krim","Ice Cream"}: return "DairyFrozen"
            if cat in {"Nugget","Kentang Goreng"}: return "FrozenMeal"
            if cat in {"Daging Segar","Seafood Segar","Sayur-Sayuran","Buah-Buahan","Buah Kering","Telur"}: return "Fresh"
            if cat in {"Sirup","Saos","Kecap","Penyedap Rasa","Kaldu Jamur","Mayones","Selai","Kornet","Sarden Kaleng"}: return "Condiment"
            return "Other"
        group_counter: Dict[str,int] = {}
        chosen: List[PromoOption] = []
        for opt in candidates:
            g = group_of(opt.category)
            if group_counter.get(g,0) >= 2: continue
            chosen.append(opt)
            group_counter[g] = group_counter.get(g,0)+1
            if len(chosen) >= max_promos: break
        current_profit = sum(o.incremental_profit for o in chosen)
        if current_profit < 0.7 * target_per_store:
            for opt in candidates[len(chosen):]:
                g = group_of(opt.category)
                if group_counter.get(g,0) >= 3: continue
                chosen.append(opt)
                group_counter[g]=group_counter.get(g,0)+1
                if len(chosen) >= min(15, max_promos+3) or sum(o.incremental_profit for o in chosen) >= target_per_store:
                    break
        chosen_by_store[store["store_id"]] = chosen
        for o in chosen:
            plan_rows.append({
                "date": day.isoformat(),
                "store_id": store["store_id"],
                "promo_type": o.promo_type,
                "category": o.category,
                "discount_pct": round(o.discount*100),
                "price_avg": int(o.price),
                "margin_pct": round(o.margin*100,1),
                "base_units": round(o.base_units,1),
                "expected_units": round(o.expected_units,1),
                "uplift_pct": round((o.expected_units/o.base_units - 1)*100, 1),
                "base_profit": int(round(o.base_profit)),
                "promo_profit": int(round(o.promo_profit)),
                "discount_cost_net": int(round(o.discount_cost_net)),
                "display_cost": o.display_cost,
                "overhead": 50_000,
                "invest_cost": int(round(o.invest_cost)),
                "incremental_profit": int(round(o.incremental_profit)),
                "roi": round(o.roi,3),
                "trade_support_of_disc": round(o.trade_support*100,1) if o.promo_type == "Trade" else 0.0,
            })
        sum_rows.append({
            "date": day.isoformat(),
            "store_id": store["store_id"],
            "max_promos_allowed": max_promos,
            "promos_scheduled": len(chosen),
            "incremental_profit_total": int(round(sum(o.incremental_profit for o in chosen))),
            "avg_roi": round(sum(o.roi for o in chosen)/len(chosen), 3) if chosen else 0.0
        })
    return plan_rows, sum_rows, chosen_by_store

def write_csv(filename: str, rows: List[Dict]):
    if not rows: return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)

# =======================================================
# OUTPUT
# =======================================================
def print_console_details(day: date, sum_rows: List[Dict], chosen_by_store: Dict[int, List[PromoOption]], topn: int):
    grand = sum(r["incremental_profit_total"] for r in sum_rows)
    print("\n" + "="*100)
    print(f"RINGKASAN PROFIT HARIAN {day.isoformat()} — SEMUA TOKO")
    for r in sum_rows:
        print(f" Toko {r['store_id']:>2} | Promos: {r['promos_scheduled']:>2}/{r['max_promos_allowed']:>2} | "
              f"Incremental: {format_idr(r['incremental_profit_total'])} | Avg ROI: {r['avg_roi']}")
    print("-"*100)
    print(f" TOTAL (7 toko) Incremental Profit: {format_idr(grand)}")
    print(f" Average per Store: {format_idr(grand/7)} | Target was: {format_idr(1_000_000)}")
    print("="*100)
    for store_id in sorted(chosen_by_store.keys()):
        chosen = sorted(chosen_by_store[store_id], key=lambda o: (o.incremental_profit, o.roi), reverse=True)
        print(f"\nToko {store_id} — TOP {min(topn, len(chosen))} Kampanye (urut profit):")
        header = ("Kategori".ljust(18) + "Tipe".ljust(10) + "Disc ".rjust(6) +
                  "  Harga→Promo".rjust(16) + "  Base→Exp Units".rjust(18) +
                  "  Uplift%".rjust(8) + "  Investasi".rjust(13) + "  IncrProfit".rjust(13) + "  ROI".rjust(7))
        print(header)
        print("-"*len(header))
        for o in chosen[:topn]:
            new_price = o.price * (1-o.discount)
            uplift_pct = (o.expected_units/o.base_units - 1) * 100
            print(
                f"{o.category[:18].ljust(18)}{o.promo_type[:10].ljust(10)}"
                f"{int(round(o.discount*100)):>3}%   "
                f"{format_idr(o.price)}→{format_idr(new_price):>9}   "
                f"{o.base_units:>6.1f}→{o.expected_units:>6.1f}   "
                f"{uplift_pct:>6.1f}%   "
                f"{format_idr(o.invest_cost):>11}   "
                f"{format_idr(o.incremental_profit):>11}   "
                f"{o.roi:>6.2f}"
            )
        tot_base = sum(o.base_profit for o in chosen)
        tot_promo = sum(o.promo_profit for o in chosen)
        tot_invest = sum(o.invest_cost for o in chosen)
        tot_incr = sum(o.incremental_profit for o in chosen)
        avg_roi = (tot_incr / tot_invest) if tot_invest > 0 else 0.0
        trade_count = sum(1 for o in chosen if o.promo_type == "Trade")
        instore_count = len(chosen) - trade_count
        print("  " + "-"*(len(header)-2))
        print(f"  Basis Profit: {format_idr(tot_base)} | Profit Saat Promo: {format_idr(tot_promo)}")
        print(f"  Total Investasi: {format_idr(tot_invest)} | Incremental Profit: {format_idr(tot_incr)} | AVG ROI: {avg_roi:.2f}")
        print(f"  Mix: {trade_count} Trade + {instore_count} In-Store | Target Achievement: {tot_incr/1_000_000:.1f}x")

# Analisis performa kategori
def print_category_performance_analysis(chosen_by_store: Dict[int, List[PromoOption]]):
    category_stats = {}
    for store_id, promos in chosen_by_store.items():
        for promo in promos:
            cat = promo.category
            if cat not in category_stats:
                category_stats[cat] = {
                    'count': 0,
                    'total_profit': 0,
                    'total_roi': 0,
                    'avg_uplift': 0,
                    'trade_vs_instore': {'Trade': 0, 'In-Store': 0}
                }
            stats = category_stats[cat]
            stats['count'] += 1
            stats['total_profit'] += promo.incremental_profit
            stats['total_roi'] += promo.roi
            stats['avg_uplift'] += (promo.expected_units/promo.base_units - 1) * 100
            stats['trade_vs_instore'][promo.promo_type] += 1
    for cat, stats in category_stats.items():
        if stats['count'] > 0:
            stats['avg_profit'] = stats['total_profit'] / stats['count']
            stats['avg_roi'] = stats['total_roi'] / stats['count']
            stats['avg_uplift'] = stats['avg_uplift'] / stats['count']
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['total_profit'], reverse=True)
    print("\n" + "="*100)
    print("ANALISIS PERFORMANCE KATEGORI")
    print("="*100)
    print("Kategori".ljust(18) + "Stores".rjust(7) + "Total Profit".rjust(15) + 
          "Avg Profit".rjust(12) + "Avg ROI".rjust(9) + "Avg Uplift%".rjust(12) + "Trade/In-Store".rjust(15))
    print("-"*100)
    for cat, stats in sorted_categories[:15]:
        trade_instore = f"{stats['trade_vs_instore']['Trade']}/{stats['trade_vs_instore']['In-Store']}"
        print(f"{cat[:17].ljust(18)}{stats['count']:>6} "
              f"{format_idr(stats['total_profit']):>13} "
              f"{format_idr(stats['avg_profit']):>10} "
              f"{stats['avg_roi']:>8.2f} "
              f"{stats['avg_uplift']:>10.1f}% "
              f"{trade_instore:>13}")

def print_optimization_summary(day: date, chosen_by_store: Dict[int, List[PromoOption]]):
    total_campaigns = sum(len(promos) for promos in chosen_by_store.values())
    total_profit = sum(sum(p.incremental_profit for p in promos) for promos in chosen_by_store.values())
    total_investment = sum(sum(p.invest_cost for p in promos) for promos in chosen_by_store.values())
    trade_campaigns = sum(sum(1 for p in promos if p.promo_type == "Trade") for promos in chosen_by_store.values())
    instore_campaigns = total_campaigns - trade_campaigns
    print("\n" + "="*100)
    print("RINGKASAN OPTIMASI & INSIGHTS")
    print("="*100)
    print(f"Total Kampanye: {total_campaigns} ({trade_campaigns} Trade + {instore_campaigns} In-Store)")
    print(f"Total Investment: {format_idr(total_investment)}")
    print(f"Total Incremental Profit: {format_idr(total_profit)}")
    print(f"Overall ROI: {total_profit/total_investment:.2f}")
    print(f"Average Profit per Campaign: {format_idr(total_profit/total_campaigns)}")
    print(f"Cost per Rupiah Earned: Rp {total_investment/total_profit:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Sistem Promosi Otomatis Supermarket Jack")
    parser.add_argument("--date", type=str, default=None, help="Tanggal rencana (YYYY-MM-DD). Contoh: 2025-11-11")
    parser.add_argument("--target", type=int, default=1_000_000, help="Target minimal profit harian per toko (IDR)")
    parser.add_argument("--topn", type=int, default=8, help="Cetak TOP-N kampanye per toko ke console")
    parser.add_argument("--no_details", action="store_true", help="Jika diset, tidak menampilkan detail console")
    parser.add_argument("--analytics", action="store_true", help="Tampilkan analisis kategori dan insights")
    args = parser.parse_args()
    if args.date:
        day = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        today = date.today()
        cands = []
        for k in range(0, 30):
            d = today + timedelta(days=k)
            boost, _ = event_boost_for_day(build_event_calendar(d.year), d)
            cands.append((boost, d))
        cands.sort(reverse=True, key=lambda x: x[0])
        day = cands[0][1]
    print("\n" + "="*60)
    print("#Sistem Promosi Otomatis untuk Supermarket Jack")
    print("="*60)
    print("Tanggal rencana:", day.isoformat())
    print("Target minimal incremental profit per toko:", f"{format_idr(args.target)}")
    events = build_event_calendar(day.year)
    boost, focus_cats = event_boost_for_day(events, day)
    if boost > 1.0:
        active_events = [e.name for e in events if e.day == day]
        print(f"Event boost: {boost:.2f}x - {', '.join(active_events)}")
        if focus_cats and "All" not in focus_cats:
            print(f"Focus categories: {', '.join(focus_cats)}")
    plan_rows, sum_rows, chosen_by_store = pick_daily_plan(day, args.target)
    write_csv("promotion_plan_optimized.csv", plan_rows)
    write_csv("promotion_summary_optimized.csv", sum_rows)
    if not args.no_details:
        print_console_details(day, sum_rows, chosen_by_store, args.topn)
        if args.analytics:
            print_category_performance_analysis(chosen_by_store)
            print_optimization_summary(day, chosen_by_store)
    else:
        total = sum(r["incremental_profit_total"] for r in sum_rows)
        print(f"\nTotal profit incremental (7 toko): {format_idr(total)}")
        print("File yang dibuat: promotion_plan_optimized.csv & promotion_summary_optimized.csv")

if __name__ == "__main__":
    main()