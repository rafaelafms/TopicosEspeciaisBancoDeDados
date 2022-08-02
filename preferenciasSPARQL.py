from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

outra_consulta = True
print('Selecione o tipo de consulta desejado: \n' + 
        '1 - Prefiro filmes de determinado diretor\n' + 
        '2 - Prefiro um filme em relação a outro se eles tem o mesmo diretor e gênero e é mais recente\n'
        '3 - Prefiro um filme em relação a outro se eles tem o mesmo gênero e é mais longo\n' + 
        '4 - Prefiro o filme mais recentes de cada diretor\n' +
        '5 - Prefiro o filme mais longo de determinado ator\n' + 
        '6 - Prefiro os filmes do diretor X com o ator Y')

tipo_consulta = input()

while outra_consulta:
    if tipo_consulta == '1':
        nome = input('Digite o nome do diretor: ')
        diretor = '"' + nome + '"'
        consulta = """
            PREFIX rdf: <https://www.w3.org/2007/OWL/wiki/RDF-Based_Semantics>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            SELECT DISTINCT ?movie ?title 
            WHERE {
                ?movie rdf:type dbo:Film.
                ?movie rdfs:label ?title.
                ?movie dbp:director ?d.
                ?d rdfs:label ?director.
                FILTER (LANG(?title)='en')
                FILTER regex (str(?director), %s, "i")
            } 
            """%(diretor)

        # Query for the description of "Capsaicin", filtered by language
        sparql.setQuery(consulta)

        # Convert results to JSON format
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # The return data contains "bindings" (a list of dictionaries)
        ret = sparql.queryAndConvert()
        pd.set_option('display.max_columns', None)
        results_df = pd.json_normalize(ret['results']['bindings'])
        final = results_df[['movie.value','title.value']]

    if tipo_consulta == '2':
        gen = input('Escolha o gênero: ')
        genero = '"' + gen + '"'
        limit = int(input('Digite o numero de resultados que deseja receber: '))
        consulta = """
            PREFIX rdf: <https://www.w3.org/2007/OWL/wiki/RDF-Based_Semantics>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>
            SELECT DISTINCT ?movie ?title ?director ?genre ?released
            WHERE {
                ?movie rdf:type dbo:Film.
                ?movie rdfs:label ?title.
                ?movie dbp:director ?d.
                ?d rdfs:label ?director.
                ?movie dbp:released ?released.
                ?movie dct:subject ?g.
                ?g rdfs:label ?genre. 
                FILTER ((LANG(?title)='en') && (LANG(?director)='en') && (datatype(?released) = xsd:integer))
                FILTER regex (str(?genre), %s, "i")
                FILTER NOT EXISTS{
                    ?movie2 rdf:type dbo:Film.
                    ?movie2 rdfs:label ?title2.
                    ?movie2 dbp:director ?d2.
                    ?d2 rdfs:label ?director2.
                    ?movie dbp:released ?released2.                    
                    ?g2 rdfs:label ?genre2.
                    FILTER ((LANG(?title2)='en') && (LANG(?director2)='en') && (datatype(?released2) = xsd:integer))
                    FILTER((?director = ?director2) && (?genre = ?genre2) && (?released2 < ?released))
                }   
            } LIMIT %d
            """%(genero,limit)

        # Query for the description of "Capsaicin", filtered by language
        sparql.setQuery(consulta)

        # Convert results to JSON format
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # The return data contains "bindings" (a list of dictionaries)
        ret = sparql.queryAndConvert()
        pd.set_option('display.max_columns', None)
        results_df = pd.json_normalize(ret['results']['bindings'])
        final = results_df[['movie.value','title.value','director.value','genre.value','released.value']]
        
    if tipo_consulta == '3':
        g = input('Digite o genero desejado: ')
        genero = '"' + g + '"'
        limit = int(input('Digite o numero de resultados que deseja receber: '))
        consulta = """
            PREFIX rdf: <https://www.w3.org/2007/OWL/wiki/RDF-Based_Semantics>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            SELECT DISTINCT ?movie ?title ?genre (xsd:double(?runtimeStr)/60.0 as ?runtime)
            WHERE {
                ?movie rdf:type dbo:Film.
                ?movie rdfs:label ?title.
                ?movie dbo:runtime ?runtimeStr.
                ?movie dct:subject ?g.
                ?g rdfs:label ?genre.
                FILTER regex (str(?genre), %s, "i")
                FILTER (LANG(?title)='en')
                FILTER NOT EXISTS{
                    ?movie2 rdf:type dbo:Film.
                    ?movie2 rdfs:label ?title2.
                    ?movie2 dbo:runtime ?runtimeStr2.
                    ?movie2 dct:subject ?g2.
                    ?g2 rdfs:label ?genre2.
                    FILTER (LANG(?title2)='en')
                    FILTER((?genre = ?genre2) && (?runtimeStr2 > ?runtimeStr))
                }   
            }LIMIT %d
        """%(genero,limit)

        sparql.setQuery(consulta)

        # Convert results to JSON format
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # The return data contains "bindings" (a list of dictionaries)
        ret = sparql.queryAndConvert()
        pd.set_option('display.max_columns', None)
        results_df = pd.json_normalize(ret['results']['bindings'])
        final = results_df[['movie.value','title.value','genre.value','runtime.value']]
        
    if tipo_consulta == '4':
        limit = int(input('Digite o numero de resultados que deseja receber: '))
        consulta = """
            PREFIX rdf: <https://www.w3.org/2007/OWL/wiki/RDF-Based_Semantics>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>        
            SELECT ?movie ?title ?director ?released
            WHERE {
                ?movie rdf:type dbo:Film.
                ?movie dbo:director ?director.
                ?movie rdfs:label ?title.
                ?movie dbp:released ?released.
                FILTER ((LANG(?title) = "en") && (datatype(?released) = xsd:integer))
                FILTER NOT EXISTS{
                    ?movie2 rdf:type dbo:Film.
                    ?movie2 dbo:director ?director2.
                    ?movie2 rdfs:label ?title2.
                    ?movie2 dbp:released ?released2.
                    FILTER ((LANG(?title) = "en") && (datatype(?released2) = xsd:integer))
                    FILTER((?director = ?director2) && (?released2 > ?released))
                }
            }LIMIT %d
        """%(limit)

        # Query for the description of "Capsaicin", filtered by language
        sparql.setQuery(consulta)

        # Convert results to JSON format
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # The return data contains "bindings" (a list of dictionaries)
        ret = sparql.queryAndConvert()
        pd.set_option('display.max_columns', None)
        results_df = pd.json_normalize(ret['results']['bindings'])
        final = results_df[['movie.value','title.value','director.value','released.value']]

    if tipo_consulta == '5':
        a = input('Digite o nome do ator: ')
        ator = '"' + a + '"'
        consulta = """
            PREFIX rdf: <https://www.w3.org/2007/OWL/wiki/RDF-Based_Semantics>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbp: <http://dbpedia.org/property/>        
            SELECT ?movie ?title ?actor (xsd:double(?runtimeStr)/60.0 as ?runtime)
            WHERE {
                ?movie rdf:type dbo:Film.
                ?movie rdfs:label ?title.
                ?movie dbp:starring ?actor.
                ?movie dbp:runtime ?runtimeStr.
                FILTER ((LANG(?title) = "en") && (LANG(?actor) = "en"))
                FILTER regex (str(?actor), %s, "i")
                FILTER NOT EXISTS{
                    ?movie2 rdf:type dbo:Film.
                    ?movie2 rdfs:label ?title2.
                    ?movie2 dbp:starring ?actor2.
                    ?movie2 dbp:runtime ?runtimeStr2.
                    FILTER ((LANG(?title2) = "en") && (LANG(?actor2) = "en"))
                    FILTER((?actor = ?actor2) && ((xsd:double(?runtimeStr2)/60.0 as ?runtime2) > (xsd:double(?runtimeStr)/60.0 as ?runtime)))
                }
            }
        """%(ator)

        # Query for the description of "Capsaicin", filtered by language
        sparql.setQuery(consulta)

        # Convert results to JSON format
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # The return data contains "bindings" (a list of dictionaries)
        ret = sparql.queryAndConvert()
        pd.set_option('display.max_columns', None)
        results_df = pd.json_normalize(ret['results']['bindings'])
        final = results_df[['movie.value','title.value','actor.value','runtime.value']]
    
    if tipo_consulta == '6':
        d = input('Digite o nome do diretor: ')
        diretor = '"' + d + '"'
        a = input('Digite o nome do ator: ')
        ator = '"' + a + '"'
        consulta = """
            PREFIX rdf: <https://www.w3.org/2007/OWL/wiki/RDF-Based_Semantics>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/>        
            SELECT ?movie ?title
            WHERE {
                ?movie rdf:type dbo:Film.
                ?movie rdfs:label ?title.
                ?movie dbo:director ?d.
                ?d rdfs:label ?director.
                ?movie dbp:starring ?actor
                FILTER ((LANG(?title) = "en") && (LANG(?director) = "en") && (LANG(?actor) = "en"))
                FILTER regex (str(?actor), %s, "i")
                FILTER regex (str(?director), %s, "i")
            }       
        """%(ator,diretor)

        # Query for the description of "Capsaicin", filtered by language
        sparql.setQuery(consulta)

        # Convert results to JSON format
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        # The return data contains "bindings" (a list of dictionaries)
        ret = sparql.queryAndConvert()
        pd.set_option('display.max_columns', None)
        results_df = pd.json_normalize(ret['results']['bindings'])
        final = results_df[['movie.value','title.value']]

    final.to_csv("saida.csv", index = False)
    
    proxima = input('Deseja realizar outra consulta(s/n)? ')
    if proxima == 'n':
        outra_consulta = False
    else:
        print('Selecione o tipo de consulta desejado: \n' + 
        '1 - Prefiro filmes de determinado diretor\n' + 
        '2 - Prefiro um filme em relação a outro se eles tem o mesmo diretor e gênero e é mais recente\n'
        '3 - Prefiro um filme em relação a outro se eles tem o mesmo gênero e é mais longo\n' + 
        '4 - Prefiro o filme mais recente de cada diretor\n' +
        '5 - Prefiro o filme mais longo de determinado ator\n' +
        '6 - Prefiro os filmes do diretor X com o ator Y')
        tipo_consulta = input()
