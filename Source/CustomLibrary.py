import pandas as pd
pd.set_option('display.max_columns', 200) #set to show all columns
pd.set_option('display.max_rows', 2000)
from glob import glob
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, accuracy_score, recall_score, confusion_matrix

def county_week():
    '''
    
    Creates a dataframe of weeks in the years 2013-2018 for each California county
    
    '''
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
    date_counties_w['year'] = pd.DatetimeIndex(date_counties_w['date']).year
    
    return date_counties_w

def county_fire(df):
    '''
    
    From the inputed dataframe (Calfire Wildfire Incidents) and returns a list of county dataframes with target variable on weekly observations
    
    '''
    counties_list = ['Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'Del Norte', 
             'El Dorado', 'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo', 'Kern','Kings', 'Lake', 
             'Lassen', 'Los Angeles', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono',
             'Monterey', 'Napa', 'Nevada', 'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 
             'San Benito', 'San Bernardino', 'San Diego', 'San Francisco', 'San Joaquin', 'San Luis Obispo', 
             'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra', 'Siskiyou', 
             'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare', 'Tuolumne', 
             'Ventura', 'Yolo', 'Yuba']
    df_s = df[['AcresBurned', 'Counties', 'Extinguished', 'Started']]
    df_s['Extinguished'] = pd.to_datetime(df_s['Extinguished'])
    df_s['Started'] = pd.to_datetime(df_s['Started'])
    df_s['Extinguished'] = df_s['Extinguished'].dt.date
    df_s['Started'] = df_s['Started'].dt.date
    df_s['Extinguished'] = pd.to_datetime(df_s['Extinguished'])
    df_s['Started'] = pd.to_datetime(df_s['Started'])
    df_dt = df_s.loc[df_s['Started'] < '2019-01-01']
    county_df = []
    for x in counties_list:
        cdf = df_dt.loc[df_dt['Counties'] == x]
        cdf = cdf.resample('W', on = 'Started').mean()
        cdf.dropna(inplace = True)
        cdf = cdf.reset_index()
        cdf['county'] = x
        county_df.append(cdf)
    return county_df

def fire_started(df):
    '''
    
    From a list of dataframes (county_fire function return), merges into one dataframe and sets the target variable as binary
    
    '''
    fire_started = pd.concat(df)
    fire_started['fire_started'] = 1
    fire_started.drop(columns = ['Counties', 'Extinguished', 'index'], inplace = True)
    fire_started.columns = ['acres_burned', 'date', 'county', 'fire_started']
    return fire_started

def ground_cover_table(dictionary, files):
    '''
    
    From a dictionary of county Summary Land Use Statistics dataframes, returns dataframe where each row is county observation with land cover acres, land cover percentage of county, and elevation of county.
    
    '''
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
    '''
    
    Finds file names for ground cover from each year, and returns a list with lists of ground cover for each year
    
    '''
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
    '''
    
    Imports csv files and returns a list of dictionaries with ground cover dataframes (a dictionary per year).
    
    '''
    # Create an empty list for the dictionaries
    gc_list = []
    # Iterate over the each file year list
    for x in range(0, len(files)):
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
    '''
    
    Takes a list of dictionaries and returns one dataframe with county ground cover from each year
    
    '''
    # Create a list of years
    years = [2013, 2014, 2015, 2016, 2017, 2018]
    # Create a list of year dataframes
    year_dfs = []
    # iterate over the list of year dictionaries
    for x in range(0, len(gc_list)):
        # Use ground_cover_table function to restructure the dataframes into a year dataframe 
        gc_year = ground_cover_table(gc_list[x], files[x])
        gc_year['year'] = years[x]
        year_dfs.append(gc_year)
    gc_data = pd.concat(year_dfs)
    return gc_data
                       
