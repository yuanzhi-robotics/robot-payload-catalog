import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLATFORMS = {p['id']: p for p in json.load(open(os.path.join(HERE, 'data', 'platforms.json'), encoding='utf-8'))}
ITEMS = {i['id']: i for i in json.load(open(os.path.join(HERE, 'data', 'payload_items.json'), encoding='utf-8'))}


def list_platforms():
    for p in PLATFORMS.values():
        pay = f"{p['rated_payload_kg']} kg" if p['rated_payload_kg'] is not None else 'n/a'
        print(f"{p['id']:<12} {p['category']:<10} {p['brand']} {p['model']}  (rated payload {pay})")


def list_items(kind):
    for i in ITEMS.values():
        if kind and i['type'] != kind:
            continue
        w = f"{i['weight_g']:g} g" if i['weight_g'] else '? g'
        pw = f"{i['power_w']:g} W" if i['power_w'] else '? W'
        print(f"{i['id']:<32} {i['type']:<18} {i['brand']} {i['model']}  [{w}, {pw}]")


def budget(platform_id, item_ids, margin):
    p = PLATFORMS.get(platform_id)
    if not p:
        sys.exit(f'unknown platform: {platform_id} (use --platforms to list)')
    unknown = [x for x in item_ids if x not in ITEMS]
    if unknown:
        sys.exit(f'unknown items: {", ".join(unknown)} (use --items to list)')
    rows, grams, watts, missing_w, missing_p = [], 0.0, 0.0, [], []
    for x in item_ids:
        i = ITEMS[x]
        rows.append(i)
        if i['weight_g']:
            grams += i['weight_g']
        else:
            missing_w.append(x)
        if i['power_w']:
            watts += i['power_w']
        else:
            missing_p.append(x)
    print(f"Platform: {p['brand']} {p['model']} ({p['category']})")
    for i in rows:
        w = f"{i['weight_g']:g} g" if i['weight_g'] else 'weight unknown'
        pw = f"{i['power_w']:g} W" if i['power_w'] else 'power unknown'
        print(f"  - {i['brand']} {i['model']}: {w}, {pw}")
    total = grams * (1 + margin)
    print(f"Sensors and compute: {grams / 1000:.2f} kg, {watts:.1f} W")
    print(f"With {margin * 100:.0f}% allowance for brackets and cables: {total / 1000:.2f} kg")
    if p['rated_payload_kg']:
        pct = total / 1000 / p['rated_payload_kg'] * 100
        state = 'OK' if pct <= 60 else ('tight' if pct <= 100 else 'OVER rated payload')
        print(f"Rated payload {p['rated_payload_kg']} kg -> {pct:.0f}% used ({state})")
    if missing_w:
        print('No weight data for: ' + ', '.join(missing_w))
    if missing_p:
        print('No power data for: ' + ', '.join(missing_p))


def main():
    ap = argparse.ArgumentParser(description='Payload weight and power budget for robot dogs, UGVs and drones.')
    ap.add_argument('platform', nargs='?', help='platform id, e.g. go2, b2, husky, m350')
    ap.add_argument('items', nargs='*', help='payload item ids, e.g. livox-mid360 orbbec-gemini335')
    ap.add_argument('--margin', type=float, default=0.25, help='allowance for brackets and cables (default 0.25 = 25%%)')
    ap.add_argument('--platforms', action='store_true', help='list platforms')
    ap.add_argument('--items', dest='list_items', nargs='?', const='', metavar='TYPE', help='list payload items, optionally of one type (lidar, depth_camera, edge_compute, ...)')
    a = ap.parse_args()
    if a.platforms:
        return list_platforms()
    if a.list_items is not None:
        return list_items(a.list_items)
    if not a.platform:
        ap.print_help()
        return
    budget(a.platform, a.items, a.margin)


if __name__ == '__main__':
    main()
