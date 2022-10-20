from collections import deque
from dataclasses import dataclass
from threading import Thread, Barrier, Event, RLock, BrokenBarrierError
from typing import Set, Callable, Any, List, Generic, TypeVar, Generator, Optional

import chipwhisperer as cw


@dataclass(frozen=True)
class CaptureContext:
    lock: RLock
    scope: cw.scopes.OpenADC
    target: cw.targets.SimpleSerial


class ChipWhispererThread(Thread):
    serial_number: Optional[str]
    trace_queue: deque

    scope: cw.scopes.OpenADC
    target: cw.targets.SimpleSerial

    _grl: RLock
    _running: Event
    _epoch_barrier_start: Barrier
    _epoch_barrier_end: Barrier
    _capture: Any

    def __init__(self, sn: Optional[str], queue: deque):
        """Thread for handling operations using ChipWhisperer

        :param sn: Serial number of the CW device
        """
        super(ChipWhispererThread, self).__init__(name=f'cw-capture-{sn}', daemon=True)
        self.serial_number = sn
        self.trace_queue = queue

    def __enter__(self):
        self.scope = cw.scope(
            sn=self.serial_number,
            scope_type=cw.scopes.OpenADC,
        )
        print(self.scope.sn)
        self.scope.default_setup()
        self.target = cw.target(
            self.scope,
            target_type=cw.targets.SimpleSerial,
        )
        self._ctx = CaptureContext(scope=self.scope, target=self.target, lock=self._grl)
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        exceptions = []
        try:
            self.scope.dis()
        except Exception as e:
            exceptions.append(e)
        try:
            self.target.dis()
        except Exception as e:
            exceptions.append(e)
        if len(exceptions) != 0:
            raise ValueError(
                'Failed to release ChipWhisperer resources',
                exceptions
            )

    def run(self) -> None:
        try:
            self._epoch_barrier_end.wait()
            while self._running.is_set():
                self._epoch_barrier_start.wait()
                if not self._running.is_set():
                    break
                for value in self._capture(self._ctx):
                    self.trace_queue.append(value)
                self._epoch_barrier_end.wait()
        except BrokenBarrierError:
            pass


T = TypeVar('T')


class CaptureHelper(Generic[T]):

    def __init__(self, devices, func):
        self._queue = deque()
        self._devices = [d for d in devices] if devices is not None else []
        self._func = func
        self._lock = RLock()
        self._start = Barrier(parties=max((len(self._devices) + 1, 2)))
        self._end = Barrier(parties=max((len(self._devices) + 1, 2)))

    def start_next(self, **kwargs) -> None:
        from functools import partial
        round_function = partial(self._func, **kwargs)
        for t in self._threads:
            t._capture = round_function
        self._start.wait()
        self._start.reset()

    def wait(self) -> List[T]:
        self._end.wait()
        self._end.reset()
        for t in self._threads:
            if hasattr(t, '_capture'):
                del t._capture
        out = [o for o in self._queue]
        self._queue.clear()
        return out

    def __enter__(self):
        self._running = Event()
        self._running.set()

        if len(self._devices) == 0:
            self._threads = [ChipWhispererThread(None, self._queue)]
        else:
            self._threads = [ChipWhispererThread(d, self._queue) for d in self._devices]

        from contextlib import ExitStack
        self._stack = ExitStack()

        for t in self._threads:
            from time import sleep
            t._epoch_barrier_start = self._start
            t._epoch_barrier_end = self._end
            t._running = self._running
            t._grl = self._lock
            self._stack.enter_context(t)
            sleep(0.5)

        self.wait()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._running.clear()
        self._start.abort()
        self._stack.close()
        del self._threads
        del self._stack


def create_capture(
        func: Callable[[CaptureContext, ...], Generator[T, None, None]],
        devices: Optional[Set[str]],
) -> CaptureHelper[T]:
    return CaptureHelper(devices, func)
