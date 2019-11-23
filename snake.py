import pygame, numpy, random, time

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



def initagent(net):
    #fills a net with random junk.
    net = numpy.zeros((netsize,netsize,timetothink))
    sense=[]
    for i in range(netsize**2):
        for j in range(timetothink):
            if i<(netsize**2)-600 or i>(netsize**2)-80:
                net[int(i/netsize)][i%netsize][j]=((random.random()-0.5)+(random.random()-0.5)*1.6)
            if not(i<(netsize**2)-600 or i>(netsize**2)-80):

                net[int(i/netsize)][i%netsize][j]=((random.random()-0.5)+(random.random()-0.5))            
    
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
                out[y][think]=numpy.sin(out[y][think])
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

        
    
    #this returns  the direction to turn in, along with a whole lot of memories. 
    if (out[len(out)-1][timetothink-1] >= 0.8):

        return (int(right),out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
    if (out[len(out)-1][timetothink-1] <= -0.8):
        return (int(left),out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
    return (0,out[memloc-7][timetothink-1],out[memloc-6][timetothink-1],out[memloc-5][timetothink-1],out[memloc-4][timetothink-1],out[memloc-3][timetothink-1],out[memloc-2][timetothink-1],out[memloc-1][timetothink-1],out[memloc][timetothink-1])
    
def stop():

    stopping=True







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
agentnum=60
agentscore=numpy.zeros((agentnum),dtype='i4')
agentlibrary=numpy.zeros((agentnum),dtype='i4')
timetothink=3
gen=0
posrandx=6
posrandy=3
similar=numpy.zeros((agentnum))
surgery=[]
retry=False
braindisplay=True

for i in range(agentnum):
    surgery=numpy.append(surgery,False)
fruit_variation=500 #higher means less variation

for agents in range(agentnum):
    netstorage.append(initagent(net))
netdifferences=numpy.zeros(numpy.shape(netstorage))
pastnets=numpy.zeros(numpy.shape(netstorage))


while not pygame.key.get_pressed()[pygame.K_t]:
    gen+=1
    posrandx2=int((random.random()*(gen/fruit_variation))-(gen/(fruit_variation*2)))+posrandx
    posrandy2=int((random.random()*(gen/fruit_variation))-(gen/(fruit_variation*2)))+posrandy
        
    for agents in range(agentnum):
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
        randx=(int(env_x/2)-posrandx2)%env_x
        randy=(int(env_y/2)-posrandy2)%env_y
        
        env[randx][randy]=-1
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


            
            
            if env[(headx-1)%env_x,(heady-1)%env_y]==-1: #this triggers when the snake eats a fruit
                random.seed(headx*length+env[headx+1][heady])

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
            env[randx][randy]=-1
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

            if len(tail)>length: #chops off the begining of the tail array. 
                tail=tail[1:]
            
            if headx<=0 or heady<=0 or (headx)>env_x or (heady)>env_y or env[(headx-1)%env_x,(heady-1)%env_y]>2:
                #what to do when the snake crashes into something.

                score-=10
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
            
        score=score+((env_x+env_y)-mindistance) #score equation

        agentscore[agents]=score #makes an array of each agent's score.

        
    if topscore>numpy.amax(agentscore): #gets the top score for all agents across time
        topscore=numpy.amax(agentscore)


    maxscore=numpy.amax(agentscore)
    minscore=numpy.amin(agentscore)
    if prevscore != numpy.amax(agentscore) or gen%100==0:
    
        print(agentscore)
        print(str(maxscore-prevscore)+" & "+str(maxscore))


    # finds top, bottom, & second best
    netdifferences=numpy.subtract(netstorage,pastnets)
    pastnets=netstorage[:]
    #if prevscore<maxscore:
        #netstorage=numpy.add(netstorage,numpy.divide(netdifferences,10))
        #retry=True
    #else:
        #if retry==True:
            #netstorage=numpy.subtract(netstorage,numpy.divide(netdifferences,10))
        #retry=False
        
    prevscore=numpy.amax(agentscore)

    
    netstorage2=numpy.zeros(numpy.shape(netstorage))
    #combines agents with a 9:1 ratio.
    if not retry: 
        for agent in range(int(agentnum)):
            topnet=numpy.argmax(agentscore)
            mutate=0.2
            
            for agent2 in range(int(agentnum)):
                similar[agent2]=abs(numpy.average(numpy.subtract(netstorage[agent],netstorage[agent2])))
                if agent==agent2:
                    similar[agent2]=100000
            netstorage2=netstorage[:]
            choice=numpy.argmin(similar)
            for z in range(int((agentnum))):
                netstorage2[int(gen+z+(agentnum))%agentnum]=modifyagent(netstorage[topnet],netstorage[topnet],mutate,similar[choice])[:]
            netstorage2[0]=modifyagent(netstorage[topnet],netstorage[topnet],0,similar[choice])[:]
            choice=0
            similar=numpy.zeros(len(similar))

        netstorage=netstorage2[:]
       
