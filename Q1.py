import scr.RandomVariantGenerators as rndClasses
import scr.StatisticalClasses as Stat
import scr.SamplePathClasses as PathCls
from enum import Enum
import scr.FigureSupport as Figs
import scr.EconEvalClasses as EconCls

TRANS_MATRIX = [
    [0.75,  0.15,   0,     0.1],   # WELL
    [0,     0,      1,     0],   # STROKE
    [0,     0.25,   0.55,  0.2],   # P_STROKE
    ]

TRANS_MATRIX_THERAPY = [
    [0.75,  0.15,     0,      0.1],   # WELL
    [0,     0,        1,      0],   # STROKE
    [0,     0.1625,   0.701,  0.1365],   # P_STROKE
    ]

TRANS=[[
    [0.75,  0.15,     0,      0.1],   # WELL
    [0,     0,        1,      0],   # STROKE
    [0,     0.25,     0.55,   0.2],   # P_STROKE
    ], [
    [0.75,     0.15,     0,      0.1],   # WELL
    [0,        0,        1,      0],   # STROKE
    [0,        0.1625,   0.701,  0.1365],   # P_STROKE
    ]
]

TRANS_UTILITY= [
    [1,   0.8865,   0.9,  0],
    [1,   0.8865,   0.9,  0]
]

TRANS_COST=[
    [0,  5196,  200,  0],
    [0,  5196,  2200, 0]
]

discounted_rate=0.03

class HealthStats:
    """ health states of patients with risk of stroke """
    WELL = 0
    STROKE = 1
    P_STROKE = 2
    DEATH = 3

class THERAPY_OR_NOT (Enum):
    WITHOUT=0
    WITH=1


class Patient:
    def __init__(self, id, THERAPY):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: parameter object
        """

        self._id = id
        # random number generator for this patient
        self._rng = None
        self.healthstat=0
        self.survival=0
        self.THERAPY = THERAPY
        self.STROKE=0
        self.totalDiscountUtility=0
        self.totalDiscountCost=0

#from MarkovModelClasses.py
    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        self._rng = rndClasses.RNG(self._id)

        k = 0  # current time step

        # while the patient is alive and simulation length is not yet reached
        while self.healthstat!=3 and k  < sim_length:
            # find the transition probabilities of the future states
            trans_probs = TRANS[self.THERAPY][self.healthstat]
            # create an empirical distribution
            empirical_dist = rndClasses.Empirical(trans_probs)
            # sample from the empirical distribution to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = empirical_dist.sample(self._rng)
            if self.healthstat==1:
                self.STROKE+=1
            #caculate cost and utality
            cost=TRANS_COST[self.THERAPY][self.healthstat]
            utility=TRANS_UTILITY[self.THERAPY][self.healthstat]
            # update total discounted cost and utility (corrected for the half-cycle effect)
            self.totalDiscountCost += \
                EconCls.pv(cost, discounted_rate, k + 1)
            self.totalDiscountUtility += \
                EconCls.pv(utility, discounted_rate, k + 1)
            # update health state
            self.healthstat =new_state_index[0]
            # increment time step
            k += 1
        self.survival=k

    def get_survival_time(self):
        """ returns the patient's survival time"""
        return self.survival

    def get_STROKE_time(self):
        """ returns the patient's survival time"""
        return self.STROKE

    def get_total_utility(self):
        return self.totalDiscountUtility

    def get_total_cost(self):
        return self.totalDiscountCost

class Cohort():
    def __init__(self,id,THERAPY):
        self._initial_pop_size=2000
        self.survivaltime=[]
        self.id=id
        self.THERAPY=THERAPY
        self.STROKE=[]
        self.totaldiscountedcost=[]
        self.totaldiscountedutility=[]

    def simulate(self):
        for i in range(self._initial_pop_size):
            patient=Patient(self.id*self._initial_pop_size+i,self.THERAPY)
            patient.simulate(1000)
            self.survivaltime.append(patient.get_survival_time())
            self.STROKE.append(patient.get_STROKE_time())
            self.totaldiscountedcost.append(patient.get_total_cost())
            self.totaldiscountedutility.append(patient.get_total_utility())

    def get_survival_time(self):
        return self.survivaltime

    def get_STROKE_time(self):
        """ returns the patient's survival time"""
        return self.STROKE

    def get_total_utility(self):
        return self.totaldiscountedutility

    def get_total_cost(self):
        return self.totaldiscountedcost


class CohortOutcomes:
    def __init__(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        self._simulatedCohort = simulated_cohort

    def get_ave_survival_time(self):
        """ returns the average survival time of patients in this cohort """
        return sum(self._simulatedCohort.get_survival_time()) / len(self._simulatedCohort.get_survival_time())

    def get_survival_curve(self):
        """ returns the sample path for the number of living patients over time """

        # find the initial population size
        n_pop = 2000
        # sample path (number of alive patients over time)
        n_living_patients = PathCls.SamplePathBatchUpdate('# of living patients', 0, n_pop)

        # record the times of deaths
        for obs in self._simulatedCohort.get_survival_time():
            n_living_patients.record(time=obs, increment=-1)

        return n_living_patients

    def get_survival_times(self):
        """ :returns the survival times of the patients in this cohort"""
        return self._simulatedCohort.get_survival_time()


cohort1=Cohort(1,THERAPY_OR_NOT.WITHOUT.value)
cohort1.simulate()

cohort2=Cohort(2,THERAPY_OR_NOT.WITH.value)
cohort2.simulate()

cohort1.get_total_utility()
cohort1.get_total_cost()

cohort2.get_total_utility()
cohort2.get_total_cost()

sum_stat = Stat.SummaryStat("dsa",cohort1.get_survival_time())
ExpectedCI=sum_stat.get_t_CI(0.05)
meansurvival=sum_stat.get_mean()

sum_stat2 = Stat.SummaryStat("dsa",cohort2.get_survival_time())
ExpectedCI2=sum_stat2.get_t_CI(0.05)
meansurvival2=sum_stat2.get_mean()

print(meansurvival, ExpectedCI)
print(meansurvival2, ExpectedCI2)

print(cohort1.get_total_utility())
print(cohort1.get_total_cost())

print(cohort2.get_total_utility())
print(cohort2.get_total_cost())

##some of the code are cited from the HWsolution from githubHPM573, retrieved from https://github.com/HPM573/HWSolutions/tree/master/HW9.
