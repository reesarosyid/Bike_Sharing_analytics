# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ANALYTIC

# Read csv
df_day = pd.read_csv('./day.csv')
df_hour = pd.read_csv('./hour.csv')

# Drop column instant from both of dataframe
df_hour.drop(['instant'], axis=1, inplace=True)
df_day.drop(['instant'], axis=1, inplace=True)

# Change data type from object to datetime on column dteday
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_hour1 = df_hour.copy()
df_hour1['dteday'] = df_hour['dteday'].dt.date

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day1 = df_day.copy()
df_day1['dteday'] = df_day['dteday'].dt.date

# Data transorfation
month_agg = df_hour.groupby("mnth").agg({
    "cnt": ["max", "mean", "sum"]
})

season_agg = df_hour.groupby("season").agg({
    "cnt": ["max", "mean", "sum"]
})

day_agg = df_hour.groupby(["weekday", "workingday"]).agg({
    "cnt": ["max", "mean", "sum"]
})

hour_agg = df_hour.groupby("hr").agg({
    "cnt": ["max", "mean", "sum"]
})

temp_agg = df_hour.groupby(by="season").agg({
    "temp": ["max", "mean", "min"]
})
temp_agg = temp_agg['temp'].apply(lambda x: x*41)



#DEF PLOT

def bikeRentalsOverTime():
    # Data Transformation
    month_index_df = df_day.resample('M', on='dteday').sum()

    # Set figure plt
    plt.figure(figsize=(10, 7))

    # Declare value x and y label
    plt.plot(month_index_df.index, month_index_df['cnt'], marker='.', markerfacecolor='Black',markersize=12, linewidth=3)
    plt.plot(month_index_df.index, month_index_df['casual'], marker='.', markerfacecolor='Black',markersize=12, linewidth=3)
    plt.plot(month_index_df.index, month_index_df['registered'], marker='.', markerfacecolor='Black',markersize=12, linewidth=3)

    # Set Title, label name, and legend
    plt.xlabel('Month')
    plt.ylabel('Number of Bike Rentals')
    plt.title('Bike Rentals Over Time (Aggregated by Month)')
    plt.legend(["CNT", "Casual", "Registered"], loc="upper left")

    # Adjustment plot
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    return(st.pyplot(plt))

def numberBikeRental2011VS2012():
    # Color palette
    blue, = sns.color_palette("muted", 1)

    # Define y1 value
    df_day2011 = df_day[df_day['dteday'].dt.year == 2011]
    y_2011 = []
    for i in df_day['dteday'].dt.month.unique():
        sum_user = df_day2011[df_day2011['dteday'].dt.month == i]['cnt'].sum()
        y_2011.append(sum_user)

    # Define y2 value
    df_day2012 = df_day[df_day['dteday'].dt.year == 2012]
    y_2012 = []
    for i in df_day['dteday'].dt.month.unique():
        sum_user = df_day2012[df_day2012['dteday'].dt.month == i]['cnt'].sum()
        y_2012.append(sum_user)

    # Define x value
    x = df_day['dteday'].dt.month.unique()

    # Define the plot
    fig, ax = plt.subplots()

    # Declare value x and y label
    ax.plot(x, y_2012, color='#0C134F', lw=3)
    ax.fill_between(x, 0, y_2012, alpha=.3, color='#1D267D')
    ax.plot(x, y_2011, color='#5C469C', lw=3)
    ax.fill_between(x, 0, y_2011, alpha=.3, color='#D4ADFC')

    # Make list of month
    month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Ags', 'Sep', 'Oct', 'Nov', 'Dec']

    # Adjustment
    ax.set(xlim=(0, len(x) - 1), ylim=(0, None), xticks=x, xticklabels=month_label, xlabel='Month',ylabel='Number of Bike Rentals', title="Number Bike Rental 2011 VS 2012")
    ax.legend(['2011','', '2012', ''], loc='upper left')
    ax.grid(True, color = "grey", alpha=0.5, linestyle = "-")

    #Show the plot
    return(st.pyplot(plt))

