# Declaração de uso de Inteligência Artificial generativa

> **Regra do trabalho:** usar IA generativa é **permitido e incentivado**, mas
> **todo e qualquer uso** precisa estar declarado e detalhado em uma seção própria
> do artigo e na apresentação (vídeo). Uso não declarado é considerado **plágio** e
> leva à **nota zero** no trabalho para todo o grupo.
>
> Este arquivo é o rascunho de trabalho da declaração: preencham **ao longo** do
> projeto (não no último dia) e copiem a tabela para o artigo. Apaguem as linhas de
> exemplo e todas as marcações TODO.

## 1. Ferramentas usadas

| Ferramenta (nome e versão/modelo)      | Como acessaram              | Quem usou  |
| -------------------------------------- | --------------------------- | ---------- |
| _OpenRouter, modelo openai/gpt-6-luna_ | _chave própria, via código_ | _Abelardo_ |
| _Codex, modelo openai/gpt-6.1-sol_ | _navegador_ | _Giovana_ |
| _Exemplo: ChatGPT (versão gratuita)_   | _navegador_                 | _Fulana_   |
| TODO                                   |                             |            |

## 2. Usos, um por linha

| #   | Etapa             | O que a IA fez                                    | Prompt (ou resumo + link para o registro)                  | O que o grupo fez com o resultado                             |
| --- | ----------------- | ------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| 1   | _Dados de treino_ | _Gerou 100 frases para 2 intenções (50 cada)_     | _ver `dados/prompts_llm.md`_                               | Os exemplos gerados são destinados ao treino após revisão.       |
| 2 | Dados de treino | Revisou 98 frases de horário e localização segundo o Passo 6 do enunciado. Conferiu naturalidade, repetições e rótulos. | Pedido no Codex para ler cada frase de dados/gerados_llm.csv e sugerir correções com base no PDF do trabalho. | Após autorização de Giovana, foram mantidas 76 frases como estavam, 4 foram reescritas e 18 foram retiradas por repetição. As mesmas alterações foram aplicadas aos exemplos correspondentes em dados/treino.csv. |
| 3 | Dados de treino | Giovana usou Codex para revisar 150 frases novas e 50 de pagamento pendentes, segundo o Passo 6 do enunciado. | “Valide as frases geradas e aplique no CSV as correções e os descartes, como na revisão anterior e no tutorial do professor.” | Validação aplicada em dados/gerados_llm.csv e nas frases correspondentes de dados/treino.csv: 170 mantidas como estavam, 4 corrigidas e 26 descartadas por formulações repetitivas. Detalhamento na seção 5. |
| 4 | Aprofundamento A4 — Giovana | Implementou no notebook a comparação de TF-IDF de caracteres e EmbeddingsSentenca multilíngue com regressão logística para escopo e tema, reutilizando o componente existente. | “Implementar o A4 para comparar os classificadores, com base nos componentes existentes, sem mexer nos outros aspectos do repositório.” | Executou as quatro buscas nas mesmas cinco partições do treino e grades de hiperparâmetros dos experimentos existentes; registrou F1 macro, acurácia, desvio, tempo de busca, extração dos vetores, memória dos pesos e latência em lote e individual. Verificou predições, probabilidades e gravação/leitura dos quatro pipelines em arquivos temporários. As células e saídas anteriores, dados, modelos e configuração foram preservados. |
| 0   | _Chatbot_         | _Redige as respostas das intenções e do chitchat_ | _prompts em `chatbot/llm.py` + persona do `grupo.yaml`_    | _Ajustamos a persona 3 vezes após testes (seção X do artigo)_ |
| 0   | _Código_          | _Sugeriu a função que plota a curva de validação_ | _"como plotar o resultado do GridSearchCV em função de C"_ | _Adaptamos nomes e eixos; entendemos e testamos_              |
| 0   | _Escrita_         | _Revisou a gramática da Introdução_               | _"revise a gramática sem mudar o conteúdo: ..."_           | _Aceitamos parte das sugestões_                               |
|     |                   |                                                   |                                                            |                                                               |

