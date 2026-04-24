EP1 resolvido com base no PDF do enunciado e nos slides do problema 2.

Arquivos principais:
- `subproblema1_convergencia_W_detalhado.png`  
  Gráfico detalhado da convergência das médias parciais de `W`, com intervalo de confiança de 95% e indicação da média final estimada.

- `subproblema1_convergencia_TM_detalhado.png`  
  Gráfico detalhado da convergência das médias parciais de `TM`, com intervalo de confiança de 95% e indicação da média final estimada.

- `subproblema1_histograma_W_detalhado.png`  
  Histograma detalhado dos valores simulados de `W`, com marcações de média, mediana e quantil 0.95.

- `subproblema1_histograma_TM_detalhado.png`  
  Histograma detalhado dos valores simulados de `TM`, com marcações de média, mediana e quantil 0.95.

- `subproblema1_ecdf_W.png`  
  Gráfico da função de distribuição acumulada empírica de `W`, útil para visualizar a distribuição dos valores simulados e identificar o quantil 0.95.

- `subproblema1_ecdf_TM.png`  
  Gráfico da função de distribuição acumulada empírica de `TM`, permitindo visualizar a proporção acumulada dos tempos máximos de permanência e analisar a referência `tm = 13`.

- `subproblema1_resumo_detalhado.txt`  
  Arquivo com o resumo numérico completo do subproblema 1, incluindo médias finais, amplitude do intervalo de confiança, probabilidade pedida e estatísticas adicionais como mediana e quantis.

- `subproblema2_media_W_por_n.png`  
  Gráfico da média de `W` em função do número de guichês `n`, mostrando como a proporção média de clientes que vão embora varia conforme a estrutura de atendimento.

- `subproblema2_probabilidade_por_n.png`  
  Gráfico da probabilidade empírica `Pr(W ≤ 0.20)` em função de `n`, usado para justificar a escolha do menor número de guichês que satisfaz a condição do enunciado.

- `subproblema2_quantil95_W_por_n.png`  
  Gráfico do quantil 0.95 de `W` para cada valor de `n`, oferecendo uma visão complementar da variabilidade do sistema no subproblema 2.

- `subproblema2_resumo_detalhado.txt`  
  Arquivo com os resultados numéricos do subproblema 2 para os valores testados de `n`, incluindo a identificação do menor número de guichês que atende ao critério proposto.

Resumo da execução usada aqui:
- Subproblema 1:
  N final = 15000
  X̄ = 115.570200
  Ȳ = 31.866467
  W̄ = 0.209308
  TM̄ = 11.569855
  Pr_d(tm > 13) = 0.243400
  w_s = 0.312886
 R̄ = 2.5541

- Subproblema 2:
  menor n = 8
