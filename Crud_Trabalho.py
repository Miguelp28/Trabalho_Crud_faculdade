#----------------------------------------------------------------
#Programa Criado: 24/05/23
#Atualizado: 02/06/23
#Instituição: UMC
#----------------------------------------------------------------
#library:
import os #cls
import random #gerar numero aleatorio
import sqlite3 #importar sqlite
import tabulate #Criar tabela

#looping:
stop=1 #principal
stopError=1 #error

#sql DB config
con=sqlite3.connect('storage_mapping.db')#criação da tabela
cursor=con.cursor()#objeto cursor para executar comandos em sql
cursor.execute("CREATE TABLE IF NOT EXISTS produtos(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE, preco REAL, codigo_barras TEXT UNIQUE )")

#programa:
while stop==1:
    try:
        os.system('cls')
        stopError=1
        opt=int(input('''
        Seja bem vindo ao app StorageMapping siga as instruções abaixo

        Escolha uma das opções abaixo para navegar no app:
        [1] Cadastrar um novo produto no estoque
        [2] Relação de produtos no estoque da loja e alterar dados relacionados
        [3] Fechar o APP
        Opção: '''))
    #--------------------------------------------------------Opção-1-------------------------------------------------------
        if opt==1:
            os.system('cls')
            print("Informe os dados para o cadastro de um novo produto: ")
            nome_produto=input("Nome do produto: ")
            preco_produto=float(input("Preço do produto: R$"))
            cB=int(input("Deseja gerar um numero aleatorio digite '1' ou colocar o codigo da barras manual digite '2'?"))
            cursor.execute("INSERT INTO produtos (nome,preco) VALUES (?,?)",(nome_produto,preco_produto))#amarzena nome e preço
            id_produto=cursor.lastrowid #armazena a id do produto
            con.commit()
            #**********GERAR CODIGO DE BARRAS ALEATORIO****************
            try:
                if cB==1:
                    os.system('cls')
                    cBnMin=int(input("Qual o número minimo do codigo de barras deseja: "))
                    cBnMax=int(input("Qual o número maximo do codigo de barras deseja: "))
                    cBnRand=random.randint(cBnMin,cBnMax)
                    cursor.execute("UPDATE produtos SET codigo_barras=? WHERE id=?", (cBnRand,id_produto))#amarzena codigo_barras
                    con.commit()
                    save=input(f"Dados salvos o id do '{nome_produto}' é '{id_produto}' codigo de barras é '{cBnRand}', precione enter para continuar ")
                    cursor.execute("UPDATE produtos SET preco='R$'||preco WHERE id=?",(id_produto,))
                    con.commit()
                #*************GERAR CODIGO DE BARRAS MANUALMENTE***************
                elif cB==2:
                    os.system('cls')
                    cBn=int(input("Qual o número do codigo de barras: "))
                    cursor.execute("UPDATE produtos SET codigo_barras=? WHERE id=?", (cBn,id_produto))#amarzena codigo_barras
                    con.commit()
                    save=input(f"Dados salvos o id do '{nome_produto}' é '{id_produto}', precione enter para continuar ")
                    cursor.execute("UPDATE produtos SET preco='R$'||preco WHERE id=?",(id_produto,))
                    con.commit()
                #*********************Caso seja uma opção invalida*******************
                else:
                    cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))#excluira o que foi digitado anteriormente
                    con.commit()
                    raise ValueError
            except (ValueError,KeyError):#*********Invalido e apagar os dados anterior***********
                while stopError==1:
                    cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))#excluira o que foi digitado anteriormente
                    con.commit()
                    os.system('cls')
                    error=input('''
                    Opção inválida! Escreva somente o que foi descrito:
                    [1] Voltar ao menu
                    [2] Fechar o App
                    Opção: ''')
                    if error=='1':
                        stopError=2
                    elif error=='2':
                        con.close()
                        stop=2
                        stopError=2
            except sqlite3.IntegrityError:#******Caso já exista um nome ou codigoBarras**********
                while stopError==1:
                    cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))#excluira o que foi digitado anteriormente
                    con.commit()
                    os.system('cls')
                    error=input('''
                    Nome ou codigo de barras já existem na tabela consulte a relação de produtos antes de inserir um novo produto!
                    Escolha uma das opções abaixo:
                    [1] Voltar ao menu
                    [2] Fechar o App
                    Opção: ''')
                    if error=='1':
                        stopError=2
                    elif error=='2':
                        con.close()
                        stop=2
                        stopError=2
    #--------------------------------------------------------Opção-2-------------------------------------------------------
        elif opt==2:
            cursor.execute("SELECT COUNT(*) FROM produtos")
            quanti=cursor.fetchone()
            if quanti[0]==0:#*****Tabela inexistente*****
                os.system('cls')
                opt01=int(input('''
                Não há registro de estoque no momento! escolha uma das opções abaixo
                [1] Voltar para o menu
                [2] Fechar o APP
                Opção: '''))
                if opt01==1:
                    stop=1
                elif opt01==2:
                    con.close()
                    stop=2
                else:
                    raise ValueError
            else:#*******************Print Tabela********
                os.system('cls')
                cursor.execute("SELECT id,nome,preco,codigo_barras FROM produtos")
                varProdutos=cursor.fetchall()
                cabe=["ID","NOME","PREÇO","CODIGO DE BARRAS"]
                tabela=tabulate.tabulate(varProdutos, headers=cabe, tablefmt="pipe")
                print(tabela)
                opt01=int(input('''
                [1] Alterar dados
                [2] Apagar dados 
                [3] Busca por ID
                [4] Busca por nomes proximos
                [5] Voltar para o menu
                [6] Fechar o APP
                Opção: '''))
                if opt01==1:#****************Alterar dados**************
                    os.system('cls')
                    opt02=int(input('''
                    O que deseja alterar?
                    [1] Nome do produto
                    [2] Preço do produto
                    [3] Codigo de barras
                    [4] Voltar para o menu
                    Opção: '''))
                    if opt02==1:#****************Alterar Nome Do Produto**************
                        os.system('cls')
                        id00=int(input('''Qual o Id do produto: '''))
                        cursor.execute("SELECT nome FROM produtos WHERE id=?",(id00,))
                        re=cursor.fetchone() 
                        lastName=re[0]
                        conf=int(input(f'''CONFIRME com '1' para alterar o nome "{lastName}" ou CANCELE com '2': '''))
                        if conf==1:
                            os.system('cls')
                            newName=input(f"Qual nome deseja atribuir ao produto de ID {id00}: ")
                            cursor.execute("UPDATE produtos SET nome=? WHERE id=?", (newName,id00))
                            con.commit()
                            os.system('cls')
                            opt03=int(input(f'''
                            Dados do id {id00} o nome "{lastName}" foi alterado para "{newName}".
                            Escolha uma das opções abaixo para prosseguir: 
                            [1] Voltar ao menu
                            [2] Fechar App
                            Opção: '''))
                            if opt03==1:
                                stop=1
                            elif opt03==2:
                                con.close()
                                stop=2
                            else:
                                raise ValueError
                        elif conf==2:
                            stop=1
                        else:
                            raise ValueError
                    elif opt02==2:#**************Alterar Preço Do Produto*************
                        os.system('cls')
                        id00=int(input('''Qual o Id do produto: '''))
                        cursor.execute("SELECT preco FROM produtos WHERE id=?",(id00,))
                        re=cursor.fetchone()
                        lastPrice=re[0]
                        conf=int(input(f'''CONFIRME com '1' para alterar o preço "{lastPrice}" ou CANCELE com '2': '''))
                        if conf==1:
                            os.system('cls')
                            newPrice=float(input(f"Qual o novo preço do produto de id= {id00}: R$"))
                            cursor.execute("UPDATE produtos SET preco='R$'||? WHERE id=?", (newPrice,id00))
                            con.commit()
                            os.system('cls')
                            opt03=int(input(f'''
                            Dados do id {id00} alterados com sucesso o preço {lastPrice} foi alterado para R${newPrice}.
                            Escolha uma das opções abaixo para prosseguir: 
                            [1] Voltar ao menu
                            [2] Fechar App
                            Opção: '''))
                            if opt03==1:
                                stop=1
                            elif opt03==2:
                                con.close()
                                stop=2
                            else:
                                raise ValueError
                        elif conf==2:
                            stop=1
                        else:
                            raise ValueError
                    elif opt02==3:#**************Alterar CodBarras Do Produto*********
                        os.system('cls')
                        id00=int(input("Qual o Id do produto: "))
                        cursor.execute("SELECT codigo_barras FROM produtos WHERE id=?",(id00,))
                        re=cursor.fetchone()
                        oldBar=re[0]
                        opt04=int(input("Digite '1' para atrubuir um número aleatorio novo ou digite '2' para atribuir manualmente: "))
                        conf=int(input(f"CONFIRME com '1' para alterar o codigo de barras '{oldBar}' ou CANCELE com '2': "))
                        if opt04==1 and conf==1:
                            os.system('cls')
                            cBnMin0=int(input("Qual o número minimo do codigo de barras deseja: "))
                            cBnMax0=int(input("Qual o número maximo do codigo de barras deseja: "))
                            newBar=random.randint(cBnMin0,cBnMax0)
                            cursor.execute("UPDATE produtos SET codigo_barras=? WHERE id=?",(newBar,id00))
                            con.commit()
                            os.system('cls')
                            print(f"Dados salvos, o codigo de barras {oldBar} foi substituido para {newBar}")
                            input("Precione enter para continuar!")
                        elif opt04==2 and conf==1:
                            os.system('cls')
                            newBar=int(input("Qual seria o novo codigo de barras: "))
                            cursor.execute("UPDATE produtos SET codigo_barras=? WHERE id=?",(newBar,id00))
                            con.commit()
                            os.system('cls')
                            print(f"Dados salvos, o codigo de barras {oldBar} foi substituido para {newBar}")
                            input("Precione enter para continuar!")
                        elif conf==2:
                            stop=1
                        else:
                            raise ValueError
                    elif opt02==4:#*******************Voltar ao menu******************
                        stop=1
                    else:#*******************************Invalido*********************
                        raise ValueError
                elif opt01==2:#**************APAGAR DADOS***************
                    os.system('cls')
                    id00=int(input("Qual o id do produto que deseja APAGAR: "))
                    cursor.execute("SELECT nome,preco,codigo_barras FROM produtos WHERE id=?",(id00,))
                    i=cursor.fetchone()
                    nome=i[0]
                    preco=i[1]
                    barra=i[2]
                    conf=int(input(f'''Realmente tem certeza que deseja apagar o produto de id:{id00}, nome:{nome}, preço:{preco}, codigo de barras:{barra}
                    
                    CONFIRME COM '1' OU PARA CANCELAR DIGITE '2': '''))
                    if conf==1:#*********DELETAR*********
                        os.system('cls')
                        cursor.execute("DELETE FROM produtos WHERE id=?", (id00,))
                        con.commit()
                        input("Dados deletados com sucesso! precione enter para continuar!")
                    elif conf==2:#*******CANCELAR********
                        os.system('cls')
                        input("Operação cançelada! precione enter para continuar!")
                    else:#**************Inexistente******#Não funciona por causa das variaveis acima
                        input(f"Nada com parecido com o id:{id00} foi encontrado!, Precione enter para continuar")
                elif opt01==3:#**************Busca por ID***************
                    os.system('cls')
                    idBusc=int(input("Qual o id do produto: "))
                    cursor.execute("SELECT nome,preco,codigo_barras FROM produtos WHERE id=?",(idBusc,))
                    i00=cursor.fetchone()
                    if not i00:
                        os.system('cls')
                        input(f"Nada foi encontrado com o id {idBusc}, Precione enter para continuar!")
                    else:
                        os.system('cls')
                        nome=i00[0]
                        preco=i00[1]
                        bar=i00[2]
                        print(f"O nome do produto de id: {idBusc} é '{nome}', preço: {preco}, codigo de barras: {bar}")
                        input("Precione enter para voltar ao menu!")
                elif opt01==4:#*************Busca por Nome**************
                    os.system('cls')
                    nome00=(input("Digite uma letra ou nome para pesquisar? "))
                    cursor.execute('SELECT * FROM produtos WHERE nome LIKE ?',('%{}%'.format(nome00),))
                    ii=cursor.fetchall()
                    if not ii:
                        os.system('cls')
                        input(f"Nada foi encontrado os caracteres {nome00}. Precione enter para continuar!")
                    else:
                        os.system('cls')
                        cabe=["ID","NOME","PREÇO","CODIGO DE BARRAS"]
                        tabela=tabulate.tabulate(ii, headers=cabe, tablefmt="pipe")
                        print(tabela)
                        print(" ")
                        input("Fim da busca! precione enter para continuar! ")
                elif opt01==5:#**************Voltar Ao Menu*************
                    stop=1
                elif opt01==6:#***************Fechar o App**************
                    con.close()
                    stop=6
                else:#************************Invalida******************
                    raise ValueError
    #--------------------------------------------------------Opção-3-------------------------------------------------------
        elif opt==3:
            con.close()
            stop=3
    #--------------------------------------------------------Invalida------------------------------------------------------
        else:
            raise ValueError
#----------------------------------------------------------Error-------------------------------------------------------
    except (ValueError,KeyError,TypeError):
        while stopError==1:
            os.system('cls')
            error=input('''
            Opção inválida! Escreva somente o que foi indicado escolha uma das opções abaixo:
            [1] Voltar ao menu
            [2] Fechar o App
            Opção: ''')
            if error=='1':
                stopError=2
            elif error=='2':
                con.close()
                stop=2
                stopError=2
    except sqlite3.IntegrityError:
        while stopError==1:
            os.system('cls')
            error=input('''
            Nome ou codigo de barras já existem na tabela, escolha uma das opções abaixo:
            [1] Voltar ao menu
            [2] Fechar o App
            Opção: ''')
            if error=='1':
                stopError=2
            elif error=='2':
                con.close()
                stop=2
                stopError=2