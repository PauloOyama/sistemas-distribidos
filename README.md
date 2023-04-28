# Systems

## Instalation

**Clone** this repo, using git CLI.

To setup your python environment, you need to have the python **installed** in your computer,
after that **run** this command in terminal,

```
python -r requirements.txt
```


Para compilar deve-se executar da seguinte forma

```
python -m <path_to_folder>.<path_of_file> <port>(optional)
```
Exemplo, "python -m client_portal.client_order_portal".

**Importante**, "<path_to_folder>.<path_of_file>", precisa ser como no exemplo, e nao pode ter um *.py*, senão causará problemas de módulo no python;


Por default a primeira instancia do servidor da **ordem portal** rodara na porta **50051**;

Por default a primeira instancia do servidor da **admin portal** rodara na porta **50055**;




## Link para o vídeo:  https://youtu.be/JBHoTCdGWNg


------


# Requisitos atendidos 


*Manipulação de Clientes*

    - Inserção de Cliente (FEITO 100%)
    - Modificação de Cliente (FEITO 100%)
    - Recuperação de Clientes (FEITO 100%)
    - Remoção de Cliente (FEITO 100%)

*Manipulação de Produtos*

    - Inserção de Produto (FEITO 100%)
    - Modificação de Produto (FEITO 100%)
    - Recuperação de Produto (FEITO 100%)
    - Remoção de Produto (FEITO 100%)


*Manipulação de Tarefa dos Pedidos*

    - Inserção de Pedido (FEITO 100%)
    - Modificação de Pedido (FEITO 100%)
    - Enumeração de Pedido (FEITO 100%) 
    - Cancelamento de Pedido (FEITO 100%) 
    - Enumareção de Pedidos (FEITO 100%)



# Das estruturas de dados 

Tanto do server do admin (server_admin_potal.py) quanto no portal(server_order_portal.py), as estruturas abaixo foram usadas

```py
# [clients] take the CID as value and the data as value
clients = {}
# [products] take the PID as value and the data as value
products = {}
```

No server do portal algumas outras estruturas foram usadas, e são essas,

```py
#Mapeia um cliente para um OID -> CID -> [OID1,OID2,...,OIDN] 
client_orders = dict()
#Mapeia um OID para suas orderns -> OID -> [{'name' : 'Laranja', 'price' : '5.00', 'quantity': '5'}]
orders_oid = dict()
# [clients] take the CID as value and the data as value
clients = {}
# [products] take the PID as value and the data as value
products = {}
# [price_by_product] take the PID as value and the price of that product as value
price_by_product = {}
# [qtd_by_product] take the PID as value and the absolut remaning quantity  of that product as value
qtd_by_product = {}
# [order_like_lst_of_dicts] is the list of dicts for better manipulation of the last order inserted
order_like_lst_of_dicts = []
```

Do MQTT, para conexáo com os tópicos usamos uma variavel 

```py
#[subscribers] is a list of tuples to be subscribe in MQTT Connection para o server admin
subscribers = [('clients',0), ('products',0)]

#[subscribers] is a list of tuples to be subscribe in MQTT Connection para o server portal
subscribers = [('clients',0), ('products',0), ('orders',0)]
```

A arquitetura MQTT, usa-se de dois tópicos entre o server admin, sendo eles **clients** e **products** e o server portal
adiciona um novo tópico chamado **orders** que é exclusivo das suas instâncias e que permite atualizações e deleções dos produtos mais facilmente.


# Das funções Auxiliares 

```def on_message(client, userdata, msg):```

Será a função que recebe os dados vindos do MQTT, para facilidade do do projeto pensamos em estruturar as mensagens dos tópicos 
**clients** e **products** de duas formas, **"<AÇÃO> <PID_OR_CID> <_DATA_>"** , por exemplo, **"CREATE 1 {'name' : 'Paulo'}"**, as 
**AÇÕES** comportados são  **CREATE, DELETE, UPDATE,** .

