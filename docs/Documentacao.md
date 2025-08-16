# Documentação Detalhada do Projeto

Este documento fornece instruções detalhadas para a instalação, configuração e execução do projeto de análise de tabelas de switch BMv2 com modelos de aprendizado de máquina.

## 1. Visão Geral do Projeto

O objetivo principal deste projeto é desenvolver um sistema capaz de coletar e analisar dados de tabelas de fluxo de um switch programável BMv2, utilizando técnicas de aprendizado de máquina para identificar anomalias ou inconsistências. O projeto abrange desde a programação do switch em P4 até a implementação e avaliação de diferentes modelos de IA.

## 2. Pré-requisitos

Para executar este projeto, você precisará dos seguintes componentes instalados e configurados em seu ambiente:

*   **Sistema Operacional**: Linux (preferencialmente Ubuntu 18.04 LTS ou superior).
*   **P4 Development Environment**: Incluindo o compilador `p4c` e o switch `BMv2`.
    *   Siga as instruções oficiais para instalação do P4 e BMv2: [https://github.com/p4lang/p4c](https://github.com/p4lang/p4c) e [https://github.com/p4lang/behavioral-model](https://github.com/p4lang/behavioral-model)
*   **Python 3.8+**: Com `pip` para gerenciamento de pacotes.
*   **Git**: Para clonar o repositório.

## 3. Instalação

Siga os passos abaixo para configurar o ambiente do projeto:

### 3.1. Clonar o Repositório

```bash
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio
```

### 3.2. Instalar Dependências Python

Certifique-se de ter um ambiente virtual ativado (recomendado) antes de instalar as dependências:

```bash
pip install -r requirements.txt
```

### 3.3. Configuração do Ambiente BMv2 e P4

Este projeto assume que você tem o ambiente P4/BMv2 configurado corretamente. Se não tiver, siga as instruções nos links abaixo:

*   **Instalação do p4c**: [https://github.com/p4lang/p4c](https://github.com/p4lang/p4c)
*   **Instalação do behavioral-model (BMv2)**: [https://github.com/p4lang/behavioral-model](https://github.com/p4lang/behavioral-model)

Certifique-se de que o `simple_switch_grpc` e o `p4c` estejam acessíveis no seu `PATH` ou que você saiba o caminho completo para eles.

## 4. Uso do Projeto

Esta seção detalha os passos para utilizar o projeto, desde a compilação do código P4 até a avaliação dos modelos de aprendizado de máquina.

### 4.1. Compilação e Execução do Código P4 no BMv2

O arquivo `p4_code/basic_forwarding.p4` contém a lógica de encaminhamento e as tabelas que serão monitoradas. Para compilar e executar o BMv2, siga os passos abaixo:

1.  **Compile o programa P4**: Utilize o compilador `p4c` para gerar o arquivo JSON do programa. Ajuste o caminho para o seu compilador `p4c` conforme necessário.
    ```bash
p4c --target bmv2 --arch v1model p4_code/basic_forwarding.p4 -o p4_code/basic_forwarding.json
    ```
2.  **Inicie o BMv2 (simple_switch_grpc)**: Este comando inicia o switch BMv2. Para um ambiente real, você precisará configurar interfaces de rede (ex: `veth0`, `veth1`).
    ```bash
sudo simple_switch_grpc --thrift-port 9090 --log-file /tmp/bmv2.log --no-p4 -- --grpc-server-addr 0.0.0.0:50051 -i 0@veth0 -i 1@veth1 -i 2@veth2
    ```
    *   `--thrift-port 9090`: Define a porta para a API Thrift, utilizada para coletar as entradas das tabelas.
    *   `--no-p4`: Inicia o switch sem carregar um programa P4 inicialmente.
    *   `--grpc-server-addr`: Endereço do servidor gRPC (opcional, mas útil para controle).
    *   `-i 0@veth0`: Exemplo de interface de rede. Adapte conforme a sua topologia de rede.

3.  **Carregue o programa P4 compilado no BMv2**: Em um terminal separado, utilize o `simple_switch_CLI` para carregar o arquivo JSON compilado. Você pode precisar criar um arquivo `commands.txt` com as regras iniciais para as tabelas, se aplicável.
    ```bash
simple_switch_CLI --thrift-port 9090 < p4_code/commands.txt
    ```

### 4.2. Coleta de Dados

Com o BMv2 em execução e o programa P4 carregado, execute o script Python para coletar os dados das tabelas:

```bash
python data_collection/collect_data.py --p4_name basic_forwarding --thrift_port 9090 --output_dir collected_data
```

Este script se conectará ao BMv2 via API Thrift, extrairá as entradas das tabelas `ethernet_table` e `ipv4_table`, e as salvará em arquivos JSON no diretório `collected_data`.

### 4.3. Pré-processamento e Limpeza de Dados

Após a coleta, os dados brutos precisam ser pré-processados e limpos para serem utilizados pelos modelos de aprendizado de máquina. Execute os seguintes scripts:

```bash
python data_collection/preprocess_data.py
python data_collection/clean_data.py
```

*   `preprocess_data.py`: Converte os arquivos JSON brutos em formato CSV, extraindo os campos relevantes para a análise.
*   `clean_data.py`: Realiza a limpeza dos dados, incluindo a remoção de duplicatas e o tratamento de valores ausentes.

Os arquivos CSV pré-processados e limpos serão salvos nos diretórios `processed_data` e `cleaned_data`, respectivamente.

### 4.4. Treinamento dos Modelos de Aprendizado de Máquina

Os scripts de treinamento utilizarão os dados limpos para treinar os modelos. Certifique-se de que os arquivos CSV limpos estejam disponíveis nos diretórios esperados antes de executar:

```bash
python models/train_neural_network.py
python models/train_random_forest.py
python models/train_ml_model.py
```

Cada script treinará um modelo específico (Rede Neural Artificial, Random Forest e Regressão Logística, como exemplo de ML tradicional) e salvará o modelo treinado (em formato `.h5` para Redes Neurais e `.pkl` para Random Forest/Regressão Logística) no diretório `models`.

### 4.5. Avaliação de Eficiência dos Modelos

Para comparar o desempenho dos modelos treinados, execute o script de avaliação:

```bash
python evaluation/compare_models.py
```

Este script carregará os modelos treinados, avaliará seu desempenho utilizando métricas como acurácia, precisão, recall e F1-score, e exibirá os resultados no console. Ele também pode ser integrado para gerar um relatório detalhado através do script `generate_report.py`.



## 5. Estrutura de Dados e Adaptação

Os scripts de pré-processamento e treinamento (`preprocess_data.py`, `train_*.py`) contêm exemplos de como as colunas `dst_mac`, `dst_ip`, `action_name` e `egress_port` são tratadas. **É crucial que você adapte a lógica de extração e pré-processamento de dados** para corresponder exatamente à estrutura das entradas de tabela que seu programa P4 está gerando e aos campos que você deseja analisar.

*   **`egress_port`**: Assumido como a variável alvo (target) para os modelos de classificação. Se seu objetivo for outro (ex: detecção de anomalias sem um target claro), a abordagem do modelo precisará ser ajustada (ex: uso de modelos de detecção de anomalias não supervisionados).
*   **Codificação de Features**: Endereços MAC e IP, bem como nomes de ações, são tratados como strings e podem precisar de codificação numérica (ex: `LabelEncoder`, `OneHotEncoder`, ou técnicas de hashing) para serem usados por modelos de ML. Os scripts fornecem um exemplo básico com `LabelEncoder` para `action_name`.