def import_cimis(filenames):
    '''
    
    Enters an alphabetically sorted list of filenames from CIMIS data source and returns a dictionary 
    of county weather dataframes with only the useful columns for the project.
    
    '''
    # Create an empty dictionary to read in new dataframes
    wd = {}
    # Iterate through list of csv files and read in the files to the dictionary
    for x in range(0, len(filenames)):
        wd[filenames[x]] = pd.read_csv(filenames[x])
    # Create a list of California Counties to add to each dataframe due the files missing this data
    weather_data_2_counties = ['Alameda','Amador','Butte','Colusa','Contra Costa','El Dorado','Fresno','Imperial',
                               'Inyo','Kern','Kings','Lassen','Los Angeles','Marin','Merced','Modoc',
                               'Monterey','Napa','Orange','Placer','Riverside','Sacramento','San Benito',
                               'San Bernardino','San Diego','San Joaquin','San Luis Obispo','Santa Barbara',
                               'Santa Clara','Santa Cruz','Shasta','Siskiyou','Solano','Sonoma','Stanislaus',
                               'Sutter','Tehama','Tulare','Ventura','Yolo','Yuba']
    # Create a list of columns that are unnecessary for the project
    drop_columns = ['Stn Id', 'CIMIS Region', 'Jul', 'ETo (in)', 'Sol Rad (Ly/day)', 'Avg Vap Pres (mBars)', 
                    'Wind Run (miles)', 'Avg Soil Temp (F)', 'qc', 'qc.1', 'qc.2', 'qc.3', 'qc.4', 'qc.5', 'qc.6', 
                    'qc.7', 'qc.8', 'qc.9', 'qc.10', 'qc.11', 'qc.12', 'qc.13', 'Stn Name']
    # Iterate through the dataframes in the dictionary
    for x in range(0, len(filenames)):
        # Drop unnecessary columns
        wd[filenames[x]].drop(columns = drop_columns, axis = 1, inplace = True)
        # Add county to dataframe
        wd[filenames[x]]['county'] = weather_data_2_counties[x]
        # Change date column from object to datetime object
        wd[filenames[x]]['Date'] = pd.to_datetime(wd[filenames[x]]['Date'])
        # Create a year column for ease of joining the dataframe to others
        wd[filenames[x]]['year'] = pd.DatetimeIndex(wd[filenames[x]]['Date']).year
        
    return wd

def import_scraped_weather(filenames):
    '''
    
    Enters an alpabetically ordered list of filenames from scraped weather data from weather underground and
    returns a dictionary of county weather dataframes with only the useful columns for the project
    
    '''
    # Create an empty dictionary to read in new dataframes
    wd = {}
    # Iterate through list of csv files and read in the files to the dictionary
    for x in range(0, len(filenames)):
        wd[filenames[x]] = pd.read_csv(filenames[x])
    # Create a list of California Counties to add to each dataframe due the files missing this data
    weather_data_counties = ['Alpine', 'Calaveras', 'Del Norte', 'Glenn', 'Humboldt', 'Lake', 'Madera', 
                             'Mariposa', 'Mendocino', 'Mono', 'Nevada', 'Plumas', 'San Francisco', 'San Mateo', 'Sierra', 
                             'Trinity', 'Tuolumne']
    # Create a list of columns that are unnecessary for the project
    drop_columns = ['Unnamed: 0', 'Max Dew Point (F)', 'Min Dew Point (F)', 'Max Wind Speed (mph)', 
                    'Min Wind Speed (mph)', 'Max Pressure (Hg)', 'Avg Pressure (Hg)', 'Min Pressure (Hg)']
    #Iterate through the dataframes in the dictionary
    for x in range(0, len(filenames)):
        # Drop unnecessary columns
        wd[filenames[x]].drop(columns = drop_columns, axis = 1, inplace = True)
        # Add county to dataframe
        wd[filenames[x]]['county'] = weather_data_counties[x]
        # Rename column to match cimis data
        wd[filenames[x]].rename(columns = {'Avg Dew Point (F)':'Dew Point (F)'}, inplace = True)
        # Change numeral values in Date column to datetime range of values
        wd[filenames[x]]['Date'] = pd.date_range('2012-12-01', '2019-12-31', freq = 'D')
        wd[filenames[x]]['year'] = pd.DatetimeIndex(wd[filenames[x]]['Date']).year
    
    return wd
                       
