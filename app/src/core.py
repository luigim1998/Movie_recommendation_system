import requests
import json
import time
from neo4j import GraphDatabase, basic_auth
from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS, cross_origin
from markupsafe import escape
from conf.settings import MOVIE_API

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class createNode:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()

    # criar filmes
    def create_films(self, id, genre_ids, title, overview, release_date, vote_average, imageUrl):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, id, genre_ids, title, overview, release_date, vote_average, imageUrl)
            return greeting

    @staticmethod
    def _create_and_return_greeting(tx, id, genre_ids, title, overview, release_date, vote_average, backdrop_path):
        result = tx.run("CREATE (n:Filme {id_filme: $id, genre_ids: $genre_ids, title: $title, overview: $overview, release_date: $release_date, vote_average: $vote_average, imageUrl: $backdrop_path })", id=id, genre_ids=genre_ids, title=title, overview=overview, release_date=release_date, vote_average=vote_average, backdrop_path=backdrop_path)
        return result.data()

    # acha os filmes de um determinado gênero (através do id do gênero)
    def find_popular_genre(self, genre_ids):
        with self.driver.session() as session:
            find_popular_by_genre = session.read_transaction(self._find_popular_by_genre, genre_ids)
            return find_popular_by_genre
    
    @staticmethod
    def _find_popular_by_genre(tx, genre_ids):
        # query = "MATCH (f:Filme) WHERE f.genre_ids[0] ="+genre_ids+"RETURN f ORDER BY f.vote_average DESC"
        query = "MATCH (f:Filme) WHERE {} IN f.genre_ids RETURN id(f) as id, f.title as title, f.imageUrl as imageUrl ORDER BY f.vote_average DESC LIMIT 4".format(genre_ids)
        result = tx.run(query)
        return result.data()

    # cria usuario
    def create_user(self, name, username, password):
        with self.driver.session() as session:
            create_user = session.write_transaction(self._create_user, name, username, password)
            return create_user

    @staticmethod
    def _create_user(tx, name, username, password):
        result = tx.run("CREATE (n:Pessoa {name: $name, username: $username, password: $password})", name=name, username=username, password=password)
        return result.data()

    # achar filmes curtidos pelo usuario
    def find_by_user(self, username):
        with self.driver.session() as session:
            find_movie_by_user = session.read_transaction(self._find_movie_by_user, username)
            return find_movie_by_user
    
    @staticmethod
    def _find_movie_by_user(tx, username):
        result = tx.run('MATCH (f:Filme)<-[:CURTIU]-(n:Pessoa) WHERE n.username = "{}" RETURN id(f) as id, f.title as title, f.imageUrl as imageUrl'.format(username))
        print(result)
        return result.data()

    #recomenda filmes baseado nos filmes que os outros usuarios curtiram, para isso ele analisa os filmes que os usuarios assistiram e que o usuario viu tambem
    def find_by_like(self, username):
        with self.driver.session() as session:
            find_movie_by_like = session.read_transaction(self._find_movie_by_like, username)
            return find_movie_by_like
    
    @staticmethod
    def _find_movie_by_like(tx, username):
        query = 'MATCH (p:Pessoa)-[:CURTIU]->(f:Filme)<-[:CURTIU]-(p2:Pessoa)-[:CURTIU]->(f2:Filme) WHERE p.username = "{}" WITH f2 WHERE NOT (p)-[:CURTIU]->(f2) RETURN id(f2) as id,f2.title as title, f2.imageUrl as imageUrl, COUNT(f2) as f2_t ORDER BY f2_t DESC LIMIT 4'.format(username)
        result = tx.run(query)
        return result.data()

    # usuario curte determinado filme
    def like_movie(self, username, movie_id):
        with self.driver.session() as session:
            movie_liked = session.write_transaction(self._like_movie, username, movie_id)
            return movie_liked

    @staticmethod
    def _like_movie(tx, username, movie_id):
        query = 'MATCH (p:Pessoa), (f:Filme) WHERE p.username = "{}" AND id(f) = {} MERGE (p)-[:CURTIU]->(f)'.format(username, movie_id)
        result = tx.run(query)
        return result.data()
    
    # descurtir filme
    def dislike_movie(self, username, movie_id):
        with self.driver.session() as session:
            movie_disliked = session.write_transaction(self._dislike_movie, username, movie_id)
            return movie_disliked

    @staticmethod
    def _dislike_movie(tx, username, movie_id):
        query = 'MATCH (p:Pessoa)-[c:CURTIU]->(f:Filme) WHERE p.username = "{}" AND id(f) = {} DELETE c'.format(username, movie_id)
        result = tx.run(query)
        return result.data()

    # mostra todos os usuarios
    def show_users(self):
        with self.driver.session() as session:
            users = session.read_transaction(self._show_users)
            return users
    
    @staticmethod
    def _show_users(tx):
        query = "MATCH (n:Pessoa) RETURN id(n) as id, n.name as name, n.username as username"
        result = tx.run(query)
        return result.data()
    
    # recomendar filmes que outros usuarios baseados no filme
    def recommend_movie_by_movie(self, movie_id):
        with self.driver.session() as session:
            movies = session.read_transaction(self._recommend_movie_by_movie, movie_id)
            return movies
    
    @staticmethod
    def _recommend_movie_by_movie(tx, movie_id):
        query = "MATCH (f:Filme)<-[:CURTIU]-(p2:Pessoa)-[:CURTIU]->(f2:Filme) WHERE id(f) = {} AND id(f2) <> {} RETURN id(f2) as id,f2.title as title, f2.imageUrl as imageUrl".format(movie_id, movie_id)
        result = tx.run(query)
        return result.data()

    def search_movie_by_id(self, movie_id):
        with self.driver.session() as session:
            search_movie = session.read_transaction(self._search_movie_by_id, movie_id)
            return search_movie
    
    @staticmethod
    def _search_movie_by_id(tx, movie_id):
        query = "MATCH (f:Filme) WHERE id(f) = {} RETURN f, id(f) as id".format(movie_id)
        result = tx.run(query)
        return result.data()

