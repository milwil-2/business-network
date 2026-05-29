#!/usr/bin/env python3
"""Generate a mocked B2B trade & trust network into the Obsidian vault.

Writes ~100 typed nodes (Company / Person / Industry / Product / License /
CreditBureau) as Obsidian markdown into ``vault/nodes/**`` and wires them with
the closed relationship vocabulary. The data is seeded (reproducible) and embeds
deliberate, query-able patterns:

  * trust clusters   — dense GAVE_REFERENCE_FOR / PARTNERS_WITH among high-trust firms
  * a fraud ring     — flagged companies sharing principals, circular SELLS_TO, lapsed licenses
  * supply chains    — vendor -> manufacturer -> distributor -> retailer via SUPPLIES
  * trust hubs       — a few heavily-referenced companies (high degree / PageRank)

Run:  uv run scripts/generate_b2b_vault.py
Then: uv run sync/obsidian_to_neo4j.py --full   (after clearing the graph)

The generator OWNS vault/nodes/: it wipes and rebuilds that tree on every run.
It does not touch vault/meta.
"""

from __future__ import annotations

import random
import shutil
from collections import Counter
from pathlib import Path

import frontmatter

CURRENT_YEAR = 2026
RATING_FACTOR = {"AAA": 1.0, "AA": 0.92, "A": 0.84, "BBB": 0.7, "BB": 0.55,
                 "B": 0.45, "CCC": 0.3, "CC": 0.2, "C": 0.12, "D": 0.0}
STATUS_FACTOR = {"verified": 1.0, "pending": 0.55, "flagged": 0.0}
# Trust-score component weights (sum to 100). Surfaced verbatim in the frontend.
TRUST_WEIGHTS = {"credit": 30, "references": 20, "status": 20,
                 "license": 12, "longevity": 8, "integrity": 10}

SEED = 42
VAULT = Path(__file__).resolve().parent.parent / "vault"
NODES = VAULT / "nodes"

# Mirror of the closed vocabulary in sync/parser.py — the generator must never
# emit a type outside these sets (the sync would reject the file otherwise).
VALID_NODE_TYPES = {"Company", "Person", "Industry", "Product", "License", "CreditBureau"}
VALID_REL_TYPES = {
    "SELLS_TO", "SUPPLIES", "OPERATES_IN", "TRADES_PRODUCT",
    "HOLDS_LICENSE", "RATED_BY", "PRINCIPAL_OF", "GAVE_REFERENCE_FOR",
    "SUBSIDIARY_OF", "PARTNERS_WITH", "COMPETES_WITH", "INVITED",
}

SUBDIR = {
    "Company": "companies", "Person": "people", "Industry": "industries",
    "Product": "products", "License": "licenses", "CreditBureau": "bureaus",
}


def slug(text: str) -> str:
    out = []
    for ch in text.lower().strip():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_./&":
            out.append("-")
    s = "".join(out)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


# ── curated reference data ────────────────────────────────────────────────
INDUSTRIES = [
    ("alcohol-beverage", "Alcohol & Beverage", "Producers, distributors, and retailers of beer, wine, and spirits."),
    ("building-materials", "Building Materials", "Cement, lumber, steel, and other construction supply trades."),
    ("chemicals", "Chemicals", "Industrial chemicals, solvents, polymers, and specialty compounds."),
    ("food-service", "Food Service", "Food production, wholesale distribution, and restaurant supply."),
    ("logistics", "Logistics", "Freight, warehousing, cold storage, and last-mile delivery."),
]

BUREAUS = [
    ("dun-bradstreet", "Dun & Bradstreet", "Business credit bureau issuing PAYDEX and risk scores."),
    ("experian-business", "Experian Business", "Commercial credit reporting and business verification agency."),
    ("equifax-business", "Equifax Business", "Business credit risk and payment-history rating agency."),
]

