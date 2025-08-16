import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

def train_lr_model(data_path, model_save_path):
    # Carregar dados pré-processados
    df = pd.read_csv(data_path)

    # Exemplo de pré-processamento para o modelo
    if 'action_name' in df.columns:
        le = LabelEncoder()
        df['action_name_encoded'] = le.fit_transform(df['action_name'])

    features = [col for col in df.columns if col not in ["egress_port", "action_name", "dst_mac", "dst_ip"]]
    if 'action_name_encoded' in df.columns:
        features.append('action_name_encoded')

    X = df[features].fillna(0)
    y = df["egress_port"]

    # Dividir dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Construir e treinar o modelo de Regressão Logística
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Avaliar o modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo de Regressão Logística: {accuracy:.4f}")

    # Salvar o modelo
    joblib.dump(model, model_save_path)
    print(f"Modelo de Regressão Logística salvo em {model_save_path}")

if __name__ == '__main__':
    # Exemplo de uso para a tabela ethernet
    ethernet_data_path = os.path.join("processed_data", "processed_ethernet_data.csv")
    ethernet_model_path = os.path.join("models", "logistic_regression_ethernet.pkl")
    if os.path.exists(ethernet_data_path):
        train_lr_model(ethernet_data_path, ethernet_model_path)
    else:
        print(f"Dados para ethernet_table não encontrados em {ethernet_data_path}. Pulando treinamento da LR para Ethernet.")

    # Exemplo de uso para a tabela ipv4
    ipv4_data_path = os.path.join("processed_data", "processed_ipv4_data.csv")
    ipv4_model_path = os.path.join("models", "logistic_regression_ipv4.pkl")
    if os.path.exists(ipv4_data_path):
        train_lr_model(ipv4_data_path, ipv4_model_path)
    else:
        print(f"Dados para ipv4_table não encontrados em {ipv4_data_path}. Pulando treinamento da LR para IPv4.")