def prev_week_weather(data, filenames, counties):
    '''
    
    Enters a dictionary of daily weather data and returns a dictionary of the previous weeks weather averages
    
    '''
    prev_week_data = {}
    # Iterate through the dictionary of county daily weather data
    for x in range(0, len(filenames)):
        # Create a new dataframe of the current data
        weather = data[filenames[x]]
        # Set date as the index for future resampling
        weather.set_index('Date', inplace=True)
        # resample the weather data on a weekly basis
        weather = weather.resample('W')
        # Take the mean of the data columns
        weather_mean = weather.mean()
        # Add suffix to to column names
        weather_mean = weather_mean.add_suffix('_Weekly')
        # Reassign the county name that was lost in resampling
        weather_mean['county'] = counties[x]
        # Shift the data one week foward so each row will have previous week's weather means
        weather_mean = weather_mean.shift(1)
        # Reset the year column to the year in the index
        weather_mean['year'] = weather_mean.index.year
        # Reset the index
        weather_mean = weather_mean.reset_index()
        # Slice the data for only the timeframe used in the project
        weather_week = weather_mean.loc[(weather_mean['Date'] > '2012-12-31') & (weather_mean['Date'] < '2019-01-01')]
        # reassign the new dataframe to the dictionary
        prev_week_data[filenames[x]] = weather_week
        
    # Return the new dictionary
    return prev_week_data
                       
def prev_month_weather(data, filenames, counties):
    '''
    
    Enters a dictionary of daily weather data and returns a dictionary of the previous month's weather averages
    
    '''
    prev_month_data = {}
    # Iterate through the dictionary of county daily weather
    for n in range(0, len(filenames)):
        # Create a new dataframe of the current data
        weather = data[filenames[n]]
        # Resample by day in case of multiple stations
        weather = weather.resample('D').mean()
        # Create a new dataframe for the monthly averages
        month_agg = pd.DataFrame()
        # Create a date series for the range of the project
        month_agg['Date'] = pd.date_range('2013-01-01', '2019-12-31', freq = 'W')
        # Create lists for columns
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        i = []
        # Create a list of lists to iterate through
        col_list = [a, b, c, d, e, f, g, h, i]
        # Iterate through each date
        for x in month_agg.Date:
            # Iterate through each column
            for y in range(0, len(col_list)):
                # Take the mean of the column type from the 4 weeks before the date
                col_list[y].append(weather.loc[x - pd.Timedelta(weeks = 4) : x][weather.columns[y]].mean())
        # Add each list as a series to the final dataset
        for z in range(0, len(col_list)):
            month_agg[weather.columns[z]] = col_list[z]
        # Reassign the county name that was lost in resampling
        month_agg['county'] = counties[n]
        # Grab only the dates within 2013-2018
        prev_month = month_agg.loc[(month_agg['Date'] > '2012-12-31') & (month_agg['Date'] < '2019-01-01')]
        # Add the dataframe to a dictionary of previous month averages
        prev_month_data[filenames[n]] = prev_month
    # Return the new dictionary
    return prev_month_data
                       
def cimis_data():
    '''
    
    Imports cimis weather data and returns past week and month averages and cimis files names
    
    '''
    # Find all cimis weather files
    cimis_files = glob('data/weather_cimis/*.csv')
    # Sort files into alphabetical order
    cimis_files.sort()
    # Import csv files into pandas dataframes
    cimis_data = import_cimis(cimis_files)
    # Create a list of cimis counties
    cimis_counties = ['Alameda','Amador','Butte','Colusa','Contra Costa','El Dorado','Fresno','Imperial',
                    'Inyo','Kern','Kings','Lassen','Los Angeles','Marin', 'Merced','Modoc',
                    'Monterey','Napa','Orange','Placer','Riverside','Sacramento','San Benito',
                    'San Bernardino','San Diego','San Joaquin','San Luis Obispo','Santa Barbara',
                    'Santa Clara','Santa Cruz','Shasta','Siskiyou','Solano','Sonoma','Stanislaus',
                    'Sutter','Tehama','Tulare','Ventura','Yolo','Yuba']
    # Aggregate weekly cimis data
    pww_cimis = prev_week_weather(cimis_data, cimis_files, cimis_counties)
    # Aggregate monthly cimis data
    pmw_cimis = prev_month_weather(cimis_data, cimis_files, cimis_counties)
    # Return weekly and monthly cimis data
    return pww_cimis, pmw_cimis, cimis_files
                       
