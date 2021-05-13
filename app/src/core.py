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

    def create_films(self, id, genre_ids, title, overview, release_date, vote_average, imageUrl):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, id, genre_ids, title, overview, release_date, vote_average, imageUrl)
            return greeting

    @staticmethod
    def _create_and_return_greeting(tx, id, genre_ids, title, overview, release_date, vote_average, backdrop_path):
        result = tx.run("CREATE (n:Filme {id_filme: $id, genre_ids: $genre_ids, title: $title, overview: $overview, release_date: $release_date, vote_average: $vote_average, imageUrl: $backdrop_path })", id=id, genre_ids=genre_ids, title=title, overview=overview, release_date=release_date, vote_average=vote_average, backdrop_path=backdrop_path)
        return result.data()

    def find_popular_genre(self, genre_ids):
        with self.driver.session() as session:
            find_popular_by_genre = session.read_transaction(self._find_popular_by_genre, genre_ids)
            return find_popular_by_genre
    
    @staticmethod
    def _find_popular_by_genre(tx, genre_ids):
        # query = "MATCH (f:Filme) WHERE f.genre_ids[0] ="+genre_ids+"RETURN f ORDER BY f.vote_average DESC"
        query = "MATCH (f:Filme) WHERE {} IN f.genre_ids RETURN f ORDER BY f.vote_average DESC LIMIT 4".format(genre_ids)
        result = tx.run(query)
        return result.data()

    def create_user(self, name, username, password):
        with self.driver.session() as session:
            create_user = session.write_transaction(self._create_user, name, username, password)
            return create_user

    @staticmethod
    def _create_user(tx, name, username, password):
        result = tx.run("CREATE (n:Pessoa {name: $name, username: $username, password: $password})", name=name, username=username, password=password)
        return result.data()

    def find_by_user(self, username):
        with self.driver.session() as session:
            find_movie_by_user = session.read_transaction(self._find_movie_by_user, username)
            return find_movie_by_user
    
    @staticmethod
    def _find_movie_by_user(tx, username):
        result = tx.run('MATCH (f:Filme)<-[:CURTIU]-(n:Pessoa) WHERE n.username = "{}" RETURN f;'.format(username))
        return result.data()

    def find_by_like(self, username):
        with self.driver.session() as session:
            find_movie_by_like = session.read_transaction(self._find_movie_by_like, username)
            return find_movie_by_like
    
    @staticmethod
    def _find_movie_by_like(tx, username):
        query = 'MATCH (p:Pessoa)-[:CURTIU]->(f:Filme)<-[:CURTIU]-(p2:Person)-[:CURTIU]->(f2:Filme) WHERE p.name = "{}" WITH f2 WHERE NOT (p)-[:CURTIU]->(f2) RETURN f2, COUNT(f2) as f2_t ORDER BY f2_t DESC LIMIT 4'.format(username)
        result = tx.run(query)
        return result.data()

    def like_movie(self, username, movie_id):
        with self.driver.session() as session:
            movie_liked = session.write_transaction(self._like_movie, username, movie_id)
            return movie_liked

    @staticmethod
    def _like_movie(tx, username, movie_id):
        query = 'MATCH (p:Pessoa), (f:Filme) WHERE p.username = "{}" AND id(f) = {} CREATE (p)-[:CURTIU]->(f)'.format(username, movie_id)
        result = tx.run(query)
        return result.data()
    
    def show_users(self):
        with self.driver.session() as session:
            users = session.read_transaction(self._show_users)
            return users
    
    @staticmethod
    def _show_users(tx):
        query = "MATCH (n:Pessoa) RETURN id(n) as id, n.name as name, n.username as username"
        result = tx.run(query)
        return result.data()

#altenative bolt://host.docker.internal:7687/ enable extra_host in docker-compose.yml
if __name__ == "__main__":
    start = time.time()

    greeter = CreateNode("bolt://host.docker.internal:7687/", "neo4j", "")

    for page in range(1, 3):
        res = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+ MOVIE_API + '&page='+str(page))
        response = json.loads(res.text)

        for filme in range(0,len(response['results'])):
            results = response['results'][filme]

            if ('id' in results) and ('original_title' in results) and ('overview' in results) and ('release_date' in results) and ('vote_average' in results) and ('backdrop_path' in results):
                # if results['genre_ids'] == []:
                    # print(results['original_title'])
                if results['backdrop_path'] == None and results['genre_ids'] != []:
                    greeter.create_films(results['id'],results['genre_ids'], results['original_title'], results['overview'], results['release_date'], results['vote_average'], "Image not found")
                    
                else:
                    if results['genre_ids'] != []:
                        greeter.create_films(results['id'],results['genre_ids'], results['original_title'], results['overview'], results['release_date'], results['vote_average'], "https://image.tmdb.org/t/p/w500/"+results['backdrop_path'])

            else:
                continue
    
    greeter.create_user("Luigi Muller", "luigim1998", 'luluzinho')
    greeter.create_user("Miller", "ttezo", 'Tarlisonzinho')
    greeter.like_movie("luigim1998", 10)
    greeter.like_movie("ttezo", 10)
    greeter.like_movie("ttezo", 15)
    greeter.like_movie("ttezo", 17)
    # print("Filmes populares do gênero 12", greeter.find_popular_genre(12))
    # print("Filmes gostados por ttezo", greeter.find_by_user("ttezo"))
    print("Filmes recomendados por ttezo", greeter.find_by_like("luigim1998"))
    print("Nomes dos usuários", greeter.show_users())
    end = time.time()
    print("tempo", end - start)
    greeter.close()