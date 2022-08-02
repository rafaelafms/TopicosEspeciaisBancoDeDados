# Expressando preferências em SPARQL

<p>
Este arquivo mostra uma forma de expressar preferências no SPARQL, a implementação <br />
é baseada no uso do 'NOT EXISTS', já implantado nos interpretadores SPARQL.
</p>
<p>
O código precisa da instalação do <a href="https://sparqlwrapper.readthedocs.io/en/latest/main.html">SPARQLWrapper</a> para enviar a consulta ao editor, neste caso, DBpedia <br />
e a biblioteca <a href="https://pandas.pydata.org/">Pandas</a> para organizar os resultados da pesquisa no banco de dados, esse resultado é enviado a um csv ("saida.csv")
</p>
<p>
Baseado no artigo <a href="https://iswc2017.ai.wu.ac.at/paper-143/">An extension of SPARQL for expressing
qualitative preferences</a> da International Semantic Web Conference (ISWC) de 2017
</p>