# (id, label, type, authority, default status)
LICENSES = [
    ("federal-liquor-permit", "Federal Liquor Permit", "Alcohol Distribution", "TTB", "active"),
    ("state-alcohol-license", "State Alcohol Distribution License", "Alcohol Distribution", "State ABC Board", "active"),
    ("contractor-license", "General Contractor License", "Construction", "State Licensing Board", "active"),
    ("hazmat-handling-license", "Hazmat Handling License", "Hazardous Materials", "DOT / PHMSA", "active"),
    ("food-handler-permit", "Food Handler Permit", "Food Safety", "County Health Dept", "active"),
    ("import-export-license", "Import/Export License", "Customs", "U.S. Customs (CBP)", "active"),
    ("motor-carrier-authority", "Motor Carrier Authority", "Freight", "FMCSA", "active"),
]

PRODUCTS = {
    "alcohol-beverage": [("craft-lager", "Craft Lager", "case"), ("bourbon-whiskey", "Bourbon Whiskey", "barrel"), ("sparkling-wine", "Sparkling Wine", "case")],
    "building-materials": [("portland-cement", "Portland Cement", "ton"), ("steel-rebar", "Steel Rebar", "ton"), ("dimensional-lumber", "Dimensional Lumber", "board-ft")],
    "chemicals": [("industrial-solvent", "Industrial Solvent", "drum"), ("polymer-resin", "Polymer Resin", "ton"), ("sodium-hydroxide", "Sodium Hydroxide", "ton")],
    "food-service": [("frozen-produce", "Frozen Produce", "pallet"), ("cooking-oil", "Cooking Oil", "drum"), ("packaged-grains", "Packaged Grains", "pallet")],
    "logistics": [("freight-services", "Freight Services", "shipment"), ("cold-storage", "Cold Storage", "pallet-month"), ("last-mile-delivery", "Last-Mile Delivery", "route")],
}

NAME_PREFIX = [
    "Cascade", "Ironclad", "Summit", "Harbor", "Cobalt", "Vertex", "Granite",
    "Meridian", "Atlas", "Pioneer", "Keystone", "Beacon", "Cardinal", "Sterling",
    "Evergreen", "Redwood", "Anchor", "Copperline", "Northgate", "Sunrise",
    "Tideline", "Brightwater", "Stonebridge", "Falcon", "Quartz", "Marlin",
    "Highland", "Crescent", "Lumen", "Trident",
]
INDUSTRY_SUFFIX = {
    "alcohol-beverage": ["Beverage Co", "Brewing", "Spirits", "Wine Imports", "Distributing"],
    "building-materials": ["Building Supply", "Materials", "Cement Works", "Lumber Co", "Construction Supply"],
    "chemicals": ["Chemical Works", "Industries", "Polymers", "Solvents", "Specialty Chemical"],
    "food-service": ["Food Distributors", "Foods", "Provisions", "Wholesale Grocers", "Culinary Supply"],
    "logistics": ["Logistics", "Freight", "Transport", "Cold Chain", "Distribution"],
}
CITIES = [
    "Portland, OR", "Tacoma, WA", "Oakland, CA", "Denver, CO", "Austin, TX",
    "Columbus, OH", "Atlanta, GA", "Newark, NJ", "Tampa, FL", "Reno, NV",
    "Boise, ID", "Memphis, TN", "Fresno, CA", "Spokane, WA", "Tulsa, OK",
]
FIRST = ["Dana", "Marcus", "Priya", "Evelyn", "Hector", "Naomi", "Theo", "Ruth",
         "Owen", "Camille", "Ravi", "Greta", "Desmond", "Ingrid", "Salim",
         "Beatrice", "Wesley", "Lena", "Cyrus", "Mabel", "Drew", "Yusuf"]
LAST = ["Whitfield", "Okafor", "Castillo", "Nakamura", "Bauer", "Delgado",
        "Hartman", "Sorensen", "Abbas", "Pruitt", "Vance", "Lindqvist",
        "Mercer", "Ramos", "Conley", "Frye", "Esposito", "Holloway"]
CREDIT_RATINGS_GOOD = ["AAA", "AA", "A", "BBB"]
CREDIT_RATINGS_MID = ["BBB", "BB", "B"]
CREDIT_RATINGS_BAD = ["CCC", "CC", "C", "D"]


