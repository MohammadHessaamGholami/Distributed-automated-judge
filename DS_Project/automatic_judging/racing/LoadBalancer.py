from multiprocessing import Queue
import time
import threading
import requests
import json

free_servers = Queue() 
helping_servers = Queue()

num_judging_server = 0
num_helping_judging_server = 0

config = open('config/config_judging_server', 'r')
for line in config:
    my_list = line.split(':')
    free_servers.put({'id':'main_server','host': my_list[0], 'port': my_list[1]})
    num_judging_server += 1    
config.close()


config = open('config/config_helping_judging_server', 'r')
for line in config:
    my_list = line.split(':')
    helping_servers.put({'id': 'helping_server' ,'host': my_list[0], 'port': my_list[1]})
    num_helping_judging_server += 1    
config.close()


sem_free_server = threading.Semaphore(num_judging_server)
sem_helping_server = threading.Semaphore(num_helping_judging_server)
myqueue = Queue(maxsize= 1000)

def add_queue(code, sample_input, sample_output, checkCode, student_id, question_id, racing_id):
    information = {
        'code': code,
        'sample_input': sample_input,
        'sample_output': sample_output,
        'checkCode': checkCode,
        'student_id': student_id,
        'question_id': question_id,
        'racing_id': racing_id
    }
    myqueue.put(information)

def judge(item, server):
    files = {
            'code': open(item['code'], 'rb'),
            'sample_input': open(item['sample_input'], 'rb'),
            'sample_output': open(item['sample_output'], 'rb'),
            'checkCode': open(item['checkCode'], 'rb'),
             }
            
    r = requests.post('http://'+ server['host'] +':'+server['port']+'/judge/', files=files)
    result = r.text
    result = json.loads(result)
    
    running_time = result['running_time']
    score = result['score']
    from racing.models import StudentQuestion
    StudentQuestion.objects.filter(racing_id=item['racing_id'], question_id=item['question_id'], student_id=item['student_id']).update(answer_score=score, running_time=str(round(float(running_time),3)))

    if (server['id'] == 'main_server'):
        sem_free_server.release()
        free_servers.put(server)
    else:
        sem_helping_server.release()
        helping_servers.put(server)
    
    

def run_loop():
    while(True):
        if (sem_free_server._value != 0):
            #print("******************************")
            #print("just main servers")
            item = myqueue.get()
            sem_free_server.acquire()
            server = free_servers.get()
            x = threading.Thread(target=judge,args=(item,server,))
            x.start()
        else:
            item = myqueue.get()
            sem_helping_server.acquire()
            server = helping_servers.get()
            x = threading.Thread(target=judge,args=(item,server,))
            x.start()
