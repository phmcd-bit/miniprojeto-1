import json
import sys
from catalogo import Catalogo

def main():
    caminho_consultas = sys.argv[1]
    caminho_respostas = sys.argv[2]

    catalogo = Catalogo("catalogo_final.json")

    with open(caminho_consultas, "r", encoding="utf-8") as arquivo:
        dados_consultas = json.load(arquivo)

    respostas = {}

    for consulta in dados_consultas["consultas"]:
        id_consulta = consulta["id"]
        tipo = consulta["tipo"]
        parametros = consulta["parametros"]

        metodo = getattr(catalogo, tipo)
        resultado = metodo(**parametros)

        respostas[str(id_consulta)] = resultado

    with open(caminho_respostas, "w", encoding="utf-8") as arquivo:
        json.dump(respostas, arquivo, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()