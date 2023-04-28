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