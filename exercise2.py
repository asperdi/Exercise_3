import json
import folium


def process_tram_data(input_file):

    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    stats = {}
    unique_stops = set()

    for i in data['lines']:
        stats[i['line']] = i['stations']

        for j in i['stations']:
            unique_stops.add(j['name'])

    print(len(unique_stops))

    count = {}

    for j in stats.keys():
        count[j] = len(stats[j])

    count = dict(sorted(count.items(), key = lambda x:x[1], reverse=True))
    for _ in count.keys():
        print(f"{_}:{count[_]}")
    return stats, len(unique_stops) 


def create_tram_map(input_file, output_map_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = data["lines"]

    m = folium.Map(location=[50.06, 19.95], zoom_start=12)

    colors = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
        "#a65628", "#f781bf", "#999999", "#66c2a5", "#fc8d62",
        "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494",
        "#b3b3b3"
    ]

    stop_to_lines = {}

    for i, l in enumerate(lines):
        line = l["line"]
        stations = l["stations"]  

        color = colors[i % len(colors)]
        points = [(s["lat"], s["lon"]) for s in stations]

        folium.PolyLine(
            points,
            color=color,
            weight=4,
            opacity=0.7,
            tooltip=f"Lines {line}"
        ).add_to(m)

        for stop in stations:
            name = stop["name"]
            stop_to_lines.setdefault(name, {"lat": stop["lat"], "lon": stop["lon"], "linie": []})
            stop_to_lines[name]["linie"].append(line)

    
    for name, info in stop_to_lines.items():
        folium.CircleMarker(
            location=[info["lat"], info["lon"]],
            radius=5,
            fill=True,
            fill_opacity=0.9,
            tooltip=f"{name} ({', '.join(info['linie'])})",
            popup=f"{name}<br>Linie: {', '.join(info['linie'])}"
        ).add_to(m)

    m.save(output_map_file)


def main():
    print("=" * 60)
    print("Analysis of the tram lines in Krakow")
    print("=" * 60)
    print()

    print("-" * 60)
    stats, unique_stops = process_tram_data('tram_lines.json')
    print(f"\nNumber of the unique stops: {unique_stops}")
    print()

    print("-" * 60)
    create_tram_map('tram_lines.json', 'tram_map.html')
    print(f"Generated map: tram_map.html")
    print()

if __name__ == "__main__":
    main()
