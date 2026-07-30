🇧🇷 Português | 🇺🇸 [English](README.md)

# URL SHORTENER API

* Criado por Marlon Ern — [Linkedin](https://www.linkedin.com/in/marlon-ern-731bb1102/) · [Github](https://github.com/MarlonErn) *

## Sobre
Uma API REST de encurtamento de URLs, construída como projeto de
estudo para portfólio técnico. O sistema recebe uma URL longa, gera
um código curto único e redireciona o acesso para o destino original,
contabilizando cliques a cada redirecionamento.

O projeto foi desenvolvido com foco em modelagem de dados consistente,
versionamento de schema via migrations, e separação clara de
responsabilidades entre camadas (models, schemas, services e routers) —
um padrão de organização inspirado em ambientes corporativos reais.

Entre as decisões técnicas do projeto está a geração de códigos curtos
via conversão numérica para base62, com um ajuste deliberado no
identificador inicial do banco para garantir um tamanho mínimo de
caracteres desde o primeiro registro (detalhado na seção
"Decisões Técnicas").