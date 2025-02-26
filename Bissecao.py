import math

def funcao_para_analise(x):
    return 2*x + 50
first = True
erp_bool = False
erp_input = int(input('Anuncie o ERP desejado em numero inteiro representando a porcentagem: '))
a = int(input('Diga o primeiro valor a ser usado para o intervalo: '))
b = int(input('Diga o último valor a ser usado para o intervalo: '))
valor_intermediario = (a+b)/2
if erp_bool == False:

   

    def testa_intervalo_oposto(v1, v2):
        func1 = funcao_para_analise(v1)
        print('Func1')
        print(func1)
        func2 = funcao_para_analise(v2)
        print('Func2')
        print(func2)
        valor_intermediario = (func1 + func2) / 2
        print('valor intermediario')
        print(valor_intermediario)
        if (func1 > 0 and func2 < 0) or (func2 > 0 and func1 < 0):
            return True, v1, v2, valor_intermediario
        else:
            return False, v1, v2, valor_intermediario
    
    def retorna_erp(valor_novo, valor_anterior):
        if (valor_anterior == False):
            return False, valor_novo
        erp_novo = (valor_novo - valor_anterior)/ valor_novo
        if  erp_novo < erp_input:
            return True, valor_novo
        else:
            return False, valor_novo

    def rec1(chamar_rec, valor_intermediario, com_a, com_b):
        com_a_bool = com_a[0]
        com_b_bool = com_b[0]
        if (first == True):
            var_valor_anterior_erp = False
        if (com_a_bool == True):
            

            a = com_a[1]
            b = com_a[2]
            var_valor_intermediario = com_a[3]
            com_a = testa_intervalo_oposto(a, var_valor_intermediario)
            com_b = testa_intervalo_oposto(b, var_valor_intermediario)
            valor_intermediario = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[1]
            erp_bool = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[0]
        elif (com_b_bool == True):
            
            a = com_b[1]
            b = com_b[2]

            var_valor_intermediario = com_a[3]
            com_a = testa_intervalo_oposto(a, var_valor_intermediario)
            com_b = testa_intervalo_oposto(b, var_valor_intermediario)  
            valor_intermediario = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[1]
            erp_bool = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[0]
        if not com_a_bool and not com_b_bool:
            print('Não há raízes em ambos os intervalos')
        
        
        chamar_rec(com_a, com_b)

    def rec2(com_a, com_b):
        com_a_bool = com_a[0]
        com_b_bool = com_b[0]
        if (first == True):
            var_valor_anterior_erp = False
        if (com_a_bool == True):
            
            a = com_a[1]
            b = com_a[2]

            var_valor_intermediario = com_a[3]
            com_a = testa_intervalo_oposto(a, var_valor_intermediario)
            com_b = testa_intervalo_oposto(b, var_valor_intermediario)
            
            valor_intermediario = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[1]
            erp_bool = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[0]
        elif (com_b_bool == True):
            
            a = com_b[1]
            b = com_b[2]

            var_valor_intermediario = com_a[3]
            com_a = testa_intervalo_oposto(a, var_valor_intermediario)
            com_b = testa_intervalo_oposto(b, var_valor_intermediario)
            valor_intermediario = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[1]
            erp_bool = retorna_erp(var_valor_intermediario, var_valor_anterior_erp)[0]
        if not com_a_bool and not com_b_bool:
            print('Não há raízes em ambos os intervalos')
        

    
    if (first == True):
            var_valor_anterior_erp = False

    valor_intermediario = (a+b)/2
    com_a = testa_intervalo_oposto(a, valor_intermediario)
    com_b = testa_intervalo_oposto(b, valor_intermediario)
    erp_bool = retorna_erp(valor_intermediario, var_valor_anterior_erp)[0]
    while erp_bool == False:
            rec1(rec2, valor_intermediario, com_a, com_b)        
    print(f'Esse é o resultado: {valor_intermediario}')


    
    



