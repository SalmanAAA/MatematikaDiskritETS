import networkx as nx
import matplotlib.pyplot as plt

# Fungsi bantu: konversi jam & menit ke menit total
def waktu_ke_menit(jam=0, menit=0):
    return jam * 60 + menit

# --- Buat Graf Berbobot (dalam menit) ---
G = nx.Graph()

# --- Rute Lintas Barat (Via Tol) ---
lintas_barat = [
    ("Bandung", "Jakarta", waktu_ke_menit(2, 30)),
    ("Jakarta", "Pelabuhan Merak", waktu_ke_menit(2, 25)),
    ("Pelabuhan Merak", "Bakauheni", waktu_ke_menit(1, 23)),
    ("Bakauheni", "Lampung", waktu_ke_menit(3, 0)),
    ("Lampung", "Palembang", waktu_ke_menit(3, 52)),
    ("Palembang", "Jambi", waktu_ke_menit(11, 27)),
    ("Jambi", "Padang", waktu_ke_menit(8, 9))
]

# --- Rute Lintas Timur (Via Non-Tol) ---
lintas_timur = [
    ("Bandung", "Jakarta", waktu_ke_menit(2, 30)),
    ("Jakarta", "Pelabuhan Merak", waktu_ke_menit(2, 25)),
    ("Pelabuhan Merak", "Bakauheni", waktu_ke_menit(1, 23)),
    ("Bakauheni", "Lampung", waktu_ke_menit(3, 0)),
    ("Lampung", "Bengkulu", waktu_ke_menit(14, 17)),
    ("Bengkulu", "Padang", waktu_ke_menit(13, 2))
]

# --- Jalur Udara (Pesawat) ---
jalur_udara = [
    ("Bandung", "Jakarta", waktu_ke_menit(2, 30)),
    ("Jakarta", "Bandara Soekarno Hatta", waktu_ke_menit(0, 40)),
    ("Bandara Soekarno Hatta", "Bandara Internasional Minangkabau", waktu_ke_menit(1, 45)),
    ("Bandara Internasional Minangkabau", "Padang", waktu_ke_menit(0, 40))
]

# Tambahkan semua edge berbobot waktu
G.add_weighted_edges_from(lintas_barat + lintas_timur + jalur_udara)

# --- Dijkstra: Jalur Tercepat dari Bandung ke Padang ---
asal, tujuan = "Bandung", "Padang"
rute_tercepat = nx.dijkstra_path(G, source=asal, target=tujuan, weight='weight')
waktu_total_menit = nx.dijkstra_path_length(G, source=asal, target=tujuan, weight='weight')

# Konversi waktu total ke jam:menit
jam_total = waktu_total_menit // 60
menit_total = waktu_total_menit % 60

print(f"Rute tercepat dari {asal} ke {tujuan}:")
print(" → ".join(rute_tercepat))
print(f"Total waktu tempuh: {int(jam_total)} jam {int(menit_total)} menit")

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

# Tandai jalur tercepat (Dijkstra) dengan warna merah
edges_path = list(zip(rute_tercepat, rute_tercepat[1:]))
nx.draw_networkx_edges(G, pos, edgelist=edges_path, edge_color='red', width=3)

# Label waktu (jam:menit) di setiap edge
def menit_ke_label(m):
    j = int(m // 60)
    menit = int(m % 60)
    return f"{j}j{menit}m"

edge_labels = {e: menit_ke_label(w) for e, w in nx.get_edge_attributes(G, 'weight').items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

plt.title(f"Graf Transportasi (Waktu Tempuh) dan Jalur Tercepat {asal} → {tujuan}")
plt.show()
