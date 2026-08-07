import json

def valores_batem(esperado, obtido):
    if isinstance(esperado, (int, float)) and not isinstance(esperado, bool):
        if not isinstance(obtido, (int, float)) or isinstance(obtido, bool):
            return False
        return abs(esperado - obtido) < 1e-6
    return esperado == obtido

def main():
    with open("gabarito_publico.json", "r", encoding="utf-8") as arquivo:
        gabarito = json.load(arquivo)

    with open("respostas.json", "r", encoding="utf-8") as arquivo:
        respostas = json.load(arquivo)

    acertos = 0
    erros = []
    ausentes = []

    for id_consulta, valor_esperado in gabarito.items():
        if id_consulta not in respostas:
            ausentes.append(id_consulta)
            continue

        valor_obtido = respostas[id_consulta]

        if valores_batem(valor_esperado, valor_obtido):
            acertos += 1
        else:
            erros.append((id_consulta, valor_esperado, valor_obtido))

    total = len(gabarito)
    print(f"{acertos}/{total} corretas")

    if ausentes:
        print(f"\n{len(ausentes)} ausentes (não apareceram no respostas.json):")
        for id_consulta in ausentes:
            print(f"  id {id_consulta}")

    if erros:
        print(f"\n{len(erros)} erradas:")
        for id_consulta, esperado, obtido in erros:
            print(f"  id {id_consulta}: esperado {esperado!r}, obtido {obtido!r}")

if __name__ == "__main__":
    main()