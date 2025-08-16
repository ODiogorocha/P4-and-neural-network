import pandas as pd
import os

def generate_report(results, output_file):
    with open(output_file, "w") as f:
        f.write("Relatório de Avaliação de Modelos\n")
        f.write("===================================\n\n")
        for model_name, metrics in results.items():
            f.write(f"Modelo: {model_name}\n")
            for metric, value in metrics.items():
                f.write(f" {metric.replace("\\'_\\', \\' \\'").title()}: {value:.4f}\n")
            f.write("\n")
    print(f"Relatório gerado em {output_file}")

if __name__ == '__main__':
    # Este script é um placeholder. Os resultados devem ser passados de compare_models.py
    # Exemplo de como os resultados seriam passados (apenas para demonstração):
    sample_results = {
        "Neural Network": {"accuracy": 0.85, "precision": 0.84, "recall": 0.86, "f1_score": 0.85},
        "Random Forest": {"accuracy": 0.88, "precision": 0.87, "recall": 0.88, "f1_score": 0.87},
        "Logistic Regression": {"accuracy": 0.82, "precision": 0.81, "recall": 0.83, "f1_score": 0.82}
    }
    output_report_path = os.path.join("evaluation", "model_evaluation_report.txt")
    generate_report(sample_results, output_report_path)


