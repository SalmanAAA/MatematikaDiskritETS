import networkx as nx
import matplotlib.pyplot as plt

# --- 1. Buat graph transportasi ---
G = nx.Graph()

# --- Jalur Lintas Barat ---
lintas_barat = [
    ("Bandung", "Jakarta"),
    ("Jakarta", "Pelabuhan Merak"),
    ("Pelabuhan Merak", "Bakauheni"),
    ("Bakauheni", "Lampung"),
    ("Lampung", "Palembang"),
    ("Palembang", "Jambi"),
    ("Jambi", "Padang")
]

# --- Jalur Lintas Timur ---
lintas_timur = [
    ("Bandung", "Jakarta"),
    ("Jakarta", "Pelabuhan Merak"),
    ("Pelabuhan Merak", "Bakauheni"),
    ("Bakauheni", "Lampung"),
    ("Lampung", "Bengkulu"),
    ("Bengkulu", "Padang")
]

# --- Jalur Udara ---
jalur_udara = [
    ("Bandung", "Jakarta"),
    ("Jakarta", "Bandara Soekarno Hatta"),
    ("Bandara Soekarno Hatta", "Bandara Internasional Minangkabau"),
    ("Bandara Internasional Minangkabau", "Padang")
]

# Tambahkan semua edge
G.add_edges_from(lintas_barat + lintas_timur + jalur_udara)

# --- 2. Posisi Node (Layout peta mini Indonesia bagian barat) ---
pos = {
    # Pulau Jawa
    "Bandung": (0, 0),
    "Jakarta": (1.2, 0.8),
    "Pelabuhan Merak": (2.2, 0.9),

    # Sumatra
    "Bakauheni": (2.4, 1.8),
    "Lampung": (3.2, 2.2),
    "Palembang": (4.2, 2.8),
    "Jambi": (5.0, 3.4),
    "Padang": (6.0, 3.0),
    "Bengkulu": (4.0, 1.8),

    # Jalur Udara (bawah)
    "Bandara Soekarno Hatta": (2.8, -0.8),  # ← digeser ke kanan
    "Bandara Internasional Minangkabau": (5.5, -0.8)
}

# --- 3. Warna edge berdasarkan jalur ---
edge_colors = []
for edge in G.edges():
    if edge in lintas_barat or (edge[1], edge[0]) in lintas_barat:
        edge_colors.append("red")
    elif edge in lintas_timur or (edge[1], edge[0]) in lintas_timur:
        edge_colors.append("green")
    elif edge in jalur_udara or (edge[1], edge[0]) in jalur_udara:
        edge_colors.append("blue")
    else:
        edge_colors.append("gray")

# --- 4. Visualisasi graph transportasi ---
plt.figure(figsize=(12, 7))
nx.draw(
    G, pos,
    with_labels=True,
    node_color="lightgrey",
    edge_color=edge_colors,
    width=2.5,
    font_weight="bold",
    node_size=1300
)

# Tambah legenda
legend_labels = {
    "red": "Lintas Barat (Darat)",
    "green": "Lintas Timur (Darat)",
    "blue": "Jalur Udara"
}
for color, label in legend_labels.items():
    plt.plot([], [], color=color, label=label, linewidth=3)
plt.legend(title="Jenis Jalur", loc="upper left")

plt.title("Graf Transportasi Bandung → Padang (3 Jalur: Barat, Timur, dan Udara)")
plt.axis("off")
plt.show()

# --- 5. Pewarnaan node (chromatic coloring heuristic) ---
coloring = nx.coloring.greedy_color(G, strategy="largest_first")
print("Pewarnaan Node (Greedy Algorithm):")
print(coloring)
num_colors = len(set(coloring.values()))
print(f"Jumlah warna yang digunakan (chromatic number heuristik): {num_colors}")

# --- 6. Visualisasi node coloring ---
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
node_colors = [colors[coloring[node] % len(colors)] for node in G.nodes()]

plt.figure(figsize=(12, 7))
nx.draw(
    G, pos,
    with_labels=True,
    node_color=node_colors,
    font_weight='bold',
    edge_color='gray',
    width=2.5,
    node_size=1300
)
plt.title("Graf Transportasi dengan Pewarnaan Node (Chromatic Coloring)")
plt.axis("off")
plt.show()
