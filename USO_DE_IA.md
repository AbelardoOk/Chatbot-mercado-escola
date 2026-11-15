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
| Codex (OpenAI, família GPT-6) | Aplicativo Codex | Integrante responsável pela revisão |
| _Exemplo: ChatGPT (versão gratuita)_   | _navegador_                 | _Fulana_   |
| TODO                                   |                             |            |

## 2. Usos, um por linha

| #   | Etapa             | O que a IA fez                                    | Prompt (ou resumo + link para o registro)                  | O que o grupo fez com o resultado                             |
| --- | ----------------- | ------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| 1   | _Dados de treino_ | _Gerou 100 frases para 2 intenções (50 cada)_     | _ver `dados/prompts_llm.md`_                               | Os exemplos gerados são destinados ao treino após revisão.       |
| 2 | Dados de treino | Revisou 98 frases de horário e localização segundo o Passo 6 do enunciado. Conferiu naturalidade, repetições e rótulos. | Pedido no Codex para ler cada frase de dados/gerados_llm.csv e sugerir correções com base no PDF do trabalho. | Após autorização do integrante responsável, foram mantidas 76 frases como estavam, 4 foram reescritas e 18 foram retiradas por repetição. As mesmas alterações foram aplicadas aos exemplos correspondentes em dados/treino.csv. |
| 0   | _Chatbot_         | _Redige as respostas das intenções e do chitchat_ | _prompts em `chatbot/llm.py` + persona do `grupo.yaml`_    | _Ajustamos a persona 3 vezes após testes (seção X do artigo)_ |
| 0   | _Código_          | _Sugeriu a função que plota a curva de validação_ | _"como plotar o resultado do GridSearchCV em função de C"_ | _Adaptamos nomes e eixos; entendemos e testamos_              |
| 0   | _Escrita_         | _Revisou a gramática da Introdução_               | _"revise a gramática sem mudar o conteúdo: ..."_           | _Aceitamos parte das sugestões_                               |
|     |                   |                                                   |                                                            |                                                               |

## 3. O que NÃO foi feito com IA

TODO: digam explicitamente o que foi feito sem IA (ex.: definição das intenções,
frases do teste, análise dos erros, conclusões).

## 4. Reflexão (2 a 4 frases)

TODO: onde a IA ajudou, onde atrapalhou ou errou, e como vocês verificaram o que ela produziu.
