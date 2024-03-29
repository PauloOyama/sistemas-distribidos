# Systems

## Instalation

**Clone** this repo, using git CLI.

To setup your python environment, you need to have the python **installed** in your computer,
after that **run** this command in terminal,

```
python -r requirements.txt
```

Para compilar deve-se executar da seguinte forma

É necessário subir os 6 bancos de dados antes de qualquer coisa, da seguinte forma,

```py
#Banco de dados de 1 a 6
python db.py [1...6]
```

E agora podemos rodar o código normal,


```
python -m <path_to_folder>.<path_of_file> <port>(optional)
```
Exemplo, "python -m client_portal.client_order_portal".

**Importante**, "<path_to_folder>.<path_of_file>", precisa ser como no exemplo, e nao pode ter um *.py*, senão causará problemas de módulo no python;


Por default a primeira instancia do servidor da **ordem portal** rodara na porta **50051**;

Por default a primeira instancia do servidor da **admin portal** rodara na porta **50055**;




## Link para o vídeo:  https://ufubr-my.sharepoint.com/:v:/g/personal/papaloyama_ufu_br/Eeu7laFuZylEt1VdXlSeYuEBGB96JLbsCFDB7oaSr3i1ow?e=f98BMC

## Lind para o relatório: https://docs.google.com/document/d/10tJOma1kJINoX2fuVKknD1gKNmGL88D3nMCH2A65RX4/edit?usp=sharing

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

    - Inserção de Pedido (SEM FAZER)
    - Modificação de Pedido (SEM FAZER)
    - Enumeração de Pedido (SEM FAZER) 
    - Cancelamento de Pedido (SEM FAZER) 
    - Enumareção de Pedidos (SEM FAZER)
    
    - TESTES (SEM FAZER)


# Das estruturas de dados 

Tanto do server do admin (server_admin_potal.py) quanto no portal(server_order_portal.py), as estruturas abaixo foram usadas

```py
# [clients] take the CID as value and the data as value and are used to improve performance
clients = {}
# [products] take the PID as value and the data as value and are used to improve performance
products = {}

# Both are sockets pair or odd
global sck1 
global sck2 
```

```def selectReplica():```
Será a função que instanciara um socket com conexão para um banco de pares e uma para impares, isso é feito através de um sorteio aleatório
entre números

Do Banco de dados, para armazenamento das informacoes e uso da difusao atomica, usamos dois arquivos, 
o arquivo *db.py*, e *lvldb.py*, o primeiro focando no banco de dados e o segundo focando na replicação de máquina de estados.

No arquivo *db.py*,

```def run(arg):```
Dado o número de 1 a 6 fará as 6 instancias das replicas do BD, usando a lógica do *quorum de mod 2*,  

```def controller(replica, conn, addr):```
Ao receber uma mensagem vinda do socket fará a tratativa da sua função com o parâmetro podendo ser '*read', 'insert', 'delete', 'update'* e chamando a 
replica instancia na funcao *run* e fará os ações devidas.


No arquivo *lvldb.py*,

```class Database(SyncObj)```
Possui em si a classe Database que implementa a SRM (State replication Machine) possui as funçoes *insertData, getData, deleteData e updateData*,
todas essas somente recebem uma **key** vindo do arquivo *db.py*, por exemplo, **um C-1 (CID:1) ou P-1(PID:1)**, e propriamente o dado a ser armazenado
o @replicated é um decorator para fazer todos as instancias executarem juntos, escrevendo ou deletando no banco juntos.


**Importante**, é o diretório file, que possui em si, dois diretórios *odd* e *pair* onde são tratatos a questão dos chord de mod 2, é necessário que esses 
diretórios estejam criados antes de rodar, pois senão a biblioteca da erro.




# Epílogo

Projeto - Sistemas Distribuídos

Integrantes:
**Paulo Kiyoshi Oyama Filho - 11911BCC022**

**Yan Stivaletti e Souza - 11821BCC002**


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



