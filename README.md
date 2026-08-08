# Decisões de modelagem

Não criei classes como Musica, Album, Usuario ou Faixa. Mantive tudo como dicionário, indexado por id (_conteudos_por_id, _usuarios_por_id), o que já garante o acesso rápido que o projeto precisa, sem exigir objetos intermediários para cada item. Em vez disso, criei dois métodos auxiliares na Catalogo para evitar duplicar lógica entre os métodos obrigatórios:

_achatar_generos — o campo generos no JSON aparece em três formatos diferentes: string solta, lista simples, ou lista aninhada em até três níveis. Em vez de tratar essa inconsistência dentro de generos_de e repetir o mesmo tratamento em conteudos_do_genero, isolei essa lógica num método recursivo próprio. Assim o achatamento acontece num lugar só, e os outros métodos trabalham só com o resultado já limpo.

descricao_de — nenhum dos métodos obrigatórios devolve algo pronto para exibição, só ids. Como o cli.py precisa mostrar título, artista e tipo em quase toda opção do menu, fazia mais sentido montar essa formatação num único lugar dentro da Catalogo, em vez de repetir a mesma lógica em cada opção do CLI.