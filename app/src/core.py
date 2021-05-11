import requests
import json
import time
from neo4j import GraphDatabase, basic_auth
from conf.settings import MOVIE_API

class CreateNode:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()

    def print_greeting(self, id, title, overview, release_date, vote_average, imageUrl):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, id, title, overview, release_date, vote_average, imageUrl)

    @staticmethod
    def _create_and_return_greeting(tx, id, title, overview, release_date, vote_average, backdrop_path):
        result = tx.run("CREATE (n:Filme {id: $id, title: $title, overview: $overview, release_date: $release_date, vote_average: $vote_average, imageUrl: $backdrop_path })", id=id, title=title, overview=overview, release_date=release_date, vote_average=vote_average, backdrop_path=backdrop_path)
        return result.single

#altenative bolt://host.docker.internal:7687/ enable extra_host in docker-compose.yml
if __name__ == "__main__":
    start = time.time()
    greeter = CreateNode("bolt://host.docker.internal:7687/", "neo4j", "")
    for page in range(1, 5):
        res = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+ MOVIE_API + '&page='+str(page))
        response = json.loads(res.text)
        for filme in range(0,len(response['results'])):

            if ('id' in response['results'][filme]) and ('original_title' in response['results'][filme]) and ('overview' in response['results'][filme]) and ('release_date' in response['results'][filme]) and ('vote_average' in response['results'][filme]) and ('backdrop_path' in response['results'][filme]):

                if response['results'][filme]['backdrop_path'] == None:
                    greeter.print_greeting(response['results'][filme]['id'],response['results'][filme]['original_title'], response['results'][filme]['overview'], response['results'][filme]['release_date'], response['results'][filme]['vote_average'], "Image not found")

                else:
                    greeter.print_greeting(response['results'][filme]['id'],response['results'][filme]['original_title'], response['results'][filme]['overview'], response['results'][filme]['release_date'], response['results'][filme]['vote_average'], "https://image.tmdb.org/t/p/w500/"+response['results'][filme]['backdrop_path'])

            else:
                continue
    end = time.time()
    print("tempo", end - start)
    greeter.close()
