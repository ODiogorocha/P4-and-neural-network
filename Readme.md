# Análise e Detecção de Anomalias em Tabelas de Fluxo BMv2 via Aprendizado de Máquina

Este repositório apresenta uma estrutura completa para a coleta, processamento e análise de dados de tabelas de fluxo de um switch programável **BMv2 (Behavioral Model v2)**, amplamente utilizado em ambientes de experimentação com **P4**. O principal objetivo é desenvolver e comparar diferentes modelos de aprendizado de máquina para identificar **anomalias ou inconsistências** nas entradas das tabelas de fluxo, contribuindo para a robustez e segurança de redes definidas por software (SDN).

## 1. Funcionalidades Principais

O projeto é modular e abrange as seguintes funcionalidades:

*   **Coleta de Dados P4**: Implementação de código P4 para instrumentar o switch BMv2, permitindo a extração programática de informações detalhadas das tabelas de fluxo (e.g., `ethernet_table`, `ipv4_table`).
*   **Processamento e Limpeza de Dados**: Scripts Python dedicados à extração, pré-processamento e limpeza dos dados brutos coletados do BMv2, transformando-os em um formato adequado para o treinamento de modelos de aprendizado de máquina.
*   **Modelos de Aprendizado de Máquina**: Implementação e treinamento de diversos algoritmos de Machine Learning para a detecção de padrões e anomalias nas tabelas de fluxo. Os modelos incluem:
    *   **Rede Neural Artificial (RNA)**: Abordagem de Deep Learning para capturar relações complexas nos dados.
    *   **Random Forest (RF)**: Modelo de ensemble robusto, conhecido por sua boa performance e interpretabilidade.
    *   **Modelo de ML Tradicional Adicional**: Exemplo de um algoritmo clássico (e.g., Regressão Logística, SVM) para comparação de desempenho.
*   **Avaliação de Desempenho**: Ferramentas para comparar a acurácia, precisão, recall, F1-score e outras métricas de desempenho de cada modelo, permitindo uma análise comparativa de suas capacidades de detecção de anomalias.
*   **Documentação Abrangente**: Instruções detalhadas para a instalação do ambiente, execução dos scripts e compreensão da arquitetura do projeto, facilitando a replicação e futuras extensões.

## 2. Estrutura do Repositório

A organização do repositório segue uma estrutura lógica para facilitar a navegação e o entendimento dos componentes do projeto:

```
./
├── p4_code/              # Contém o código P4 para instrumentação do switch BMv2 e arquivos de configuração.
├── data_collection/      # Scripts Python para coleta, pré-processamento e limpeza dos dados das tabelas.
├── models/               # Implementações e scripts de treinamento dos modelos de aprendizado de máquina.
├── evaluation/           # Scripts para avaliação de desempenho e comparação entre os modelos treinados.
├── README.md             # Este arquivo, fornecendo uma visão geral e instruções de alto nível do projeto.
├── documentation.md      # Documentação detalhada com instruções passo a passo para configuração e uso.
├── requirements.txt      # Lista de dependências Python necessárias para o projeto.
└── .gitignore            # Arquivo de configuração para ignorar arquivos e diretórios específicos no controle de versão.
```

## 3. Tecnologias Utilizadas

Este projeto faz uso das seguintes tecnologias e bibliotecas:

*   **P4**: Linguagem de programação para planos de dados, utilizada para definir o comportamento do switch e a coleta de dados.
*   **BMv2 (Behavioral Model v2)**: Um switch de software programável que simula o comportamento de um switch P4, ideal para experimentação e desenvolvimento.
*   **Python 3.8+**: Linguagem de programação principal para todos os scripts de coleta, processamento, modelagem e avaliação.
*   **Scikit-learn**: Biblioteca Python para aprendizado de máquina, utilizada para a implementação de modelos tradicionais e métricas de avaliação.
*   **TensorFlow/Keras**: Framework de Deep Learning para a construção e treinamento de Redes Neurais Artificiais.
*   **Pandas**: Biblioteca para manipulação e análise de dados, essencial para o pré-processamento e organização das tabelas de fluxo.
*   **NumPy**: Biblioteca fundamental para computação numérica em Python, utilizada para operações com arrays e matrizes.
*   **p4utils**: Biblioteca Python para interagir com switches P4, facilitando a coleta de dados via API Thrift.

## 4. Instalação

Para configurar o ambiente e executar o projeto, siga os passos abaixo:

1.  **Clone o repositório**: Utilize o Git para baixar o código-fonte do projeto.
    ```bash
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio
    ```
2.  **Crie e ative um ambiente virtual (recomendado)**: Isso ajuda a gerenciar as dependências do projeto isoladamente.
    ```bash
python3 -m venv venv
source venv/bin/activate
    ```
3.  **Instale as dependências Python**: As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
    ```bash
pip install -r requirements.txt
    ```
4.  **Configure o ambiente BMv2 e P4**: Este projeto requer um ambiente P4/BMv2 funcional. Consulte o arquivo `documentation.md` para instruções detalhadas sobre a instalação e configuração do `p4c` e `BMv2`.

## 5. Uso

Após a instalação e configuração do ambiente, você pode seguir o fluxo de trabalho do projeto:

1.  **Coleta de Dados**: 
    *   Compile e execute o código P4 no BMv2 conforme as instruções em `documentation.md`.
    *   Execute o script Python de coleta para extrair e salvar as entradas das tabelas de fluxo:
        ```bash
python data_collection/collect_data.py
        ```
2.  **Pré-processamento e Limpeza de Dados**: 
    *   Transforme os dados brutos em um formato utilizável e realize a limpeza:
        ```bash
python data_collection/preprocess_data.py
python data_collection/clean_data.py
        ```
3.  **Treinamento dos Modelos de Aprendizado de Máquina**: 
    *   Treine os diferentes modelos utilizando os dados limpos:
        ```bash
python models/train_neural_network.py
python models/train_random_forest.py
python models/train_ml_model.py
        ```
4.  **Avaliação de Eficiência**: 
    *   Compare o desempenho dos modelos treinados:
        ```bash
python evaluation/compare_models.py
        ```



