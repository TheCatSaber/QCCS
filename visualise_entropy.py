import matplotlib.pyplot as plt

from information_theory import ClassicalPDF


def visualize_pdf(PDF: ClassicalPDF):
    plt.bar(range(1, len(PDF) + 1), [x.probability for x in PDF], tick_label=[x.symbol for x in PDF])  # type: ignore
    plt.show()