def wu_data():
    '''
    
    Imports weather underground data and returns past week and month averages and weather underground files names
    
    '''
    # Find all weather underground files
    wu_files = glob('data/weather_mc/*.csv')
    # Sort files into alphabetical order
    wu_files.sort()
    # Import csv files into pandas dataframes
    wu_data = import_scraped_weather(wu_files)
    # Two of the files still have an extra index column. Drop the extra index columns
    wu_data[wu_files[2]].drop(columns = 'index', inplace = True)
    wu_data[wu_files[-2]].drop(columns = 'index', inplace = True)
    # Reset the index for the two files
    wu_data[wu_files[2]].reset_index(drop = True)
    wu_data[wu_files[-2]].reset_index(drop = True)
    # Create a list of weather underground counties
    wu_counties = ['Alpine', 'Calaveras', 'Del Norte', 'Glenn', 'Humboldt', 'Lake', 'Madera', 
                 'Mariposa', 'Mendocino', 'Mono', 'Nevada', 'Plumas', 'San Francisco', 'San Mateo', 'Sierra', 
                 'Trinity', 'Tuolumne']
    # Aggregate weekly weather underground data
    pww_wu = prev_week_weather(wu_data, wu_files, wu_counties)
    # Aggregate monthly weather underground data
    pmw_wu = prev_month_weather(wu_data, wu_files, wu_counties)
    # Return weekly and monthly weather underground data
    return pww_wu, pmw_wu, wu_files
           
def weekly_data(cimis, wu, cimis_files, wu_files):
    '''
    
    Takes in dictionaries and returns a dataframe with all past week weather data
    
    '''
    # create a new dataframe for weekly data
    pw_weather = pd.DataFrame()
    # iterate through each cimis county weather dataframe
    for x in range(0, len(cimis)):
        # add each cimis county weather dataframe to pw_weather
        pw_weather = pw_weather.append(cimis[cimis_files[x]])
    # Iterate through each weather underground dataframe
    for y in range(0, len(wu)):
        # add each weather undergound dataframe to pw_weather
        pw_weather = pw_weather.append(wu[wu_files[y]])
    # Drop unnecessary columns
    pw_weather.drop(['year', 'year_Weekly'], axis = 1, inplace = True)
    # Rename the Date column as date for ease of merging with other dataframes
    pw_weather = pw_weather.rename(columns = {'Date': 'date'})
    # Return Past Week's Dataframe
    return pw_weather
                       
def monthly_data(cimis, wu, cimis_files, wu_files):
    '''
    
    Takes in dictionaries and returns a dataframe with all past month weather data
    
    '''
    # create a new dataframe for monthly data
    pm_weather = pd.DataFrame()
    # iterate through each cimis county weather dataframe
    for x in range(0, len(cimis)):
        # add each cimis county weather dataframe to pm_weather
        pm_weather = pm_weather.append(cimis[cimis_files[x]])
    # Iterate through each weather underground dataframe
    for y in range(0, len(wu)):
        # add each weather undergound dataframe to pm_weather
        pm_weather = pm_weather.append(wu[wu_files[y]])
    # Add month suffix to column names
    pm_weather = pm_weather.add_suffix('_month')
    # Change back date and county to original for ease of merging with other dataframes
    pm_weather = pm_weather.rename(columns = {'Date_month': 'date', 'county_month': 'county'})
    # Return Past Week's Dataframe
    return pm_weather

def year_example(df):
    '''
    
    Creates a new dataframe from a year slice from the given dataframe
    
    '''
    # Slice only a year of data
    year_ex = df.loc[df['date'] < '2014-01-01']
    # Change column date from object to datetime
    year_ex['date'] = pd.to_datetime(year_ex['date'])
    # Resample data on a monthly frequency and take the sum
    year_ex = year_ex.resample('M', on = 'date').sum()
    # Reset the index
    year_ex = year_ex.reset_index()
    return year_ex
                       
