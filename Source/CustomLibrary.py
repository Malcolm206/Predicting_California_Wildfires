import pandas as pd
pd.set_option('display.max_columns', 200) #set to show all columns
pd.set_option('display.max_rows', 2000) 

def county_week():
    counties_list = ['Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'Del Norte', 
                 'El Dorado', 'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo', 'Kern','Kings', 'Lake', 
                 'Lassen', 'Los Angeles', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono',
                 'Monterey', 'Napa', 'Nevada', 'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 
                 'San Benito', 'San Bernardino', 'San Diego', 'San Francisco', 'San Joaquin', 'San Luis Obispo', 
                 'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra', 'Siskiyou', 
                 'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare', 'Tuolumne', 
                 'Ventura', 'Yolo', 'Yuba']
    county_w = []
    for x in range(0, 313):
        for y in range(0, 58):
            county_w.append(counties_list[y])
    date_w = pd.date_range('2013-01-01', '2018-12-31', freq = 'W')
    date_w = date_w.repeat(58)
    date_counties_w = pd.DataFrame()
    date_counties_w['date'] = date_w
    date_counties_w['county'] = county_w
    date_counties_w = date_counties_w.reset_index(drop = True)
    
    return date_counties_w

def county_fire(df):
    counties_list = ['Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'Del Norte', 
             'El Dorado', 'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo', 'Kern','Kings', 'Lake', 
             'Lassen', 'Los Angeles', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono',
             'Monterey', 'Napa', 'Nevada', 'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 
             'San Benito', 'San Bernardino', 'San Diego', 'San Francisco', 'San Joaquin', 'San Luis Obispo', 
             'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra', 'Siskiyou', 
             'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare', 'Tuolumne', 
             'Ventura', 'Yolo', 'Yuba']
    df_dt = df.loc[df['Started'] < '2019-01-01']
    county_df = []
    for x in counties_list:
        cdf = df_dt.loc[kag_df_dt['Counties'] == x]
        cdf = cdf.resample('W', on = 'Started').mean()
        cdf.dropna(inplace = True)
        cdf = cdf.reset_index()
        cdf['county'] = x
        county_df.append(cdf)
    return county_df

def fire_started(df):
    fire_started = pd.concat(df)
    fire_started['fire_started'] = 1
    fire_started.drop(columns = ['Counties', 'Extinguished', 'burn_time', 'index'], inplace = True)
    fire_started.columns = ['acres_burned', 'date', 'county', 'fire_started']
    return fire_started

def ground_cover_table(dictionary, files):
    counties_list = ['Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'Del Norte', 
                     'El Dorado', 'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo', 'Kern','Kings', 'Lake', 
                     'Lassen', 'Los Angeles', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono',
                     'Monterey', 'Napa', 'Nevada', 'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 
                     'San Benito', 'San Bernardino', 'San Diego', 'San Francisco', 'San Joaquin', 'San Luis Obispo', 
                     'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra', 'Siskiyou', 
                     'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare', 'Tuolumne', 
                     'Ventura', 'Yolo', 'Yuba']
    min_elevation = [-42, 1442, 43, -1, 787, -9, -30, 120, 145, 47, 2, 27, -81, -96, 58, 46, 18, 1145, 69, 61, -53, 
                     269, 7, 2, 1271, 1283, 95, -32, 256, -16, 174, 978, -81, 27, 15, -3, -72, 30, 6, 56, -11, 14, 
                     -22, 16, 111, 658, 490, -22, -24, -2, 234, 50, 114, 149, 374, 34, -26, 199]
    max_elevation = [1242, 3556, 3121, 2192, 3522, 1022, 680, 2215, 3299, 4153, 1756, 2709, 799, 3345, 2689, 524, 
                     2140, 2666, 3032, 3959, 577, 3952, 2252, 543, 3004, 4323, 1594, 84, 2784, 1732, 2787, 2543, 
                     3263, 1329, 1299, 3493, 1981, 667, 1889, 1538, 1317, 2693, 1316, 1153, 3159, 2687, 4294, 118, 
                     1438, 1026, 1652, 2444, 2450, 4409, 3959, 2332, 346, 2541]
    ground_cover = pd.DataFrame()
    for x in range(0, 58):
        df = dictionary[files[x]]
        df.drop(columns = ['OBJECTID', 'County', 'Count_', 'Min_', 'Max_', 'Mean', 'Perc25th', 'Median', 'Perc75th', 
                    'Perc95th', 'PercentMaxOwnerCounty', 'Gini', 'label', 'data', 'color'], inplace = True)
        df.dropna(inplace=True)
        df = df.T
        df1a = df
        df1a.columns = df.iloc[0]
        df1a = df.iloc[1:]
        df1a = df1a.reset_index(drop = True)
        df1b = pd.DataFrame(columns = df.iloc[0])
        df1b = df1b.append(df1a.loc[0])
        df1b.columns = df1b.columns + '_acres'
        df1c = pd.DataFrame(columns = df.iloc[0])
        df1c = df1c.append(df1a.loc[1] * 100)
        df1c.columns = df1c.columns + '_percentage'
        df1d = pd.concat([df1b, df1c], axis = 1)
        df1d.loc[2] = df1d.sum()
        df1d = df1d.iloc[2:]
        ground_cover = ground_cover.append(df1d)
    ground_cover['county'] = counties_list
    ground_cover['min_elevation'] = min_elevation
    ground_cover['max_elevation'] = max_elevation
    return ground_cover

def file_names():
    # find the files names for the ground cover each year. Then sort the files in alphabetical order
    files_2013 = glob('data/ground_cover_2013/*.csv')
    files_2013.sort()
    files_2014 = glob('data/ground_cover_2014/*.csv')
    files_2014.sort()
    files_2015 = glob('data/ground_cover_2015/*.csv')
    files_2015.sort()
    files_2016 = glob('data/ground_cover_2016/*.csv')
    files_2016.sort()
    files_2017 = glob('data/ground_cover_2017/*.csv')
    files_2017.sort()
    files_2018 = glob('data/ground_cover_2018/*.csv')
    files_2018.sort()
    # Create a list of files for each year
    files = [files_2013, files_2014, files_2015, files_2016, files_2017, files_2018]
    return files

def import_ground_cover(files):
    # Create an empty list for the dictionaries
    gc_list = []
    # Iterate over the each file year list
    for x in range(0, len(files):
        # create an empty dictionary for each county dataframe
        d = {}
        # Iterate over the list of counties
        for y in range(0, len(files[x])):
            # read in each file as a dataframe and enter it into the dictionary
            d[files[x][y]]= pd.read_csv(files[x][y])
        # Append the year dictionary to the list of year dictionaries
        gc_list.append(d)
    # Return the list of year dictionaries
    return gc_list


def ground_cover_data(gc_list, files):
    # Create a list of years
    years = [2013, 2014, 2015, 2016, 2017, 2018]
    # Create a list of year dataframes
    year_dfs = []
    # iterate over the list of year dictionaries
    for x in range(0, len(gc_list):
        # iterate over each dataframe in the year dictionary
        for y in range(0, len(gc_list[x])
            # Use ground_cover_table function to restructure the dataframes into a year dataframe 
            gc_year = ground_cover_table(gc_list[x], files[x][y])
            gc_year['year'] = years[x]
            year_dfs.append(gc_year)
    gc_data = pd.concat(year_dfs)
    return gc_data
                       
                   
                   
                   
                   
                   