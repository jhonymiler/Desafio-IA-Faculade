# Chat IA - README

## Descrição
Esta aplicação Flask fornece uma interface de chat baseada em inteligência artificial especializada em dados fiscais do Brasil. O sistema utiliza modelos de linguagem para processar e responder perguntas com base em um conjunto de dados estruturados.

## Tecnologias Utilizadas
- **Flask**: Framework para desenvolvimento web em Python.
- **python-dotenv**: Gerenciamento de variáveis de ambiente.
- **langchain-groq**: Integração com modelos de linguagem.
- **langchain-core**: Ferramentas centrais para processamento de linguagem.
- **pandas**: Manipulação e análise de dados.
- **langchain_community**: Integração com fontes de dados externas.
- **langchain-huggingface**: Conexão com modelos de IA da Hugging Face.
- **qdrant-client**: Vetorizador para armazenamento e busca eficiente de embeddings.
- **protobuf==3.20.1**: Dependência para comunicação eficiente entre sistemas.

## Instalação
### 1. Clonar o repositório
```bash
$ git clone https://github.com/seu-repositorio/chat-ia.git
$ cd chat-ia
```

### 2. Criar um ambiente virtual (opcional, mas recomendado)
```bash
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
$ pip install -r requirements.txt
```

### 4. Criar um arquivo `.env`
Crie um arquivo chamado `.env` na raiz do projeto e defina as variáveis de ambiente necessárias:
```env
GROQ_API_KEY=sua_api_key_aqui
SECRET_KEY=uma_chave_secreta
```

## Execução
Para iniciar a aplicação, execute:
```bash
$ python app.py
```
O servidor será iniciado na porta **3000** e estará acessível via `http://localhost:3000`.

## Como Funciona a IA
1. O histórico de conversação do usuário é armazenado na sessão do Flask.
2. Cada mensagem do usuário é processada e analisada pelo **LangChain**, que estrutura a conversa.
3. O modelo de IA, baseado no **ChatGroq**, recebe a consulta e retorna uma resposta gerada dinamicamente.
4. Se a consulta for relacionada a dados fiscais, a IA utiliza funções especializadas para realizar buscas e cálculos no dataset.
5. A resposta final é retornada ao usuário e armazenada no histórico da sessão.

## API
A API possui dois endpoints principais:

### 1. **`GET /chat_ia`**
Inicializa a sessão de conversa e retorna a página de chat.

### 2. **`POST /send_message`**
Envia uma mensagem para a IA e recebe uma resposta.
#### **Parâmetros (JSON)**
```json
{
    "message": "Qual foi a arrecadação de IRPF em 2020?",
    "apikey": "sua_chave_api"
}
```
#### **Resposta (JSON)**
```json
{
    "reply": "A arrecadação de IRPF em 2020 foi R$ XXX.XXX.XXX."
}
```

## Contribuição
Se desejar contribuir com melhorias, siga os passos:
1. **Fork** o repositório.
2. Crie uma branch com a funcionalidade ou correção (`git checkout -b minha-branch`).
3. Realize as alterações e faça commit (`git commit -m "Descrição das mudanças"`).
4. Envie a branch (`git push origin minha-branch`).
5. Crie um Pull Request no GitHub.

## Licença
Este projeto está sob a licença MIT.