def dummy_variables(df):
    '''
    
    Creates dummy variables for dataframe (specific to this project)
    
    '''
    # Create dummy variables for the county column
    counties = pd.get_dummies(df.county, drop_first = True)
    # Drop county column along with unnecessary columns (year and acres burned)
    df2 = df.drop(columns = ['county', 'year', 'acres_burned'], axis = 1)
    # Feature engineer month column from the date column
    df2['month'] = pd.DatetimeIndex(df2['date']).month
    # Drop the date column
    df2.drop(columns = ['date'], axis = 1, inplace = True)
    # Create dummy variables for the months
    month = pd.get_dummies(df2.month, drop_first = True)
    # Drop the month column
    df2.drop(columns = 'month', axis =1, inplace = True)
    # Combine the original dataframe with the dummy variables
    df2 = pd.concat([df2, counties, month], axis = 1)
    # Return the new dataframe
    return df2
                   
def model_recall_scores_viz(score1, score2, score3, score4, score5, score6, score7):
    yplot = sorted([score1, score2, score3, score4, score5, score6, score7], reverse=True)
    xplot = [0, 1, 2, 3, 4, 5, 6]
    x_label = ["Logistic Regression", "Adaboost", "XGBoost", "GradientBoosting", "Random Forest", "Decision Tree", "KNN"]

    sns.set_palette("rocket")

    plt.figure(figsize = [14, 9])
    sns.barplot(x = xplot,y = yplot, alpha=0.9, label=x_label)
    plt.xticks(xplot, x_label, rotation=60, fontsize=18)
    plt.ylabel("Recall Score", fontsize=18)

    for x_pos, y_pos in zip(xplot,yplot):
        plt.text(x_pos-0.1, y_pos - 0.1, str(round(y_pos,3)), color="white")

    plt.title("Recall Scores by Model", fontsize=20)
    plt.tight_layout()
    plt.savefig("Images/recall_score_model.png")
    return plt.show()


def confusion_matrix_viz(test, predict):
    fig, ax = plt.subplots(figsize = [14,9])
    sns.heatmap(confusion_matrix(test, predict),
                annot = True,
                ax = ax,
                fmt = 'd')
    ax.set_ylim([0,2])
    ax.set_yticks([0.75, 1.75])
    ax.set_title('Confusion Matrix', fontsize = 20)
    ax.set_xlabel('Predicted', fontsize = 18)
    ax.set_ylabel('True', fontsize = 18)
    ax.yaxis.set_ticklabels(['No Wildfire', 'Wildfire'], fontsize = 18)
    ax.xaxis.set_ticklabels(['No Wildfire', 'Wildfire'], fontsize = 18)
    fig.savefig('images/confmatrix.png', bbox_inches='tight')


def population_data(pop_data, area_data):
    '''
    
    Inputs two dataframes and returns a dataframe with Counties population, area, and population density
    
    '''
    # We only want the data from 2013-2018
    pop_df = pop_data.loc[pop_data['Year'] > 2012]
    # Rename columns for ease of combining with final dataframe
    pop_df.rename(columns = {'County':'county', 'Year':'year'}, inplace = True)
    # Take the county and square miles columns in a new dataframe
    area_df = area_data[['County', 'Square Miles']]
    # Rename the County column for ease of combining with final dataframe
    area_df.rename(columns = {'County':'county'}, inplace = True)
    # Merge the dataframes into one
    pop_area_df = pd.merge(pop_df, area_df, how = 'left', left_on = ['county'], right_on = ['county'])
    # Rename area to new units
    pop_area_df.rename(columns = {'Square Miles':'county_acres'}, inplace = True)
    # Convert units to acres to match units in final dataframe
    pop_area_df.county_acres = pop_area_df.county_acres * 640
    # Create a new column pop_density using the population and area
    pop_area_df['pop_density'] = pop_area_df.Population / pop_area_df.county_acres
    # Return the dataframe
    return pop_area_df


