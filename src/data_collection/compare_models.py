import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.models import load_model
import joblib
import os

def evaluate_model(model, X_test, y_test, model_name):
    if model_name == "Neural Network":
        _, accuracy = model.evaluate(X_test, y_test, verbose=0)
        y_pred = np.argmax(model.predict(X_test), axis=1)
        y_test_labels = np.argmax(y_test, axis=1)
    else:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        y_test_labels = y_test

    precision = precision_score(y_test_labels, y_pred, average=\'weighted\', zero_division=0)
    recall = recall_score(y_test_labels, y_pred, average=\'weighted\', zero_division=0)
    f1 = f1_score(y_test_labels, y_pred, average=\'weighted\', zero_division=0)

    print(f"\n--- Avaliação do Modelo: {model_name} ---")
    print(f"Acurácia: {accuracy:.4f}")
    print(f"Precisão: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    return accuracy, precision, recall, f1

def compare_models(data_path, nn_model_path, rf_model_path, ml_model_path):
    df = pd.read_csv(data_path)

    if 'action_name' in df.columns:
        le = LabelEncoder()
        df['action_name_encoded'] = le.fit_transform(df['action_name'])

    features = [col for col in df.columns if col not in ["egress_port", "action_name", "dst_mac", "dst_ip"]]
    if 'action_name_encoded' in df.columns:
        features.append('action_name_encoded')

    X = df[features].fillna(0)
    y = df["egress_port"]

    # Para NN, y precisa ser one-hot encoded
    from tensorflow.keras.utils import to_categorical
    y_nn = to_categorical(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    _, _, _, y_test_nn = train_test_split(X, y_nn, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    results = {}

    # Avaliar Rede Neural Artificial
    if os.path.exists(nn_model_path):
        nn_model = load_model(nn_model_path)
        acc, prec, rec, f1 = evaluate_model(nn_model, X_test, y_test_nn, "Neural Network")
        results["Neural Network"] = {"accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1}
    else:
        print(f"Modelo de Rede Neural não encontrado em {nn_model_path}")

    # Avaliar Random Forest
    if os.path.exists(rf_model_path):
        rf_model = joblib.load(rf_model_path)
        acc, prec, rec, f1 = evaluate_model(rf_model, X_test, y_test, "Random Forest")
        results["Random Forest"] = {"accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1}
    else:
        print(f"Modelo Random Forest não encontrado em {rf_model_path}")

    # Avaliar Modelo ML Tradicional (Regressão Logística)
    if os.path.exists(ml_model_path):
        ml_model = joblib.load(ml_model_path)
        acc, prec, rec, f1 = evaluate_model(ml_model, X_test, y_test, "Logistic Regression")
        results["Logistic Regression"] = {"accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1}
    else:
        print(f"Modelo ML Tradicional não encontrado em {ml_model_path}")

    print("\n--- Resumo dos Resultados ---")
    for model_name, metrics in results.items():
        print(f"Modelo: {model_name}")
        for metric, value in metrics.items():
            print(f"  {metric.replace("\'_\', \' \'").title()}: {value:.4f}")

if __name__ == '__main__':
    # Exemplo de uso para a tabela ethernet
    print("\nComparando modelos para a tabela Ethernet:")
    ethernet_data_path = os.path.join("processed_data", "processed_ethernet_data.csv")
    ethernet_nn_model = os.path.join("models", "neural_network_ethernet.h5")
    ethernet_rf_model = os.path.join("models", "random_forest_ethernet.pkl")
    ethernet_ml_model = os.path.join("models", "logistic_regression_ethernet.pkl")
    compare_models(ethernet_data_path, ethernet_nn_model, ethernet_rf_model, ethernet_ml_model)

    # Exemplo de uso para a tabela ipv4
    print("\nComparando modelos para a tabela IPv4:")
    ipv4_data_path = os.path.join("processed_data", "processed_ipv4_data.csv")
    ipv4_nn_model = os.path.join("models", "neural_network_ipv4.h5")
    ipv4_rf_model = os.path.join("models", "random_forest_ipv4.pkl")
    ipv4_ml_model = os.path.join("models", "logistic_regression_ipv4.pkl")
    compare_models(ipv4_data_path, ipv4_nn_model, ipv4_rf_model, ipv4_ml_model)


