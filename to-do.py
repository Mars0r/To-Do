#!/bin/python3

from cgi import print_arguments
import colorama
import os
from colorama import Fore
from colorama import Style
import optparse
import re 
import csv
import time
import pandas as pd
from requests import options

paths = str(os.environ['HOME']) + '/.Todo'

def add():
    global paths
    cont = 0
    with open(paths, 'r') as f_object:
        csv_reader = csv.reader(f_object, delimiter=',')
        for row in csv_reader:
            cont += 1
        f_object.close()

    with open(paths, 'a') as f_object:
        task = input('Tarea --> ')
        priority = int(input('1 --> '+ Fore.RED + Style.BRIGHT + "High" + Style.RESET_ALL + '\n2 --> '+ Fore.GREEN + Style.BRIGHT + "Mid" + Style.RESET_ALL+ '\n3 --> '+ Fore.BLUE + Style.BRIGHT + "Low" + Style.RESET_ALL+ '\nPriority: '))
        save = [cont, 0,task, priority, time.time()]   
        writer = csv.writer(f_object)
        writer.writerow(save)
        f_object.close()


def mark_as_done():
    list()
    global paths
    TaskToM_D = int(input('Qué terea has terminado? --> '))
    if type(TaskToM_D) != int:
        exit
    else:
        data = pd.read_csv(paths, header=None, names=["Count", "Done", "Task", "Priority", "Time"])
        df = pd.DataFrame(data)
        df.loc[df.Count==TaskToM_D,'Done']=1
        df.to_csv(paths, index=False, header=False)
        
def list():
    global paths
    data = pd.read_csv(paths, header=None, names=["Count", "Done", "Task", "Priority", "Time"])
    df = pd.DataFrame(data)
    by_priority = df.sort_values('Priority',ascending=True)
    by_priority.to_csv(paths, index=False, header=False)

    count = 0
    with open(paths, 'r') as f_object:
        csv_reader = csv.reader(f_object, delimiter=',')

        for row in csv_reader:
            if int(row[1]) == 1:
                None
            else:
                count += 1
                if int(row[3]) == 1:
                    print(Fore.RED + Style.BRIGHT + f'{row[0]}' + '  -->    ' + f'{row[2]}' + Style.RESET_ALL)
                
                elif int(row[3]) == 2:
                    print(Fore.GREEN + Style.BRIGHT + f'{row[0]}' + '  -->    ' + f'{row[2]}' + Style.RESET_ALL)

                elif int(row[3]) == 3:
                    print(Fore.BLUE + Style.BRIGHT + f'{row[0]}' + '  -->    ' + f'{row[2]}' + Style.RESET_ALL)

                else:
                    print(f'\n-->   ' + row[2])
        
        f_object.close()

    if count == 0:
        print('Parece que no tienes tareas pendientes, muy bien.')
        exit()

    else:
        None

def list_all():
    global paths
    count = 0

    data = pd.read_csv(paths, header=None, names=["Count", "Done", "Task", "Priority", "Time"])
    df = pd.DataFrame(data)
    by_priority = df.sort_values(['Done', 'Priority'], ascending=[True,True])
    by_priority.to_csv(paths, index=False, header=False)

    with open(paths, 'r') as f_object:
        csv_reader = csv.reader(f_object, delimiter=',')

        for row in csv_reader:
            count += 1
            if int(row[1]) == 1:
                if int(row[3]) == 1:
                    print(Fore.BLUE  + f'{row[0]}' + '  -->    ' + f'{row[2]} *(Done)' + Style.RESET_ALL)
                
                elif int(row[3]) == 2:
                    print(Fore.BLUE + f'{row[0]}' + '  -->    ' + f'{row[2]} *(Done)' + Style.RESET_ALL)

                elif int(row[3]) == 3:
                    print(Fore.BLUE  + f'{row[0]}' + '  -->    ' + f'{row[2]} *(Done)' + Style.RESET_ALL)

                else:
                    print(f'\n-->   ' + row[2])
            else: 
                if int(row[3]) == 1:
                    print(Fore.RED + Style.BRIGHT + f'{row[0]}' + '  -->    ' + f'{row[2]}' + Style.RESET_ALL)
                
                elif int(row[3]) == 2:
                    print(Fore.YELLOW + Style.BRIGHT + f'{row[0]}' + '  -->    ' + f'{row[2]}' + Style.RESET_ALL)

                elif int(row[3]) == 3:
                    print(Fore.GREEN + Style.BRIGHT + f'{row[0]}' + '  -->    ' + f'{row[2]}' + Style.RESET_ALL)

                else:
                    print(f'\n-->   ' + row[2])
        
        f_object.close()
    if count == 0:
        print('Parece que no tienes tareas pendientes, muy bien.')
        exit()

    else:
        None

def what_to_do(input):

    if input.list: 
        list_all()

    elif input.add:
        add()

    elif input.markasdone:
        mark_as_done()
    
    else:
        print('Emm creo que has escrito algo mal. ')

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-a", '--add', action="store_true", dest="add")
    parser.add_option("-m", '--markasdone', action="store_true", dest="markasdone")
    parser.add_option("-l", "--list", action="store_true", dest="list", help='Mustra todas las tareas las no completadas.')

    (options, args) = parser.parse_args()

    if not (options.add or options.markasdone or options.list ):
        options.list = True
        

    elif (options.add and (options.markasdone or options.list )) or (options.markasdone and options.list):
        print('No puedes poner dos argumentos a la vez, no tiene sentido')

    return options

try:
    what_to_do(get_arguments())

except KeyboardInterrupt:
    exit()
