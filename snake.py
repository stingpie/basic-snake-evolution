import pygame, numpy, random, time, os

from pygame.locals import *

def setup():
    pygame.init()
    global window
    window=pygame.display.set_mode((win_x, win_y))
    global env
    env=numpy.zeros((env_x, env_y))




    
def draw():
    for i in range(env_x):
        for j in range(env_y):
            if env[i][j]>0:
                
                pygame.draw.rect(window, ((env[i, j]*(255/length)), (env[i, j]*(255/length)), (env[i, j]*(255/length)),20), (gridx*i, gridy*j, gridx, gridy), 0 )


    pygame.draw.rect(window, (240,60 ,40,20 ), (gridx*(headx-1), gridy*(heady-1), gridx, gridy), 0 )
    pygame.draw.rect(window, (80,200 ,120,20 ), (gridx*randx, gridy*randy, gridx, gridy), 0 )
         
    pygame.display.flip()

def spec(x):
    
    if abs(x)>6:
        return ((numpy.arctan(x*3)**3)+(x-6))

        
    return numpy.arctan(x*3)**3





def initagent(net):
    #fills a net with random junk.
    net = numpy.zeros((netsize,netsize,timetothink))
    sense=[]
    for i in range(netsize**2):
        for j in range(timetothink):
            if i<(netsize**2)-600 or i>(netsize**2)-80:
                net[int(i/netsize)][i%netsize][j]=((random.random()-0.5)+(random.random()-0.5)*1.6)
            if not(i<(netsize**2)-600 or i>(netsize**2)-120):

                net[int(i/netsize)][i%netsize][j]=0     
    
    return net

def modifyagent(net1, net2, mutate,similarity):
    #takes net one, multiplies it by 0.5, and adds it to net two, multiplied by 0.5.
    #then a random value is added/subtracted.
    inter = []
    similarity=abs(numpy.arctan(similarity))
    square=netsize
    inter = numpy.zeros(numpy.shape(net1))
    for z in range(timetothink):
        for x in range(int(square)):
            for y in range(int(square)):
                
                inter[x][y][z] =((net1[x][y][z]*0.5)+(net2[x][y][z]*0.5))+((random.random()-0.5)*mutate)

    return inter[:]

def duplicate(net1,mutate):
    inter=[]
    inter = numpy.zeros(numpy.shape(net1))
    square=numpy.shape(net1)[0]
    
    for z in range(timetothink):
        
        for x in range(square):
            
            for y in range(square):
                
                inter[x][y][z] =(net1[x][y][z]+((random.random()-0.5)*mutate))
                if (25<x and x<37)and (not enablememory):

                    inter[x][y][z]=0 
     
    return inter






