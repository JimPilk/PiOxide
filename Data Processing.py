import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def convert(timestamp): #convert timestamp to datetime object
  fmt = "%H:%M:%S/%d-%m-%Y"
  datetime_str = datetime.datetime.strptime(timestamp, fmt)
  return datetime_str
  
def read_data(address): #read data from file and split into a list
  file=open(address,"r")
  data=[x.split(",") for x in file.read().split("\n")] #split by new line, then split each line by comma
  try:
    #remove null item created by newline charcter at end of file
    data.remove([""])
    print("removed null item...")
    print("data loaded...")
  except:
    #catch in case this character is removed
    print("data loaded...")
  file.close()
  return data

def get_location(): #get file location input from user
  valid=False
  while not valid:
    filename=input("file name:\n>")
    try:
      #check if file exists
      file=open(filename,"r")
      file.close()
      print("file found")
      valid=True
    except:
      #if file not found
      print("no such file/invalid file name")
      print("common errors:\n-include .txt file extension\n-file not in program directory\n-typo in file name\n")
  return filename

def process_data(data): #output data in a graph
  #split data array into components
  times=[]
  ppms=[]
  temps=[]
  humidities=[]

  for i in data:
    times.append(convert(i[0]))
    ppms.append(int(i[1]))
    temps.append(float(i[2]))
    humidities.append(float(i[3]))
  
  #set up axes
  fig,ax1=plt.subplots(figsize=(12,7),num="PiOxide")
  ax2=ax1.twinx()
  ax3=ax1.twinx()
  ax3.spines.right.set_position(("axes", 1.1))
  
  #plot data
  p1, = ax1.plot(times,ppms,label="CO2",color="blue")
  p2, = ax2.plot(times,temps,label="Temperature",color="red")
  p3, = ax3.plot(times,humidities,label="Humidity",color="green")
  
  #label axes and add minor grid lines
  label_size=12
  ax1.set_xlabel("Time",fontsize=label_size+1)
  ax1.set_ylabel("CO2 Concentration (ppm)",fontsize=label_size)
  ax1.minorticks_on()
  ax2.set_ylabel("Temperature (*C)",fontsize=label_size)
  ax2.minorticks_on()
  ax3.set_ylabel("Humidity (%)",fontsize=label_size)
  ax3.minorticks_on()
  
  #add legend
  plt.legend(handles=[p1, p2, p3], loc="upper left")
  
  #draw grid
  ax1.grid(linewidth=1)
  ax1.grid(which="minor",linewidth=0.2)
  
  #change title
  plt.title("Air Quality Data",fontsize=20)
  
  #format time labels on x axis
  myFmt = mdates.DateFormatter("%H:%M, %D")
  plt.gca().xaxis.set_major_formatter(myFmt)
  plt.gcf().autofmt_xdate()
  
  #decrease plot width so all y scales are seen on startup
  plt.subplots_adjust(right=0.85)
  plt.show()
  
#body code
data=read_data(get_location())
print("processing data...")
try:
  process_data(data)
  print("done")
except: 
  print("error in data handling")
  print("make sure:\n-file name is correct\n-data is in correct format, e.g: 23:03:04/20-03-2025,1152,31.43,28.00")