def write_node(node_type: str, node_id: str, label: str, summary: str,
               properties: dict, relationships: list[dict], body: str) -> None:
    assert node_type in VALID_NODE_TYPES, node_type
    for r in relationships:
        assert r["type"] in VALID_REL_TYPES, r["type"]
    meta = {
        "id": node_id,
        "label": label,
        "node_type": node_type,
        "tags": [node_type],
        "summary": summary,
    }
    if properties:
        meta["properties"] = properties
    if relationships:
        meta["relationships"] = relationships
    post = frontmatter.Post(body.strip() + "\n", **meta)
    path = NODES / SUBDIR[node_type] / f"{node_id}.md"
    path.write_text(frontmatter.dumps(post) + "\n", encoding="utf-8")


def main() -> None:
    rng = random.Random(SEED)

    if NODES.exists():
        shutil.rmtree(NODES)
    for sub in SUBDIR.values():
        (NODES / sub).mkdir(parents=True, exist_ok=True)

    # ── industries, bureaus, products, licenses ──────────────────────────
    for iid, label, summ in INDUSTRIES:
        write_node("Industry", iid, label, summ, {"sector": label}, [],
                   f"The **{label}** sector. Companies operating here trade via the "
                   f"network's SELLS_TO / SUPPLIES edges and are rated by credit bureaus.")

    for bid, label, summ in BUREAUS:
        write_node("CreditBureau", bid, label, summ, {"kind": "credit-bureau"}, [],
                   f"{label} issues business credit ratings used as trust signals across the network.")

    for pid, label, unit in [p for ps in PRODUCTS.values() for p in ps]:
        # find the industry this product belongs to
        ind = next(i for i, ps in PRODUCTS.items() if any(x[0] == pid for x in ps))
        write_node("Product", pid, label, f"{label}, a commodity traded in the {ind.replace('-', ' ')} sector.",
                   {"category": ind, "unit": unit}, [],
                   f"{label} is traded between companies that [[OPERATES_IN]] [[{ind}]].")

    for lid, label, ltype, authority, status in LICENSES:
        write_node("License", lid, label,
                   f"{label} ({ltype}), issued by {authority}.",
                   {"license_type": ltype, "issuing_authority": authority, "status": status,
                    "expires": f"{rng.randint(2026, 2030)}-{rng.randint(1, 12):02d}"},
                   [],
                   f"A {ltype} license issued by {authority}. Companies link to it via HOLDS_LICENSE.")

    # ── companies ────────────────────────────────────────────────────────
    n_companies = 55
    used_names: set[str] = set()
    companies: list[dict] = []
    ind_ids = [i[0] for i in INDUSTRIES]

    # Designate special sets up front (by index) for deterministic patterns.
    flagged_idx = {5, 12, 21, 33}        # the fraud ring
    pending_idx = {3, 9, 17, 24, 29, 41, 48}
    trust_cluster_idx = {0, 1, 2, 6, 10, 14, 18, 26}  # high-trust hubs

    for i in range(n_companies):
        ind = ind_ids[i % len(ind_ids)]
        # build a unique name
        while True:
            name = f"{rng.choice(NAME_PREFIX)} {rng.choice(INDUSTRY_SUFFIX[ind])}"
            if name not in used_names:
                used_names.add(name)
                break
        cid = slug(name)

        if i in flagged_idx:
            status = "flagged"
            fico = rng.randint(470, 560)
            rating = rng.choice(CREDIT_RATINGS_BAD)
        elif i in pending_idx:
            status = "pending"
            fico = rng.randint(600, 689)
            rating = rng.choice(CREDIT_RATINGS_MID)
        else:
            status = "verified"
            fico = rng.randint(690, 820)
            rating = rng.choice(CREDIT_RATINGS_GOOD)

        companies.append({
            "id": cid, "label": name, "industry": ind, "status": status,
            "fico": fico, "rating": rating,
            "revenue": rng.choice([2, 5, 8, 12, 20, 35, 60, 120, 250]) * 1_000_000,
            "founded": rng.randint(1972, 2019),
            "city": rng.choice(CITIES),
            "employees": rng.choice([12, 30, 75, 140, 320, 600, 1100]),
            "rels": [],
        })

    by_id = {c["id"]: c for c in companies}
    cid_list = [c["id"] for c in companies]
    by_industry: dict[str, list[str]] = {ind: [] for ind in ind_ids}
    for c in companies:
        by_industry[c["industry"]].append(c["id"])

    def add(c: dict, rtype: str, target: str) -> None:
        if target == c["id"]:
            return
        pair = {"type": rtype, "target": target}
        if pair not in c["rels"]:
            c["rels"].append(pair)

    # OPERATES_IN, TRADES_PRODUCT, RATED_BY, HOLDS_LICENSE
    for c in companies:
        add(c, "OPERATES_IN", c["industry"])
        for pid, _, _ in rng.sample(PRODUCTS[c["industry"]], k=rng.randint(1, 2)):
            add(c, "TRADES_PRODUCT", pid)
        add(c, "RATED_BY", rng.choice([b[0] for b in BUREAUS]))
        if c["status"] != "flagged":
            for lid, *_ in rng.sample(LICENSES, k=rng.randint(1, 2)):
                add(c, "HOLDS_LICENSE", lid)

    # SELLS_TO + SUPPLIES: trade edges, biased within-industry
    for c in companies:
        pool = [x for x in by_industry[c["industry"]] if x != c["id"]] or [x for x in cid_list if x != c["id"]]
        for tgt in rng.sample(pool, k=min(len(pool), rng.randint(1, 3))):
            add(c, "SELLS_TO", tgt)
        for tgt in rng.sample(pool, k=min(len(pool), rng.randint(0, 2))):
            add(c, "SUPPLIES", tgt)

    # Supply chains: ordered SUPPLIES chain within each industry
    for ind, ids in by_industry.items():
        chain = ids[:5]
        for a, b in zip(chain, chain[1:]):
            add(by_id[a], "SUPPLIES", b)

    # COMPETES_WITH within industry (sparse)
    for ind, ids in by_industry.items():
        for a in ids:
            if rng.random() < 0.25:
                others = [x for x in ids if x != a]
                if others:
                    add(by_id[a], "COMPETES_WITH", rng.choice(others))

    # Trust cluster: dense GAVE_REFERENCE_FOR + PARTNERS_WITH among hubs
    hub_ids = [companies[i]["id"] for i in sorted(trust_cluster_idx) if i < len(companies)]
    for a in hub_ids:
        for b in hub_ids:
            if a != b and rng.random() < 0.55:
                add(by_id[a], "GAVE_REFERENCE_FOR", b)
            if a != b and rng.random() < 0.3:
                add(by_id[a], "PARTNERS_WITH", b)
    # verified non-hub companies occasionally reference a hub (inbound trust)
    for c in companies:
        if c["status"] == "verified" and c["id"] not in hub_ids and rng.random() < 0.4:
            add(c, "GAVE_REFERENCE_FOR", rng.choice(hub_ids))

    # SUBSIDIARY_OF + INVITED (sparse corporate / network-growth signal)
    for c in companies:
        if rng.random() < 0.12:
            add(c, "SUBSIDIARY_OF", rng.choice([x for x in cid_list if x != c["id"]]))
        if rng.random() < 0.2:
            add(c, "INVITED", rng.choice([x for x in cid_list if x != c["id"]]))

    # ── fraud ring: circular SELLS_TO + lapsed/revoked licenses ──────────
    ring = [companies[i]["id"] for i in sorted(flagged_idx)]
    for a, b in zip(ring, ring[1:] + ring[:1]):  # circular
        add(by_id[a], "SELLS_TO", b)
    # give the ring lapsed/revoked licenses (override the active default by
    # writing dedicated license nodes the ring shares)
    write_node("License", "lapsed-liquor-permit", "Lapsed Liquor Permit",
               "A liquor permit that has lapsed and is pending revocation.",
               {"license_type": "Alcohol Distribution", "issuing_authority": "TTB",
                "status": "lapsed", "expires": "2024-03"}, [],
               "A lapsed permit flagged during vendor verification.")
    write_node("License", "revoked-hazmat-license", "Revoked Hazmat License",
               "A hazmat handling license that has been revoked.",
               {"license_type": "Hazardous Materials", "issuing_authority": "DOT / PHMSA",
                "status": "revoked", "expires": "2023-11"}, [],
               "A revoked hazmat license tied to flagged companies.")
    for cid in ring:
        add(by_id[cid], "HOLDS_LICENSE", rng.choice(["lapsed-liquor-permit", "revoked-hazmat-license"]))

    # ── people / principals ──────────────────────────────────────────────
    people: list[dict] = []
    used_people: set[str] = set()

    def new_person(title: str) -> dict:
        while True:
            nm = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
            if nm not in used_people:
                used_people.add(nm)
                break
        pid = slug(nm)
        p = {"id": pid, "label": nm, "title": title, "rels": []}
        people.append(p)
        return p

    # One principal per company (most companies), some principals run several.
    multi = [new_person("Managing Partner") for _ in range(3)]
    for c in companies:
        if c["status"] == "flagged":
            continue  # ring principals assigned below
        if rng.random() < 0.18 and multi:
            p = rng.choice(multi)
        else:
            p = new_person(rng.choice(["CEO", "Owner", "President", "CFO"]))
        p["rels"].append({"type": "PRINCIPAL_OF", "target": c["id"]})

    # Fraud ring: 2 shared principals each tied to MULTIPLE flagged companies.
    ring_principal_a = new_person("Owner")
    ring_principal_b = new_person("Owner")
    for idx, cid in enumerate(ring):
        ring_principal_a["rels"].append({"type": "PRINCIPAL_OF", "target": cid})
        if idx % 2 == 0:
            ring_principal_b["rels"].append({"type": "PRINCIPAL_OF", "target": cid})

    # ── compute composite trust scores (final pass: all rels + people exist) ──
    flagged_ids = {c["id"] for c in companies if c["status"] == "flagged"}
    refs_received = Counter(
        r["target"] for c in companies for r in c["rels"]
        if r["type"] == "GAVE_REFERENCE_FOR"
    )
    lic_status = {lid: st for lid, _, _, _, st in LICENSES}
    lic_status["lapsed-liquor-permit"] = "lapsed"
    lic_status["revoked-hazmat-license"] = "revoked"
    person_companies: dict[str, set[str]] = {}
    company_principals: dict[str, set[str]] = {}
    for p in people:
        for r in p["rels"]:
            if r["type"] == "PRINCIPAL_OF":
                person_companies.setdefault(p["id"], set()).add(r["target"])
                company_principals.setdefault(r["target"], set()).add(p["id"])

    for c in companies:
        cid = c["id"]
        # 1. creditworthiness — FICO blended with credit-rating tier
        credit = 0.6 * (c["fico"] - 300) / 550.0 + 0.4 * RATING_FACTOR.get(c["rating"], 0.5)
        credit = max(0.0, min(1.0, credit))
        # 2. trade references received (network trust)
        references = min(refs_received.get(cid, 0) / 8.0, 1.0)
        # 3. verification status
        status_f = STATUS_FACTOR[c["status"]]
        # 4. license validity
        held = [r["target"] for r in c["rels"] if r["type"] == "HOLDS_LICENSE"]
        sts = [lic_status.get(t) for t in held]
        lic = 0.0 if "revoked" in sts else 0.4 if "lapsed" in sts else 1.0 if sts else 0.5
        # 5. longevity
        longevity = min((CURRENT_YEAR - c["founded"]) / 40.0, 1.0)
        # 6. principal integrity — penalty if a principal also runs a flagged company
        principals = company_principals.get(cid, set())
        shares_flagged = any((person_companies.get(p, set()) & flagged_ids) - {cid} for p in principals)
        integrity = 0.0 if shares_flagged else 1.0

        parts = {
            "credit": TRUST_WEIGHTS["credit"] * credit,
            "references": TRUST_WEIGHTS["references"] * references,
            "status": TRUST_WEIGHTS["status"] * status_f,
            "license": TRUST_WEIGHTS["license"] * lic,
            "longevity": TRUST_WEIGHTS["longevity"] * longevity,
            "integrity": TRUST_WEIGHTS["integrity"] * integrity,
        }
        c["trust"] = max(0, min(100, round(sum(parts.values()))))
        c["refs_received"] = refs_received.get(cid, 0)
        for k, v in parts.items():
            c[f"trust_{k}"] = round(v, 1)

    # ── write companies & people ─────────────────────────────────────────
    for c in companies:
        ind_label = next(l for i, l, _ in INDUSTRIES if i == c["industry"])
        flag = " This profile is **flagged** pending review." if c["status"] == "flagged" else ""
        body = (
            f"**{c['label']}** is a {c['status']} business in the [[{c['industry']}]] sector, "
            f"headquartered in {c['city']} and founded in {c['founded']}. "
            f"Trust score **{c['trust']}/100**, credit rating **{c['rating']}**, FICO **{c['fico']}**.{flag}\n\n"
            f"## Trade profile\n"
            f"- Industry: {ind_label}\n"
            f"- Annual revenue: ${c['revenue']:,}\n"
            f"- Employees: {c['employees']}\n"
            f"- Trade references received: {c['refs_received']}\n\n"
            f"## Trust score breakdown ({c['trust']}/100)\n"
            f"- Creditworthiness: {c['trust_credit']}/30\n"
            f"- Trade references: {c['trust_references']}/20\n"
            f"- Verification status: {c['trust_status']}/20\n"
            f"- License validity: {c['trust_license']}/12\n"
            f"- Longevity: {c['trust_longevity']}/8\n"
            f"- Principal integrity: {c['trust_integrity']}/10\n\n"
            f"The business trust score is a weighted composite of the company's own "
            f"data points (credit, licenses, age, verification) and its network "
            f"signals (trade references, principal integrity)."
        )
        props = {
            "trust_score": c["trust"], "credit_rating": c["rating"], "fico": c["fico"],
            "annual_revenue_usd": c["revenue"], "founded_year": c["founded"],
            "hq_location": c["city"], "employee_count": c["employees"], "status": c["status"],
            "references_received": c["refs_received"],
            "trust_credit": c["trust_credit"], "trust_references": c["trust_references"],
            "trust_status": c["trust_status"], "trust_license": c["trust_license"],
            "trust_longevity": c["trust_longevity"], "trust_integrity": c["trust_integrity"],
        }
        summary = (f"{c['label']} — a {c['status']} {ind_label.lower()} business "
                   f"(trust {c['trust']}/100, credit {c['rating']}, FICO {c['fico']}).")
        write_node("Company", c["id"], c["label"], summary, props, c["rels"], body)

    for p in people:
        runs = [r["target"] for r in p["rels"]]
        summary = f"{p['label']} — {p['title']}; principal of {len(runs)} compan{'y' if len(runs)==1 else 'ies'}."
        body = (f"**{p['label']}** serves as {p['title']}. "
                f"Listed as a principal (PRINCIPAL_OF) on {len(runs)} business profile(s). "
                f"Shared principals across multiple flagged companies are a fraud signal.")
        write_node("Person", p["id"], p["label"], summary, {"title": p["title"], "verified": rng.random() < 0.8},
                   p["rels"], body)

    # ── report ───────────────────────────────────────────────────────────
    counts = {t: len(list((NODES / SUBDIR[t]).glob("*.md"))) for t in VALID_NODE_TYPES}
    total_nodes = sum(counts.values())
    total_rels = sum(len(c["rels"]) for c in companies) + sum(len(p["rels"]) for p in people)
    print(f"Wrote {total_nodes} nodes ({total_rels} relationships) to {NODES}")
    for t in sorted(counts):
        print(f"  {t:12s} {counts[t]}")
    print(f"  fraud ring: {ring}")
    print(f"  trust hubs: {hub_ids}")


if __name__ == "__main__":
    main()