############## front end requests ##############

# GET movie by gender
@app.route('/gender/<int:genre_id>', methods=['GET'])
@cross_origin()
def api_genre_id(genre_id):
    if request.method == 'GET':
        return jsonify(greeter.find_popular_genre(genre_id))

# GET movie by user
@app.route('/movies/<username>', methods=['GET'])
@cross_origin()
def api_user_like_movie(username):
    if request.method == 'GET':
        return jsonify(greeter.find_by_user(username))

# GET movie details
@app.route('/movieDetails/<int:movie_id>', methods=['GET'])
@cross_origin()
def api_movie_details(movie_id):
    if request.method == 'GET':
        return jsonify(greeter.search_movie_by_id(movie_id))

# GET movies by user movies
@app.route('/moviesRecommended/<username>', methods=['GET'])
@cross_origin()
def api_movie_by_like(username):
    if request.method == 'GET':
        return jsonify(greeter.find_by_like(username))

# GET movies by movie
@app.route('/moviesByMovie/<int:movie_id>', methods=['GET'])
@cross_origin()
def api_recommend_movie_by_movie(movie_id):
    if request.method == 'GET':
        return jsonify(greeter.recommend_movie_by_movie(movie_id))

# POST like movie or DELETE dislike movie
@app.route('/likeMovie/<username>/<int:movie_id>', methods=['POST', 'DELETE'])
@cross_origin()
def api_like_movie(username, movie_id):
    if request.method == 'POST':
        greeter.like_movie(username, movie_id)
        return 'OK', 201

    if request.method == 'DELETE':
        greeter.dislike_movie(username, movie_id)
        res = make_response(jsonify({}), 204)
        return res

# GET all users or POST create user
@app.route('/users', methods=['GET', 'POST'])
@cross_origin()
def api_users():
    if request.method == 'GET':
        return jsonify(greeter.show_users())

    if request.method == 'POST':
        # print(request.is_json)
        content = request.json
        greeter.create_user(content['name'], content['username'], content['password'])
        return 'OK', 201

############## the end ##############

if __name__ == "__main__":
    start = time.time()

    global greeter
    greeter = createNode("bolt://host.docker.internal:7687/", "neo4j", "")

    for page in range(1, 3):
        res = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+ MOVIE_API + '&page='+str(page))
        response = json.loads(res.text)

        for filme in range(0,len(response['results'])):
            results = response['results'][filme]

            if ('id' in results) and ('original_title' in results) and ('overview' in results) and ('release_date' in results) and ('vote_average' in results) and ('poster_path' in results):
                # if results['genre_ids'] == []:
                    # print(results['original_title'])
                if results['poster_path'] == None and results['genre_ids'] != []:
                    greeter.create_films(results['id'],results['genre_ids'], results['original_title'], results['overview'], results['release_date'], results['vote_average'], "Image not found")
                    
                else:
                    if results['genre_ids'] != []:
                        greeter.create_films(results['id'],results['genre_ids'], results['original_title'], results['overview'], results['release_date'], results['vote_average'], "https://image.tmdb.org/t/p/w500/"+results['poster_path'])

            else:
                continue
    
    greeter.create_user("Luigi Muller", "luigim1998", 'luluzinho')
    greeter.create_user("Miller", "ttezo", 'Tarlisonzinho')
    greeter.create_user("Pedro Aleph", "pedroaleph", 'password')
    greeter.create_user("Talirson", "magictorto", 'hatsunemiku')
    greeter.create_user("Leandro", "balico", 'kubernates')
    greeter.create_user("Joshua", "joshua", 'joshua')
    greeter.create_user("Victor", "rocha", 'barbosa')
    greeter.create_user("Franscisco", "chico", 'chicael')
    greeter.create_user("Ewelly", "ewelly", 'ewelly')
    greeter.create_user("Josemar", "jukka", 'rodrigo')
    
    greeter.like_movie("pedroaleph", 1)
    greeter.like_movie("pedroaleph", 3)
    greeter.like_movie("pedroaleph", 25)
    greeter.like_movie("rocha", 25)
    greeter.like_movie("rocha", 7)
    greeter.like_movie("rocha", 6)
    greeter.like_movie("joshua", 6)
    greeter.like_movie("magictorto", 6)
    greeter.like_movie("balico", 6)
    greeter.like_movie("chico", 6)
    greeter.like_movie("jukka", 7)
    greeter.like_movie("ewelly", 25)
    greeter.like_movie("luigim1998", 7)
    greeter.like_movie("luigim1998", 10)
    greeter.like_movie("ttezo", 10)
    greeter.like_movie("ttezo", 15)
    greeter.like_movie("ttezo", 17)
    
    print("Filmes populares do gênero 12", greeter.find_popular_genre(12))
    print("Filmes gostados por ttezo", greeter.find_by_user("ttezo"))
    greeter.dislike_movie("ttezo", 17)
    print("Filmes gostados por ttezo", greeter.find_by_user("ttezo"))
    print("Filmes recomendados por luigim1998", greeter.find_by_like("luigim1998"))
    print("Filmes recomendados pelo filme 15", greeter.recommend_movie_by_movie(15))
    print("Nomes dos usuários", greeter.show_users())
    print("Filme 12", greeter.search_movie_by_id(12))

    end = time.time()
    print("tempo", end - start)

    app.run(host="0.0.0.0", debug=True)
    greeter.close()
