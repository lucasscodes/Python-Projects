#SARSA Algorithm

#pip install gym==0.18.3

# import stuff
import gym
from IPython import display
import time
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1337)

def nb_render(env):
    # render gym environments in jupyter notebooks
    display.clear_output(wait=True)
    env.render()
    time.sleep(0.05)

env = gym.make('Taxi-v3')
env.reset() # resets the environment
nb_render(env)
print("State:",env.s,"\nMoves:",env.P[env.s])

print(env.action_space.n)

print(env.observation_space.n)

points = 0

s, r, done, _ = env.step(5)
#0=South,1=North,2=East,3=West
#4=Pickup,5=Dropoff
nb_render(env)
points += r
print(s,r,done)
print("Summe:",points)

def random_policy(state):
    return np.random.default_rng().integers(low=0,high=6,size=1)[0]

rands = np.array(list(map(random_policy,np.arange(100000))))
print(np.reshape(np.unique(rands,return_counts=True),(2,6)))

def evaluate(policy,envs=20):
    points = []
    for i in range(envs):
        res = []
        env = gym.make('Taxi-v3')
        env.reset() #Startzustand erzeugen
        s = env.s
        a = policy(s) #MBewegungs-Kommando berechnen
        done = False
        while not done:
            s_prime, r, done, _ = env.step(a) #Speichere results
            a_prime = policy(s_prime)
            s,a = s_prime,a_prime
            res += [r] #Speichere Punkte
        points += [np.sum(res)]
    #nb_render(env) #Rendert die letzte Episode
    return points #Gib kummultative Liste aus
np.shape(evaluate(random_policy,123))

plt.title("Punkteverteilung")
plt.plot(evaluate(random_policy))
plt.xlabel("Episode")
plt.ylabel("Punkte")
plt.show()

def init_table():
    states = env.observation_space.n
    actions = env.action_space.n
    return np.zeros((states, actions))
q_values = init_table()
q_values.shape

def exploit(state):
    #Liefere Index des ersten Vorkommens vom Maximums
    return np.where(q_values[state]==np.max(q_values[state]))[0][0]

#Testwerte einfügen und return überprüfen
q_values[0]=[0,1,3,4,2,0]
print(exploit(0)) #sollte 3 sein!

#Änderungen zurücknehmen
if not (np.unique(q_values)==np.array([0.0]))[0]:
    q_values = init_table()
    if not (np.unique(q_values)==np.array([0.0]))[0]:
        print("q_values sind nicht wiederherstellbar!")

def explore(state):
    return np.random.default_rng().integers(low=0,high=6,size=1)[0]

np.reshape(np.unique(list(map(explore,range(10000))),return_counts=True),(2,6))

epsilon = 0.1

def eps_greedy(state):
    if(np.random.rand()<=epsilon):
        return explore(state)
    else:
        return exploit(state)
        
gamma = 0.99

def td_error(s, a, r, s_prime, a_prime):
    #print(s,a,r,s_prime,a_prime)
    return r + gamma*q_values[s_prime,a_prime] - q_values[s,a]

eta = 0.1

def update_table(s, a, delta):
    #print(s,a,delta)
    q_values[s,a] = q_values[s,a]+eta*delta

table = init_table()
episodes = 2000

def episode():
    rews = [] #Liste der Rewards
    env = gym.make('Taxi-v3')
    env.reset() #Startzustand erzeugen
    s = env.s     #Startzustand
    a = explore(s) #Bewegungs-Kommando berechnen
    done = False
    while not done:
        s_prime, r, done, _ = env.step(a) #execute action 𝑎, read reward 𝑟 and new state 𝑠′
        a_prime = eps_greedy(s_prime) #select next action 𝑎′
        delta = td_error(s, a, r, s_prime, a_prime) #compute TD-error
        update_table(s, a, delta) #update Q table
        s,a = s_prime,a_prime #set variables for next iteration: 𝑠←𝑠′, 𝑎←𝑎′
        rews += [r] #Speichere Punkte
    #print(done)
    return rews

def train(n=1):
    rews = []
    for i in range(n):
        print("Episode:",i+1,"von",n)
        rews += [np.sum(episode())]
    return rews

train_rewards = train(episodes)

#Das Spiel scheint nach 200 Schritten immer Game-Over zu sagen (Ende==True, letztePunkte!=20)
for i in range(3):
    print("Episode",i,"Punkte",train_rewards[i])

plt.title("Endpunktzahlen")
plt.plot(train_rewards)
plt.xlabel("Episode")
plt.ylabel("Punkte")
plt.show()

#evaluate(random_policy,200)
plt.plot(evaluate(exploit))

plt.title("Policy-Vergleich")
plt.plot(evaluate(exploit))
plt.plot(evaluate(random_policy))
plt.xlabel("Episoden")
plt.ylabel("exploit(blau)\n\n\nrandom(gelb)",rotation=0)
plt.show()

