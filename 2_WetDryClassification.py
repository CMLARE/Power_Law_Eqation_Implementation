import pyproj as pyproj
import csv
import geopy.distance
from datetime import datetime, timedelta
import statistics

MinHoursPmin = 6
PeriodHoursPmin=24
Radius=10
ThresholdMedian =-1.4
ThresholdMedianL = -0,7
ThresholdNumberLinks = 3
ThresholdWetDry =2

def find_distance(CX1,CY1,CX2,CY2):
    return geopy.distance.vincenty((CX1,CY1),(CX2,CY2)).km


with open("dataset.csv",'r') as dataset_file:
    reader= list(csv.reader(dataset_file))

    links_ID=[]

    index_start_x = reader[0].index("XStart")
    index_start_y=reader[0].index("YStart")
    index_end_x=reader[0].index("XEnd")
    index_end_y=reader[0].index("YEnd")

    link_location=[]
    temp = ""
    record_counter=1
    record_counter_arr=[]
    for x in range(1,len(reader)):
        if(temp!= reader[x][0]):
            links_ID.append(reader[x][0])
            link_location.append([reader[x][0],(reader[x][index_start_x],reader[x][index_start_y]),(reader[x][index_end_x],reader[x][index_end_y])])
            temp = reader[x][0]
            record_counter_arr.append(record_counter)
            record_counter = 1
        else:
            record_counter+=1
            if(x==(len(reader)-1)):
                record_counter_arr.append(record_counter)

    record_counter_arr=record_counter_arr[1:] #information about number of records for each unique link(use it to optimize the below iteration)

    # selecting nearby links
    for x in range (0,len(link_location)):
        new_data_values = []
        links_except_selected_one=link_location[0:x]+link_location[x+1:len(link_location)]
        nearby_links=[]
        for link in links_except_selected_one:
            distance_1 = find_distance(float(link_location[x][1][0]), float(link_location[x][1][1]), float(link[1][0]), float(link[1][1]))
            distance_2 = find_distance(float(link_location[x][1][0]), float(link_location[x][1][1]), float(link[2][0]), float(link[2][1]))
            distance_3 = find_distance(float(link_location[x][2][0]), float(link_location[x][2][1]), float(link[1][0]), float(link[1][1]))
            distance_4 = find_distance(float(link_location[x][2][0]), float(link_location[x][2][1]), float(link[2][0]), float(link[2][1]))
            if ((distance_1<Radius or distance_2<Radius) and (distance_3<Radius or distance_4<Radius)):
                nearby_links.append(link)

        nearby_links.append(link_location[x])

        if len(nearby_links)>=4:
            data_values = []  # An array containing the details about delta_p and delta_p_L for each time interval for a link
            for link in nearby_links:
                link_record = []  # contains records for a specific link
                for y in range(0,sum(record_counter_arr)): #TODO: this iteration needs to be optimized
                    if(link[0]==reader[y][0]):
                        link_record.append(reader[y])

                time_record=[]

                for record in link_record:
                    time_record.insert(0,record[1])

                for time_interval in range(0,len(link_record)): #iterate through time intervals
                    datetime_object = datetime.strptime(link_record[time_interval][1], '%d-%m-%y %H:%M')
                    selected_time_interval=datetime_object.strftime('%d-%m-%y %H:%M')

                    Pmin=[]

                    for z in range(0,96): #check for 24 hours
                        datetime_object= datetime_object - timedelta(minutes=15)
                        new_date=datetime_object.strftime('%d-%m-%y %H:%M')
                        if(new_date in time_record):
                            index=time_record.index(new_date)
                            Pmin.append(link_record[index][4])

                    if (len(Pmin)>25):
                        max_Pmin=max(Pmin)
                        delta_P=(float(link_record[time_interval][4]) - float(max_Pmin))
                        delta_p_L=(delta_P/float(link_record[time_interval][20]))
                        data_values.append([link_record[time_interval][0],selected_time_interval,delta_P,delta_p_L])


            for p in range(0,record_counter_arr[x]):
                temp_delta_p = [data_values[p][2]]
                temp_delta_p_l=[data_values[p][3]]
                selected_time_interval = data_values[p][1]
                for q in range(record_counter_arr[x],len(data_values)):
                    if(selected_time_interval== data_values[q][1]):
                        temp_delta_p.append(data_values[q][2])
                        temp_delta_p_l.append(data_values[q][3])

                if (statistics.median(temp_delta_p)<-1.4 and statistics.median(temp_delta_p_l)< -0.7):
                    new_data_values.append(data_values[p][0], data_values[p][1], "wet")
                else:
                    new_data_values.append(data_values[p][0], data_values[p][1], "dry")






















