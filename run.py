"""
Machine shop example

Covers:

- Interrupts
- Resources: PreemptiveResource

Scenario:
  A workshop has *n* identical machines. A stream of jobs (enough to
  keep the machines busy) arrives. Each machine breaks down
  periodically. Repairs are carried out by one repairman. The repairman
  has other, less important tasks to perform, too. Broken machines
  preempt theses tasks. The repairman continues them when he is done
  with the machine repair. The workshop works continuously.

"""
import random
from datetime import datetime, timedelta
import simpy
import uuid
import pickle
from jukebox import JukeboxInc
from tinybird import TinyBird

RANDOM_SEED = 42
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 300.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME = 30.0     # Time it takes to repair a machine in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_MACHINES = 10      # Number of machines in the machine shop

AVG_SALES_PER_MONTH = 5
AVG_SONGS_PER_DAY = 50

PRICE = 700
ROYALTIES = 0.2

START_DATE = '2020-11-01 08:00'
DAYS = 730              # Simulation time in days
WEEKS = 100

START_DATE = (datetime.now() - timedelta(days=DAYS)).date().isoformat()
SIM_TIME = timedelta(days=DAYS).total_seconds() / 60  # Simulation time in minutes

from music import MusicService

if False:
    mm = MusicService()
    tracks = mm.get_tracks()

    with open('tracks.pkl', 'wb') as f:
        pickle.dump(tracks, f)

with open('tracks.pkl', 'rb') as f:
    tracks = pickle.load(f)

jk = JukeboxInc()

tn = TinyBird()

def time_to_sale():
    """Return time until next failure for a machine."""
    return random.expovariate( AVG_SALES_PER_MONTH / (30 *24 * 60) )


def time_to_song():
    """Return time until next failure for a machine."""
    return random.expovariate( AVG_SONGS_PER_DAY / (24 * 60) )
    
def real_time(n, start_time=START_DATE):
    return (datetime.fromisoformat(start_time) + timedelta(minutes=n)) #.isoformat()


class MusicMaker(object):
    """A machine produces parts and my get broken every now and then.

    If it breaks, it requests a *repairman* and continues the production
    after the it is repaired.

    A machine has a *name* and a numberof *parts_made* thus far.

    """
    def __init__(self, env, sold_by):
        self.env = env
        self.id = str(uuid.uuid4())
        self.machine = simpy.Resource(env, 1)
        self.sold_by = sold_by
        self.owner = {
            "id": str(uuid.uuid4()),
            "name": jk.get_name(),
            "country": sold_by['country']
        }    
        self.location = {"id": str(uuid.uuid4()),
                         "address": jk.get_place(sold_by['country'])
                        }

        at = real_time(self.env.now)

        tn.location_registered(self.owner['id'], self.location['id'], at )
        tn.device_purchased(self.id, at)
        tn.device_allocated(sold_by, self.id, self.location['id'], at)

        payment = PRICE * random.randint(10, 25) / 100 
        self.left = PRICE - payment
        tn.payment_received( str(uuid.uuid4()), self.owner['id'], payment, at)
        self.due = 0

        self.tracks = []

        env.process(self.pay())

    def str(self):
        return self.name

    def repr(self):
        return self.name
        
    def play(self, track):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
 
        at = real_time(self.env.now)
        print(f"{real_time(self.env.now).isoformat()} Playing {track['name']} at machine {self.id}")
        #tn.song_listened(track['id'], self.id, track['duration'], at)
        track.update({'at':at})
        self.tracks.append(track)

        self.due += ROYALTIES
        yield self.env.timeout(track['duration'])

    def pay(self):
        """Break the machine every now and then."""
        while True:
            yield self.env.timeout(24 * 60)

            if self.tracks:
                tn.songs_listened(self.id, self.tracks)
                self.tracks = []

            if self.due > 0:
                at = real_time(self.env.now)
                tn.payment_received(str(uuid.uuid4()), self.owner['id'], self.due, at)
                self.left =- self.due
                self.due = 0

def customer(env, mm):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    while True:
        yield env.timeout(random.randint(3, 7))
        with mm.machine.request() as request:
            yield request
            track = random.choice(tracks)
            yield env.process(mm.play(track))


class Agent(object):
    """A machine produces parts and my get broken every now and then.

    If it breaks, it requests a *repairman* and continues the production
    after the it is repaired.

    A machine has a *name* and a numberof *parts_made* thus far.

    """
    def __init__(self, env, name):
        self.env = env
        self.id = str(uuid.uuid4())
        self.name = jk.get_name()
        self.country = jk.get_country()
        print(f'New agent {self.name} in {self.country}')

        self.machines = []

        env.process(self.sell())

    def str(self):
        return self.name

    def repr(self):
        return self.name
        
    def sell(self):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""

        while True:
            yield self.env.timeout(time_to_sale())
            mm = MusicMaker(env, {
                "id": self.id,
                "name": self.name,
                "country": self.country
            })
            print(f"New Machine sold machine {mm.id} by {self.name}")
            self.machines.append(mm)
            env.process( customer(env, mm) )



# Setup and start the simulation
print('Carwash')
print('Check out http://youtu.be/fXXmeP9TvBg while simulating ... ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results



# Create an environment and start the setup process
env = simpy.Environment()

#machines = [  MusicMaker(env, f'mm{i}')   for i in range(2)]

agents = [Agent(env, f'Agente {i}') for i in range(5)]

# Execute!
env.run(until=SIM_TIME)

for a in agents:
    print(f'{a.name} sold {len(a.machines)} machines')