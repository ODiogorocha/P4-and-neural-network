Segue a **documentação detalhada** no formato solicitado.
Estruturei como se fosse um **relatório técnico de pesquisa**, explicando passo a passo o funcionamento, uso e implementação dos códigos, para atender ao padrão acadêmico/profissional.

---

# Documentation.md

## 1. Introdução

Este projeto foi desenvolvido para **coletar e analisar tabelas históricas de um switch P4 (BMv2)**, utilizando diferentes abordagens de Inteligência Artificial e Aprendizado de Máquina.
O objetivo principal é identificar **possíveis erros ou inconsistências** nessas tabelas, comparando a eficácia de três modelos diferentes:

1. **Rede Neural Artificial (ANN)**
2. **Random Forest (RF)**
3. **Modelo de Aprendizado de Máquina Tradicional**

Além disso, o projeto inclui um **script em P4** para extrair as tabelas diretamente do BMv2 e um **script de análise comparativa** para medir a eficiência dos modelos.

---

## 2. Estrutura do Projeto

A organização dos arquivos segue um padrão para facilitar a manutenção:

```
├── p4_switch_code/           # Código P4 para coleta das tabelas do BMv2
│   ├── table_extractor.p4
│
├── data/                     # Armazena as tabelas extraídas
│   ├── switch_tables.csv
│
├── models/                   # Implementações dos modelos de IA e ML
│   ├── neural_network.py
│   ├── random_forest.py
│   ├── ml_model.py
│
├── analysis/                 # Código para avaliar a eficiência dos modelos
│   ├── efficiency_analysis.py
│
├── main.py                    # Script principal para execução do pipeline
├── requirements.txt           # Dependências do projeto
├── README.md                  # Descrição geral do projeto
└── Documentation.md           # Documentação técnica detalhada
```

---

## 3. Tecnologias Utilizadas

* **P4** → Programação do pipeline do switch BMv2
* **BMv2 (Behavioral Model)** → Switch virtual que executa o código P4
* **Python 3.10+** → Linguagem de integração, análise e IA
* **Scikit-learn** → Modelos de Machine Learning
* **TensorFlow / Keras** → Rede Neural Artificial
* **Pandas / NumPy** → Manipulação e análise de dados
* **Matplotlib / Seaborn** → Visualização dos resultados

---

## 4. Funcionamento

O processo completo é dividido em **4 etapas principais**:

### 4.1 Coleta das Tabelas no Switch (P4)

* O código `table_extractor.p4` é carregado no BMv2.
* Ele intercepta e exporta as tabelas históricas do switch, salvando-as em formato CSV.
* Essas tabelas incluem informações como:

  * Regras instaladas
  * Contadores de pacotes
  * Estatísticas de portas
  * Erros detectados pelo pipeline

### 4.2 Pré-processamento dos Dados

* Os arquivos CSV extraídos são carregados pelo Python.
* É feita a **limpeza** dos dados:

  * Remoção de colunas irrelevantes
  * Normalização de valores
  * Conversão de dados categóricos para numéricos
* Os dados são então divididos em **treinamento** e **teste**.

### 4.3 Treinamento dos Modelos

* **Rede Neural Artificial (ANN)**:
  Estrutura densa (`Dense`) com múltiplas camadas ocultas e função de ativação `ReLU`.
  Treinada com otimizador `Adam` e função de perda `binary_crossentropy` ou `mse` dependendo do tipo de detecção.

* **Random Forest (RF)**:
  Modelo baseado em múltiplas árvores de decisão, robusto contra ruído e bom para detectar padrões não lineares.

* **Modelo Tradicional de ML**:
  Implementação simples, como **Regressão Logística** ou **SVM**, para comparação de desempenho.

### 4.4 Análise de Eficiência

* O script `efficiency_analysis.py` calcula métricas como:

  * **Acurácia**
  * **Precisão**
  * **Recall**
  * **F1-score**
  * **Tempo de execução**
* É gerado um relatório comparativo, identificando qual modelo apresentou o melhor desempenho.

---

## 5. Como Usar

### 5.1 Requisitos

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 5.2 Executar o Switch BMv2 com o Código P4

```bash
simple_switch --log-console build/table_extractor.json
```

### 5.3 Extrair as Tabelas

O script Python se conecta ao BMv2 via API Thrift e salva as tabelas:

```bash
python main.py --extract
```

### 5.4 Treinar e Avaliar os Modelos

Para rodar a análise de IA:

```bash
python main.py --analyze
```

---

## 6. Resultados Esperados

Ao final da execução, o projeto fornece:

* Arquivo CSV com tabelas extraídas do BMv2
* Relatórios de desempenho para cada modelo de IA/ML
* Comparação visual em gráficos

---

## 7. Aplicações

* Diagnóstico automático de problemas em redes programáveis
* Suporte à pesquisa acadêmica em detecção de falhas em P4
* Base para desenvolvimento de sistemas de monitoramento inteligentes

---