def play(env, headx, heady, mem, fruitx, fruity, network, steps):
    #this whole thing takes in inputs & memory, puts in through a layered network,
    #& outputs an array with the net's action & new memory state
    right= int(-1)
    left= int(1)

    # this junk is appending senses to the net.
    view=numpy.zeros((5,5))
    for i in range(25):
            
        view[int(i/5),i%5] = env[(int(i/5)+headx)%env_x,((i%5)+heady-1)%env_y] 
   
    sense=[]
    out=numpy.zeros((netsize,timetothink))


    for i in range(len(view.flatten())):
        sense.append(view.flatten()[i])
    sense.append(headx)
    sense.append(heady)
    sense.append(fruitx)
    sense.append(fruity)

    for i in range(len(mem)):
        sense.append(mem[i])
        memloc=i
    sense.append(steps)
    for i in range(netsize-len(sense)):
        sense.append(1)
    for i in range(netsize):
        if i<len(sense):
            out[i][0]=sense[i]
        else:
            out[i][0]=0

    # the net is formated in a grid, where each node is a certain x value,
    # and for every x value, it multiplys by a certain xy value, to add to the
    # node[y]. then, once it goes through the entire grid, it repeats this
    # for timetothink times, taking in the old node values, and repeating the
    # process.

    
    for think in range(timetothink):
        for x in range(netsize):

            for y in range(netsize):
                  
                out[y][think] += (network[x][y][think]*(out[x][think-1]))
                out[y][think]=spec(out[y][think])
                if braindisplay:
                    color1=abs(int(network[x][y][think]*30)+128)
                    if color1>254:
                        color1=254
                    color2=abs(int(out[y][think]*70)+128)
                    if color2>254:
                        color2=254
                    color3=abs(int(out[x][think]*network[x][y][think]*30)+128)
                    if color3>254:
                        color3=254
                    pygame.draw.rect(window, (color1, color2, color3), (((x*2)+(think*netsize*2))+gridx+think,(y*2)+gridy,2,2), 0 )
                    
    pygame.display.flip()                    
    if debug==True:
        time.sleep(0.03)
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]: return (int(right),out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
        if key[pygame.K_RIGHT]:return (int(left),out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])

    choice=numpy.argmax((out[len(out)-1][timetothink-1],out[len(out)-2][timetothink-1],out[len(out)-3][timetothink-1]))

    if out[len(out)-1][timetothink-1]==0 and out[len(out)-2][timetothink-1]==0 and out[len(out)-3][timetothink-1]==0:
        choice=1
        
    
    #this returns  the direction to turn in, along with a whole lot of memories. 
    if choice==0 :

        return (int(right),out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
    if choice==2 :
        return (int(left),out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
    return (0,out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
    
def stop():

    stopping=True
    
def brainsurgery(net1,neuron,layer,polar, power):
    
    if polar>0:
        nudge=10**(layer-(1+numpy.shape(net1)[2]))
        for i in range(numpy.shape(net1)[0]):
            net1[i][neuron][layer]+= nudge*power
            if layer>0.5:
                brainsurgery(net1,i,layer-1,polar,power)
    if polar<0:
        nudge= -(10**(layer-(1+numpy.shape(net1)[2])))
        for i in range(numpy.shape(net1)[0]):
            net1[i][neuron][layer]+= nudge*power
            if layer>0.5:
                brainsurgery(net1,i,layer-1,polar,power)
    if polar==0:
        for i in range(numpy.shape(net1)[0]):
            net1[i][neuron][layer]*= (0.9-(layer+1)/10)*power
            if layer>0.5:
                brainsurgery(net1,i,layer-1,polar,power)
            
    return net1    


def autosave(net):

    f = open("ML_SNAKE.txt", 'wb', "r")
    numpy.save(f, net,allow_pickle=False)


def load():
    return numpy.load("ML_SNAKE.txt",allow_pickle=False )
     






global netsize
global seed
global debug
debug=False
pastnets=[]
actionlibrary=[]
maxdistance=0
mindistance=1000000
netsize=40
seed=random.random()*100000
topscore=0
prevscore=0
length=5
win_x=700
win_y=700
env_x=25 #enviroment width
env_y=25 #enviroment height
headx=int(env_x/2)
heady=int(env_y/2)
setup()
direc=0
score=0
randx=0
randy=0
enablefruit=False
gridx=win_x/env_x
gridy=win_y/env_y
trainingsteps=0
env[randx,randy]=1
tail=[]
net=[]
stopping=False
view=[]
view=numpy.zeros((5,5))
netstorage=[]
agentnum=200
agentscore=numpy.zeros((agentnum),dtype='i4')
agentlibrary=numpy.zeros((agentnum),dtype='i4')
timetothink=2
gen=0
posrandx=6
posrandy=3
similar=numpy.zeros((agentnum))
surgery=[]
retry=False
braindisplay=True
enablememory=False
save=False
prev_reliability=0

for i in range(agentnum):
    surgery=numpy.append(surgery,False)
fruit_variation=500 #higher means less variation

for agents in range(agentnum):
    netstorage.append(initagent(net))
netdifferences=numpy.zeros(numpy.shape(netstorage))
pastnets=numpy.zeros(numpy.shape(netstorage))

netstorage[0]= load()
enablememory=True
enablefruit=True

while not pygame.key.get_pressed()[pygame.K_t]:
    gen+=1
    posrandx2=int((random.random()*(gen/fruit_variation))-(gen/(fruit_variation*2)))+posrandx
    posrandy2=int((random.random()*(gen/fruit_variation))-(gen/(fruit_variation*2)))+posrandy
        
    for agents in range(agentnum):
        fruitcollected=0
        mindistance=1000000
        score=0
        headx=int(env_x/2)
        heady=int(env_y/2)
        length=8
        direc=0
        env=numpy.zeros((env_x, env_y))
        tail=[]
        stopping=False
        steps=0
        random.seed(gen*agents+prevscore)

        
        randx=int(((env_x/2)-posrandx2+(random.random()*env_x))%(env_x-2))+1
        randy=int(((env_y/2)-posrandy2+(random.random()*env_x))%(env_y-2))+1
        if randx>(env_x/2)-3 and randx<(env_x/2)+3:
            if random.random()>0.5:
                randx+=6
            else:
                randx-=6
        if randy>(env_y/2)-3 and randy<(env_y/2)+3:
            if random.random()>0.5:
                randy+=6
            else:
                randy-=6
        
        env[randx][randy]= -100
        mem2=[0,0,0,0,0,0,0,0]
        prevescore=0

        pygame.draw.rect(window,(0,0,0),(0,0,win_x,win_y))
        for i in range(length*17):
            



            
            steps+=1
            for j in range(len(tail)): #adds 1 to each part of the tail, and
                                       #shortens the tail when a part is
                                       #greater than the length.
            
                if env[tail[j]]>=1:
                    env[tail[j]]-=1
                        
                if env[tail[j]]<=1:
                    env[tail[j]]=0
                    
                if env[tail[j]]==0:
                    pygame.draw.rect(window, (0,0,0), (tail[j][0]*gridx,tail[j][1]*gridy,gridx,gridy), 0 )
                    


            # actuall decisions by the net are made here.
            # it outputs a decision(left, right, or straight as 1,-1,0)followed by
            # 8 units of memory.
            if steps%(length-1)==0 or steps==1:
                for i in range(env_x):
                    env[i][0]=length
                    env[i][env_y-1]=length 
                    env[0][i]=length
                    env[env_x-1][i]=length


            
            draw()
            output=play(env, headx, heady, mem2, randx, randy, netstorage[agents],steps%length)
            mem2=output[1:]
            turn=output[0]

            direc+=turn


            
            if enablefruit:
                if env[(headx-1)%env_x,(heady-1)%env_y]== -100: #this triggers when the snake eats a fruit
                    random.seed(headx*length+env[heady][randy])
                    fruitcollected+=1
                    score+=500
                    randx=random.randint(0,env_x-1)
                    randy=random.randint(0,env_y-1)
                
                    while env[randx,randy]!=0:
                        randx=random.randint(0,env_x-1)
                        randy=random.randint(0,env_y-1)



                
                
            #this next part is just basic house keeping. 
            tail.append((headx-1,heady-1))
            env[headx-1,heady-1]=length

            
            
            direc=direc%4

            # this next section rewards an agent for pointing towards the fruit
            # this rewards it for going towards the fruit, and punishes it for
            # moving away. of course, it doens't know the score till the end.
            if enablefruit==True:
                if randx-headx<0:
                    
                    if direc == 0:
                        pygame.draw.rect(window,(128,200,128),(win_x-gridx-40,gridy,20,20))
                        score+=3
                    else:
                        score-=3
                        pygame.draw.rect(window,(200,128,128),(win_x-gridx-40,gridy,20,20))
                if randx-headx>0:
                    if direc == 2:
                        pygame.draw.rect(window,(128,200,128),(win_x-gridx-60,gridy,20,20))
                        score+=3
                    else:
                        score-=3
                        pygame.draw.rect(window,(200,128,128),(win_x-gridx-60,gridy,20,20))
                if randy-heady>0:
                    if direc == 3:
                        pygame.draw.rect(window,(128,200,128),(win_x-gridx-80,gridy,20,20))
                        score+=3
                    else:
                        score-=3
                        pygame.draw.rect(window,(200,128,128),(win_x-gridx-80,gridy,20,20))
                if randy-heady<0:
                    if direc == 1:
                        pygame.draw.rect(window,(128,200,128),(win_x-gridx-100,gridy,20,20))
                        score+=3
                    else:
                        score-=3
                        pygame.draw.rect(window,(200,128,128),(win_x-gridx-100,gridy,20,20))


            #this just moves the sanke's head in the right direction
            env[randx][randy]= -100
            if direc == 0:

                headx-=1
            
            
            if direc == 2:

                headx+=1
            
            if direc == 1:

                heady-=1
            
            if direc == 3:
            
                heady+=1
    

            key=pygame.key.get_pressed() #activates debug mode
            if key[pygame.K_e]:
                time.sleep(0.3)
                if debug==False:
                    debug=True
                else:
                    debug=False
            if key[pygame.K_b]:
                time.sleep(0.1)
                if braindisplay==False:
                    braindisplay=True
                else:
                    braindisplay=False
            if key[pygame.K_r]:
                time.sleep(0.1)
                for agents in range(agentnum):
                    netstorage[agents]=initagent(net)

            if key[pygame.K_s]:
                save=True

            if len(tail)>length: #chops off the begining of the tail array. 
                tail=tail[1:]
            
            if headx<=0 or heady<=0 or (headx)>env_x or (heady)>env_y or env[(headx-1)%env_x,(heady-1)%env_y]>2:
                #what to do when the snake crashes into something.
                surgery[agents]=True
                score-=800
                stop()
                stopping=True


            if mindistance > abs(headx-randx)+abs(heady-randy): #tracks the minimum distance from the fruit to the snake
                mindistance=(abs(headx-randx)+abs(heady-randy))

            if maxdistance < abs(headx-randx)+abs(heady-randy): #tracks the maximum distance from the fruit to the snake
                maxdistance=(abs(headx-randx)+abs(heady-randy))

            if stopping: #just to make things pythonic     
                break
            
            if True : #display each step
                pygame.event.pump()
                scorediff=int(numpy.arctan((score-prevscore)/3)*81)
                scorepos=((abs(scorediff)+scorediff)/2)+128
                scoreneg=(abs(-abs(scorediff)+scorediff)/2)+128
                pygame.draw.rect(window,(scoreneg,scorepos,128),(win_x-gridx-20,gridy,20,20))
                
            prevescore=score
            turn=0
        if steps<((env_x-2)/2)-1: #punishes if the snake immedeatly crashes
            score-=500
        if enablefruit:
            score=(score+((env_x+env_y)-mindistance)+(steps*8))+(80*fruitcollected/steps)#score equation
        else:
            score=score+(steps*8)
        agentscore[agents]=score #makes an array of each agent's score.

        
    if topscore>numpy.amax(agentscore): #gets the top score for all agents across time
        topscore=numpy.amax(agentscore)


    maxscore=numpy.amax(agentscore)
    minscore=numpy.amin(agentscore)
    if maxscore>=500:
        enablememory=True
    if maxscore>=700:
        enablefruit=True
    if prevscore != numpy.amax(agentscore) or gen%100==0:
        print(agentscore)
        print(str(maxscore-prevscore)+" & "+str(maxscore)+" ==> "+str(numpy.average(numpy.greater(agentscore,numpy.zeros(len(agentscore))))))
    reliability=numpy.average(numpy.greater(agentscore,numpy.zeros(len(agentscore))))
    
    # finds top, bottom, & second best
    netdifferences=numpy.subtract(netstorage,pastnets)
    pastnets=netstorage[:]
    if (prevscore<maxscore and gen>1) :
        netstorage=numpy.add(netstorage,numpy.divide(netdifferences,10))
        retry=True
    else:
        if retry==True:
            netstorage=numpy.subtract(netstorage,numpy.divide(netdifferences,10))
        retry=False
        
    prevscore=numpy.amax(agentscore)
    for i in range(agentnum):

        if surgery[i]:
            if random.random()>=0.5:
                                          
                brainsurgery(netstorage[i],netsize-1,timetothink-1,1,0.01)
            else:
                brainsurgery(netstorage[i],netsize-3,timetothink-1,1,0.01)
                                          
    netstorage2=numpy.zeros(numpy.shape(netstorage))
    if prev_reliability-reliability > 0.1:
        netstorage2=reversion[:]

    prev_reliability=numpy.average(numpy.greater(agentscore,numpy.zeros(len(agentscore))))
    reversion=netstorage[:]
    #combines agents with a 9:1 ratio.
    #if gen%10==0 or save:
        #autosave(netstorage[numpy.argmax(agentscore)])
    if not retry: 
        
        topnet=numpy.argmax(agentscore)
        mutate=0.01
            
        
        netstorage2=netstorage[:]
        for z in range(int((agentnum))):
            if not agentscore[z]+200 >= numpy.amax(agentscore):
                netstorage2[z]=duplicate(netstorage[topnet],mutate)[:]
            else:
                netstorage2[z]=duplicate(netstorage[z],mutate)[:]
                
            pygame.draw.rect(window,(120,200,250), (0,0,z*(win_x/agentnum),20))
            pygame.display.flip()
            pygame.event.pump()
                
        netstorage2[0]=duplicate(netstorage[topnet],0)[:]
        choice=0
        
        netstorage=netstorage2[:]
        
