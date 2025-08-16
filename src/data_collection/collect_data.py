import argparse
import json
import os
import time
from p4utils.utils.thrift_API import ThriftAPI

def collect_table_entries(p4_name, thrift_port, output_dir):
    client = ThriftAPI(p4_name, thrift_port)
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Coletar entradas da tabela ethernet_table
    ethernet_entries = client.get_entries('ethernet_table')
    with open(os.path.join(output_dir, 'ethernet_table_entries.json'), 'w') as f:
        json.dump(ethernet_entries, f, indent=4)
    print(f"Coletadas {len(ethernet_entries)} entradas da ethernet_table.")

    # Coletar entradas da tabela ipv4_table
    ipv4_entries = client.get_entries('ipv4_table')
    with open(os.path.join(output_dir, 'ipv4_table_entries.json'), 'w') as f:
        json.dump(ipv4_entries, f, indent=4)
    print(f"Coletadas {len(ipv4_entries)} entradas da ipv4_table.")

    print("Coleta de dados concluída.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coleta entradas de tabelas de um switch BMv2.')
    parser.add_argument('--p4_name', type=str, default='basic_forwarding', help='Nome do programa P4.')
    parser.add_argument('--thrift_port', type=int, default=9090, help='Porta Thrift do BMv2.')
    parser.add_argument('--output_dir', type=str, default='collected_data', help='Diretório para salvar os dados coletados.')
    args = parser.parse_args()

    collect_table_entries(args.p4_name, args.thrift_port, args.output_dir)


