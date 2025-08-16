import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import os

def train_nn_model(data_path, model_save_path):
    # Carregar dados pré-processados
    df = pd.read_csv(data_path)

    # Exemplo de pré-processamento para o modelo
    # Assumindo que a coluna 'egress_port' é o target e as outras são features
    # Você precisará adaptar isso à sua estrutura de dados real
    
    # Codificar a coluna 'action_name' se for categórica
    if 'action_name' in df.columns:
        le = LabelEncoder()
        df['action_name_encoded'] = le.fit_transform(df['action_name'])
        # Salvar o LabelEncoder para uso posterior na inferência
        # import joblib
        # joblib.dump(le, 'label_encoder_action_name.pkl')

    # Selecionar features e target
    # Remova colunas que não são numéricas ou que não devem ser usadas como features
    # Exemplo: 'dst_mac' e 'dst_ip' podem precisar de codificação ou hashing
    features = [col for col in df.columns if col not in ["egress_port", "action_name", "dst_mac", "dst_ip"]]
    if 'action_name_encoded' in df.columns:
        features.append('action_name_encoded')

    X = df[features].fillna(0) # Preencher NaNs com 0 ou outra estratégia
    y = df["egress_port"]

    # Converter 'egress_port' para categórico se for um problema de classificação multi-classe
    # Se for regressão, mantenha como está
    y = to_categorical(y) # Assumindo que egress_port são inteiros sequenciais a partir de 0

    # Dividir dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Construir o modelo da Rede Neural Artificial
    model = Sequential([
        Dense(64, activation=\'relu\', input_shape=(X_train.shape[1],)),
        Dense(32, activation=\'relu\'),
        Dense(y.shape[1], activation=\'softmax\') # Saída para classificação multi-classe
    ])

    # Compilar o modelo
    model.compile(optimizer=\'adam\', loss=\'categorical_crossentropy\', metrics=[\'accuracy\'])

    # Treinar o modelo
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=0)

    # Avaliar o modelo
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Acurácia do modelo de Rede Neural Artificial: {accuracy:.4f}")

    # Salvar o modelo
    model.save(model_save_path)
    print(f"Modelo de Rede Neural Artificial salvo em {model_save_path}")

if __name__ == \'__main__\':
    # Exemplo de uso para a tabela ethernet
    ethernet_data_path = os.path.join("processed_data", "processed_ethernet_data.csv")
    ethernet_model_path = os.path.join("models", "neural_network_ethernet.h5")
    if os.path.exists(ethernet_data_path):
        train_nn_model(ethernet_data_path, ethernet_model_path)
    else:
        print(f"Dados para ethernet_table não encontrados em {ethernet_data_path}. Pulando treinamento da NN para Ethernet.")

    # Exemplo de uso para a tabela ipv4
    ipv4_data_path = os.path.join("processed_data", "processed_ipv4_data.csv")
    ipv4_model_path = os.path.join("models", "neural_network_ipv4.h5")
    if os.path.exists(ipv4_data_path):
        train_nn_model(ipv4_data_path, ipv4_model_path)
    else:
        print(f"Dados para ipv4_table não encontrados em {ipv4_data_path}. Pulando treinamento da NN para IPv4.")


