# EP1 - Sistema de Atendimento com Clientes Impacientes

Trabalho da disciplina **ACH2158 - Simulação de Sistemas Complexos**.

Este repositório contém a solução do EP1 sobre o problema de **balcão de atendimento com fila e clientes impacientes**. O modelo usado segue o algoritmo descrito nos slides do Problema 2: chegadas por processo de Poisson com taxa λ, tempos de atendimento exponenciais com parâmetro μ, fila única e desistência com probabilidade p_r = r/(r+n) quando o cliente encontra fila de tamanho r

## Enunciado resumido

No **subproblema 1**, o cenário pedido é T = 50, n = 5, λ = 3, μ = 0.5, com incremento de N em blocos de 500 até que a amplitude do intervalo de confiança de 95% para W seja menor que 0.002. Também são pedidos:
- gráfico de convergência de W_k;
- gráfico de convergência de TM_k;
- histogramas de`W e tm
- médias finais X, Y, W, TM;
- Pr_d(tm > 13);
- o valor w_s tal que Pr_d(w > w_s) < 5%, isto é, o quantil 0.95 de w. 

No **subproblema 2**, o cenário pedido é λ = 4, μ = 0.5, T = 60, e deve-se determinar o menor número de guichês n tal que Pr(W ≤ 20%) ≥ 0.95. 

## Estrutura do repositório

- ep1_solucao_final.py` 
  Código-fonte da simulação.

- outputs/subproblema1/  
  Gráficos e resumo do subproblema 1.

- outputs/subproblema2/
  Resumo do subproblema 2.

## Como executar

### Requisitos
- Python 3
- Bibliotecas:
  - numpy
  - matplotlib

### Instalação das dependências
```bash
pip install numpy matplotlib
Execução
python ep1_solucao_final.py

Após a execução, os arquivos de saída serão gerados nas pastas de resultados.

Metodologia

Cada replicação da simulação retorna a tupla:

x: número de clientes atendidos;
y: número de clientes que foram embora sem entrar na fila;
r: comprimento da fila no instante final;
w: proporção de clientes que foram embora;
tm: tempo máximo de permanência entre os clientes atendidos.

Para o subproblema 1, as replicações são acumuladas em blocos de 500 até que a amplitude do IC95% de W satisfaça:

|LS - LI| = 2 × 1.96 × ep(μ̂W) < 0.002

conforme pedido no enunciado.

Resultados obtidos
Subproblema 1

Na execução realizada, foram obtidos os seguintes resultados:

N = 15000
X̄ = 115.5702
Ȳ = 31.8665
W̄ = 0.209308
TM̄ = 11.569855
Pr_d(tm > 13) = 0.2434
w_s = 0.312886
Subproblema 2

Foi testado o número de guichês n até encontrar o menor valor que satisfaz:

Pr(W ≤ 0.20) ≥ 0.95

Na execução realizada, a resposta encontrada foi:

menor n = 8


Observação

Como se trata de um método de simulação estocástica, pequenas variações podem ocorrer entre execuções dependendo da semente aleatória utilizada. Ainda assim, a estrutura do algoritmo e o procedimento experimental seguem diretamente o enunciado e os slides fornecidos.
