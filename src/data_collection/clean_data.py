import pandas as pd
import os

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # Exemplo de limpeza: remover linhas com valores ausentes em colunas críticas
    # Adapte as colunas conforme a necessidade do seu dataset
    initial_rows = len(df)
    df.dropna(subset=["egress_port"], inplace=True) # Exemplo: egress_port não pode ser nulo
    rows_after_dropna = len(df)
    print(f"Removidas {initial_rows - rows_after_dropna} linhas com valores ausentes em colunas críticas.")

    # Exemplo de limpeza: remover duplicatas
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    rows_after_drop_duplicates = len(df)
    print(f"Removidas {initial_rows - rows_after_drop_duplicates} linhas duplicadas.")

    # Exemplo de limpeza: converter tipos de dados se necessário
    # df["egress_port"] = pd.to_numeric(df["egress_port"], errors=\'coerce\')

    # Salvar dados limpos
    df.to_csv(output_path, index=False)
    print(f"Dados limpos salvos em {output_path}")

if __name__ == '__main__':
    processed_dir = 'processed_data'
    cleaned_dir = 'cleaned_data'
    os.makedirs(cleaned_dir, exist_ok=True)

    # Limpar dados da tabela Ethernet
    ethernet_processed_path = os.path.join(processed_dir, 'processed_ethernet_data.csv')
    ethernet_cleaned_path = os.path.join(cleaned_dir, 'cleaned_ethernet_data.csv')
    if os.path.exists(ethernet_processed_path):
        clean_data(ethernet_processed_path, ethernet_cleaned_path)
    else:
        print(f"Arquivo {ethernet_processed_path} não encontrado. Pulando limpeza da tabela Ethernet.")

    # Limpar dados da tabela IPv4
    ipv4_processed_path = os.path.join(processed_dir, 'processed_ipv4_data.csv')
    ipv4_cleaned_path = os.path.join(cleaned_dir, 'cleaned_ipv4_data.csv')
    if os.path.exists(ipv4_processed_path):
        clean_data(ipv4_processed_path, ipv4_cleaned_path)
    else:
        print(f"Arquivo {ipv4_processed_path} não encontrado. Pulando limpeza da tabela IPv4.")


