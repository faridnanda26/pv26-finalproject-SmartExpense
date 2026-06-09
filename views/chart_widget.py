from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ExpensePieChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Membuat figure dengan background transparan/putih bersih
        self.figure = Figure(figsize=(5, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot(self, df, title):
        self.figure.clear()
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)
        ax = self.figure.add_subplot(111)

        if df is None or df.empty:
            ax.text(0.5, 0.5, "Tidak ada data pengeluaran\npada periode ini", 
                    ha='center', va='center', fontsize=11, color='gray')
            ax.axis('off')
            self.canvas.draw()
            return

        labels = df.iloc[:, 0].tolist()
        values = df.iloc[:, 1].tolist()
        colors = ["#005088", "#00a676", "#f39c12", "#e74c3c", "#9b59b6", "#34495e", "#1abc9c", "#d81b60"]

        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct="%1.1f%%", 
            startangle=140, 
            colors=colors, 
            pctdistance=0.75,      
            labeldistance=1.2,    
            explode=[0.03] * len(labels) 
        )

        # Efek Donut 
        centre_circle = plt.Circle((0,0), 0.60, fc='white')
        self.figure.gca().add_artist(centre_circle)

        # Ukuran teks persen dikecilkan sedikit agar muat di potongan kecil
        plt.setp(autotexts, size=8, weight="bold", color="white")
        
        # Teks label kategori dibuat miring jika diperlukan (otomatis)
        plt.setp(texts, size=9, color="#2c3e50")

        ax.set_title(title, fontsize=13, fontweight='bold', color='#005088', pad=25)
        ax.axis("equal")

        self.canvas.draw()