def numberRentalBasedOnTheirClass():
    # Create list query to know each total value per class during 2011 and 2012 as y value for a plot
    cnt = [df_day[df_day['dteday'].dt.year == 2011]['cnt'].sum(),df_day[df_day['dteday'].dt.year == 2012]['cnt'].sum()]
    reg = [df_day[df_day['dteday'].dt.year == 2011]['registered'].sum(), df_day[df_day['dteday'].dt.year == 2012]['registered'].sum()]
    cas = [df_day[df_day['dteday'].dt.year == 2011]['casual'].sum(), df_day[df_day['dteday'].dt.year == 2012]['casual'].sum()]

    # Declare x value year
    x = df_day['dteday'].dt.year.unique()

    # Set width to give a space for bar chart
    width = 0.25

    # Declare value y label
    bar_reg = plt.bar(x+width, reg, width, color='#1D5B79')
    bar_cas = plt.bar(x+width*2, cas, width, color='#468B97')
    bar_cnt = plt.bar(x, cnt, width, color='#EF6262')

    # Set the title, label, and legend
    plt.xlabel('Years')
    plt.ylabel("Number of Bike Rental")
    plt.title("Number Rental Based on Their Class (Aggregated by Year)")
    plt.legend( (bar_cnt, bar_reg, bar_cas), ('CNT', 'Reg', 'Cas'))

    # Adjustment plot
    plt.grid(True, color = "grey", alpha=0.5, linestyle = "-")
    plt.xticks(x+width,['2011', '2012'])

    # Show the plot
    return(st.pyplot(plt))

def behaviourBasedOnSeason():    
    # Plotting
    # Declare x value year
    x = season_agg.index
    y = season_agg['cnt']['sum']

    # Set figure plt
    plt.figure(figsize=(10, 7))

    # Create a colormap
    cmap = plt.get_cmap('coolwarm')

    # Generate colors based on the values using the colormap
    colors = cmap(np.linspace(0, 1, len(y)))

    # Declare y value year
    bar_chart = plt.barh(x, y, color=colors)
    #color='#9E6F21', edgecolor='#4C3D3D'
    # Set the title, label, and legend
    plt.xlabel('Number of Bike Rental')
    plt.ylabel("Season")
    plt.title("Number Bike Rental (Aggregated by Season)")

    # Anotate the value
    values = season_agg[('cnt', 'sum')].tolist()
    plt.text(1, 1, str(values[0]), fontweight='bold', color='#EEEEEE')
    plt.text(1, 2, str(values[1]), fontweight='bold', color='#EEEEEE')
    plt.text(1, 3, str(values[2]), fontweight='bold', color='#EEEEEE')
    plt.text(1, 4, str(values[3]), fontweight='bold', color='#EEEEEE')

    # Adjustment plot
    plt.grid(True, color = "#9E6F21", alpha=0.5, linestyle = "-")
    plt.yticks(x, ['Winter', 'Spring', 'Summer', 'Fall'])

    # Show the plot
    return(st.pyplot(plt))

