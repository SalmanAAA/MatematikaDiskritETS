import networkx as nx
import matplotlib.pyplot as plt

# =====================================
# POSISI NODE (TETAP UNTUK SEMUA GRAF)
# =====================================
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

# =====================================
# DATA JALUR
# =====================================
lintas_barat = [
    ("Bandung", "Jakarta"),
    ("Jakarta", "Pelabuhan Merak"),
    ("Pelabuhan Merak", "Bakauheni"),
    ("Bakauheni", "Lampung"),
    ("Lampung", "Palembang"),
    ("Palembang", "Jambi"),
    ("Jambi", "Padang")
]

lintas_timur = [
    ("Bandung", "Jakarta"),
    ("Jakarta", "Pelabuhan Merak"),
    ("Pelabuhan Merak", "Bakauheni"),
    ("Bakauheni", "Lampung"),
    ("Lampung", "Bengkulu"),
    ("Bengkulu", "Padang")
]

jalur_udara = [
    ("Bandung", "Jakarta"),
    ("Jakarta", "Bandara Soekarno Hatta"),
    ("Bandara Soekarno Hatta", "Bandara Internasional Minangkabau"),
    ("Bandara Internasional Minangkabau", "Padang")
]


# =====================================
# 1️⃣  GRAF TRANSPORTASI TANPA BOBOT
# =====================================
def graf_transportasi():
    G = nx.Graph()
    G.add_edges_from(lintas_barat + lintas_timur + jalur_udara)

    # Warna edge berdasarkan jenis jalur
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

    # Legenda
    legend_labels = {
        "red": "Lintas Barat (Darat)",
        "green": "Lintas Timur (Darat)",
        "blue": "Jalur Udara"
    }
    for color, label in legend_labels.items():
        plt.plot([], [], color=color, label=label, linewidth=3)
    plt.legend(title="Jenis Jalur", loc="upper left")

    plt.title("Graf Transportasi Bandung → Padang (3 Jalur: Barat, Timur, Udara)")
    plt.axis("off")
    plt.show()


