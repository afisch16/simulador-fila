from math import inf

x = 1234
a = 1664525
c = 1013904223
m = 4294967296
aleatorios_usados = 0


def gerar_aleatorio():
    global x, aleatorios_usados
    x = (a * x + c) % m
    aleatorios_usados += 1
    return x / m


def simular_fila(servidores, capacidade):
    global x, aleatorios_usados

    x = 1234
    aleatorios_usados = 0

    tempo_atual = 0.0
    ultimo_tempo = 0.0

    proxima_chegada = 2.0
    saidas_servidores = [inf] * servidores

    em_atendimento = 0
    fila = 0
    perdas = 0
    saidas_realizadas = 0

    tempos_estados = [0.0] * (capacidade + 1)

    while aleatorios_usados < 100000:
        menor_saida = min(saidas_servidores)

        if proxima_chegada <= menor_saida:
            proximo_evento = proxima_chegada
            tipo = "chegada"
            servidor_evento = -1
        else:
            proximo_evento = menor_saida
            tipo = "saida"
            servidor_evento = saidas_servidores.index(menor_saida)

        if proximo_evento == inf:
            break

        total_clientes = em_atendimento + fila
        tempos_estados[total_clientes] += proximo_evento - ultimo_tempo

        tempo_atual = proximo_evento
        ultimo_tempo = proximo_evento

        if tipo == "chegada":
            total_clientes = em_atendimento + fila

            if total_clientes < capacidade:
                if em_atendimento < servidores:
                    em_atendimento += 1

                    if aleatorios_usados < 100000:
                        u = gerar_aleatorio()
                        tempo_atendimento = 3 + 2 * u

                        for i in range(servidores):
                            if saidas_servidores[i] == inf:
                                saidas_servidores[i] = tempo_atual + tempo_atendimento
                                break
                else:
                    fila += 1
            else:
                perdas += 1

            if aleatorios_usados < 100000:
                u = gerar_aleatorio()
                intervalo_chegada = 2 + 3 * u
                proxima_chegada = tempo_atual + intervalo_chegada
            else:
                proxima_chegada = inf

        else:
            saidas_servidores[servidor_evento] = inf
            em_atendimento -= 1
            saidas_realizadas += 1

            if fila > 0:
                fila -= 1
                em_atendimento += 1

                if aleatorios_usados < 100000:
                    u = gerar_aleatorio()
                    tempo_atendimento = 3 + 2 * u
                    saidas_servidores[servidor_evento] = tempo_atual + tempo_atendimento

    tempo_global = tempo_atual
    probabilidades = []

    for tempo in tempos_estados:
        if tempo_global > 0:
            probabilidades.append(tempo / tempo_global)
        else:
            probabilidades.append(0.0)

    return tempos_estados, probabilidades, perdas, saidas_realizadas, tempo_global, aleatorios_usados


def mostrar_resultado(nome_fila, tempos_estados, probabilidades, perdas, saidas_realizadas, tempo_global, aleatorios):
    print("=" * 60)
    print("Fila:", nome_fila)
    print("Chegadas entre 2 e 5 segundos")
    print("Atendimento entre 3 e 5 segundos")
    print("Aleatórios usados:", aleatorios)
    print("Perdas:", perdas)
    print("Saídas:", saidas_realizadas)
    print(f"Tempo global: {tempo_global:.6f} segundos")
    print()

    print("Tempos acumulados por estado:")
    for i in range(len(tempos_estados)):
        print(f"Estado {i}: {tempos_estados[i]:.6f} segundos")

    print()
    print("Probabilidades por estado:")
    for i in range(len(probabilidades)):
        print(f"Estado {i}: {probabilidades[i]:.6f}")


tempos1, probs1, perdas1, saidas1, tempo1, aleat1 = simular_fila(1, 5)
mostrar_resultado("G/G/1/5", tempos1, probs1, perdas1, saidas1, tempo1, aleat1)

print()

tempos2, probs2, perdas2, saidas2, tempo2, aleat2 = simular_fila(2, 5)
mostrar_resultado("G/G/2/5", tempos2, probs2, perdas2, saidas2, tempo2, aleat2)
