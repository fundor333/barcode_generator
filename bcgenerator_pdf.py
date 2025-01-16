"""
Script per generare EAN13

Va chiamato passando come argomenti il path del csv di input e il path per l'output

Esempio d'uso
python bcgenerator_pdf.py example.csv example.pdf

Dipendenze:
pip install reportlab pillow
"""

from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import csv
import sys


class A4Printer:

    def generate_label(
        self,
        ean13: str,
        description: str,
        n_label_x: int,
        n_label_y: int,
        label_w: float = 0.0,
        label_h: float = 0.0,
        bar_with: float = 1.5,
        bar_height: float = 51.0,
    ) -> Drawing:
        """
        Generate a drawing with EAN-13 barcode and descriptive text.
        :param ean13: The EAN-13 Code.
        :type ean13: str
        :param description: Short product description.
        :type description: str
        :return: Drawing with barcode and description
        :rtype: Drawing
        """
        if label_w == 0.0:
            label_w = A4[0] / n_label_x
        if label_h == 0.0:
            label_h = A4[1] / n_label_y
        text = String(
            0,
            80,
            description,
            fontName="Helvetica",
            fontSize=6,
            textAnchor="middle",
        )
        text.x = label_w / 2

        barcode = Ean13BarcodeWidget(ean13)
        barcode.barWidth = bar_with
        barcode.barHeight = bar_height
        _, _, bw, _ = barcode.getBounds()
        barcode.x = (label_w - bw) / 2  # center barcode
        barcode.y = 18  # spacing from label bottom (pt)

        label_drawing = Drawing(label_w, label_h)
        label_drawing.add(text)
        label_drawing.add(barcode)
        return label_drawing

    def get_pdf(
        self,
        datas: list[str, str],
        filepath: str | None,
        pagesize: list[float, float] | None = None,
        n_lab_x=3,
        n_lab_y=8,
    ):
        if pagesize is None:
            pagesize = A4
        if filepath is None:
            filepath = "hello-world.pdf"

        lab_w = pagesize[0] / n_lab_x
        lab_h = pagesize[1] / n_lab_y
        sheet_t = pagesize[1]

        p = canvas.Canvas(filename=filepath, pagesize=pagesize)
        j = 0
        print(datas)
        for _ in range(len(datas) // (n_lab_x * n_lab_y) + 1):
            for u in range(0, n_lab_y):
                for i in range(0, n_lab_x):
                    if j < len(datas):
                        data = datas[j]
                        cb, desc = data
                        try:
                            label = self.generate_label(
                                ean13=cb,
                                description=desc,
                                n_label_x=n_lab_x,
                                n_label_y=n_lab_y,
                            )
                            x = i * lab_w
                            y = sheet_t - lab_h - u * lab_h
                            label.drawOn(p, x, y)
                        except AttributeError:
                            pass
                        j += 1
            p.showPage()
        p.save()


def run(path_csv: str, path_out: str):
    with open(path_csv) as file:
        csv_file = list(csv.reader(file, delimiter=","))
        A4Printer().get_pdf(datas=csv_file, filepath=path_out)


_, path_csv, path_out = sys.argv

run(
    path_csv=path_csv,
    path_out=path_out,
)
