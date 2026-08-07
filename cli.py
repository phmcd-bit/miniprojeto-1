import sys
from catalogo import Catalogo

def main():
    caminho_catalogo = sys.argv[1]
    catalogo = Catalogo(caminho_catalogo)

    while True:
        print("TrilhaSonora")
        print("============")
        print("1. Listar todos os usuários")
        print("2. Ver playlist completa de um usuário")
        print("3. Conteúdo na posição N da playlist")
        print("4. Interseção de playlists (N usuários)")
        print("5. Dados de um conteúdo (rating, duração, gêneros, plataformas, data, execuções)")
        print("6. Conteúdos de um gênero")
        print("7. Enfileirar conteúdo na fila de reprodução")
        print("8. Tocar próximo da fila")
        print("9. Ver fila atual")
        print("0. Sair")
        opcao = input("> ")

        if opcao == "0":
            break

        elif opcao == "1":
            for usuario in catalogo.listar_usuarios():
                print(usuario)

        elif opcao == "2":
            usuario_digitado = input("Nome do usuário: ")
            usuario_id = catalogo.buscar_usuario_por_nome(usuario_digitado)
            playlist = catalogo.playlist_de(usuario_id)

            if usuario_id is not None:
                for conteudo in playlist:
                    print(conteudo)
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            usuario_digitado = input("Nome do usuário: ")
            usuario_id = catalogo.buscar_usuario_por_nome(usuario_digitado)
            if usuario_id is not None:
                print(f"Playlist de {usuario_digitado} tem {len(catalogo.playlist_de(usuario_id))} itens. (Posições 1 a {len(catalogo.playlist_de(usuario_id))}). ")
                posicao_humana = int(input("Posição: "))
                conteudo = catalogo.conteudo_na_posicao(usuario_id, posicao_humana - 1)
                if conteudo is not None:
                    print(f"Posição {posicao_humana} de {usuario_digitado}: {conteudo}")
                else:
                    print("Posição inválida.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "4":
            usuarios_digitados = input("Nomes dos usuários separados por vírgula (ex.: Nicholas, Uchoa): ")
            nomes = usuarios_digitados.split(",")

            if len(nomes) == 1:
                print("Informe pelo menos dois usuários.")
                continue
            usuario_ids = []
            for nome in nomes:
                usuario_id = catalogo.buscar_usuario_por_nome(nome.strip())
                if usuario_id is None:
                    print("Sem interseção.")
                    break
                usuario_ids.append(usuario_id)
            else:
                intersecao = catalogo.intersecao_playlists(usuario_ids)
                if intersecao:
                    print(f"Interseção: {len(intersecao)} conteúdos:")
                    for conteudo in intersecao:
                        print(conteudo)
                else:
                    print("Sem interseção.")
     
if __name__ == "__main__":
    main()