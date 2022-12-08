#Get max duration movie according to: year and platform

def get_max_duration(year: int, platform: str, type: str): 

    #if type agrees with min it is a movie
    if type == 'min': 
        # validate year and platform exist inside the dataframe

        if ((year in df_movies.release_year.unique()) & (platform in df_movies.platform.unique())):
            #Generates a bolean to find the wanted rows according to year and platform
            year_condition = (df_movies['release_year'] == year) 
            platform_condition = (df_movies['platform'] == platform)
            #Creates an auxiliar dataframe to search the row
            df_aux = df_movies[platform_condition & year_condition]
            #Store the values of the max duration movie
            value_list = df_aux[df_aux.duration ==
                                df_aux.duration.max()].values[0].tolist()
            #Store tittle value
            title = value_list[0]
            #Store duration value
            duration = f"{value_list[8]} min"
        else:
            return {'ERROR': 'something went wrong with year or platform'} #Return an error if year or platform are wrong 

    #if type agrees with season it is a tv_show
    elif type == 'season':
        # validate year and platform exist inside the dataframe
        if ((year in df_tv.release_year.unique()) & (platform in df_tv.platform.unique())):
            #Generates a bolean to find the wanted rows according to year and platform
            year_condition = (df_tv['release_year'] == year)
            platform_condition = (df_tv['platform'] == platform)
            #Creates an auxiliar dataframe to search the row
            df_aux = df_tv[platform_condition & year_condition]
            #Store the values of the max duration movie 
            value_list = df_aux[df_aux.duration ==
                                df_aux.duration.max()].values[0].tolist()
            #Store tittle value
            title = value_list[0]
            #Store duration value
            duration = f"{value_list[8]} seasons"
        else:
            return {'ERROR': 'something went wrong with year or platform'} #Return an error if year or platform are wrong 
    else:
        return {'ERROR': 'something went wrong with type'} #Return an error if type is wrong 

    #Store the corresponding values
    response = {'title': title, 'year': year,
                'platform': platform, 'duration': duration}

    return response #Return the response