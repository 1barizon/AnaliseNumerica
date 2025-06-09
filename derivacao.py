import numpy as np
import matplotlib.pyplot as plt

def derivada(y, x, hs, f):

    valores = []
    for h in hs:
        progressiva = (f(x+h)-y)/h
        regressiva = (y - f(x-h))/h
        central = (f(x+h) - f(x-h))/(2*h)
        valores.append([progressiva, regressiva, central])
    return valores



def main():
    """
    Função principal que executa o programa interativo.
    """
    # 1. Crie o seu dicionário de funções.
    # A chave é o nome amigável (string), e o valor é o objeto da função.
    # Usamos 'lambda' para criar funções simples de forma rápida.
    function_library = {
        "sin(x)": np.sin,
        "cos(x)": np.cos,
        "tan(x)": np.tan,
        "e^x": np.exp,
        "x^2": lambda x: x**2,
        "x^3": lambda x: x**3,
        "ln(x)": np.log # Logaritmo natural
    }

    # Loop principal para manter o programa a ser executado
    while True:
        print("\n--- Biblioteca de Funções Disponíveis ---")
        # Imprime as opções para o utilizador
        for name in function_library.keys():
            print(f"- {name}")
        print("-----------------------------------------")
        
        # 2. Peça ao utilizador para escolher uma função
        user_choice = input("Digite o nome da função que deseja usar (ou 'sair' para terminar): ").lower()

        if user_choice == 'sair':
            print("Programa terminado.")
            break

        # 3. Verifique se a escolha do utilizador é válida
        if user_choice in function_library:
            # 4. Se for válida, obtenha a função real do dicionário
            selected_function = function_library[user_choice]
            print(f"Você selecionou a função: {user_choice}")

            # Agora, vamos usar a função selecionada
            try:
                # Pede um número para aplicar a função

                value_str = input("Digite um número para aplicar a função: ").replace(',', '.')
                number = float(value_str)
                
                h_values = [0.1, 0.01, 0.001]
                y = selected_function(number)
                
                # Calcula o resultado
                val_derivada = derivada(y, number, h_values, selected_function)
                for i in range(len(h_values)):
                    print(f"h = {h_values[i]}\n Diferenca progressiva = {val_derivada[i][0]} \n Diferenca regressiva = {val_derivada[i][1]} \n Diferenca central = {val_derivada[i][2]}")
                    
                

               
               

            except ValueError:
                print("Erro: Por favor, insira um número válido.")
            except Exception as e:
                # Captura outros erros matemáticos, ex: tan(pi/2) ou ln(-1)
                print(f"Ocorreu um erro ao calcular: {e}")

        else:
            print("Função não encontrada. Por favor, escolha uma da lista.")


# Executa o programa principal
if __name__ == "__main__":
    main()


