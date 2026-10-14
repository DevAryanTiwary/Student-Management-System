from PySide6.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, dark_mode=True):
        bg = "#1A1D24" if dark_mode else "#FFFFFF"
        fg = "#E2E8F0" if dark_mode else "#2D3748"
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=bg)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor(bg)
        self.axes.tick_params(colors=fg)
        self.axes.xaxis.label.set_color(fg)
        self.axes.yaxis.label.set_color(fg)
        for spine in self.axes.spines.values():
            spine.set_color("#2D3748" if dark_mode else "#CBD5E0")
        super().__init__(self.fig)

class ChartView(QWidget):
    def __init__(self, dark_mode: bool = True, parent=None):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = MplCanvas(self, dark_mode=self.dark_mode)
        self.layout.addWidget(self.canvas)

    def render_bar(self, labels: list, values: list, title: str, xlabel: str = "", ylabel: str = "", color="#3182CE"):
        self.canvas.axes.clear()
        fg = "#E2E8F0" if self.dark_mode else "#2D3748"
        self.canvas.axes.bar(labels, values, color=color, edgecolor="#2B6CB0", width=0.5)
        self.canvas.axes.set_title(title, color=fg, fontsize=12, fontweight="bold", pad=10)
        if xlabel: self.canvas.axes.set_xlabel(xlabel, color=fg)
        if ylabel: self.canvas.axes.set_ylabel(ylabel, color=fg)
        self.canvas.fig.tight_layout()
        self.canvas.draw()

    def render_pie(self, labels: list, values: list, title: str, colors: list = None):
        self.canvas.axes.clear()
        fg = "#E2E8F0" if self.dark_mode else "#2D3748"
        if sum(values) == 0:
            self.canvas.axes.text(0.5, 0.5, "No Data Available", horizontalalignment='center', color=fg)
        else:
            self.canvas.axes.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=140,
                textprops={'color': fg, 'fontsize': 10},
                colors=colors
            )
        self.canvas.axes.set_title(title, color=fg, fontsize=12, fontweight="bold", pad=10)
        self.canvas.fig.tight_layout()
        self.canvas.draw()