## 3. O que NÃO foi feito com IA

TODO: digam explicitamente o que foi feito sem IA (ex.: definição das intenções,
frases do teste, análise dos erros, conclusões).

## 4. Reflexão (2 a 4 frases)

TODO: onde a IA ajudou, onde atrapalhou ou errou, e como vocês verificaram o que ela produziu.

## 5. Parecer de validação de Giovana — 19/11/2026

Validação aplicada por solicitação de Giovana nos arquivos dados/gerados_llm.csv e dados/treino.csv, seguindo o Passo 6, página 17, do enunciado Trabalho IA.pdf. Foram revisadas as 150 frases novas de produtos, produtores e objetivo e as 50 frases de pagamento pendentes da rodada anterior.

Das 200 frases revisadas, 170 foram mantidas como estavam, 4 foram corrigidas e 26 foram descartadas por formulações repetitivas. As alterações foram aplicadas às mesmas frases nos dois CSVs, mantendo origem llm. As linhas deste registro identificam a versão anterior à aplicação, no commit [97f0f97](https://github.com/AbelardoOk/Chatbot-mercado-escola/blob/97f0f97111e402228091bb42abc5464fb8da0607/dados/gerados_llm.csv), com cabeçalho na linha 1.

Este registro atualiza o parecer anterior com a aplicação da revisão nos dados. As perguntas sobre inscrição e participação foram aprovadas como produtores após conferir que o grupo já utiliza esse rótulo em seus exemplos humanos para cadastro, requisitos e ingresso na feira. A descrição geral do tema também inclui como participar. A configuração e os exemplos humanos foram preservados.

### Resultado por intenção

| Intenção | Revisadas | Mantidas como estavam | Corrigidas | Descartadas | Aproveitadas |
| --- | --- | --- | --- | --- | --- |
| pagamento | 50 | 42 | 2 | 6 | 44 |
| produtos | 50 | 47 | 0 | 3 | 47 |
| produtores | 50 | 40 | 1 | 9 | 41 |
| objetivo | 50 | 41 | 1 | 8 | 42 |

### Correções aplicadas

| Linha anterior | Intenção | Texto anterior | Texto corrigido | Motivo |
| --- | --- | --- | --- | --- |
| 108 | pagamento | O pagamento é feito na hora ou posso usar algum app? | Posso pagar minhas compras por algum aplicativo? | Tornar o pedido específico sobre o meio de pagamento. |
| 110 | pagamento | Aceitam transferência bancária ou apenas pagamento presencial? | Aceitam transferência bancária como forma de pagamento? | Retirar a oposição entre transferência e pagamento presencial, que podem ocorrer juntos. |
| 230 | produtores | Tem produtor cadastrado? | Há produtores participando da feira? | Explicitar a pergunta sobre a existência de produtores participantes. |
| 235 | objetivo | Qual é a proposta central do Mercado Escola para a comunidade escolar? | Qual é a proposta central do Mercado Escola para a comunidade acadêmica? | Adequar a referência à comunidade ao contexto universitário do projeto. |

### Descartes aplicados por formulação repetitiva

Os exemplos abaixo foram retirados para reduzir a repetição de formulações nos lotes revisados. Cada descarte preserva outro exemplo da mesma intenção. Mensagens curtas e informais foram mantidas quando contribuem com variação.

| Linha anterior | Intenção | Frase retirada | Exemplo preservado na versão de referência |
| --- | --- | --- | --- |
| 102 | pagamento | Quais formas de pagamento são aceitas no Mercado Escola? | Linha 82 — Por gentileza, quais formas de pagamento são aceitas no Mercado Escola? |
| 105 | pagamento | Posso pagar com cartão de débito nas compras? | Linha 87 — Por favor, vocês aceitam cartão de débito nas compras? |
| 106 | pagamento | Tem como fazer o pagamento por aproximação? | Linha 95 — Posso pagar por aproximação? |
| 109 | pagamento | Consigo pagar com vale-alimentação no Mercado Escola? | Linha 91 — Poderiam me dizer se posso usar vale-alimentação para pagar no Mercado Escola? |
| 127 | pagamento | Tem pagamento por aproximação? | Linha 95 — Posso pagar por aproximação? |
| 129 | pagamento | Pix é aceito? | Linha 123 — Pagamento por Pix? |
| 138 | produtos | Vocês poderiam informar quais produtos estão disponíveis para compra? | Linha 132 — Por gentileza, quais produtos estão disponíveis no Mercado Escola? |
| 146 | produtos | Que produtos posso encontrar na feira? | Linha 137 — Que variedades de produtos posso encontrar na feira, por favor? |
| 156 | produtos | Quais são os itens que vocês oferecem? | Linha 145 — Queria saber quais itens vcs oferecem. |
| 192 | produtores | Quem são os produtores que participam do Mercado Escola? | Linha 182 — Por gentileza, quem são os produtores que participam do Mercado Escola? |
| 200 | produtores | Tem uma lista dos produtores que fazem parte do Mercado Escola? | Linha 184 — Gostaria de saber se há uma lista dos produtores participantes do Mercado Escola. |
| 202 | produtores | Quais produtores participam do Mercado Escola? | Linha 182 — Por gentileza, quem são os produtores que participam do Mercado Escola? |
| 203 | produtores | Tem uma lista dos produtores que estão na feira? | Linha 184 — Gostaria de saber se há uma lista dos produtores participantes do Mercado Escola. |
| 205 | produtores | Os produtores que participam são daqui da região? | Linha 195 — Os feirantes são produtores da região? |
| 206 | produtores | Queria saber quais produtores fazem parte do Mercado Escola, tem como? | Linha 183 — Você poderia me informar quais produtores fazem parte da feira? |
| 211 | produtores | Sabe me dizer quais agricultores estão participando desta vez? | Linha 204 — Quem são os agricultores participantes dessa edição? |
| 225 | produtores | Quem participa como produtor? | Linha 196 — Quem participa como produtor no Mercado Escola? |
| 231 | produtores | Quais são os produtores? | Linha 222 — Quem são os produtores? |
| 252 | objetivo | Qual é o objetivo principal da feira do Mercado Escola? | Linha 232 — Por gentileza, qual é o principal objetivo do Mercado Escola? |
| 253 | objetivo | Pra que foi criada essa feira do Mercado Escola? | Linha 233 — Poderia me explicar com que finalidade a feira Mercado Escola foi criada? |
| 254 | objetivo | Queria entender melhor: qual a proposta da feira? | Linha 250 — Me explica rapidinho qual é a proposta do Mercado Escola? |
| 256 | objetivo | O que o Mercado Escola busca promover com essa feira? | Linha 241 — O que a organização espera promover com a realização do Mercado Escola? |
| 259 | objetivo | Pode me explicar qual é a ideia por trás da feira do Mercado Escola | Linha 243 — Qual é a ideia por trás dessa feira? |
| 261 | objetivo | Fiquei na dúvida sobre a proposta da feira, qual é mesmo? | Linha 245 — Queria entender o objetivo da feira, qual é? |
| 278 | objetivo | Feira serve pra quê? | Linha 277 — Pra que essa feira? |
| 280 | objetivo | Objetivo do Mercado Escola? | Linha 272 — Objetivo da feira? |

A conferência final verificou o cabeçalho texto,intencao,origem, três campos em cada linha e a correspondência das frases aprovadas nos dois CSVs. Os textos e rótulos humanos, as frases da primeira rodada de horário e localização, os demais registros dos integrantes e dados/teste.csv foram preservados.
