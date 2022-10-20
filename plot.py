from typing import List

import numpy as np

from mlss.entity import Trace


def create_informative_plots(training_data: List[Trace]):
    """Creates plots displaying SAD and percentile etc.
    """
    from itertools import cycle
    from bokeh.palettes import Dark2_7
    from bokeh.plotting import figure, show
    from bokeh.models import Span, Label

    key_length_bytes = len(training_data[0].key)
    samples = len(training_data[0].wave)
    print(f'Loaded {len(training_data)} traces')
    print(f'- key length {key_length_bytes * 8} bit')

    from mlss.processing import calculate_sads
    sads = calculate_sads(training_data)

    plot = figure(
        title=f'SAD for each key byte, n_s = {len(training_data)}',
        x_axis_label='Sample Number',
        y_axis_label='SAD'
    )

    masks = [sad > np.percentile(sad, 96) for sad in sads]

    print(f'Selected {min(map(sum, masks))}-{max(map(sum, masks))} features')

    for key_byte, mask, color in zip(sads, masks, cycle(Dark2_7)):
        plot.line(range(samples), key_byte, color=color, line_width=2, line_alpha=0.6, line_dash='dashed')
        plot.scatter(
            [v for v, t in zip(range(len(key_byte)), mask) if t],
            [v for v, t in zip(key_byte, mask) if t],
            color=color,
            size=4
        )
        break

    pcs = [5, 10, 25, 50, 75, 90, 95, 96, 97, 98, 99]
    for percentile, pc in zip(np.percentile(sads[0], pcs), pcs):
        plot.renderers.append(Span(location=percentile, dimension='width', line_width=2, line_alpha=0.4))
        plot.renderers.append(Label(y=percentile + 1, x=10, text=f'{pc}'))

    # plot.line(range(samples), np.var(X, axis=0), color='black', line_width=1, line_alpha=0.8)

    plot.width = 1800
    plot.height = 900
    show(plot)
