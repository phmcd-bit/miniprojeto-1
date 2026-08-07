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

            if usuario_id is not None:
                playlist = catalogo.playlist_de(usuario_id)
                if len(playlist) == 1:
                    print(f"Playlist de {usuario_digitado} (1 item):")
                else:
                    print(f"Playlist de {usuario_digitado} ({len(playlist)} itens):")
                for indice, conteudo_id in enumerate(playlist, start=1):
                    print(f"{indice}. {catalogo.descricao_de(conteudo_id)}")
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            usuario_digitado = input("Nome do usuário: ")
            usuario_id = catalogo.buscar_usuario_por_nome(usuario_digitado)

            if usuario_id is not None:
                if len(catalogo.playlist_de(usuario_id)) == 0:
                    print(f"Playlist de {usuario_digitado} está vazia.")
                    continue
                if len(catalogo.playlist_de(usuario_id)) == 1:
                    print(f"Playlist de {usuario_digitado} tem 1 item. (Posição 1).")
                else:
                    print(f"Playlist de {usuario_digitado} tem {len(catalogo.playlist_de(usuario_id))} itens. (Posições 1 a {len(catalogo.playlist_de(usuario_id))}). ")

                try:
                    posicao_humana = int(input("Posição: "))
                except ValueError:
                    print("Posição inválida.")
                    continue

                conteudo = catalogo.conteudo_na_posicao(usuario_id, posicao_humana - 1)
                if conteudo is not None:
                    print(f"Posição {posicao_humana} de {usuario_digitado}: {catalogo.descricao_de(conteudo)}")
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
                    if len(intersecao) == 1:
                        print("Interseção (1 conteúdo):")
                    else:
                        print(f"Interseção ({len(intersecao)} conteúdos):")
                    for indice, conteudo_id in enumerate(intersecao, start=1):
                        print(f"{indice}. {catalogo.descricao_de(conteudo_id)}")
                else:
                    print("Sem interseção.")

        elif opcao == "5":
            conteudo_id = input("ID do conteúdo (ex.: t000000): ")
            descricao = catalogo.descricao_de(conteudo_id)

            if descricao is None:
                print("Conteúdo não encontrado.")
                continue
            print(f"Descrição: {descricao}")

            rating = catalogo.rating_de(conteudo_id)
            if rating is not None:
                print(f"Rating: {rating:.1f}")
            else:
                print("Rating: N/D")

            duracao = catalogo.duracao_total_de(conteudo_id)
            if duracao is not None:
                print(f"Duração: {duracao//60}m{duracao%60}s")
            else:
                print("Duração: N/D")

            generos = catalogo.generos_de(conteudo_id)
            if generos is not None:
                print(f"Gêneros: {', '.join(generos)}")
            else:
                print("Gêneros: N/D")

            plataformas = catalogo.plataformas_de(conteudo_id)
            if plataformas is not None:
                print(f"Plataformas: {', '.join(plataformas)}")
            else:
                print("Plataformas: N/D")

            data = catalogo.data_adicionado_de(conteudo_id)
            if data is not None:
                print(f"Adicionado: {data}")
            else:
                print("Adicionado: N/D")

            execucoes = catalogo.execucoes_de(conteudo_id)
            if execucoes is not None:
                execucoes_formatado = f"{execucoes:,}".replace(",", ".")
                print(f"Execuções: {execucoes_formatado}")
            else:
                print("Execuções: N/D")

        elif opcao == "6":
            genero_digitado = input("Gênero (ex.: Pop): ")
            conteudos = catalogo.conteudos_do_genero(genero_digitado)

            if conteudos:
                print(f"{len(conteudos)} conteúdos em '{genero_digitado}':")
                for indice, conteudo_id in enumerate(conteudos, start=1):
                    print(f"{indice}. {catalogo.descricao_de(conteudo_id)}")
            else:
                print("Nenhum conteúdo nesse gênero.")

        elif opcao == "7":
            conteudo_id = input("ID do conteúdo pra enfileirar (ex.: t000000): ")
            sucesso = catalogo.enfileirar(conteudo_id)

            if sucesso:
                descricao = catalogo.descricao_de(conteudo_id)
                if len(catalogo.fila_atual()) == 1:
                    print(f"Enfileirado: {descricao} (fila com 1 item).")
                else:
                    print(f"Enfileirado: {descricao} (fila com {len(catalogo.fila_atual())} itens).")
            else:
                print(f"Conteúdo {conteudo_id} não existe - nada foi enfileirado.")

        elif opcao == "8":
            conteudo_id = catalogo.proximo()

            if conteudo_id is not None:
                descricao = catalogo.descricao_de(conteudo_id)
                print(f"Tocando: {descricao}")
                if len(catalogo.fila_atual()) == 1:
                    print(f"Resta {len(catalogo.fila_atual())} item na fila.")
                else:
                    print(f"Restam {len(catalogo.fila_atual())} itens na fila.")
            else:
                print("Fila vazia.")

        elif opcao == "9":
            fila = catalogo.fila_atual()
            
            if fila:
                print(f"Fila atual ({len(fila)} itens), próximo primeiro:")
                for indice, conteudo_id in enumerate(fila, start=1):
                    print(f"{indice}. {catalogo.descricao_de(conteudo_id)}")
            else:
                print("Fila vazia.")

        else:
            print("Opção inválida.")
     
if __name__ == "__main__":
    main()