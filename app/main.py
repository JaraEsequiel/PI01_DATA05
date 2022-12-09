from fastapi import FastAPI
import pandas as pd
import numpy as np
from collections import Counter
from starlette.responses import RedirectResponse

#Instance of FastApi
app = FastAPI()

#Import DF's
df_movies = pd.read_csv('Data/movies.csv')
df_tv = pd.read_csv('Data/tv_shows.csv')

#First root
@app.get('/')
def read_root():
    return RedirectResponse(url='/docs/')

#Get max duration of a movie according to year and platform
@app.get('/get_max_duration({year}, {platform}, {type})')
def get_max_duration(year: int, platform: str, type: str):
    # if type agrees with min it is a movie
    if type == 'min':
        # validate year and platform exist inside the dataframe

        if ((year in df_movies.release_year.unique()) & (platform in df_movies.platform.unique())):
            # Generates a bolean to find the wanted rows according to year and platform
            year_condition = (df_movies['release_year'] == year)
            platform_condition = (df_movies['platform'] == platform)
            # Creates an auxiliar dataframe to search the row
            df_aux = df_movies[platform_condition & year_condition]
            # Store the values of the max duration movie
            value_list = df_aux[df_aux.duration ==
                                df_aux.duration.max()].values[0].tolist()
            # Store tittle value
            title = value_list[0]
            # Store duration value
            duration = f"{value_list[8]} min"
        else:
            # Return an error if year or platform are wrong
            return {'ERROR': 'something went wrong with year or platform'}

    # if type agrees with season it is a tv_show
    elif type == 'season':
        # validate year and platform exist inside the dataframe
        if ((year in df_tv.release_year.unique()) & (platform in df_tv.platform.unique())):
            # Generates a bolean to find the wanted rows according to year and platform
            year_condition = (df_tv['release_year'] == year)
            platform_condition = (df_tv['platform'] == platform)
            # Creates an auxiliar dataframe to search the row
            df_aux = df_tv[platform_condition & year_condition]
            # Store the values of the max duration movie
            value_list = df_aux[df_aux.duration ==
                                df_aux.duration.max()].values[0].tolist()
            # Store tittle value
            title = value_list[0]
            # Store duration value
            duration = f"{value_list[8]} seasons"
        else:
            # Return an error if year or platform are wrong
            return {'ERROR': 'something went wrong with year or platform'}
    else:
        # Return an error if type is wrong
        return {'ERROR': 'something went wrong with type'}

    # Store the corresponding values
    response = {'title': title, 'year': year,
                'platform': platform, 'duration': duration}

    return response  # Return the response

# Get amount of movies and tv shows according to platform parameter


@app.get('/get_count_platform({platform})')
def get_count_platform(platform: str):
    # validate if the parameter passed is in platform column.
    if (platform in df_movies['platform'].unique()) | (platform in df_tv['platform'].unique()):
        # store the amount of movies and shows.
        movies = len(df_movies[df_movies['platform'] == platform])
        shows = len(df_tv[df_tv['platform'] == platform])
        # return the data
        return {'platform': platform, 'movies': movies, 'shows': shows}
    else:
        # return error if the platform don't exist
        return {'ERROR': 'Wrong platform'}

# return the platform with max coincidence of a genre according to genre parameter


@app.get('/get_listedin({genre})')
def get_listedin(genre: str):

    # If the genre exists in the dataframe
    if ((genre in df_movies['genre'].unique()) | (genre in df_tv['genre'].unique())):

        # existing platforms, use set to store only unique values and convert to list
        platforms = list(set(df_movies['platform'].unique(
        ).tolist() + df_tv['platform'].unique().tolist()))

        max_reps = 0  # max reps of a genre
        max_platform = ''  # platform with max reps

        print(platforms)
        # for each platform in the list
        for platform in platforms:

            # generates a df of that platform fot movies and shows
            df_m = df_movies[df_movies['platform'] == platform]
            df_s = df_movies[df_movies['platform'] == platform]

            # concat the df's
            df = pd.concat([df_m, df_s])

            # Count reps
            reps = df.genre.str.count(genre).sum()

            # if the reps of the actual platform is greater than last platform rewrite the content
            if reps > max_reps:
                max_reps = int(reps)
                max_platform = platform

    else:
        # return a error msg if not exist that genre
        return {'ERROR': 'Genre not found.'}

    # return the platform, genre and reps
    return {'platform': max_platform, 'genre': genre, 'count': max_reps}

# Get actor with more repetitions according to platform and year


@app.get('/get_actor({platform}, {year})')
def get_actor(platform: str, year: int):
    # Create a general df
    df = pd.concat([df_movies, df_tv])

    if ((platform in df.platform.unique()) & (year in df.release_year.unique())):
        # Search conditions
        year_condition = (df['release_year'] == year)
        platform_condition = (df['platform'] == platform)

        # DF according to year and platform
        df = df.loc[(year_condition & platform_condition)]

        # list for actors
        actors_list = []

        # for each actor in column cast
        for actor in df.cast:
            # if type is float continue the iteration
            if actor == "No Data":
                continue

            # Split list's of actors
            splited_list = actor.split(',')
            # Trim the str
            for striped in splited_list:
                # add the trimmed str to actors list
                actors_list.append(striped.strip())

        # Use counter to generate a dicc with the name of the actor and the times its appears in the list
        actors_list = Counter(actors_list)
        result = actors_list.most_common()[0]  # get the most common actor

        # return the request
        return {'platform': platform, 'year': year, 'actor': result[0], 'amount': result[1]}
    else:
        return {'ERROR': 'platform or year not found.'}
