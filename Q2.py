import scr.StatisticalClasses as Stat
import scr.FormatFunctions as Format
from Q1 import cohort1
from Q1 import cohort2
from Q1 import meansurvival
from Q1 import meansurvival2
from Q1 import ExpectedCI
from Q1 import ExpectedCI2

def print_comparative_cost(sim_output_high, sim_output_low):
    # increase in survival time
    increase = Stat.DifferenceStatIndp(
        name='Increase in cost',
        x=sim_output_high,
        y_ref=sim_output_low
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=0.05),
        deci=1
    )
    print("Average increase in cost and {:.{prec}%} confidence interval:".format(1 - 0.05, prec=0),
          estimate_CI)

def print_comparative_utility(sim_output_high, sim_output_low):

    # increase in survival time
    increase = Stat.DifferenceStatIndp(
        name='Increase in utility',
        x=sim_output_high,
        y_ref=sim_output_low
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=0.05),
        deci=1
    )
    print("Average increase in utility and {:.{prec}%} confidence interval:".format(1 - 0.05, prec=0),
          estimate_CI)

def print_comparative_stroke(sim_output_high, sim_output_low):

    # increase in survival time
    increase = Stat.DifferenceStatIndp(
        name='Increase in stroke',
        x=sim_output_high,
        y_ref=sim_output_low
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=0.05),
        deci=1
    )
    print("Average increase in stroke and {:.{prec}%} confidence interval:".format(1 - 0.05, prec=0),
          estimate_CI)

print(meansurvival, ExpectedCI)
print(meansurvival2, ExpectedCI2)
print_comparative_cost(cohort1.get_total_cost(),cohort2.get_total_cost())
print_comparative_utility(cohort1.get_total_utility(),cohort2.get_total_utility())
print_comparative_stroke(cohort1.get_STROKE_time(),cohort2.get_STROKE_time())
