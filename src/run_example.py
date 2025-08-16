import os
import subprocess
import time

def run_command(command, message):
    print(f"\n--- {message} ---")
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"Erro ao executar: {command}")
        print(process.stderr)
        # exit(1) # Descomente para parar a execução em caso de erro
    else:
        print(process.stdout)

if __name__ == '__main__':
    # 1. Compilar o código P4 (assumindo que p4c está no PATH)
    run_command("p4c --target bmv2 --arch v1model p4_code/basic_forwarding.p4 -o p4_code/basic_forwarding.json", "Compilando código P4")

    # 2. Iniciar o BMv2 (requer sudo e interfaces de rede configuradas, este é um exemplo simplificado)
    #    Para um ambiente real, você precisaria de interfaces veth ou similar.
    #    Este comando apenas demonstra o início, mas não manterá o BMv2 rodando em segundo plano para os próximos passos.
    #    Em um ambiente real, você iniciaria o BMv2 em um terminal separado ou como um serviço.
    print("\n--- Iniciando BMv2 (requer configuração manual de interfaces e execução em segundo plano para uso real) ---")
    print("Exemplo de comando para iniciar o BMv2 (execute em um terminal separado ou com nohup):")
    print("sudo simple_switch_grpc --thrift-port 9090 --log-file /tmp/bmv2.log --no-p4 -- --grpc-server-addr 0.0.0.0:50051 -i 0@veth0 -i 1@veth1")
    print("Após iniciar o BMv2, carregue o programa P4 com: simple_switch_CLI --thrift-port 9090 < p4_code/commands.txt")
    print("Aguarde alguns segundos para o BMv2 iniciar antes de prosseguir com a coleta de dados.")
    time.sleep(5) # Simula espera pelo BMv2

    # Criar diretórios de saída se não existirem
    os.makedirs("collected_data", exist_ok=True)
    os.makedirs("processed_data", exist_ok=True)
    os.makedirs("cleaned_data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("evaluation", exist_ok=True)

    # Criar arquivos dummy para simular dados coletados (para que os scripts de processamento e treinamento funcionem)
    # Em um cenário real, collect_data.py geraria estes arquivos.
    dummy_ethernet_data = [
        {"match_fields": {"hdr.ethernet.dstAddr": "00:00:00:00:00:01"}, "action_name": "set_egress_port", "action_params": {"port": 1}},
        {"match_fields": {"hdr.ethernet.dstAddr": "00:00:00:00:00:02"}, "action_name": "set_egress_port", "action_params": {"port": 2}},
        {"match_fields": {"hdr.ethernet.dstAddr": "00:00:00:00:00:03"}, "action_name": "set_egress_port", "action_params": {"port": 1}},
        {"match_fields": {"hdr.ethernet.dstAddr": "00:00:00:00:00:04"}, "action_name": "set_egress_port", "action_params": {"port": 2}},
        {"match_fields": {"hdr.ethernet.dstAddr": "00:00:00:00:00:05"}, "action_name": "set_egress_port", "action_params": {"port": 1}},
    ]
    dummy_ipv4_data = [
        {"match_fields": {"hdr.ipv4.dstAddr": "10.0.1.1", "hdr.ipv4.dstAddr_prefix_len": 24}, "action_name": "ipv4_forward", "action_params": {"port": 1, "dst_mac": "00:00:00:00:00:01"}},
        {"match_fields": {"hdr.ipv4.dstAddr": "10.0.2.1", "hdr.ipv4.dstAddr_prefix_len": 24}, "action_name": "ipv4_forward", "action_params": {"port": 2, "dst_mac": "00:00:00:00:00:02"}},
        {"match_fields": {"hdr.ipv4.dstAddr": "10.0.1.2", "hdr.ipv4.dstAddr_prefix_len": 24}, "action_name": "ipv4_forward", "action_params": {"port": 1, "dst_mac": "00:00:00:00:00:01"}},
        {"match_fields": {"hdr.ipv4.dstAddr": "10.0.3.1", "hdr.ipv4.dstAddr_prefix_len": 24}, "action_name": "ipv4_forward", "action_params": {"port": 3, "dst_mac": "00:00:00:00:00:03"}},
        {"match_fields": {"hdr.ipv4.dstAddr": "10.0.2.2", "hdr.ipv4.dstAddr_prefix_len": 24}, "action_name": "ipv4_forward", "action_params": {"port": 2, "dst_mac": "00:00:00:00:00:02"}},
    ]
    import json
    with open("collected_data/ethernet_table_entries.json", "w") as f: json.dump(dummy_ethernet_data, f, indent=4)
    with open("collected_data/ipv4_table_entries.json", "w") as f: json.dump(dummy_ipv4_data, f, indent=4)
    print("\n--- Arquivos dummy de dados coletados criados para simulação. ---")

    # 3. Coleta de Dados (neste exemplo, simulada pelos arquivos dummy)
    # run_command("python data_collection/collect_data.py --p4_name basic_forwarding --thrift_port 9090 --output_dir collected_data", "Coletando dados das tabelas")

    # 4. Pré-processamento de Dados
    run_command("python data_collection/preprocess_data.py", "Pré-processando dados")

    # 5. Limpeza de Dados
    run_command("python data_collection/clean_data.py", "Limpando dados")

    # 6. Treinamento dos Modelos
    run_command("python models/train_neural_network.py", "Treinando Rede Neural Artificial")
    run_command("python models/train_random_forest.py", "Treinando Random Forest")
    run_command("python models/train_ml_model.py", "Treinando Modelo ML Tradicional (Regressão Logística)")

    # 7. Avaliação de Eficiência
    run_command("python evaluation/compare_models.py", "Comparando Modelos")

    print("\n--- Exemplo de execução do projeto concluído. ---")
    print("Verifique os diretórios 'collected_data', 'processed_data', 'cleaned_data', 'models' e 'evaluation' para os resultados.")


