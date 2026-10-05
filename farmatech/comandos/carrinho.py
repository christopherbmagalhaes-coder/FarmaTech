import datetime
import mysql.connector
from utilidades import conexao_bd

def carrinho():
    print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        FARMATECH - CARRINHO DE COMPRAS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
    carrinho = []

    #Loop principal do carrinho: Usuário pode continuar adicionando ao carrinho até cancelar ou concluir
    while True:
        print("""
                          FARMATECH - TIPO DE ITEM
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                  [1] Produto           [2] Medicamento
   ---------------------------------------------------------------------
              [-1] Concluir compra        [-2] Cancelar compra
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        tipo = input("Digite uma opção: ").strip()

        if tipo == '-1':
            #Impede que conclua a venda com o carrinho vazio
            if len(carrinho) == 0:
                print("ERRO: O carrinho está vazio, adicione itens antes de concluir a compra.")
                continue
            break

        elif tipo == '-2':
            print("COMPRA CANCELADA...")
            return
        #Verifica se o número esta dentro das opções pedidas

        elif tipo not in ["1", "2"]:
            print("ERRO: Opção inválida")
            continue

        #Essa parte é necessária para saber qual tabela o sistema irá consultar
        tabela = "produtos" if tipo == "1" else "medicamentos"

        try:
            id_item = int(input(f"Digite o [ID] do {tabela[:-1]}: ")) # O {tabela[:-1]} remove o s do final para a escrita ficar melhor para o usuario
        except ValueError:
            print("ERRO: ID deve ser um número inteiro")
            continue

        item_encontrado = None

        try:
            conexao, cursor = conexao_bd()

            if tabela == "medicamentos":
                cursor.execute(
                    "SELECT nome, preco, qtd, tarja FROM medicamentos WHERE id = %s AND ativo = 1",
                    (id_item,),
                )

            else: 
                cursor.execute(
                    "SELECT nome, preco, qtd FROM produtos WHERE id = %s AND ativo = 1",
                    (id_item,),
                )

            item_encontrado = cursor.fetchone() #Pega a linha encontrada no banco de dados

        except mysql.connector.Error as erro:
            print(f"Erro ao acessar banco: {erro}")
            continue
        #Bloco que finaliza o banco de dados pós consulta
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

        if not item_encontrado:
            print(f"ERRO: ID inválido ou item desativado na categoria {tabela}." )
            continue

        if tabela == "medicamentos":
            nome_prod, preco_prod, estoque_real, tarja = item_encontrado
        else:
            nome_prod, preco_prod, estoque_real = item_encontrado
            tarja = "Livre"

        #Validar Tarja
        if tabela == "medicamentos" and tarja.lower() in [
            "preta",
            "vermelha",
        ]:
            print(f"ATENÇÃO: Medicamento de Tarja {tarja.upper()}")

            crm = input("Digite o CRM do médico para liberação: ").strip()
            #Se for digitado menos que 4 caracters a venda é bloqueada
            if len(crm) < 4:
                print("VENDA BLOQUEADA: CRM Inválido ou não informado.")
                continue
            
        try:
            qtd = int(input(f"Digite a quantidade que deseja de '{nome_prod}'? Estoque atual: [{estoque_real}] "))
        except ValueError:
            print("ERRO: Quantidade Inválida")
            continue

        #Verifica o que já está no carrinho
        #Soma o que já foi adicionado para não permitir vender mais do que o estoque atual
        possui_no_carr = sum(
            item["qtd"]
            for item in carrinho
            if item["id"] == id_item and item["tabela"] == tabela
        )
        #Calculo do que sobrou em estoque
        estoque_disp = estoque_real - possui_no_carr

        if qtd <= 0:
            print("ERRO: Quantidade Inválida")
        elif qtd > estoque_disp:
            print(f"ESTOQUE INSUFICIENTE: Já tem {possui_no_carr} no carrinho, estoque é {estoque_real}.")
        else:
            carrinho.append(
                {
                    "id": id_item,
                    "nome": nome_prod,
                    "preco": preco_prod,
                    "qtd": qtd,
                    "subtotal": qtd * preco_prod,
                    "tabela": tabela,  # Guardamos para saber onde atualizar o estoque depois
                }
            )
            print(f"--> {qtd} x '{nome_prod}' adicionado ao carrinho.")

    #Fechamento de compra:
    if len(carrinho) > 0:
        total_compra = sum(item["subtotal"] for item in carrinho)
        print("""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                          FECHAMENTO DE CAIXA
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""")
        print(f"TOTAL A PAGAR: R$ {total_compra:.2f} ")

        #Loop que garante que o usuario digite s/n  e trata falhas sem que o carrinho se perca
        while True:
            confirmar = input("Confirmar pagamento e registrar venda? (s/n): ")

            if confirmar == "s":
                conexao = None
                cursor = None

                try:
                    conexao, cursor = conexao_bd()
                    horario_venda = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

                    for item in carrinho:
                        #Atualizar o estoque
                        cursor.execute(
                            f"UPDATE {item['tabela']} SET qtd = qtd - %s WHERE id = %s",
                            (item["qtd"], item["id"]),
                        ) 
                    #Registra na tabela  
                        cursor.execute(
                            """
                            INSERT INTO vendas (horario, id_produto, quantidade, valor_total)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                horario_venda,
                                id_item,
                                item["qtd"],       
                                item["subtotal"],  
                            ),
                        )

                    conexao.commit()
                    print("VENDA CONCLUIDA COM SUCESSO !! :) ")

                        
                except mysql.connector.Error as erro:
                    conexao.rollback()
                    print("\n ERRO FATAL NO BANCO DE DADOS: transação")
                    print(f"Motivo técnico: {erro}")
                finally:
                    if "conexao" in locals() and conexao.is_connected():
                        cursor.close()
                        conexao.close()

                break

            elif confirmar == "n":
                print("VENDA CANCELADA :( ")
                break

            else:
                print("Opção Inválida! Digite apenas 's' para confirmar ou 'n' para cancelar!")



