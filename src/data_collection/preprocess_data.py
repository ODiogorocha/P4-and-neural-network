import pandas as pd
import json
import os

def preprocess_ethernet_entries(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    processed_data = []
    for entry in data:
        # Exemplo de como extrair e processar dados de uma entrada
        # Adapte isso com base na estrutura real das suas entradas de tabela
        match_fields = entry.get('match_fields', {})
        action_name = entry.get('action_name', 'N/A')
        action_params = entry.get('action_params', {})

        dst_mac = match_fields.get('hdr.ethernet.dstAddr', 'N/A')
        egress_port = action_params.get('port', 'N/A')

        processed_data.append({
            'dst_mac': dst_mac,
            'action_name': action_name,
            'egress_port': egress_port
        })
    return pd.DataFrame(processed_data)

def preprocess_ipv4_entries(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    processed_data = []
    for entry in data:
        match_fields = entry.get('match_fields', {})
        action_name = entry.get('action_name', 'N/A')
        action_params = entry.get('action_params', {})

        dst_ip = match_fields.get('hdr.ipv4.dstAddr', 'N/A')
        prefix_len = match_fields.get('hdr.ipv4.dstAddr_prefix_len', 'N/A')
        egress_port = action_params.get('port', 'N/A')
        dst_mac = action_params.get('dst_mac', 'N/A')

        processed_data.append({
            'dst_ip': dst_ip,
            'prefix_len': prefix_len,
            'action_name': action_name,
            'egress_port': egress_port,
            'dst_mac': dst_mac
        })
    return pd.DataFrame(processed_data)

if __name__ == '__main__':
    input_dir = 'collected_data'
    output_dir = 'processed_data'
    os.makedirs(output_dir, exist_ok=True)

    # Pré-processar e salvar dados da tabela Ethernet
    ethernet_json_path = os.path.join(input_dir, 'ethernet_table_entries.json')
    if os.path.exists(ethernet_json_path):
        df_ethernet = preprocess_ethernet_entries(ethernet_json_path)
        df_ethernet.to_csv(os.path.join(output_dir, 'processed_ethernet_data.csv'), index=False)
        print(f"Dados da ethernet_table pré-processados e salvos em {os.path.join(output_dir, 'processed_ethernet_data.csv')}")
    else:
        print(f"Arquivo {ethernet_json_path} não encontrado. Pulando pré-processamento da tabela Ethernet.")

    # Pré-processar e salvar dados da tabela IPv4
    ipv4_json_path = os.path.join(input_dir, 'ipv4_table_entries.json')
    if os.path.exists(ipv4_json_path):
        df_ipv4 = preprocess_ipv4_entries(ipv4_json_path)
        df_ipv4.to_csv(os.path.join(output_dir, 'processed_ipv4_data.csv'), index=False)
        print(f"Dados da ipv4_table pré-processados e salvos em {os.path.join(output_dir, 'processed_ipv4_data.csv')}")
    else:
        print(f"Arquivo {ipv4_json_path} não encontrado. Pulando pré-processamento da tabela IPv4.")


