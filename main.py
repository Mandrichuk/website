from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask("Movies")


# movies = {
#     "AIR (2023)": ("https://upload.wikimedia.org/wikipedia/en/d/de/AirFilmPoster.png", "FREE", "FILM", "Drama"),
#     "JOHN WICK (2023)": ("https://m.media-amazon.com/images/M/MV5BMDExZGMyOTMtMDgyYi00NGIwLWJhMTEtOTdkZGFjNmZiMTEwXkEyXkFqcGdeQXVyMjM4NTM5NDY@._V1_.jpg", "2.99$", "SERIES", "Horror"), 
#     "TETRIS (2023)": ("https://m.media-amazon.com/images/M/MV5BZmZmNTdiYjMtZDdmNi00ZGU4LThkYmQtZTFhZWNlYmUxYWZkXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_QL75_UX190_CR0,0,190,281_.jpg", "FREE", "SERIES", "Comedy"), 
#     "JUNIPER (2021)": ("https://m.media-amazon.com/images/M/MV5BZmNjMjA4OGItMzc5OS00MWJlLWJlM2UtNWQ0MTZjZmIwNmQyXkEyXkFqcGdeQXVyOTM5NzYzNTU@._V1_QL75_UY281_CR0,0,190,281_.jpg", "1.20$", "SERIES", "Drama"),
#     "AVATAR (2022)": ("https://m.media-amazon.com/images/M/MV5BYjhiNjBlODctY2ZiOC00YjVlLWFlNzAtNTVhNzM1YjI1NzMxXkEyXkFqcGdeQXVyMjQxNTE1MDA@._V1_FMjpg_UX1000_.jpg", "3$", "FILM", "Comedy"),
#     "CREED III (2023)": ("https://m.media-amazon.com/images/M/MV5BYWY1ZDY4MmQtYjhiYS00N2QwLTk1NzgtOWI2YzUwZThjNDYwXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg", "4.49$", "FILM", "Drama"),
#     "RYE LANE (2023)": ("https://m.media-amazon.com/images/M/MV5BMzczMjMyZjUtMGE4ZS00MDAwLTg5OGItY2ZhNDA3ZTA5ZTAzXkEyXkFqcGdeQXVyNDQxOTAyNA@@._V1_.jpg", "2.99$", "FILM", "Roman"),
#     "HIS ONLY SON (2023)": ("https://m.media-amazon.com/images/M/MV5BZTU5MTY4OGMtYTRiMS00ZTA1LThmMGQtOWQ4YzE4NThlYjljXkEyXkFqcGdeQXVyNzYzMjAyMzU@._V1_FMjpg_UX1000_.jpg", "FREE", "SERIES", "Roman"),
#     "SHOWING UP (2022)": ("https://m.media-amazon.com/images/M/MV5BNTIxODkxMDYtNDIxMC00NzU4LTgzYjgtZjkyNDVlNmRmNDNhXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_.jpg", "FREE", "SERIES", "Roman"),
#     "I SEE YOU (2019)": ("https://m.media-amazon.com/images/M/MV5BNzVkOWM5YTEtMDdkNi00YjMzLWEzNWEtODEwN2IyZTc4Yjg2XkEyXkFqcGdeQXVyMjc5MTg0MzQ@._V1_.jpg", "5$", "FILM", "Horror")}