def behaviourBasedOnMonth():
    # Plotting
    # Declare x value year
    x = month_agg.index

    # Set figure plt
    plt.figure(figsize=(10, 7))


    # Declare y value year
    bar_chart = plt.bar(x, month_agg['cnt']['sum'], color='#78C1F3')
    line_plot = plt.plot(x, month_agg['cnt']['sum'], marker='.', markerfacecolor='#E2F6CA',markersize=12, linewidth=3, color='#9BE8D8')

    # Set the title, label, and legend
    plt.xlabel('Month')
    plt.ylabel("Number of Bike Rental")
    plt.title("Number Bike Rental (Aggregated by Month)")

    # Adjustment plot
    plt.grid(True, color = "#F8FDCF", alpha=0.5, linestyle = "-")
    plt.xticks(x, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Ags', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Show the plot
    return(st.pyplot(plt))

def behaviourBasedOnDay(typeDay, color, label):
    
    x = [0,1,2,3,4,5,6]
    
    # Set figure plt
    plt.figure(figsize=(10, 7))

    # Set width to give a space for bar chart
    #width = 0.25

    
    plt.bar(x, typeDay, color=color, label = label)

    # Set the title, label, and legend
    plt.xlabel('Day')
    plt.ylabel("Average Number of Bike Rental")
    plt.title("Average Number Rental Based on Holiday or Weekday  (Aggregated by Day)")
    plt.legend(loc="upper left")
    
    # Adjustment plot
    plt.grid(True, color = "grey", alpha=0.5, linestyle = "-")
    plt.xticks(x,['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], rotation=45)

    # Show the plot
    return(st.pyplot(plt))

def behaviourBasedOnHour():
    # Plotting
    # Declare x value year
    x = hour_agg.index

    # Set figure plt
    plt.figure(figsize=(10, 7))


    # Declare y value year
    bar_chart = plt.bar(x, hour_agg['cnt']['sum'], color='#3C486B')
    line_plot = plt.plot(x, hour_agg['cnt']['sum'], marker='.', markerfacecolor='#F0F0F0',markersize=12, linewidth=3, color='#F45050')

    # Set the title, label, and legend
    plt.xlabel('Hour')
    plt.ylabel("Number of Bike Rental")
    plt.title("Number Bike Rental (Aggregated by Hour)")

    # Adjustment plot
    hr_labels = [str(i) for i in x]
    plt.grid(True, color = "#61677A", alpha=0.5, linestyle = "-")
    plt.xticks(x, hr_labels)

    # Show the plot
    return(st.pyplot(plt))





# UI STREAMLIT

#Tittle
st.image("../Img/bike_share.jpg")
st.markdown("<p style='font-size: 60px; text-align: center; '><b>Bike Sharing Analytics</b></p>", unsafe_allow_html=True)

# Side Bar
with st.sidebar:
    # Add header
    st.markdown("<p style='font-size: 30px; text-align: center; '><b>Bike Sharing Analytics</b></p>", unsafe_allow_html=True)
    # Add the logo
    st.image("../Img/bike_share.jpg")
    
    # Add text
    st.text("Name   : Muhammad Reesa Roysid")
    st.text("Email   : mreesa669@gmail.com")
    
    
    # Add caption
    st.caption("<footer><p style='font-size: 15px; text-align: center; '><b>Copyright (c) 2023</b></p></footer>", unsafe_allow_html=True)


# Tab
# Add Tab
tab1, tab2, tab3, tab4 = st.tabs(["Data", "Question 1", "Question 2", "Question 3"])

with tab1:
    st.markdown("<p style='font-size: 40px; text-align: center; '><b>Bike Sharing data</b></p>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 30px; text-align: center; '><b>Data Information</b></p>", unsafe_allow_html=True)
    st.markdown("Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of over 500 thousands bicycles. Today, there exists great interest in these systems due to their important role in traffic, environmental and health issues.")
    st.markdown("Apart from interesting real world applications of bike sharing systems, the characteristics of data being generated by these systems make them attractive for the research. Opposed to other transport services such as bus or subway, the duration of travel, departure and arrival position is explicitly recorded in these systems. This feature turns bike sharing system into a virtual sensor network that can be used for sensing mobility in the city. Hence, it is expected that most of important events in the city could be detected via monitoring these data.")
    st.markdown("Bike-sharing rental process is highly correlated to the environmental and seasonal settings. For instance, weather conditions, precipitation, day of week, season, hour of the day, etc. can affect the rental behaviors. The core data set is related to the two-year historical log corresponding to years 2011 and 2012 from Capital Bikeshare system, Washington D.C., USA which is  publicly available in http://capitalbikeshare.com/system-data. We aggregated the data on two hourly and daily basis and then extracted and added the corresponding weather and seasonal information. Weather information are extracted from http://www.freemeteo.com.")
    
    st.markdown("<p style='font-size: 30px; text-align: center; '><b>Data</b></p>", unsafe_allow_html=True)
    
    #Make date chooser
    min_date = df_day1['dteday'].min()
    max_date = df_day1['dteday'].max()
    start_date, end_date = st.date_input(
        label='Range Time',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Make column
    data1, data2 = st.columns(2)
    
    with data1:
        st.markdown("<p style='font-size: 20px; text-align: center; '><b>Data Bike Sharing Daily</b></p>", unsafe_allow_html=True)
        
        #Make multiselect for data daily
        feature_daily = st.multiselect(
        label="Feature list",
        options = ('dteday', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual','registered', 'cnt'))
        
        feature_daily = list(feature_daily)
        
        df_mod_day = df_day1[(df_day1["dteday"] >= start_date) & (df_day1["dteday"] <= end_date)]
        if len(feature_daily)==0:
            df_mod_day = df_mod_day
        else:
            df_mod_day = df_mod_day[feature_daily]
        st.write(df_mod_day)
    
    with data2:
        st.markdown("<p style='font-size: 20px; text-align: center; '><b>Data Bike Sharing Hourly</b></p>", unsafe_allow_html=True)
        
        #Make multiselect for data hourly
        feature_hourly = st.multiselect(
        label="Feature list",
        options = ('dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday',
       'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed',
       'casual', 'registered', 'cnt'))
        
        feature_hourly = list(feature_hourly)
        
        df_mod_hour = df_hour1[(df_hour1["dteday"] >= start_date) & (df_hour1["dteday"] <= end_date)]
        if len(feature_hourly)==0:
            df_mod_hour = df_mod_hour
        else:
            df_mod_hour = df_mod_hour[feature_hourly]
        st.write(df_mod_hour)
with tab2:
    
    st.markdown("<p><b>Question 1: What is the trend of bicycle rental from casual, registered or both types of customers as a whole from time to time?</b></p>", unsafe_allow_html=True)
    
    st.markdown("<p><b>Answer:</b></p>", unsafe_allow_html=True)
    
    st.markdown("The trend of bicycle renters from casual, registered, and a combination of both from 2011 to 2012 can be seen in the Bike Rental Over Time (Aggregated by Month) plot. The blue line in the plot shows a very significant increase in users from 2011 to 2012 and this has also been re-proved through the Number Bike Rental 2011 VS 2012 plot. Most bicycle renters in 2011 occurred in June with 143,512 bicycle renters and in 2012 the most occurred in september with 218,573 tenants. For rentals in other months, there are fluctuations because in certain months there are a lot of bicycles rented and in other months there are very few bicycle renters. This can be related to temperature and season because these two features have a high data correlation with bicycle renters as evidenced by the heatmap plot. Triangle Correlation Heatmap df day and Triangle Correlation Heatmap df hour with each correlation between 0.34-0.63.")
    st.markdown("There are two types of tenants, namely casual and registered. The registered type has the largest portion of tenants with a total of 995,851 people in 2011 and 1,676,811 people in 2012, while the casual type has a small portion of tenants with 247,252 people in 2011 and 372,765 people in 2012. For both numbers, in 2011 the number tenants reached 1,243,103 people and in 2012 this number increased to 2,049,576 people. This is evidenced by the bar plot Number Rental Based on Their Class (Aggregated by Year).")
    
    plot = st.selectbox(
        label="Select the plot",
        options=  ('Bike Rentals Over Time (Aggregated by Month)', 'Number Bike Rental 2011 VS 2012', 'Number Rental Based on Their Class (Aggregated by Year)')
    )
    
    if plot == 'Bike Rentals Over Time (Aggregated by Month)':
        bikeRentalsOverTime()
    elif plot == 'Number Bike Rental 2011 VS 2012':
        numberBikeRental2011VS2012()
    elif plot == 'Number Rental Based on Their Class (Aggregated by Year)':
        numberRentalBasedOnTheirClass()

with tab3:
    
    st.markdown("<p><b>Question 2: What are the habits of customers renting bicycles based on season, month, day, and hour, judging by the number of rentals or the number of rentals?</b></p>", unsafe_allow_html=True)
    
    st.markdown("<p><b>Answer:</b></p>", unsafe_allow_html=True)
    
    bhv = st.selectbox(
        label="Select the behaviour",
        options=  ('Behaviour based on season', 'Behaviour based on month', 'Behaviour based on day', 'Behaviour based on hour')
    )
    
    if bhv == 'Behaviour based on season':
        st.markdown("the customer's bicycle rental habits based on season can be seen in the Number Bike Rental plot (Aggregated by Season). In this plot it can be seen that the season most often used for renting bicycles is summer with a total of 1,061,129 people renting, followed by spring with 918,589 people, fall as many as 841,613 people, and the least in winter with 471,348 people.")
        behaviourBasedOnSeason()
        
    elif bhv == 'Behaviour based on month':
        
        st.markdown("Bike rental habits by customers by month can be seen in the Number Bike Rental plot (Aggregated by Month). It can be seen in the plot that people who rent bicycles with the highest peak are in May to October where the month is expected to occur in the summer season with total rentals between 322,352 people to 351,194 people. winter heading into spring with rental figures of 134,933 people to 151,352 people.")
        behaviourBasedOnMonth()
        
    elif bhv == 'Behaviour based on day':
        st.markdown("Bike rental habits by customers by day can be seen in the Average Number Rental Based on Holiday or Weekday (Aggregated by Day) plot. In the plot it can be seen that there are two types of days in the week, namely holidays and working days. On weekdays, the average number of people renting bicycles is quite stable at 150-200 rented per day. While on holidays, the average is very fluctuating where the lowest is less than 50 tenants per day to more than 300 tenants per day.")
        # Create list value for average rentaler holiday and weekday season
        list_holiday = []
        for i in range(7):
            list_holiday.append(day_agg.loc[(i, 0), ('cnt','mean')])
            
        list_weekday = []
        for i in range(5):
            list_weekday.append(day_agg.loc[(1+i, 1), ('cnt','mean')])
        list_weekday.insert(0,0)
        list_weekday.append(0)
        
        day = st.selectbox(label="Choose the day",
                           options= ("Holiday", "Weekday"))
        #bar_hol = plt.bar(x, list_holiday, width, color='#CD1818')
        #bar_week = plt.bar(x + width, list_weekday, width, color='#468B97')
        
        if day == "Holiday":
            color = '#CD1818'
            behaviourBasedOnDay(list_holiday, color, "Holiday")
        elif day == "Weekday":
            color = '#468B97'
            behaviourBasedOnDay(list_weekday, color, "Weekday")

        
        
    elif bhv == "Behaviour based on hour":
        
        st.markdown("Bike rental habits by customers by hour can be seen in the Number Bike Rental (Aggregated by Hour) plot. It can be seen in the table that there are two peaks of the number of people renting bicycles, namely at 7-9 in the morning and 4-19 in the afternoon where these times are the time to go to and from school or work, especially in the morning and evening it is very suitable because of the cooler temperatures. not too hot. Meanwhile, between 12-5 am is the rarest time for people to rent bicycles because that time is when people are sleeping.")
        behaviourBasedOnHour()
        
        
with tab4:
    st.markdown("Question 3: What is the correlation between the number of bicycle rentals and the temperature in a particular season?", unsafe_allow_html=True)
    st.markdown("<p><b>Answer:</b></p>", unsafe_allow_html=True)
    st.markdown("There is a strong correlation between bicycle rotation and temperature, the magnitude of which has already been mentioned in answer number one. In the Max, Average, and Min Rental Based on Temperature (Aggregated by Season) plots, the maximum, average, and minimum temperatures in each season have been described. Spring and summer are the seasons when most people rent bicycles and you can see here the average temperature is 22-28 degrees Celsius, the maximum is 38-41 degrees Celsius. Meanwhile, spring is in the third position with the most rents where this season the average temperature is 22 degrees Celsius, the maximum is 38 degrees Celsius, and the minimum is 6 degrees Celsius. The season with the least number of flights is in winter where the temperature this season is very low compared to other seasons with an average temperature of 12 degrees Celsius, a maximum of 29 degrees Celsius, and a minimum of 0 degrees Celsius. This is correlated because warm temperatures will be perfect for outdoor activities and at cold temperatures people will rarely do outdoor activities. That way it will be directly correlated to the number or number of bicycle rentals.")
    # Plotting
    # Create list query to know min, avg, max of the temperature as y value for a plot
    max_temp = temp_agg['max'].tolist()
    min_temp = temp_agg['min'].tolist()
    mean_temp = temp_agg['mean'].tolist()

    temp= st.selectbox(label="Choose the season",
                           options= ('Winter', 'Spring', 'Summer', 'Fall'))
    if temp == "Winter":
      st.markdown("<p style='font-size: 20px; text-align: center; '><b>Winter</b></p>", unsafe_allow_html=True)
      col1, col2, col3 = st.columns(3)
      col1.metric("Maximum Temperature", f"{int(max_temp[0])}°C")
      col2.metric("Average Temperature", f"{int(mean_temp[0])}°C")
      col3.metric("Minimum Temperature", f"{int(min_temp[0])}°C")
    elif temp == "Spring":
      st.markdown("<p style='font-size: 20px; text-align: center; '><b>Spring</b></p>", unsafe_allow_html=True)
      col1, col2, col3 = st.columns(3)
      col1.metric("Maximum Temperature", f"{int(max_temp[1])}°C")
      col2.metric("Average Temperature", f"{int(mean_temp[1])}°C")
      col3.metric("Minimum Temperature", f"{int(min_temp[1])}°C")       
    elif temp == "Summer":
      st.markdown("<p style='font-size: 20px; text-align: center; '><b>Summer</b></p>", unsafe_allow_html=True)
      col1, col2, col3 = st.columns(3)
      col1.metric("Maximum Temperature", f"{int(max_temp[2])}°C")
      col2.metric("Average Temperature", f"{int(mean_temp[2])}°C")
      col3.metric("Minimum Temperature", f"{int(min_temp[2])}°C")
    elif temp == "Fall":
      st.markdown("<p style='font-size: 20px; text-align: center; '><b>Fall</b></p>", unsafe_allow_html=True)
      col1, col2, col3 = st.columns(3)
      col1.metric("Maximum Temperature", f"{int(max_temp[3])}°C")
      col2.metric("Average Temperature", f"{int(mean_temp[3])}°C")
      col3.metric("Minimum Temperature", f"{int(min_temp[3])}°C")
          

        
        
    
    
    

    
    
    