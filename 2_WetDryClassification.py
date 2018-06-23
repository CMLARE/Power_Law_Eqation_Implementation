import csv
import geopy.distance
from datetime import datetime, timedelta
import statistics

MinHoursPmin = 6*4
PeriodHoursPmin=24*4
Radius=10
ThresholdMedian =-1.4
ThresholdMedianL = -0.7
ThresholdNumberLinks = 3
#ThresholdWetDry =2

def find_distance(CX1,CY1,CX2,CY2):
    return geopy.distance.vincenty((CX1,CY1),(CX2,CY2)).km

with open("dataset.csv","r") as dataset_file:
    reader= list(csv.reader(dataset_file))

    links_ID=[] #link id array

    index_start_x = reader[0].index("XStart")
    index_start_y=reader[0].index("YStart")
    index_end_x=reader[0].index("XEnd")
    index_end_y=reader[0].index("YEnd")

    link_location=[] #each element = [link id,(CX1,CY1),(CX2,CY2)]
    temp = "" #tempory variable used in populating links_ID array
    record_counter=1
    record_counter_arr=[] #each element = number of rows for a link
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

    record_counter_arr=record_counter_arr[1:] #information about number of records for each unique link

    new_record_counter_arr=[0]+record_counter_arr #used in later part of the code in writing a new wet/dry classified csv file

    with open("new_dataset.csv", "w",newline='') as new_dataset_file:
        writer=csv.writer(new_dataset_file)
        new_header_arr=reader[0]
        new_header_arr.append("Wet/Dry")
        writer.writerow(new_header_arr) #writing the header for the new csv file
        arr_counter = 0 #used in later part of the code in writing a new wet/dry classified csv file

        for x in range (0,len(link_location)): #selecting each link for consideration
            new_data_values = []  #each element = [link id, timestamp, wet/dry] .populated later in the code
            links_except_selected_one=link_location[0:x]+link_location[x+1:len(link_location)]
            nearby_links=[]
            for link in links_except_selected_one:
                distance_1 = find_distance(float(link_location[x][1][0]), float(link_location[x][1][1]), float(link[1][0]), float(link[1][1]))
                distance_2 = find_distance(float(link_location[x][1][0]), float(link_location[x][1][1]), float(link[2][0]), float(link[2][1]))
                distance_3 = find_distance(float(link_location[x][2][0]), float(link_location[x][2][1]), float(link[1][0]), float(link[1][1]))
                distance_4 = find_distance(float(link_location[x][2][0]), float(link_location[x][2][1]), float(link[2][0]), float(link[2][1]))
                if ((distance_1<Radius or distance_2<Radius) and (distance_3<Radius or distance_4<Radius)):
                    nearby_links.append(link)

            nearby_links.append(link_location[x])  #appneding also the selected link to the array

            if len(nearby_links)>=(ThresholdNumberLinks+1):
                data_values = []  # An array containing the details about delta_p and delta_p_L for each time interval for all nearby link
                for link in nearby_links:
                    link_record = []  #contains records for a specific link
                    for y in range(0, sum(record_counter_arr)):
                        if(link[0]==reader[y][0]):
                            link_record.append(reader[y])

                    time_record=[] #contains time records for a specific link

                    for record in link_record:
                        time_record.append(record[1])

                    for time_interval in range(0,len(link_record)): #iterate through time intervals
                        datetime_object = datetime.strptime(link_record[time_interval][1], '%d-%m-%y %H:%M')
                        selected_time_interval=datetime_object.strftime('%d-%m-%y %H:%M')

                        Pmin=[]

                        for z in range(0,PeriodHoursPmin): #check for 24 hours
                            datetime_object= datetime_object - timedelta(minutes=15)
                            new_date=datetime_object.strftime('%d-%m-%y %H:%M')
                            if(new_date in time_record):
                                index=time_record.index(new_date)
                                Pmin.append(link_record[index][4])

                        if (len(Pmin)>=MinHoursPmin): #check whether it has data for at least 6 hours
                            max_Pmin=max(Pmin)
                            delta_P=(float(link_record[time_interval][4]) - float(max_Pmin)) #calculate "delta P"
                            delta_p_L=(delta_P/float(link_record[time_interval][20])) #calculate "delta P L"
                            data_values.append([link_record[time_interval][0],selected_time_interval,delta_P,delta_p_L])


                for p in range(0,len(link_record)): #iterate through selected links record
                    temp_delta_p = []
                    temp_delta_p_l=[]
                    selected_time_interval = link_record[p][1]
                    for q in range(0,len(data_values)):
                        if(selected_time_interval== data_values[q][1]): #putting "delta P" and "delta P L" in two seperate arrays for selected time interval
                            temp_delta_p.append(data_values[q][2])
                            temp_delta_p_l.append(data_values[q][3])
                    if (len(temp_delta_p)>(ThresholdNumberLinks+1)): #calculate median of the above two values if records are present above threshold values
                        if (statistics.median(temp_delta_p)<ThresholdMedian and statistics.median(temp_delta_p_l)< ThresholdMedianL):
                            new_data_values.append([link_record[p][0], selected_time_interval, "Wet"])
                        else:
                            new_data_values.append([link_record[p][0], selected_time_interval, "Dry"])

            print(new_data_values)
            for data in new_data_values: #writing the classification data into a new csv file
                for r in range(new_record_counter_arr[arr_counter]+1,new_record_counter_arr[arr_counter+1]+1):
                    if(data[0]==reader[r][0]  and data[1]==reader[r][1]):
                        new_arr=reader[r]
                        new_arr.append(data[2])
                        writer.writerow(new_arr)
                        break
            arr_counter+=1





















