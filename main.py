import numpy as np


def pipeline():
    from sklearn.preprocessing import StandardScaler
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import Pipeline

    return Pipeline([
        ('pre', StandardScaler()),
        ('mod', MLPClassifier()),
    ])


def setup_online_capture():
    import chipwhisperer as cw

    from mlss.capture import create_capture, CaptureContext
    from mlss.entity import Trace

    ktp = cw.ktp.Basic()
    ktp.fixed_key = False
    ktp.fixed_text = True

    def capture(ctx: CaptureContext, n=10):
        with ctx.lock:
            text = ktp.next_text()
            keys = [ktp.next_key() for _ in range(n)]
        for key in keys:
            (wave, text, _, key) = cw.capture_trace(ctx.scope, ctx.target, text, key)
            yield Trace(key=key, wave=wave, text=text)

    return create_capture(capture, None)


def online():
    from sklearn.model_selection import train_test_split

    from mlss.aes_utils import train_and_score, load_from_disk
    from mlss.processing import create_masks, calculate_sads

    capturer = setup_online_capture()

    if input('Demo from disk?') == 'y':
        import random
        from mlss.aes_utils import load_from_disk, train_and_score
        all_traces = load_from_disk()
        random.shuffle(all_traces)
        all_traces = all_traces
        train = all_traces[:int(0.8 * len(all_traces))]
        check = all_traces[int(0.8 * len(all_traces)):]
        sads = calculate_sads(train)
        cached_masks = create_masks(sads)
        pipes = [pipeline() for _ in range(16)]
        res = train_and_score(
            *((i, pipes[i]) for i in range(16)),
            feature_masks=cached_masks,
            training_data=train,
            predict_data=check,
        )
        print(res)
        import time
        import chipwhisperer as cw
        with capturer:
            ktp = cw.ktp.Basic()
            ktp.fixed_key = False
            ktp.fixed_text = True
            while True:
                time.sleep(1)
                trace = cw.capture_trace(
                    capturer._threads[0]._ctx.scope,
                    capturer._threads[0]._ctx.target,
                    ktp.next_text(),
                    ktp.next_key()
                )
                p_key = [p.predict(
                    [[v for idx, v in enumerate(trace.wave) if idx in m.indices]]
                )[0] for p, k, m in zip(pipes, trace.key, cached_masks)]
                print(bytearray(p_key).hex(sep=' '))
                print(bytearray(trace.key).hex(sep=' '))
                print(*(1 if k == v else 0 for k, v in zip(trace.key, p_key)))

    n = int(input('N-Traces per epoch: '))
    pipes = [
        pipeline()
        for _ in range(16)
    ]

    for p in pipes:
        p['pre'].fit = p['pre'].partial_fit
        p['mod'].fit = p['mod'].partial_fit

    with capturer:

        warmup_data = []

        if input('Load warmup from disk?: ') == 'y':
            import random
            warmup_data.extend(random.choices(load_from_disk(), k=5000))

        if input('Collect larger warmup batch?: ') == 'y':
            capturer.start_next(n=int(input('N: ')))
            warmup_data.extend(capturer.wait())

        while True:
            capturer.start_next(n=n)
            warmup_data.extend(capturer.wait())
            cached_masks = create_masks(calculate_sads(warmup_data))
            min_features = min(map(lambda m: sum(m.boolean), cached_masks))
            max_features = max(map(lambda m: sum(m.boolean), cached_masks))
            if min_features > 0:
                if input(f'Detected feature range {min_features}-{max_features}, start?') == 'y':
                    break
        del warmup_data

        print('Warmed up, starting...')

        capturer.start_next(n=n)

        data = capturer.wait()
        capturer.start_next(n=n)
        train, test = train_test_split(data, train_size=0.8)
        scores = train_and_score(
            *enumerate(pipes),
            training_data=train,
            predict_data=test,
            show_print=False,
            feature_masks=cached_masks,
            mod__classes=[i for i in range(256)]
        )
        print(scores)
        print('Initialized model')

        while input('continue?') != 'n':
            data = capturer.wait()
            capturer.start_next(n=n)
            train, test = train_test_split(data, train_size=0.8)
            scores = train_and_score(
                *enumerate(pipes),
                training_data=train,
                predict_data=test,
                show_print=False,
                feature_masks=cached_masks,
            )
            trace = test[0]
            print(scores)
            print([k == p.predict(
                [[v for idx, v in enumerate(trace.wave) if idx in m.indices]]
            )[0] for p, k, m in zip(pipes, trace.key, cached_masks)])


def main():
    import random

    from mlss.aes_utils import load_from_disk, train_and_score
    all_traces = load_from_disk()

    nn_pipe = pipeline()

    cached_masks = None
    for rsp in np.arange(25, 101, 5):
        p = rsp / 100
        random.shuffle(all_traces)
        train = all_traces[:int(p * 0.8 * len(all_traces))]
        check = all_traces[int(p * 0.8 * len(all_traces)):]

        print(f'Samples: {len(train)}')
        print(f'Verify:  {len(check)}')

        if cached_masks is None:
            from mlss.processing import create_masks, calculate_sads
            sads = calculate_sads(train)
            cached_masks = create_masks(sads)

        train_and_score(
            *((i, nn_pipe) for i in range(16)),
            feature_masks=cached_masks,
            training_data=train,
            predict_data=check,
        )


if __name__ == '__main__':
    online()
