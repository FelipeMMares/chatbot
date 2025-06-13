# chatbot

é um pequeno projeto que utliza principlamente python, utiliza ollama para agilizar a resposta, ngrok para fazer a comunicação entre o localhost e web, e o site twillio para testar o chatbot.

# instalação
## passo 1
acesse seu cmd ou unbutu<br>
``` 
git clone https://github.com/FelipeMMares/chatbot.git
```
para copiar todo conteúdo do repositório
acesse seu terminal (cmd ou unbutu) <br>
``` 
cd chatbot
```
com isso você acessa especificamente a pasta clonada<br>
## passo 2
```
. code
```
esse comando fará com que execute o vscode caso, você já o tenha instalado. (caso não tenha instale ou use outra ide para rodar a aplicação)

## passo 3

no visual studio, acesse o terminal de lá 
```
python -m venv venv       # cria ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
## passo 4 
```
pip install -r requirements.txt
```
assim todos requisitos para a aplicação funcionar serão baixados
## passo 5
comece aplicação
```
pip chatbot.py
```
caso tenha dado certo deve aparecer um localhost com a porta 5000 no final<br>
abra outro terminal e nele digite
```
ngrok http 5000
```
nesse caso talvez você precisa de uma conta ngrok, para gerar um token 
## passo 6
para o teste vai no twillio, faz uma conta e monte um projeto coloque no develepment para receber um número sandbox gratuíto<br>
se tiver dado certo o número deve retornar o menu do chatbot.
