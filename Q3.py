from Q1 import cohort1
from Q1 import cohort2
import scr.EconEvalClasses as EconCls

def report_CEA():
    """ performs cost-effectiveness and cost-benefit analyses
    :param simOutputs_mono: output of a cohort simulated under mono therapy
    :param simOutputs_combo: output of a cohort simulated under combination therapy
    """

    # define two strategies
    without_therapy= EconCls.Strategy(
        name='Without Therapy',
        cost_obs=cohort1.get_total_cost(),
        effect_obs=cohort1.get_total_utility()
    )
    with_therapy= EconCls.Strategy(
        name='With Therapy',
        cost_obs=cohort2.get_total_cost(),
        effect_obs=cohort2.get_total_utility()
    )

    # do CEA
    CEA = EconCls.CEA(
        strategies=[without_therapy, with_therapy],
        if_paired=False
    )
    # show the CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=EconCls.Interval.CONFIDENCE,
        alpha=0.05,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )
report_CEA()