if __name__ == "__main__":

    @app.route("/login")
    def login():
        return render_template("login.html")


    @app.route("/")
    def main():
        return render_template("main.html")

    @app.route("/add_movie")
    def add_movie():
        return render_template("add_movie.html")

    @app.route("/movies")
    @app.route("/movies", methods=["POST"])
    def all_movies():
        with open("data.json", "r") as file:
            movies = json.loads(file.read())
            
        if request.method == "POST":

            new_name = request.form["new_name"].upper()
            new_picture = request.form["new_picture"]
            new_cost = request.form["new_cost"]
            new_movie = request.form["new_movie"].upper()
            new_genre = request.form["new_genre"].capitalize()

            if new_cost != "FREE":
                new_cost += "$"

            movies[new_name] = (new_picture, new_cost, new_movie, new_genre)

            with open("data.json", "w", encoding="utf-8") as file:  
                json.dump(movies, file, indent=4)

        return render_template("movies.html", movies=movies)

    @app.route("/watch_later/clear")
    @app.route("/watch_later/clear", methods=["POST"])
    def clear_watch_later():
        with open("watch_later.json", "w", encoding="utf-8") as file:  
                json.dump({}, file,indent=4)
        return redirect(url_for("watch_later"))

    @app.route("/watch_later/add", methods=["POST"])
    def watch_later_add():
        watch_later = {}
        if request.method == "POST":
            movie_name = request.form["movie_name"].upper()
            movie_picture = request.form["movie_picture"]
            movie_cost = request.form["movie_cost"]
            movie_type = request.form["movie_type"].upper()
            movie_genre = request.form["movie_genre"].capitalize()

            referrer = request.referrer
            if referrer == "http://127.0.0.1:5000/movies":
                referrer = "all_" + referrer.split("/")[-1]

            else:
                referrer = referrer.split("/")[-1] + "_movies"


            with open("watch_later.json", "r") as file:
                watch_later = json.loads(file.read())

            watch_later[movie_name] = (movie_picture, movie_cost, movie_type, movie_genre)

            with open("watch_later.json", "w", encoding="utf-8") as file:  
                json.dump(watch_later, file,indent=4)

        return redirect(url_for(referrer))


    @app.route("/watch_later")
    def watch_later():
        
        with open("watch_later.json", "r") as file:
            watch_later = json.loads(file.read())

        with open("watch_later.json", "w", encoding="utf-8") as file:  
            json.dump(watch_later, file,indent=4)
        
        return render_template("watch_later.html", watch_later=watch_later)

    



    @app.route("/movies/drama")
    def drama_movies():
        drama_films = {}
        drama_series = {}

        with open("data.json", "r") as file:
            movies = json.loads(file.read())

        for data in movies:
            if movies[data][3].lower() == "drama":
                if movies[data][2].lower() == "film":
                    drama_films[data] = movies[data]
                else:
                    drama_series[data] = movies[data]

        return render_template("media.html", genre=movies[data][3], films=drama_films, series=drama_series)

    @app.route("/movies/horror")
    def horror_movies():
        horror_films = {}
        horror_series = {}

        with open("data.json", "r") as file:
            movies = json.loads(file.read())

        for data in movies:
            if movies[data][3].lower() == "horror":
                if movies[data][2].lower() == "film":
                    horror_films[data] = movies[data]
                else:
                    horror_series[data] = movies[data]

        return render_template("media.html", genre=movies[data][3], films=horror_films, series=horror_series)

    @app.route("/movies/comedy")
    def comedy_movies():
        comedy_films = {}
        comedy_series = {}

        with open("data.json", "r") as file:
            movies = json.loads(file.read())

        for data in movies:
            if movies[data][3].lower() == "comedy":
                if movies[data][2].lower() == "film":
                    comedy_films[data] = movies[data]
                else:
                    comedy_series[data] = movies[data]

        return render_template("media.html", genre=movies[data][3], films=comedy_films, series=comedy_series)

    @app.route("/movies/roman")
    def roman_movies():
        roman_films = {}
        roman_series = {}

        with open("data.json", "r") as file:
            movies = json.loads(file.read())

        for data in movies:
            if movies[data][3].lower() == "roman":
                if movies[data][2].lower() == "film":
                    roman_films[data] = movies[data]
                else:
                    roman_series[data] = movies[data]

        return render_template("media.html", genre=movies[data][3], films=roman_films, series=roman_series)

    



    app.run(debug=True)

