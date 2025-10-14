import networkx as nx
import matplotlib.pyplot as plt

# === 1. Buat Graph Berbobot ===
G = nx.Graph()

# --- Rute Lintas Barat (Via Tol) ---
lintas_barat = [
    ("Bandung", "Jakarta", 152),
    ("Jakarta", "Pelabuhan Merak", 112),
    ("Pelabuhan Merak", "Bakauheni", 36),
    ("Bakauheni", "Lampung", 221),
    ("Lampung", "Palembang", 239),
    ("Palembang", "Jambi", 271),
    ("Jambi", "Padang", 524)
]

# --- Rute Lintas Timur (Via Non-Tol) ---
lintas_timur = [
    ("Bandung", "Jakarta", 152),
    ("Jakarta", "Pelabuhan Merak", 112),
    ("Pelabuhan Merak", "Bakauheni", 36),
    ("Bakauheni", "Lampung", 221),
    ("Lampung", "Bengkulu", 600),
    ("Bengkulu", "Padang", 535)
]

# --- Rute Jalur Udara (Pesawat) ---
jalur_udara = [
    ("Bandung", "Jakarta", 525),
    ("Jakarta", "Bandara Soekarno Hatta", 32),
    ("Bandara Soekarno Hatta", "Bandara Internasional Minangkabau", 1320),
    ("Bandara Internasional Minangkabau", "Padang", 22)
]

# Tambahkan semua edge dengan bobot jarak
G.add_weighted_edges_from(lintas_barat + lintas_timur + jalur_udara)

# === 2. Posisi Node (Layout mini Indonesia bagian barat) ===
pos = {
    "Bandung": (0, 0),
    "Jakarta": (1.2, 0.8),
    "Pelabuhan Merak": (2.2, 0.9),
    "Bakauheni": (2.4, 1.8),
    "Lampung": (3.2, 2.2),
    "Palembang": (4.2, 2.8),
    "Jambi": (5.0, 3.4),
    "Padang": (6.0, 3.0),
    "Bengkulu": (4.0, 1.8),
    "Bandara Soekarno Hatta": (2.8, -0.8),
    "Bandara Internasional Minangkabau": (5.5, -0.8)
}

# === 3. Warna Edge berdasarkan jenis jalur ===
edge_colors = []
for u, v, data in G.edges(data=True):
    if any({u, v} == {a, b} for a, b, _ in lintas_barat):
        edge_colors.append("red")
    elif any({u, v} == {a, b} for a, b, _ in lintas_timur):
        edge_colors.append("green")
    elif any({u, v} == {a, b} for a, b, _ in jalur_udara):
        edge_colors.append("blue")
    else:
        edge_colors.append("gray")

# === 4. Visualisasi Graf Transportasi dengan Bobot ===
plt.figure(figsize=(13, 8))
nx.draw(
    G, pos,
    with_labels=True,
    node_color="lightgrey",
    edge_color=edge_colors,
    width=2.5,
    font_weight="bold",
    node_size=1300
)

# Tampilkan jarak (bobot) di tiap edge
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

# Tambahkan legenda
legend_labels = {
    "red": "Lintas Barat (Via Tol)",
    "green": "Lintas Timur (Non-Tol)",
    "blue": "Jalur Udara (Pesawat)"
}
for color, label in legend_labels.items():
    plt.plot([], [], color=color, label=label, linewidth=3)
plt.legend(title="Jenis Jalur", loc="upper left")

plt.title("Graf Transportasi Bandung → Padang (Berbobot Jarak per Jalur)")
plt.axis("off")
plt.show()

# === 5. Analisis Rute Terpendek (Dijkstra) ===
asal = "Bandung"
tujuan = "Padang"

# Hitung jalur dan jarak terpendek
shortest_path = nx.shortest_path(G, source=asal, target=tujuan, weight='weight')
shortest_distance = nx.shortest_path_length(G, source=asal, target=tujuan, weight='weight')

print(f"Rute terpendek dari {asal} ke {tujuan}:")
print(" → ".join(shortest_path))
print(f"Total jarak: {shortest_distance} km")

# === 6. Visualisasi Rute Terpendek ===
plt.figure(figsize=(13, 8))

# Warna default abu-abu untuk semua edge
edge_colors = ["lightgray"] * len(G.edges())

# Ganti warna edge yang termasuk jalur terpendek
path_edges = list(zip(shortest_path, shortest_path[1:]))
for i, edge in enumerate(G.edges()):
    if edge in path_edges or (edge[1], edge[0]) in path_edges:
        edge_colors[i] = "orange"

# Gambar ulang graf dengan penekanan pada rute terpendek
nx.draw(
    G, pos,
    with_labels=True,
    node_color="lightblue",
    edge_color=edge_colors,
    width=3.5,
    font_weight="bold",
    node_size=1300
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

plt.title(f"Rute Terpendek dari {asal} ke {tujuan} (Dijkstra) - {shortest_distance} km")
plt.axis("off")
plt.show()
