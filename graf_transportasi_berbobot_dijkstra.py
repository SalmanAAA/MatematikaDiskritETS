import networkx as nx
import matplotlib.pyplot as plt

# --- Buat Graf Berbobot Tak Berarah ---
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

# Tambahkan semua edge berbobot
G.add_weighted_edges_from(lintas_barat + lintas_timur + jalur_udara)

# --- Dijkstra: Jalur Terpendek dari Bandung ke Padang ---
asal, tujuan = "Bandung", "Padang"
rute_terpendek = nx.dijkstra_path(G, source=asal, target=tujuan, weight='weight')
jarak_total = nx.dijkstra_path_length(G, source=asal, target=tujuan, weight='weight')

print(f"Rute terpendek dari {asal} ke {tujuan}:")
print(" → ".join(rute_terpendek))
print(f"Total jarak: {jarak_total} km")

# --- Visualisasi Graf ---
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

plt.figure(figsize=(12, 7))
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=900)

# Tandai jalur terpendek dengan warna merah
edges_path = list(zip(rute_terpendek, rute_terpendek[1:]))
nx.draw_networkx_edges(G, pos, edgelist=edges_path, edge_color='red', width=3)

# Tampilkan bobot jarak
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

plt.title(f"Graf Transportasi dan Rute Terpendek {asal} → {tujuan}")
plt.show()
