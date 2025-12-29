import numpy as np
import matplotlib.pyplot as plt


def plot_predicted_vs_actual(labels, predicted_vals, actual_vals, output_path: str) -> None:
    x = np.arange(len(labels))
    width = 0.38

    plt.figure()
    plt.bar(x - width / 2, predicted_vals, width, label="Predicted y_2024")
    plt.bar(x + width / 2, actual_vals, width, label="Actual y_2024")
    plt.xticks(x, labels, rotation=15, ha="right")
    plt.ylabel("GDP per capita (constant 2015 US$)")
    plt.title("Germany 2024: Predicted vs Actual GDP per capita (3 cases)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_errors(labels, errors, output_path: str) -> None:
    x = np.arange(len(labels))

    plt.figure()
    plt.bar(x, errors)
    plt.axhline(0)
    plt.xticks(x, labels, rotation=15, ha="right")
    plt.ylabel("Prediction error (%) = (Actual − Predicted) / Predicted · 100")
    plt.title("Germany 2024: Prediction error by case")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
