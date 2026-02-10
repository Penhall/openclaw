---
summary: "Exploration: model config, auth profiles, and fallback behavior"
read_when:
  - Exploring future model selection + auth profile ideas
---

# Configuração do Modelo (Exploração)

Este documento captura **ideas** para configuração futura do modelo. Não é um
Espectro de transporte. Para o comportamento atual, veja:

- [Modelos] /concepts/models
- [Modelo failover] /concepts/model-failover
- [OAuth + perfis] /concepts/oauth

## Motivação

Operadores querem:

- Vários perfis de autenticação por provedor (pessoal vs trabalho).
- Simples seleção`/model`com retrocessos previsíveis.
- Limpar a separação entre modelos de texto e modelos capazes de imagem.

## Possível direção (alto nível)

- Mantenha a seleção do modelo simples:`provider/model`com aliases opcionais.
- Deixe os provedores ter vários perfis de autenticação, com uma ordem explícita.
- Use uma lista global para que todas as sessões falhem de forma consistente.
- Apenas sobreponha o roteamento da imagem quando explicitamente configurado.

## Perguntas abertas

- A rotação do perfil deve ser por fornecedor ou por modelo?
- Como deve a seleção de perfil de superfície de IU para uma sessão?
- Qual é o caminho de migração mais seguro das chaves de configuração legadas?
