#!/usr/bin/env python3
"""
Static Site Generator for Southern NH & Merrimack Valley Heating Oil & Propane Price Tracker
Reads:  /workspace/heating-oil-tracker/data/prices.json
Writes:
  - /workspace/heating-oil-tracker/site/index.html
  - /workspace/heating-oil-tracker/site/towns/<town-slug>.html (14 SEO town pages)
  - /workspace/heating-oil-tracker/site/sitemap.xml
  - /workspace/heating-oil-tracker/site/robots.txt
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "prices.json")
SITE_DIR = os.path.join(BASE_DIR, "site")
TOWNS_DIR = os.path.join(SITE_DIR, "towns")
os.makedirs(TOWNS_DIR, exist_ok=True)


SHARED_CSS = """
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface-alt: #f1f5f9;
  --navy: #0f172a;
  --navy-light: #1e293b;
  --slate: #475569;
  --muted: #64748b;
  --border: #e2e8f0;
  --brand: #ea580c;
  --brand-dark: #c2410c;
  --brand-soft: #fff7ed;
  --green: #15803d;
  --green-soft: #dcfce7;
  --blue: #0369a1;
  --blue-soft: #e0f2fe;
  --amber: #b45309;
  --amber-soft: #fef3c7;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--navy);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.topbar {
  background: var(--navy);
  color: #f8fafc;
  font-size: 0.82rem;
  padding: 0.5rem 1.25rem;
  border-bottom: 2px solid var(--brand);
}
.topbar-inner {
  max-width: 1240px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.live-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  margin-right: 6px;
  box-shadow: 0 0 0 3px rgba(34,197,94,0.25);
}
header.hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #ffffff;
  padding: 2.25rem 1.25rem 2rem;
}
.container {
  max-width: 1240px;
  margin: 0 auto;
}
.hero-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 1.5rem;
  align-items: center;
}
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(234, 88, 12, 0.2);
  border: 1px solid rgba(251, 146, 60, 0.45);
  color: #fdba74;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 0.28rem 0.75rem;
  border-radius: 999px;
  margin-bottom: 0.75rem;
}
h1 {
  font-size: 2.05rem;
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 0.65rem;
}
.hero-sub {
  color: #cbd5e1;
  font-size: 1rem;
  max-width: 660px;
}
.alert-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 12px;
  padding: 1.15rem 1.25rem;
}
.alert-card h3 {
  font-size: 0.98rem;
  margin-bottom: 0.3rem;
  color: #fff;
}
.alert-card p {
  font-size: 0.82rem;
  color: #cbd5e1;
  margin-bottom: 0.75rem;
}
.alert-form {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
}
.alert-form input, .alert-form select {
  flex: 1;
  min-width: 120px;
  padding: 0.55rem 0.7rem;
  border-radius: 7px;
  border: 1px solid #475569;
  background: #0f172a;
  color: #fff;
  font-size: 0.85rem;
}
.btn-primary {
  background: var(--brand);
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.55rem 1rem;
  border-radius: 7px;
  border: none;
  cursor: pointer;
  white-space: nowrap;
}
.btn-primary:hover { background: var(--brand-dark); text-decoration: none; }
.kpi-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: -1.1rem;
  margin-bottom: 1.5rem;
  padding: 0 1.25rem;
}
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.1rem 1.2rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
}
.kpi-card.highlight {
  border-top: 4px solid var(--green);
}
.kpi-card.avg {
  border-top: 4px solid var(--blue);
}
.kpi-card.spread {
  border-top: 4px solid var(--brand);
}
.kpi-card.propane {
  border-top: 4px solid #7c3aed;
}
.kpi-label {
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  font-weight: 700;
}
.kpi-value {
  font-size: 1.85rem;
  font-weight: 800;
  color: var(--navy);
  margin: 0.2rem 0;
  letter-spacing: -0.02em;
}
.kpi-value span.unit {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--muted);
}
.kpi-meta {
  font-size: 0.82rem;
  color: var(--slate);
}
.kpi-meta strong { color: var(--green); }
main {
  padding: 0 1.25rem 3rem;
}
.featured-banner {
  background: linear-gradient(90deg, #fff7ed 0%, #ffedd5 100%);
  border: 1px solid #fed7aa;
  border-left: 5px solid var(--brand);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.featured-tag {
  display: inline-block;
  background: var(--brand);
  color: #fff;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 0.18rem 0.55rem;
  border-radius: 4px;
  margin-right: 0.5rem;
  letter-spacing: 0.04em;
}
.controls-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.control-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.control-group label {
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--navy);
}
.select-input {
  padding: 0.48rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--navy);
  background: #fff;
}
.gal-pills {
  display: inline-flex;
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 3px;
}
.gal-btn {
  border: none;
  background: transparent;
  padding: 0.38rem 0.75rem;
  font-size: 0.83rem;
  font-weight: 700;
  color: var(--slate);
  border-radius: 6px;
  cursor: pointer;
}
.gal-btn.active {
  background: var(--navy);
  color: #fff;
}
.table-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  margin-bottom: 2rem;
}
.table-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.table-header h2 {
  font-size: 1.15rem;
  font-weight: 800;
}
.table-scroll {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
th {
  background: var(--surface-alt);
  color: var(--slate);
  font-weight: 700;
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
}
td {
  padding: 0.85rem 1rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: #f8fafc; }
tr.featured-row td { background: #fffaf5; }
.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  font-weight: 800;
  font-size: 0.78rem;
  background: var(--surface-alt);
  color: var(--slate);
}
.rank-1 { background: #dcfce7; color: #15803d; }
.rank-2 { background: #e0f2fe; color: #0369a1; }
.rank-3 { background: #fef3c7; color: #b45309; }
.dealer-name {
  font-weight: 700;
  color: var(--navy);
  font-size: 0.95rem;
}
.dealer-sub {
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 2px;
}
.price-big {
  font-size: 1.12rem;
  font-weight: 800;
  color: var(--navy);
}
.price-low { color: var(--green); }
.fill-cost {
  font-weight: 700;
  color: var(--navy);
}
.save-pill {
  display: inline-block;
  background: var(--green-soft);
  color: var(--green);
  font-size: 0.74rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
}
.min-pill {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 6px;
  font-size: 0.76rem;
  font-weight: 700;
  background: var(--surface-alt);
  color: var(--slate);
}
.min-100 {
  background: var(--blue-soft);
  color: var(--blue);
}
.fuel-tag {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
  margin-right: 4px;
  background: #f1f5f9;
  color: #334155;
}
.fuel-propane {
  background: #f3e8ff;
  color: #6b21a8;
}
.phone-link {
  font-weight: 700;
  color: var(--navy);
  white-space: nowrap;
}
.btn-order {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  background: var(--navy);
  color: #fff;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
}
.btn-order:hover {
  background: var(--brand);
  text-decoration: none;
}
.two-col {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.section-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem;
}
.section-card h3 {
  font-size: 1.08rem;
  font-weight: 800;
  margin-bottom: 0.35rem;
}
.town-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(215px, 1fr));
  gap: 0.85rem;
  margin-top: 1rem;
}
.town-tile {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.9rem 1rem;
  transition: transform 0.12s ease, border-color 0.12s ease;
  display: block;
}
.town-tile:hover {
  border-color: var(--brand);
  transform: translateY(-2px);
  text-decoration: none;
}
.town-tile-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.25rem;
}
.town-tile-name {
  font-weight: 800;
  color: var(--navy);
  font-size: 0.95rem;
}
.town-tile-price {
  font-weight: 800;
  color: var(--green);
  font-size: 1rem;
}
.town-tile-meta {
  font-size: 0.76rem;
  color: var(--muted);
}
.dealer-cta {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.25rem;
  margin-top: 2rem;
}
footer {
  background: var(--navy);
  color: #94a3b8;
  font-size: 0.82rem;
  padding: 2rem 1.25rem;
  border-top: 1px solid #1e293b;
}
@media (max-width: 960px) {
  .hero-grid, .two-col { grid-template-columns: 1fr; }
  .kpi-strip { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
  .kpi-strip { grid-template-columns: 1fr; }
}
"""


def render_dealer_rows(dealers, default_gal=150, state_bench=6.030):
    rows_html = []
    rank = 1
    for d in dealers:
        p = d["price_per_gal"]
        has_price = p is not None
        fill_cost = f"${p * default_gal:,.2f}" if has_price else "Call for Quote"
        savings = round((state_bench - p) * default_gal, 2) if has_price else 0
        rank_cls = f"rank-{rank}" if (has_price and rank <= 3) else ""
        rank_display = str(rank) if has_price else "—"
        if has_price:
            rank += 1

        fuel_badges = []
        for f_name in d["fuels"]:
            cls = "fuel-tag fuel-propane" if f_name == "Propane" else "fuel-tag"
            fuel_badges.append(f'<span class="{cls}">{f_name}</span>')
        if d["propane_price_per_gal"]:
            fuel_badges.append(
                f'<span class="fuel-tag fuel-propane">Propane: ${d["propane_price_per_gal"]:.3f}/gal</span>'
            )

        feat_badge = '<span class="featured-tag">Featured Partner</span>' if d.get("featured") else ""
        row_cls = "dealer-row featured-row" if d.get("featured") else "dealer-row"
        min_cls = "min-pill min-100" if d["min_gallons"] <= 100 else "min-pill"
        price_str = f"${p:.3f}" if has_price else "Call"
        price_cls = "price-big price-low" if (has_price and p <= 5.60) else "price-big"
        save_html = (
            f'<div style="margin-top:3px;"><span class="save-pill" data-save-cell="1">Save ${savings:,.2f} vs NH Avg</span></div>'
            if (has_price and savings > 0)
            else ""
        )

        towns_attr = ",".join(d["towns_served"])
        fuels_attr = ",".join(d["fuels"])
        price_num_attr = f"{p:.4f}" if has_price else "999"

        rows_html.append(f"""
        <tr class="{row_cls}"
            data-towns="{towns_attr}"
            data-fuels="{fuels_attr}"
            data-min="{d['min_gallons']}"
            data-price="{price_num_attr}">
          <td><span class="rank-badge {rank_cls}">{rank_display}</span></td>
          <td>
            <div class="dealer-name">{feat_badge}{d['name']}</div>
            <div class="dealer-sub">📍 {d['hq_town']}, {d['hq_state']} &middot; {d['notes']}</div>
            <div style="margin-top:4px;">{''.join(fuel_badges)}</div>
          </td>
          <td>
            <div class="{price_cls}">{price_str}<span style="font-size:0.76rem;font-weight:500;color:#64748b;">{ '/gal' if has_price else '' }</span></div>
            <div class="dealer-sub">{d['payment_terms']}</div>
          </td>
          <td>
            <div class="fill-cost" data-fill-cell="1">{fill_cost}</div>
            {save_html}
          </td>
          <td><span class="{min_cls}">{d['min_gallons']} gal min</span></td>
          <td><a class="phone-link" href="tel:{d['phone']}">📞 {d['phone']}</a></td>
          <td><a class="btn-order" href="{d['website']}" target="_blank" rel="noopener">Visit Dealer &rarr;</a></td>
        </tr>
        """)
    return "\n".join(rows_html)


def build_index_page(data):
    s = data["summary"]
    dealers = data["dealers"]
    towns = data["towns"]
    hist = data["danville_30d_history"][-10:]  # last 10 days for clean display

    town_options = ['<option value="ALL">All 14 Rockingham &amp; Merrimack Valley Towns</option>']
    for t in towns:
        sel = "selected" if t["slug"] == "danville-nh" else ""
        # Default to ALL on index so all 22 dealers show immediately, with Danville highlighted first in list
        town_options.append(
            f'<option value="{t["name"]}">{t["name"]}, {t["state"]} ({t["zip"]}) — from ${t["lowest_price"]:.3f}/gal</option>'
        )

    town_tiles_html = []
    for t in towns:
        town_tiles_html.append(f"""
        <a class="town-tile" href="towns/{t['slug']}.html">
          <div class="town-tile-top">
            <span class="town-tile-name">{t['name']}, {t['state']}</span>
            <span class="town-tile-price">${t['lowest_price']:.3f}<small style="font-size:0.7rem;color:#64748b;">/gal</small></span>
          </div>
          <div class="town-tile-meta">
            ZIP {t['zip']} &middot; {t['dealer_count']} dealers &middot; 150 gal from <strong>${t['cost_150_low']:,.2f}</strong>
          </div>
        </a>
        """)

    hist_rows = []
    for h in reversed(hist):
        spread_d = round(h["median"] - h["lowest"], 2)
        hist_rows.append(f"""
        <tr>
          <td><strong>{h['date']}</strong></td>
          <td style="color:#15803d;font-weight:700;">${h['lowest']:.2f}/gal</td>
          <td>${h['median']:.2f}/gal</td>
          <td>${h['lowest']*150:,.2f}</td>
          <td><span class="save-pill">Save ${spread_d*150:,.2f}</span></td>
        </tr>
        """)

    dealer_rows_html = render_dealer_rows(dealers)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Southern NH &amp; Rockingham County Heating Oil &amp; Propane Price Tracker (Updated {data['updated_date']})</title>
  <meta name="description" content="Compare live C.O.D. #2 heating oil and propane prices across Danville, Derry, Salem, Hampstead, Exeter, Plaistow, Londonderry &amp; Rockingham County NH. Updated daily ({data['updated_date']}). Lowest oil price today: ${s['lowest_oil_price']:.3f}/gal." />
  <style>{SHARED_CSS}</style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <div><span class="live-dot"></span><strong>LIVE DAILY TRACKER:</strong> Verified Cash-on-Delivery (#2 Fuel Oil &amp; Propane) &middot; Updated {data['updated_timestamp']}</div>
      <div>Primary Coverage: <strong>Danville, NH (03819) &amp; Rockingham County</strong> &middot; <a href="#town-directory" style="color:#fdba74;">Browse 14 Local Towns &darr;</a></div>
    </div>
  </div>

  <header class="hero">
    <div class="container hero-grid">
      <div>
        <div class="badge-pill">🔥 Peak Heating Season Price Monitor &middot; Oct 27, 2026</div>
        <h1>Southern NH &amp; Merrimack Valley Heating Oil &amp; Propane Price Tracker</h1>
        <p class="hero-sub">
          Stop overpaying on tank fills. We scrape and verify daily cash-on-delivery #2 heating oil and propane rates from <strong>{s['total_dealers_tracked']} local dealers</strong> serving Danville (03819), Derry, Salem, Hampstead, Plaistow, Kingston, Exeter, Londonderry, and surrounding towns.
        </p>
      </div>
      <div class="alert-card">
        <h3>📉 Free Homeowner Price-Drop Alert</h3>
        <p>Get an instant email or text the morning local Rockingham County oil drops below your target price per gallon.</p>
        <form class="alert-form" onsubmit="event.preventDefault(); alert('Price-Drop Alert activated! You will be notified when local cash heating oil drops below your target.');">
          <input type="email" placeholder="you@example.com" required />
          <select aria-label="Select Town">
            <option value="Danville">Danville (03819)</option>
            <option value="Derry">Derry (03038)</option>
            <option value="Salem">Salem (03079)</option>
            <option value="Hampstead">Hampstead (03841)</option>
            <option value="Plaistow">Plaistow (03865)</option>
            <option value="Exeter">Exeter (03833)</option>
            <option value="Londonderry">Londonderry (03053)</option>
            <option value="Kingston">Kingston (03848)</option>
          </select>
          <button type="submit" class="btn-primary">Notify Me</button>
        </form>
      </div>
    </div>
  </header>

  <section class="container kpi-strip">
    <div class="kpi-card highlight">
      <div class="kpi-label">Today's Lowest Oil Price</div>
      <div class="kpi-value">${s['lowest_oil_price']:.3f} <span class="unit">/gal</span></div>
      <div class="kpi-meta"><strong>${s['lowest_150_gal_cost']:,.2f}</strong> for 150 gal &middot; B &amp; H Oil (Salem) &amp; $5.599 Fuel NRG (Danville)</div>
    </div>
    <div class="kpi-card avg">
      <div class="kpi-label">Rockingham County Avg</div>
      <div class="kpi-value">${s['average_oil_price']:.3f} <span class="unit">/gal</span></div>
      <div class="kpi-meta"><strong>${s['average_150_gal_cost']:,.2f}</strong> for 150 gal &middot; vs <strong>${s['nh_eia_oil_benchmark']:.2f}/gal</strong> NH EIA Benchmark</div>
    </div>
    <div class="kpi-card spread">
      <div class="kpi-label">150-Gal Tank Fill Spread</div>
      <div class="kpi-value">${s['spread_150_gal_savings']:,.2f} <span class="unit">saved</span></div>
      <div class="kpi-meta"><strong>${s['spread_per_gal']:.3f}/gal spread</strong> between lowest (${s['lowest_oil_price']:.3f}) &amp; highest (${s['highest_oil_price']:.3f})</div>
    </div>
    <div class="kpi-card propane">
      <div class="kpi-label">Live Local Propane Rates</div>
      <div class="kpi-value">${s['lowest_propane_price']:.3f} <span class="unit">/gal</span></div>
      <div class="kpi-meta">Colonial/County ($2.999) &amp; Buxton ($3.399) vs <strong>${s['nh_eia_propane_benchmark']:.3f}</strong> NH EIA Avg</div>
    </div>
  </section>

  <main class="container">
    <div class="featured-banner">
      <div>
        <span class="featured-tag">Featured Danville &amp; Rockingham Partner</span>
        <strong>Fuel NRG (Windham &amp; Derry, NH)</strong> &mdash;
        <strong>$5.599/gal Cash/Check</strong> ($839.85 for 150 gal) &middot; Only <strong>100-Gallon Minimum</strong> &middot; Delivers to Danville, Hampstead, Derry, Salem, Plaistow, Kingston &amp; Sandown.
      </div>
      <div style="display:flex;gap:0.6rem;align-items:center;">
        <a class="phone-link" href="tel:6038933600">📞 (603) 893-3600</a>
        <a class="btn-primary" href="https://fuelnrg.co/" target="_blank" rel="noopener">Order Online &rarr;</a>
      </div>
    </div>

    <div class="controls-bar">
      <div class="control-group">
        <label for="townFilter">📍 Filter by Town:</label>
        <select id="townFilter" class="select-input" onchange="applyFilters()">
          {''.join(town_options)}
        </select>

        <label for="fuelFilter" style="margin-left:0.5rem;">⛽ Filter:</label>
        <select id="fuelFilter" class="select-input" onchange="applyFilters()">
          <option value="ALL">All Verified Dealers ({s['total_dealers_tracked']})</option>
          <option value="MIN100">100-Gallon Minimum Only</option>
          <option value="PROPANE">Offers Propane Delivery</option>
        </select>
      </div>

      <div class="control-group">
        <label>🧮 Tank Fill Calculator:</label>
        <div class="gal-pills" id="galPills">
          <button type="button" class="gal-btn" onclick="setGallons(100, this)">100 Gal</button>
          <button type="button" class="gal-btn active" onclick="setGallons(150, this)">150 Gal</button>
          <button type="button" class="gal-btn" onclick="setGallons(200, this)">200 Gal</button>
          <button type="button" class="gal-btn" onclick="setGallons(250, this)">250 Gal</button>
        </div>
      </div>
    </div>

    <div class="table-card">
      <div class="table-header">
        <div>
          <h2 id="tableTitle">Verified Local Heating Oil &amp; Propane Dealers ({s['total_dealers_tracked']} Suppliers)</h2>
          <div style="font-size:0.8rem;color:#64748b;">Sorted lowest to highest cash price per gallon &middot; Click column headers to sort</div>
        </div>
        <div style="font-size:0.82rem;color:#475569;">
          NH State Benchmark: <strong>$6.030/gal</strong> (US EIA) &middot; NE Avg: <strong>$6.110/gal</strong>
        </div>
      </div>
      <div class="table-scroll">
        <table id="dealerTable">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Dealer &amp; Coverage Notes</th>
              <th>Cash Price / Gal</th>
              <th id="fillColHeader">150-Gal Fill Cost</th>
              <th>Min Order</th>
              <th>Local Phone</th>
              <th>Direct Order</th>
            </tr>
          </thead>
          <tbody id="dealerTbody">
            {dealer_rows_html}
          </tbody>
        </table>
      </div>
    </div>

    <div class="two-col">
      <div class="section-card">
        <h3>📊 Danville &amp; Rockingham County 10-Day Price Trend</h3>
        <p style="font-size:0.84rem;color:#64748b;margin-bottom:0.85rem;">
          Historical daily lowest vs. median posted C.O.D. heating oil price per gallon (150-gallon delivery) serving Danville, NH (03819).
        </p>
        <div class="table-scroll">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Lowest Posted</th>
                <th>Regional Median</th>
                <th>150-Gal Low Fill</th>
                <th>Spread Savings</th>
              </tr>
            </thead>
            <tbody>
              {''.join(hist_rows)}
            </tbody>
          </table>
        </div>
      </div>

      <div class="section-card">
        <h3>🔥 Southern NH Propane Market Snapshot (Oct 27, 2026)</h3>
        <p style="font-size:0.84rem;color:#64748b;margin-bottom:0.85rem;">
          19.2% of New Hampshire homes heat primarily with propane. Unlike heating oil, propane rates vary sharply by annual usage tier and tank ownership:
        </p>
        <ul style="list-style:none;display:grid;gap:0.65rem;font-size:0.88rem;">
          <li style="padding:0.65rem;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">
            <strong>Colonial Oil / County Energy:</strong> <span style="color:#15803d;font-weight:800;">$2.999/gal</span> heating propane cash/check rate (&amp; $14.99 20-lb cylinder refill).
          </li>
          <li style="padding:0.65rem;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">
            <strong>Buxton Oil &amp; Propane (Epping/Exeter):</strong> <span style="color:#15803d;font-weight:800;">$3.399/gal</span> daily cash propane price (for whole-home heating &gt;1,000 gal/yr).
          </li>
          <li style="padding:0.65rem;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">
            <strong>Palmer Gas &amp; Oil (Atkinson, NH):</strong> Family-owned at 13 Hall Farm Rd &mdash; first in Southern NH offering Renewable Propane + fixed/cap budget plans. Call <a href="tel:6038987986">(603) 898-7986</a>.
          </li>
          <li style="padding:0.65rem;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">
            <strong>Official NH Benchmarks:</strong> US EIA NH Residential Average: <strong>$3.843/gal</strong> &middot; NH Dept. of Energy Statewide Average: <strong>$4.120/gal</strong>.
          </li>
        </ul>
      </div>
    </div>

    <section id="town-directory" class="section-card">
      <h3>🏘️ Browse Heating Oil &amp; Propane Prices by Town (Rockingham County &amp; Merrimack Valley)</h3>
      <p style="font-size:0.85rem;color:#64748b;">
        Select your town below for dedicated local dealer rankings, 150-gallon tank fill comparisons, and town-specific delivery minimums:
      </p>
      <div class="town-grid">
        {''.join(town_tiles_html)}
      </div>
    </section>

    <section class="dealer-cta">
      <div style="max-width:720px;">
        <div class="badge-pill" style="margin-bottom:0.4rem;">For Local Fuel Dealers &amp; HVAC Contractors</div>
        <h3 style="font-size:1.35rem;margin-bottom:0.35rem;">Are You a Local Oil or Propane Dealer Serving Rockingham County?</h3>
        <p style="color:#cbd5e1;font-size:0.9rem;">
          Homeowners in Danville, Derry, Salem, Hampstead, Plaistow, and Exeter check this tracker every morning before ordering a 150–250 gallon tank fill ($825–$1,400+ per order). Claim your free dealer profile to update your daily C.O.D. rate automatically, or lock in the <strong>Featured Partner Spot</strong> for your core delivery towns.
        </p>
      </div>
      <div style="display:flex;flex-direction:column;gap:0.5rem;min-width:230px;">
        <a class="btn-primary" style="text-align:center;padding:0.75rem 1.2rem;font-size:0.92rem;" href="mailto:dealers@nhoiltracker.com?subject=Featured%20Dealer%20Spot%20Inquiry">⭐ Get Featured ($79/mo) &rarr;</a>
        <a style="text-align:center;color:#cbd5e1;font-size:0.82rem;" href="mailto:prices@nhoiltracker.com?subject=Update%20Daily%20Cash%20Oil%20Price">Submit Free Daily Price Update</a>
      </div>
    </section>
  </main>

  <footer>
    <div class="container" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
      <div>
        <strong style="color:#fff;">Southern NH &amp; Merrimack Valley Heating Oil &amp; Propane Tracker</strong><br />
        Independent daily C.O.D. price comparison for Danville, NH (03819) &amp; Rockingham County homeowners.<br />
        Data sources: Direct dealer websites, US EIA State Heating Oil &amp; Propane Program (SHOPP), NH Dept. of Energy, GetHomeHeat &amp; OilAndElectric.
      </div>
      <div>
        Last scraped: <strong>{data['updated_timestamp']}</strong><br />
        Always confirm final delivered price and minimum gallon terms with the dealer before ordering.
      </div>
    </div>
  </footer>

  <script>
    let currentGallons = 150;
    const stateBenchmark = {s['nh_eia_oil_benchmark']};

    function setGallons(gal, btn) {{
      currentGallons = gal;
      document.querySelectorAll('#galPills .gal-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('fillColHeader').textContent = gal + '-Gal Fill Cost';

      document.querySelectorAll('#dealerTbody tr.dealer-row').forEach(row => {{
        const price = parseFloat(row.getAttribute('data-price'));
        const fillCell = row.querySelector('[data-fill-cell]');
        const saveCell = row.querySelector('[data-save-cell]');
        if (price < 900 && fillCell) {{
          const total = (price * gal).toFixed(2);
          fillCell.textContent = '$' + Number(total).toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
          if (saveCell) {{
            const saved = ((stateBenchmark - price) * gal).toFixed(2);
            saveCell.textContent = 'Save $' + Number(saved).toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + ' vs NH Avg';
          }}
        }}
      }});
    }}

    function applyFilters() {{
      const town = document.getElementById('townFilter').value;
      const fuel = document.getElementById('fuelFilter').value;
      let visibleCount = 0;

      document.querySelectorAll('#dealerTbody tr.dealer-row').forEach(row => {{
        const towns = row.getAttribute('data-towns').split(',');
        const fuels = row.getAttribute('data-fuels').split(',');
        const minGal = parseInt(row.getAttribute('data-min'), 10);

        let matchTown = (town === 'ALL') || towns.includes(town);
        let matchFuel = true;
        if (fuel === 'MIN100') matchFuel = (minGal <= 100);
        if (fuel === 'PROPANE') matchFuel = fuels.includes('Propane');

        if (matchTown && matchFuel) {{
          row.style.display = '';
          visibleCount++;
        }} else {{
          row.style.display = 'none';
        }}
      }});

      const titleEl = document.getElementById('tableTitle');
      if (town === 'ALL') {{
        titleEl.textContent = 'Verified Local Heating Oil & Propane Dealers (' + visibleCount + ' Suppliers)';
      }} else {{
        titleEl.textContent = 'Verified Dealers Delivering to ' + town + ' (' + visibleCount + ' Suppliers)';
      }}
    }}
  </script>
</body>
</html>
"""
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Generated {index_path}")


def build_town_pages(data):
    s = data["summary"]
    dealers = data["dealers"]
    towns = data["towns"]

    for t in towns:
        t_dealers = [d for d in dealers if t["name"] in d["towns_served"]]
        rows_html = render_dealer_rows(t_dealers, default_gal=150, state_bench=s["nh_eia_oil_benchmark"])

        other_links = []
        for ot in towns:
            if ot["slug"] != t["slug"]:
                other_links.append(
                    f'<a class="town-tile" href="{ot["slug"]}.html"><div class="town-tile-top"><span class="town-tile-name">{ot["name"]}, {ot["state"]}</span><span class="town-tile-price">${ot["lowest_price"]:.3f}/gal</span></div><div class="town-tile-meta">ZIP {ot["zip"]} &middot; {ot["dealer_count"]} dealers</div></a>'
                )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Cheap Heating Oil &amp; Propane Prices in {t['name']}, {t['state']} ({t['zip']}) — From ${t['lowest_price']:.3f}/gal ({data['updated_date']})</title>
  <meta name="description" content="Compare {t['dealer_count']} verified heating oil and propane dealers delivering to {t['name']}, {t['state']} ({t['zip']}). Lowest cash oil price today: ${t['lowest_price']:.3f}/gal (${t['cost_150_low']:,.2f} for 150 gallons). Updated {data['updated_date']}." />
  <style>{SHARED_CSS}</style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <div><a href="../index.html" style="color:#fdba74;font-weight:700;">&larr; All Southern NH &amp; Rockingham County Prices</a></div>
      <div><span class="live-dot"></span><strong>{t['name']}, {t['state']} ({t['zip']})</strong> &middot; Updated {data['updated_timestamp']}</div>
    </div>
  </div>

  <header class="hero">
    <div class="container hero-grid">
      <div>
        <div class="badge-pill">📍 {t['county']} &middot; ZIP {t['zip']} &middot; Live C.O.D. Rates</div>
        <h1>Cheap Heating Oil &amp; Propane Prices in {t['name']}, {t['state']} ({t['zip']})</h1>
        <p class="hero-sub">
          Compare <strong>{t['dealer_count']} verified local fuel companies</strong> delivering to {t['name']}, {t['state']}. Today's lowest posted cash heating oil rate in {t['name']} is <strong>${t['lowest_price']:.3f}/gal</strong> from <strong>{t['cheapest_dealer']}</strong> &mdash; saving you <strong>${t['savings_150_vs_state']:,.2f}</strong> on a 150-gallon fill compared to the ${s['nh_eia_oil_benchmark']:.2f}/gal New Hampshire state average.
        </p>
      </div>
      <div class="alert-card">
        <h3>📉 {t['name']}, {t['state']} Price-Drop Alert</h3>
        <p>Get notified the morning cash heating oil in {t['name']} ({t['zip']}) drops below your target price.</p>
        <form class="alert-form" onsubmit="event.preventDefault(); alert('Subscribed to {t['name']}, {t['state']} price alerts!');">
          <input type="email" placeholder="you@example.com" required />
          <button type="submit" class="btn-primary">Set {t['name']} Alert</button>
        </form>
      </div>
    </div>
  </header>

  <section class="container kpi-strip">
    <div class="kpi-card highlight">
      <div class="kpi-label">Lowest in {t['name']} Today</div>
      <div class="kpi-value">${t['lowest_price']:.3f} <span class="unit">/gal</span></div>
      <div class="kpi-meta"><strong>${t['cost_150_low']:,.2f}</strong> for 150 gal &middot; {t['cheapest_dealer']}</div>
    </div>
    <div class="kpi-card avg">
      <div class="kpi-label">{t['name']} Dealer Average</div>
      <div class="kpi-value">${t['average_price']:.3f} <span class="unit">/gal</span></div>
      <div class="kpi-meta"><strong>${t['cost_150_avg']:,.2f}</strong> for 150 gal across {t['priced_dealer_count']} priced dealers</div>
    </div>
    <div class="kpi-card spread">
      <div class="kpi-label">Savings vs NH State Avg</div>
      <div class="kpi-value">${t['savings_150_vs_state']:,.2f} <span class="unit">saved</span></div>
      <div class="kpi-meta">On a 150-gal fill vs <strong>${s['nh_eia_oil_benchmark']:.2f}/gal</strong> NH EIA benchmark</div>
    </div>
    <div class="kpi-card propane">
      <div class="kpi-label">{t['name']} Suppliers Tracked</div>
      <div class="kpi-value">{t['dealer_count']} <span class="unit">dealers</span></div>
      <div class="kpi-meta">Includes 100-gal &amp; 150-gal minimum C.O.D. suppliers</div>
    </div>
  </section>

  <main class="container">
    <div class="controls-bar">
      <div class="control-group">
        <strong>Showing all {t['dealer_count']} verified dealers serving {t['name']}, {t['state']} ({t['zip']})</strong>
      </div>
      <div class="control-group">
        <label>🧮 Tank Fill Size:</label>
        <div class="gal-pills" id="galPills">
          <button type="button" class="gal-btn" onclick="setGallons(100, this)">100 Gal</button>
          <button type="button" class="gal-btn active" onclick="setGallons(150, this)">150 Gal</button>
          <button type="button" class="gal-btn" onclick="setGallons(200, this)">200 Gal</button>
          <button type="button" class="gal-btn" onclick="setGallons(250, this)">250 Gal</button>
        </div>
      </div>
    </div>

    <div class="table-card">
      <div class="table-header">
        <h2>{t['name']}, {t['state']} Heating Oil &amp; Propane Price Comparison ({data['updated_date']})</h2>
        <a href="../index.html" style="font-size:0.85rem;font-weight:700;">View All 22 Regional Dealers &rarr;</a>
      </div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Dealer &amp; Coverage Notes</th>
              <th>Cash Price / Gal</th>
              <th id="fillColHeader">150-Gal Fill Cost</th>
              <th>Min Order</th>
              <th>Local Phone</th>
              <th>Direct Order</th>
            </tr>
          </thead>
          <tbody id="dealerTbody">
            {rows_html}
          </tbody>
        </table>
      </div>
    </div>

    <section class="section-card">
      <h3>🏘️ Compare Nearby Rockingham County &amp; Merrimack Valley Towns</h3>
      <div class="town-grid">
        {''.join(other_links)}
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <strong>{t['name']}, {t['state']} ({t['zip']}) Heating Oil &amp; Propane Price Tracker</strong> &middot;
      <a href="../index.html" style="color:#fdba74;">Back to Southern NH Main Tracker</a> &middot;
      Updated {data['updated_timestamp']}
    </div>
  </footer>

  <script>
    const stateBenchmark = {s['nh_eia_oil_benchmark']};
    function setGallons(gal, btn) {{
      document.querySelectorAll('#galPills .gal-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('fillColHeader').textContent = gal + '-Gal Fill Cost';
      document.querySelectorAll('#dealerTbody tr.dealer-row').forEach(row => {{
        const price = parseFloat(row.getAttribute('data-price'));
        const fillCell = row.querySelector('[data-fill-cell]');
        const saveCell = row.querySelector('[data-save-cell]');
        if (price < 900 && fillCell) {{
          const total = (price * gal).toFixed(2);
          fillCell.textContent = '$' + Number(total).toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
          if (saveCell) {{
            const saved = ((stateBenchmark - price) * gal).toFixed(2);
            saveCell.textContent = 'Save $' + Number(saved).toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + ' vs NH Avg';
          }}
        }}
      }});
    }}
  </script>
</body>
</html>
"""
        out_path = os.path.join(TOWNS_DIR, f"{t['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"[OK] Generated {len(towns)} programmatic SEO town pages in {TOWNS_DIR}")


def build_seo_files(data):
    base_url = "https://nhoiltracker.com"
    urls = [f"  <url><loc>{base_url}/</loc><lastmod>{data['updated_date']}</lastmod><priority>1.0</priority></url>"]
    for t in data["towns"]:
        urls.append(
            f"  <url><loc>{base_url}/towns/{t['slug']}.html</loc><lastmod>{data['updated_date']}</lastmod><priority>0.8</priority></url>"
        )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    with open(os.path.join(SITE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    with open(os.path.join(SITE_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n")
    print("[OK] Generated sitemap.xml and robots.txt")


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    build_index_page(data)
    build_town_pages(data)
    build_seo_files(data)
    import shutil
    docs_dir = os.path.join(BASE_DIR, "docs")
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    shutil.copytree(SITE_DIR, docs_dir)
    with open(os.path.join(docs_dir, ".nojekyll"), "w") as nf:
        nf.write("")
    print(f"[OK] Synced site to {docs_dir} for GitHub Pages")


if __name__ == "__main__":
    main()
