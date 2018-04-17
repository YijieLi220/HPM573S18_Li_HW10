from Q1 import cohort1
from Q1 import cohort2
import scr.EconEvalClasses as EconCls

def report_CBA():
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

    NBA = EconCls.CBA(
        strategies=[with_therapy, without_therapy],
        if_paired=False
    )
    # show the net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=EconCls.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )
report_CBA()
print("According to the output, I would  recommend use the therapy when the willingness-to-pay is about more than 10000")