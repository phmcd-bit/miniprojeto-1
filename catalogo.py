import json
from collections import deque

class Catalogo:
    def __init__(self, caminho_json: str):

        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            catalogo_bruto = json.load(arquivo)

        lista_conteudos = catalogo_bruto["conteudos"]
        lista_usuarios = catalogo_bruto["usuarios"]

        self._conteudos_por_id = {
            conteudo["id"]: conteudo for conteudo in lista_conteudos
        }

        self._usuarios_por_id = {
            usuario["id"]: usuario for usuario in lista_usuarios
        }

        self.fila = deque()

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]:
        nomes_usuarios = [usuario["nome"] for usuario in self._usuarios_por_id.values()]
        return sorted(nomes_usuarios)
    
    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        for usuario in self._usuarios_por_id.values():
            if usuario["nome"].lower() == nome.lower():
                return usuario["id"]
        return None

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        usuario = self._usuarios_por_id.get(usuario_id)
        if usuario is not None:
            return usuario.get("playlist", [])
        return None

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        playlist = self.playlist_de(usuario_id)
        if playlist is not None and 0 <= posicao < len(playlist):
            return playlist[posicao]
        return None
    
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        if not usuario_ids:
            return []

        playlists = [set(self.playlist_de(usuario_id) or []) for usuario_id in usuario_ids]
        intersecao = set.intersection(*playlists)
        return sorted(intersecao)

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None:
        conteudo = self._conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        rating = conteudo.get("rating")
        if rating is not None:
            return float(rating)
        return None

    def duracao_total_de(self, conteudo_id: str) -> int | None:
        conteudo = self._conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        if conteudo.get("tipo") == "musica":
            return conteudo.get("duracao_seg")
        if conteudo.get("tipo") == "album":
            soma = 0
            for faixa in conteudo.get("faixas"):
                if faixa.get("duracao_seg") is not None:
                    soma += faixa.get("duracao_seg")
            return soma
        return None

    def achatar_generos(self, valor):
        if isinstance(valor, str):
            return [valor]
        resultado = []
        for item in valor:
            resultado.extend(self._achatar_generos(item))
        return resultado
                
    def generos_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self._conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        generos = conteudo.get("genero", [])
        return sorted(self.achatar_generos(generos))

    def plataformas_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self._conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        plataformas = conteudo.get("plataformas", [])
        return sorted(plataformas)

    def data_adicionado_de(self, conteudo_id: str) -> str | None:
        conteudo = self._conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        data = conteudo.get("data_adicionado")
        if "/" in data:
            partes = data.split("/")
            return f"{partes[2]}-{partes[1]}-{partes[0]}"
        else:
            return data
        
    def execucoes_de(self, conteudo_id: str) -> int | None:
        conteudo = self._conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        engajamento = conteudo.get("engajamento", {})
        execucoes = engajamento.get("execucoes")
        if isinstance(execucoes, str):
            execucoes = execucoes.replace(",", "")
            return int(execucoes)
        else:
            return execucoes
        
    def conteudos_do_genero(self, genero: str) -> list[str]:
        conteudos_filtrados = [
            conteudo_id
            for conteudo_id in self._conteudos_por_id
            if genero in self.generos_de(conteudo_id)
        ]
        return sorted(conteudos_filtrados)
    
    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool:
        if conteudo_id in self._conteudos_por_id:
            self.fila.append(conteudo_id)
            return True
        return False
    
    def proximo(self) -> str | None:
        if self.fila:
            return self.fila.popleft()
        return None
    
    def fila_atual(self) -> list[str]:
        return list(self.fila)