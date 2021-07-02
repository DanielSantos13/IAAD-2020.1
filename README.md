# IAAD-2020.1
Repositório da disciplina Introdução ao Armazenamento e Análise de Dados.

Projeto BestFood

- 1° Passo: Para inicializar o projeto deve-se ter instalado na sua máquina local o Visual Studio Code. Caso ainda não tenha siga os passos abaixo:

- VS Code

O Visual Studio Code é um editor de código muito leve e multiplataforma. Consequentemente, atende uma gama enorme de projetos que vão de ASP até Node.js. Nativamente o editor também possui suporte a linguagens como Python, Ruby e C++. Além disso, esse editor de código é Open Source, ou seja, totalmente gratuito. O seu código está disponibilizado no GitHub, que permite à comunidade contribuir com melhorias, desenvolvendo plugins e extensões.

- Instalação

Para baixar a última versão do VS Code é só acessar: https://code.visualstudio.com/
O VS Code é multiplataforma, ou seja, existe versão para Windows, Mac e Linux. Porém, neste tutorial veremos a instalação do para Windows.

![Capturar](https://user-images.githubusercontent.com/33495675/124311988-f9caab00-db44-11eb-8b4f-fda709ce2577.PNG) 

Logo após o download, você deverá clicar no pacote de instalação. A próxima opção será escolher a linguagem:

![Capturar2](https://user-images.githubusercontent.com/33495675/124312592-ed931d80-db45-11eb-96dd-8121bbce784b.PNG)

Depois é só clicar em ok e continuar.
A instalação do VS Code é bem simples, nas próximas telas é só ir apertando em avançar.

- VS Code e Python

Para fazer a instalação do ambiente no VS Code você deverá seguir os seguintes passos:
Faça o download e instale a última versão em: https://www.python.org/downloads/
Instale a extensão como na imagem abaixo:

![Capturar3](https://user-images.githubusercontent.com/33495675/124312898-7b6f0880-db46-11eb-833f-1c1daa5436a5.PNG)

Após a instalação da extensão, já podemos ir para o próximo passo.

- 2° Passo:  Instale as bibliotecas necessárias para o projeto, nesse caso iremos utilizar a biblioteca nativa do python Tkinter e a extensão  MySQL Connector. Como o Tkinter é uma biblioteca nativa do python não será necessário fazer sua instalação. O Tkinter será utilizado para criar a interface gráfica e a extensão MySQL Connector para realizar a integração do Python com o nosso banco de dados MySQL. 

Para instalação do MySQL Connector na sua máquina local, abra o seu CMD e execute o comando no diretório do projeto: 

pip install mysql-connector-python

Quaisquer dúvidas na instalação desta biblioteca você pode consultar o site: https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html

OBS: No próximo passo vamos configurar o Workbench caso não tenha o Workbench instalado na sua máquina siga os passos descritos neste link: https://dicasdeprogramacao.com.br/como-instalar-o-mysql-no-windows/

- 3° Passo: Após isso crie uma conexão localhost dentro do MySQL Workbench clicando no ícone “+” conforme imagem a seguir:

![Capturar4](https://user-images.githubusercontent.com/33495675/124313710-a148dd00-db47-11eb-879b-02b1503fbf77.PNG)

Na aba seguinte que irá aparecer preencha com as seguintes informações da imagem:

![conexao](https://user-images.githubusercontent.com/33495675/124313758-b0c82600-db47-11eb-9982-739af06f84a6.PNG)

Após ter preenchido as informações aperte OK. O Workbench irá criar a sua conexão localhost, conforme imagem a seguir:

![workbench](https://user-images.githubusercontent.com/33495675/124313785-bde51500-db47-11eb-85de-ea132f3ebd26.PNG)

Agora basta apenas apertar na conexão criada denominada ‘localhost’. Quando o Workbench abrir a sua conexão pegue o nosso código “BD_BestFood.sql” disponível na branch "Atividades" e execute para criar o esquema e as tabelas do nosso projeto.

Ainda no Workbench abra e execute também o nosso arquivo “populando_bestfood.sql” para que seja inserido os dados no nosso banco de dados BestFood.

- 4° Passo: Por fim, após essas configurações iniciais basta executar nosso arquivo “BestFood_Interface” no Visual Studio Code para gerar a interface gráfica onde nós poderemos realizar todas as operações CRUD(Create, Read, Update, Delete) com o Python e o MySQL. 