# =====================================
# 2️⃣  DIJKSTRA BERDASARKAN JARAK (KM)
# =====================================
def dijkstra_jarak():
    G = nx.Graph()

    lintas_barat_km = [
        ("Bandung", "Jakarta", 152),
        ("Jakarta", "Pelabuhan Merak", 112),
        ("Pelabuhan Merak", "Bakauheni", 36),
        ("Bakauheni", "Lampung", 221),
        ("Lampung", "Palembang", 239),
        ("Palembang", "Jambi", 271),
        ("Jambi", "Padang", 524)
    ]

    lintas_timur_km = [
        ("Bandung", "Jakarta", 152),
        ("Jakarta", "Pelabuhan Merak", 112),
        ("Pelabuhan Merak", "Bakauheni", 36),
        ("Bakauheni", "Lampung", 221),
        ("Lampung", "Bengkulu", 600),
        ("Bengkulu", "Padang", 535)
    ]

    jalur_udara_km = [
        ("Bandung", "Jakarta", 525),
        ("Jakarta", "Bandara Soekarno Hatta", 32),
        ("Bandara Soekarno Hatta", "Bandara Internasional Minangkabau", 1320),
        ("Bandara Internasional Minangkabau", "Padang", 22)
    ]

    G.add_weighted_edges_from(lintas_barat_km + lintas_timur_km + jalur_udara_km)

    asal, tujuan = "Bandung", "Padang"
    rute = nx.dijkstra_path(G, source=asal, target=tujuan, weight='weight')
    total = nx.dijkstra_path_length(G, source=asal, target=tujuan, weight='weight')

    print(f"Rute terpendek berdasarkan jarak dari {asal} ke {tujuan}:")
    print(" → ".join(rute))
    print(f"Total jarak: {total} km")

    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=900, font_weight='bold')
    edges_path = list(zip(rute, rute[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges_path, edge_color='red', width=3)

    edge_labels = {e: f"{w} km" for e, w in nx.get_edge_attributes(G, 'weight').items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title(f"Rute Terpendek {asal} → {tujuan} (Berdasarkan Jarak)")
    plt.show()


# =====================================
# 3️⃣  DIJKSTRA BERDASARKAN WAKTU (MENIT)
# =====================================
def waktu_ke_menit(jam=0, menit=0):
    return jam * 60 + menit

def dijkstra_waktu():
    G = nx.Graph()

    lintas_barat_waktu = [
        ("Bandung", "Jakarta", waktu_ke_menit(2, 30)),
        ("Jakarta", "Pelabuhan Merak", waktu_ke_menit(2, 25)),
        ("Pelabuhan Merak", "Bakauheni", waktu_ke_menit(1, 23)),
        ("Bakauheni", "Lampung", waktu_ke_menit(3, 0)),
        ("Lampung", "Palembang", waktu_ke_menit(3, 52)),
        ("Palembang", "Jambi", waktu_ke_menit(11, 27)),
        ("Jambi", "Padang", waktu_ke_menit(8, 9))
    ]

    lintas_timur_waktu = [
        ("Bandung", "Jakarta", waktu_ke_menit(2, 30)),
        ("Jakarta", "Pelabuhan Merak", waktu_ke_menit(2, 25)),
        ("Pelabuhan Merak", "Bakauheni", waktu_ke_menit(1, 23)),
        ("Bakauheni", "Lampung", waktu_ke_menit(3, 0)),
        ("Lampung", "Bengkulu", waktu_ke_menit(14, 17)),
        ("Bengkulu", "Padang", waktu_ke_menit(13, 2))
    ]

    jalur_udara_waktu = [
        ("Bandung", "Jakarta", waktu_ke_menit(2, 30)),
        ("Jakarta", "Bandara Soekarno Hatta", waktu_ke_menit(0, 40)),
        ("Bandara Soekarno Hatta", "Bandara Internasional Minangkabau", waktu_ke_menit(1, 45)),
        ("Bandara Internasional Minangkabau", "Padang", waktu_ke_menit(0, 40))
    ]

    G.add_weighted_edges_from(lintas_barat_waktu + lintas_timur_waktu + jalur_udara_waktu)

    asal, tujuan = "Bandung", "Padang"
    rute = nx.dijkstra_path(G, source=asal, target=tujuan, weight='weight')
    total_menit = nx.dijkstra_path_length(G, source=asal, target=tujuan, weight='weight')
    jam_total, menit_total = divmod(total_menit, 60)

    print(f"Rute tercepat berdasarkan waktu dari {asal} ke {tujuan}:")
    print(" → ".join(rute))
    print(f"Total waktu tempuh: {int(jam_total)} jam {int(menit_total)} menit")

    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=900, font_weight='bold')
    edges_path = list(zip(rute, rute[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges_path, edge_color='red', width=3)

    def label_waktu(m):
        j, mn = divmod(m, 60)
        return f"{int(j)}j{int(mn)}m"

    edge_labels = {e: label_waktu(w) for e, w in nx.get_edge_attributes(G, 'weight').items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title(f"Rute Tercepat {asal} → {tujuan} (Berdasarkan Waktu)")
    plt.show()


# =====================================
# MENU UTAMA
# =====================================
def main():
    while True:
        print("\n=== MENU GRAF TRANSPORTASI BANDUNG - PADANG ===")
        print("1. Tampilkan Graf Transportasi (Tanpa Bobot)")
        print("2. Jalur Terpendek (Berdasarkan Jarak)")
        print("3. Jalur Tercepat (Berdasarkan Waktu)")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            graf_transportasi()
        elif pilihan == "2":
            dijkstra_jarak()
        elif pilihan == "3":
            dijkstra_waktu()
        elif pilihan == "0":
            print("Terima kasih! 🚗✈️")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
