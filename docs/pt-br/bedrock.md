---
summary: "Use Amazon Bedrock (Converse API) models with OpenClaw"
read_when:
  - You want to use Amazon Bedrock models with OpenClaw
  - You need AWS credential/region setup for model calls
---

"Amazónia Bedrock"

OpenClaw pode usar **Amazon Bedrock** modelos através de **Bedrock Converse**
fornecedor de streaming. Bedrock auth usa a cadeia de credenciais padrão ** AWS SDK **,
não é uma chave API.

## O que o pi-ai suporta

- Provedor:`amazon-bedrock`- API:`bedrock-converse-stream`- Auth: Credenciais AWS (env vars, configuração compartilhada ou função de instância)
- Região:`AWS_REGION`ou`AWS_DEFAULT_REGION`(por omissão:`us-east-1`

## Descoberta automática do modelo

Se as credenciais do AWS forem detectadas, o OpenClaw pode descobrir automaticamente o Bedrock
modelos que suportam **streaming** e **text output**. Discovery usa`bedrock:ListFoundationModels`e está em cache (padrão: 1 hora).

Opções de configuração ao vivo sob`models.bedrockDiscovery`:

```json5
{
  models: {
    bedrockDiscovery: {
      enabled: true,
      region: "us-east-1",
      providerFilter: ["anthropic", "amazon"],
      refreshInterval: 3600,
      defaultContextWindow: 32000,
      defaultMaxTokens: 4096,
    },
  },
}
```

Notas:

-`enabled`defaults to`true`quando as credenciais AWS estão presentes.
-`region`não aplica o`AWS_REGION`ou o`AWS_DEFAULT_REGION`, e depois o`us-east-1`.
-`providerFilter`corresponde aos nomes dos fornecedores de Bedrock (por exemplo,`anthropic`.
-`refreshInterval`é segundos; definido para`0`para desativar o cache.
-`true`0 (por omissão:`true`1) e`true`2 (por omissão:`true`3)
são usados para modelos descobertos (sobrepor se você conhece seus limites do modelo).

## Configuração (manual)

1. Certifique-se de que as credenciais AWS estão disponíveis no host **gateway**:

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"
# Optional:
export AWS_SESSION_TOKEN="..."
export AWS_PROFILE="your-profile"
# Optional (Bedrock API key/bearer token):
export AWS_BEARER_TOKEN_BEDROCK="..."
```

2. Adicione um provedor e modelo de Bedrock à sua configuração (sem necessidade de`apiKey`:

```json5
{
  models: {
    providers: {
      "amazon-bedrock": {
        baseUrl: "https://bedrock-runtime.us-east-1.amazonaws.com",
        api: "bedrock-converse-stream",
        auth: "aws-sdk",
        models: [
          {
            id: "anthropic.claude-opus-4-5-20251101-v1:0",
            name: "Claude Opus 4.5 (Bedrock)",
            reasoning: true,
            input: ["text", "image"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "amazon-bedrock/anthropic.claude-opus-4-5-20251101-v1:0" },
    },
  },
}
```

# Funções da instância EC2

Ao executar OpenClaw em uma instância EC2 com uma função IAM anexada, o AWS SDK
usará automaticamente o serviço de metadados de instância (IMDS) para autenticação.
No entanto, a detecção de credenciais da OpenClaw atualmente só verifica o ambiente
variáveis, não credenciais do IMDS.

** Solução:** Definir`AWS_PROFILE=default`para sinalizar que as credenciais AWS são
disponível. A autenticação real ainda usa o papel de instância via IMDS.

```bash
# Add to ~/.bashrc or your shell profile
export AWS_PROFILE=default
export AWS_REGION=us-east-1
```

**As permissões necessárias do IAM** para o papel de instância EC2:

-`bedrock:InvokeModel`-`bedrock:InvokeModelWithResponseStream`-`bedrock:ListFoundationModels`(para descoberta automática)

Ou anexar a política gerenciada`AmazonBedrockFullAccess`.

** Configuração rápida:**

```bash
# 1. Create IAM role and instance profile
aws iam create-role --role-name EC2-Bedrock-Access \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy --role-name EC2-Bedrock-Access \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam create-instance-profile --instance-profile-name EC2-Bedrock-Access
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-Bedrock-Access \
  --role-name EC2-Bedrock-Access

# 2. Attach to your EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-xxxxx \
  --iam-instance-profile Name=EC2-Bedrock-Access

# 3. On the EC2 instance, enable discovery
openclaw config set models.bedrockDiscovery.enabled true
openclaw config set models.bedrockDiscovery.region us-east-1

# 4. Set the workaround env vars
echo 'export AWS_PROFILE=default' >> ~/.bashrc
echo 'export AWS_REGION=us-east-1' >> ~/.bashrc
source ~/.bashrc

# 5. Verify models are discovered
openclaw models list
```

## Notas

- Bedrock requer **model access** habilitado em sua conta/região AWS.
- A descoberta automática precisa da permissão`bedrock:ListFoundationModels`.
- Se você usar perfis, defina`AWS_PROFILE`na máquina de gateway.
- OpenClaw apresenta a fonte credencial nesta ordem:`AWS_BEARER_TOKEN_BEDROCK`,
em seguida,`AWS_ACCESS_KEY_ID`+`AWS_SECRET_ACCESS_KEY`, em seguida,`AWS_PROFILE`, em seguida, o
cadeia padrão AWS SDK.
- Raciocínio de suporte depende do modelo; verifique o cartão modelo Bedrock para
capacidades actuais.
- Se preferir um fluxo de chaves gerido, pode também colocar um OpenAI compatível
proxy na frente do Bedrock e configurá-lo como um provedor OpenAI.
