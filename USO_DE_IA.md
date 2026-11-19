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
| 3 | Dados de treino | Giovana usou Codex para validar 150 frases novas e 50 frases de pagamento pendentes, segundo o Passo 6 do enunciado. | “Valide as novas frases geradas, use minha identificação e mantenha os textos, registrando o parecer no meu registro de revisão.” | Parecer registrado por solicitação de Giovana: 162 aprovadas sem ressalvas, 26 com observação de diversidade e 12 a revisar. Detalhamento na seção 5. |
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

Revisão feita com Codex, identificado na seção 1 como modelo openai/gpt-6.1-sol. O parâmetro foi o Passo 6, página 17, do enunciado Trabalho IA.pdf, considerando clareza, naturalidade, intenção e repetição. Mensagens curtas, abreviações, acentuação informal e paráfrases são aceitáveis quando a intenção permanece clara.

As linhas abaixo se referem a dados/gerados_llm.csv no commit [97f0f97](https://github.com/AbelardoOk/Chatbot-mercado-escola/blob/97f0f97111e402228091bb42abc5464fb8da0607/dados/gerados_llm.csv), contando o cabeçalho como linha 1. Foram lidas as 150 frases novas de produtos, produtores e objetivo, mais as 50 de pagamento que estavam pendentes da revisão anterior.

Resultado da análise das 200 frases: 162 aprovadas sem ressalvas, 26 com observação de diversidade e 12 que precisam de ajuste ou definição do grupo. As 26 paráfrases apontadas são compreensíveis e têm rótulo adequado. A observação indica pouca informação nova em relação ao exemplo comparado. O grupo pode priorizar formulações mais variadas ao selecionar exemplos. Nenhuma frase é uma duplicata exata, inclusive após normalizar maiúsculas, acentos e pontuação.

Por decisão de Giovana, este parecer registra sugestões para conferência humana. Os textos e os rótulos existentes foram preservados nos CSVs. A aprovação de uma pergunta avalia seu uso na classificação de intenções. A base de conhecimento ainda pode precisar de informação para respondê-la.

### Cobertura por intenção

| Intenção | Lidas | Aprovadas sem ressalvas | Observação de diversidade | Revisar | Linhas aprovadas sem ressalvas |
| --- | --- | --- | --- | --- | --- |
| pagamento | 50 | 42 | 6 | 2 | 82–101, 103–104, 107, 111–126, 128, 130–131 |
| produtos | 50 | 47 | 3 | 0 | 132–137, 139–145, 147–155, 157–181 |
| produtores | 50 | 32 | 9 | 9 | 182–191, 193–199, 201, 204, 207–210, 215, 217, 222–224, 226–229 |
| objetivo | 50 | 41 | 8 | 1 | 232–234, 236–251, 255, 257–258, 260, 262–277, 279, 281 |

### Observações de diversidade

| Linha | Intenção | Frase analisada | Exemplo com formulação próxima |
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

### Frases que precisam de revisão

| Linha | Intenção atual | Frase analisada | Parecer |
| --- | --- | --- | --- |
| 108 | pagamento | O pagamento é feito na hora ou posso usar algum app? | Mistura o momento do pagamento com o meio utilizado. Sugestão para tornar a pergunta específica: “Posso pagar minhas compras por algum aplicativo?”. Manter pagamento. |
| 110 | pagamento | Aceitam transferência bancária ou apenas pagamento presencial? | Transferência e atendimento presencial podem ocorrer juntos. Sugestão: “Aceitam transferência bancária como forma de pagamento?”. Manter pagamento. |
| 212 | produtores | Estou fazendo um trabalho sobre o Mercado Escola e queria saber quem pode participar como produtor. | Pergunta quem pode se candidatar. A descrição de produtores cobre os participantes atuais. Confirmar se o grupo inclui elegibilidade nessa intenção. |
| 213 | produtores | Minha turma está pesquisando os participantes da feira; vocês conseguem explicar como alguém se torna produtor por lá? | Pergunta como se tornar produtor. Confirmar se o procedimento de ingresso pertence a produtores. |
| 214 | produtores | Tenho uma pequena produção artesanal e queria entender se posso me inscrever como produtora no Mercado Escola. | Pergunta sobre inscrição como produtora. Confirmar a abrangência de produtores antes de aprovar o rótulo. |
| 216 | produtores | Minha mãe produz alimentos em casa e está pensando em participar. Como ela pode descobrir os requisitos para ser produtora? | Pergunta sobre requisitos de ingresso. Confirmar a abrangência de produtores antes de aprovar o rótulo. |
| 218 | produtores | Participo de um projeto de agricultura na faculdade e queria saber se o grupo pode se candidatar para atuar como produtor na feira. | Pergunta se um grupo pode se candidatar. Confirmar a abrangência de produtores antes de aprovar o rótulo. |
| 219 | produtores | Conheci o Mercado Escola numa visita com a escola e fiquei com vontade de saber como funciona a participação dos produtores. | “Como funciona a participação” pode pedir informações sobre os participantes ou sobre ingresso. Tornar o objetivo explícito após definir a abrangência da intenção. |
| 220 | produtores | Já vendo peças feitas à mão em eventos do bairro e gostaria de saber se há um processo para entrar como produtora participante. | Pergunta sobre processo de ingresso. Confirmar a abrangência de produtores antes de aprovar o rótulo. |
| 221 | produtores | Estou ajudando um colega que quer expor o que produz no Mercado Escola; onde ele pode consultar as orientações para participar? | Pede orientações para começar a expor. Confirmar a abrangência de produtores antes de aprovar o rótulo. |
| 230 | produtores | Tem produtor cadastrado? | “Produtor cadastrado” pode indicar a existência de participantes ou cadastro para ingresso. Sugestão para o primeiro sentido: “Há produtores participando da feira?”. |
| 235 | objetivo | Qual é a proposta central do Mercado Escola para a comunidade escolar? | “Comunidade escolar” destoa do contexto universitário definido no projeto. Sugestão: “Qual é a proposta central do Mercado Escola para a comunidade acadêmica?”. Manter objetivo. |

A intenção produtores tem a descrição “produtores participantes” no grupo.yaml, enquanto a descrição geral do tema também menciona “como participar”. As dúvidas de ingresso foram deixadas para decisão do grupo por essa diferença de abrangência. Este parecer preserva a configuração atual e os exemplos dos integrantes.
