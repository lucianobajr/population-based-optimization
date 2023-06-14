# population-based-optimization
Trabalho Prático II - Meta-heurísticas - CCF-480

## Trabalho

Considerando a seguinte formulação:

<center>

Minimize $f(\overset{\rightarrow}{x}),\overset{\rightarrow}{x} = [ {x_1},{x_2},{...},{x_n} ]$

</center>

Subject to:

<center>

$g_i(\overset{\rightarrow}{x}) \leq 0$, $i = 1,..., q$

$h_j(\overset{\rightarrow}{x}) = 0$, $j = q+1,..., m$

</center>

Usually equality constraints are transformed into inequalities of the form

<center>

$\left| h_j(\overset{\rightarrow}{x}) \right| - \epsilon \leq 0, for$ $j = q + 1,...,m $

</center>

A solution $\overset{\rightarrow}{x}$ is regarded as *feasible* if $g_i(\overset{\rightarrow}{x}) \leq 0$, for j = 1,...,q  and $\left| h_j(\overset{\rightarrow}{x}) \right| - \epsilon \leq 0, for$ $j = q + 1,...,m$.  In this special session $\epsilon$ is set to  0.0001.


Implementar um algoritmo baseado em Computação Evolutiva (AG, ES, PE ou PG) ou
Evolução Diferencial (ED) ou Particle Swarm Optimization (PSO) para resolver os
seguintes problemas restritos de otimização:

### 1) Problema com 13 variáveis de decisão ($x_1$ até $x_{13}$ ) e 9 restrições de desigualdade.

g01

$Minimize [1]$:

````markdown

f(\overset{\rightarrow}{x}) = 5 \sum_{i=1}^{4} x_i  -  5 \sum_{i=1}^{4} x^2_i  - \sum_{i=5}^{13} x_i
````


subject to:

<center>

$g_1$($\overset{\rightarrow}{x}$)  =  $2x_1$ + $2x_2$ + $x_{10}$ + $x_{11}$ - 10 $\leq 0 $

$g_2$($\overset{\rightarrow}{x}$) = $2x_1$ + $2x_3$ + $x_{10}$ + $x_{12}$ - 10 $\leq 0 $

$g_3$($\overset{\rightarrow}{x}$) = $2x_2$ + $2x_3$ + $x_{11}$ + $x_{12}$ - 10 $\leq 0 $

$g_4$($\overset{\rightarrow}{x}$) = $-8x_1$ + $x_{10}$ $\leq 0 $

$g_5$($\overset{\rightarrow}{x}$) = $-8x_2$ + $x_{11}$ $\leq 0 $

$g_6$($\overset{\rightarrow}{x}$) = $-8x_3$ + $x_{12}$ $\leq 0 $

$g_7$($\overset{\rightarrow}{x}$) = $-2x_4$ - $x_5$ + $x_{10}$ $\leq 0 $

$g_8$($\overset{\rightarrow}{x}$) = $-2x_6$ - $x_7$ + $x_{11}$ $\leq 0 $

$g_9$($\overset{\rightarrow}{x}$) = $-2x_8$ - $x_9$ + $x_{12}$ $\leq 0 $

</center>

com

<center>

$0 \leq x \leq 1 (i = 1,...,9), 0 \leq  x_i \leq 100$  $(i = 10, 11, 12)$ and $0 \leq  x_{13} \leq 1$

</center>

### 2) Problema com 2 variáveis de decisão (x 1 até x 2 ) e 5 restrições (2 de desigualdade e 3 de
igualdade).

g05

$Minimize [3]$:

<center>

$f(\overset{\rightarrow}{x}) =  3x_1 + 0.000001x³_1 + 2x_2 + (0.000002/3)x³_2 $

</center>

subject to:

<center>

$g_1(\overset{\rightarrow}{x})  =  -x_4 + x_3 - 0.55 \leq 0 $

$g_2(\overset{\rightarrow}{x}) = -x_3 + x_4 - 0.55 \leq 0 $

$h_3(\overset{\rightarrow}{x}) = 1000sin(-x_3 - 0.25) + 1000sin(-x_4 - 0.25) + 894.8 -x_1   = 0 $

$h_4(\overset{\rightarrow}{x}) = 1000sin(x_3 - 0.25) + 1000sin(x_3 - x_4 - 0.25) + 894.8 -x_2   = 0 $

$h_5(\overset{\rightarrow}{x}) = 1000sin(x_4 - 0.25) + 1000sin(x_4 - x_3 - 0.25) + 1294.8   = 0 $

</center>

com

<center>

$0 \leq x_1 \leq 1200$, $0 \leq x_2 \leq 1200$, $-0.55 \leq x_3 \leq 0.55$ and $-0.55 \leq x_4 \leq 0.55$

</center>

### Tratamento de Restrições

Terá que ser implementado duas formas de tratamento de restrições, sendo elas:

- Penalidade Estática.
- ɛ-constrained method


### A fazer

Execute o algoritmo genético proposto 30 vezes de modo independente para cada função
objetivo utilizando a Configuração A (Penalidade Estática) e uma configuração B
(tratamento sorteado). E baseado no valor final da função objetivo retornado em cada uma
das 30 execuções faça uma tabela que mostre: média, valor mínimo, valor máximo e desvio
padrão do valor da função objetivo retornada pelo algoritmo. Mostre também o resultado
graficamente com boxplot. Faça um relatório que explique como os algoritmos foram
implementados (pode ser feito em qualquer linguagem de programação), quais foram
as configurações utilizadas para os parâmetros da meta-heurística escolhida e como foi
feito o tratamento das restrições em cada problema. Envie também o código fonte. Para a
melhor solução encontrada para cada problema com cada configuração especifique
os valores das variáveis de decisão. Apresente as seguintes tabelas e discuta os resultados
obtidos