No server portal é um pouco diferente, ele aceita algumas ações a mais, sua especificação é

```py
    #CREATE - Create this OID in this CID with this DATA
        <ACAO> <OID> <CID> <DATA>

    #CHANGE - Change the current PID to this QUANTITY
        <ACAO> <PID> <QUANTITY>
    
    #DELETE - Delete this OID from this CID 
        <ACAO> <OID> <CID>
```

No server portal, algumas funções são necessárias para o json vindo como string do cliente logo precisamos tratá-los e filtrá-los, por isso usamos as funções,

```def get_name(pid: str):``` - Given a data find a pattern with RegEx **"\'[a-zA-Z]+\'"** an return name

```def productParser(data:str) -> None:``` - Initiate **price_by_product** and **qtd_by_product** variables using RegEx to filter the data coming as string

```def orderParser(data: str)-> None:``` - Initiate **order_like_lst_of_dicts** variable to be used in the creation of the product

# Epílogo

Projeto - Sistemas Distribuídos

Integrantes:
**Paulo Kiyoshi Oyama Filho - 11911BCC022

Yan Stivaletti e Souza - 11821BCC002**


## Descrição do Projeto

_O projeto desenvolvido pelos integrantes visa, desenvolver os conhecimentos estudados na aula, implementando o conceito Cliente/Administrador e Peer-2-Peer, com uma arquitetura híbrida. A linguagem usada para o desenvolvimento foi Python. A seguir temos as descrições dos seguintes trechos do código._

## Cliente e Produtos

As operações feitas em cliente feitas no arquivo client_admin.py. Ao lidar com o lado cliente das operações, há a possibilidade de criação, recuperação, atualização e remoção do mesmo, para o endereçamento, foi utilizada a porta 5055.
Para realizar as operações, usa-se o código do cliente, no caso o CID, para fazer a busca e verificação dos dados dos clientes já inseridos. Há também a criação de um Stub, para estabelecer uma conexão com a base de dados e averiguar as correspondências.
As ideais de funções aplicadas ao cliente, são implementadas também no produto, as alterações que ocorrem dentro do código são referentes a descrição do produto. Para o fácil manuseio da aplicação, houve a criação de uma interface, implementada no terminal, para facilitar as escolhas de operações.


## Pedidos do Cliente

O arquivo client_order_portal.py tem a finalidade de lidar com os pedidos feitos pelos clientes dentro da aplicação, verificando a realização da operação de compra de um pedido com seus detalhes específicos, as mesmas funções relacionadas a cliente e produto são implementadas em pedido. Há, também, a função de mostrar todos os pedidos feitos pelo cliente em questão. Na criação é possível realizar mais de um pedido durante a operação.

## Servidor e Base de Dados

Para assegurar as transações de clientes e pedidos dentro da aplicação, houve a criação do arquivo server_admin_portal.py. O transporte de dados utiliza o método MQTT para publicar e subscrever dentro das funções de criação, atualização, remoção e busca dos itens. 
Ao utilizar uma destas funções dentro da aplicação, a parte do servidor é encarregada de ler os atributos e dados dentro da função e anexá-las ao dicionário, sendo o método implementado dentro do Python para registrar os dados dos clientes. Se ocorrer algum erro durante a transação, como um CID não existir dada uma busca no banco, ou um CID já estar sendo usado no caso de uma criação, o servidor envia uma mensagem de erro (erro 2), podendo ter uma descrição do possível erro ocasionado. Caso o oposto, o servidor encarrega-se de anexar os novos dados ou dados atualizados ao banco (error = 0).
Outro fato importante é que na função server há a conexão ao gRPC e a criação de Threads, no caso 10, para subdividir os processos dentro da aplicação.
Em relação à base de dados criada, ela tem a função de armazenar os diversos dados inseridos na aplicação enquanto a mesma esta operante, um fator a ser evidenciado é que ela armazena os dados de forma serializada e é conectada ao servidor por um canal gRPC.



