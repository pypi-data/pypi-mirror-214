import os
import time
from typing import Any, Optional

import pytest
from attrs import define
from cog.server.eventtypes import (
    Done,
    Heartbeat,
    Log,
    PredictionOutput,
    PredictionOutputType,
)
from cog.server.exceptions import FatalWorkerException, InvalidStateException
from cog.server.worker import Worker
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.stateful import (
    RuleBasedStateMachine,
    precondition,
    rule,
)

# Set a longer deadline on CI as the instances are a bit slower.
settings.register_profile("ci", max_examples=100, deadline=1000)
settings.register_profile("default", max_examples=10, deadline=500)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))

ST_NAMES = st.sampled_from(["John", "Barry", "Elspeth", "Hamid", "Ronnie", "Yasmeen"])

SETUP_FATAL_FIXTURES = [
    ("exc_in_setup", {}),
    ("exc_in_setup_and_predict", {}),
    ("exc_on_import", {}),
    ("exit_in_setup", {}),
    ("exit_on_import", {}),
    ("missing_predictor", {}),
    ("nonexistent_file", {}),  # this fixture doesn't even exist
]

PREDICTION_FATAL_FIXTURES = [
    ("exit_in_predict", {}),
    ("killed_in_predict", {}),
]

RUNNABLE_FIXTURES = [
    ("simple", {}),
    ("exc_in_predict", {}),
    ("missing_predict", {}),
]

OUTPUT_FIXTURES = [
    (
        "hello_world",
        {"name": ST_NAMES},
        lambda x: f"hello, {x['name']}",
    ),
    (
        "count_up",
        {"upto": st.integers(min_value=0, max_value=100)},
        lambda x: list(range(x["upto"])),
    ),
    ("complex_output", {}, lambda _: {"number": 42, "text": "meaning of life"}),
]

SETUP_LOGS_FIXTURES = [
    (
        "logging",
        (
            "writing some stuff from C at import time\n"
            "writing to stdout at import time\n"
            "setting up predictor\n"
        ),
        "writing to stderr at import time\n",
    )
]

PREDICT_LOGS_FIXTURES = [
    (
        "logging",
        {},
        ("writing from C\n" "writing with print\n"),
        ("WARNING:root:writing log message\n" "writing to stderr\n"),
    )
]


@define
class Result:
    stdout: str = ""
    stderr: str = ""
    heartbeat_count: int = 0
    output_type: Optional[PredictionOutputType] = None
    output: Any = None
    done: Optional[Done] = None
    exception: Optional[Exception] = None


def _process(events, swallow_exceptions=False):
    """
    Helper function to collect events generated by Worker during tests.
    """
    result = Result()
    stdout = []
    stderr = []

    try:
        for event in events:
            if isinstance(event, Log) and event.source == "stdout":
                stdout.append(event.message)
            elif isinstance(event, Log) and event.source == "stderr":
                stderr.append(event.message)
            elif isinstance(event, Heartbeat):
                result.heartbeat_count += 1
            elif isinstance(event, Done):
                assert not result.done
                result.done = event
            elif isinstance(event, PredictionOutput):
                assert result.output_type, "Should get output type before any output"
                if result.output_type.multi:
                    result.output.append(event.payload)
                else:
                    assert (
                        result.output is None
                    ), "Should not get multiple outputs for output type single"
                    result.output = event.payload
            elif isinstance(event, PredictionOutputType):
                assert (
                    result.output_type is None
                ), "Should not get multiple output type events"
                result.output_type = event
                if result.output_type.multi:
                    result.output = []
            else:
                pytest.fail(f"saw unexpected event: {event}")
    except Exception as exc:
        result.exception = exc
        if not swallow_exceptions:
            raise
    result.stdout = "".join(stdout)
    result.stderr = "".join(stderr)
    return result


def _fixture_path(name):
    test_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(test_dir, f"fixtures/{name}.py") + ":Predictor"


@pytest.mark.parametrize("name,payloads", SETUP_FATAL_FIXTURES)
def test_fatalworkerexception_from_setup_failures(name, payloads):
    """
    Any failure during setup is fatal and should raise FatalWorkerException.
    """
    w = Worker(predictor_ref=_fixture_path(name), tee_output=False)

    with pytest.raises(FatalWorkerException):
        _process(w.setup())

    w.terminate()


@pytest.mark.parametrize("name,payloads", PREDICTION_FATAL_FIXTURES)
@given(data=st.data())
def test_fatalworkerexception_from_irrecoverable_failures(data, name, payloads):
    """
    Certain kinds of failure during predict (crashes, unexpected exits) are
    irrecoverable and should raise FatalWorkerException.
    """
    w = Worker(predictor_ref=_fixture_path(name), tee_output=False)

    result = _process(w.setup())
    assert not result.done.error

    with pytest.raises(FatalWorkerException):
        for _ in range(5):
            payload = data.draw(st.fixed_dictionaries(payloads))
            _process(w.predict(payload))

    w.terminate()


@pytest.mark.parametrize("name,payloads", RUNNABLE_FIXTURES)
@given(data=st.data())
def test_no_exceptions_from_recoverable_failures(data, name, payloads):
    """
    Well-behaved predictors, or those that only throw exceptions, should not
    raise.
    """
    w = Worker(predictor_ref=_fixture_path(name), tee_output=False)

    try:
        result = _process(w.setup())
        assert not result.done.error

        for _ in range(5):
            payload = data.draw(st.fixed_dictionaries(payloads))
            _process(w.predict(payload))
    finally:
        w.terminate()


@pytest.mark.parametrize("name,payloads,output_generator", OUTPUT_FIXTURES)
@given(data=st.data())
def test_output(data, name, payloads, output_generator):
    """
    We should get the outputs we expect from predictors that generate output.

    Note that most of the validation work here is actually done in _process.
    """
    w = Worker(predictor_ref=_fixture_path(name), tee_output=False)

    try:
        result = _process(w.setup())
        assert not result.done.error

        payload = data.draw(st.fixed_dictionaries(payloads))
        expected_output = output_generator(payload)

        result = _process(w.predict(payload))

        assert result.output == expected_output
    finally:
        w.terminate()


@pytest.mark.parametrize("name,expected_stdout,expected_stderr", SETUP_LOGS_FIXTURES)
def test_setup_logging(name, expected_stdout, expected_stderr):
    """
    We should get the logs we expect from predictors that generate logs during
    setup.
    """
    w = Worker(predictor_ref=_fixture_path(name), tee_output=False)

    try:
        result = _process(w.setup())
        assert not result.done.error

        assert result.stdout == expected_stdout
        assert result.stderr == expected_stderr
    finally:
        w.terminate()


@pytest.mark.parametrize(
    "name,payloads,expected_stdout,expected_stderr", PREDICT_LOGS_FIXTURES
)
def test_predict_logging(name, payloads, expected_stdout, expected_stderr):
    """
    We should get the logs we expect from predictors that generate logs during
    predict.
    """
    w = Worker(predictor_ref=_fixture_path(name), tee_output=False)

    try:
        result = _process(w.setup())
        assert not result.done.error

        result = _process(w.predict({}))

        assert result.stdout == expected_stdout
        assert result.stderr == expected_stderr
    finally:
        w.terminate()


def test_cancel_is_safe():
    """
    Calls to cancel at any time should not result in unexpected things
    happening or the cancelation of unexpected predictions.
    """

    w = Worker(predictor_ref=_fixture_path("sleep"), tee_output=True)

    try:
        for _ in range(50):
            w.cancel()

        _process(w.setup())

        for _ in range(50):
            w.cancel()

        result1 = _process(w.predict({"sleep": 0.5}), swallow_exceptions=True)

        for _ in range(50):
            w.cancel()

        result2 = _process(w.predict({"sleep": 0.1}), swallow_exceptions=True)

        assert not result1.exception
        assert not result1.done.canceled
        assert not result2.exception
        assert not result2.done.canceled
        assert result2.output == "done in 0.1 seconds"
    finally:
        w.terminate()


def test_cancel_idempotency():
    """
    Multiple calls to cancel within the same prediction, while not necessary or
    recommended, should still only result in a single cancelled prediction, and
    should not affect subsequent predictions.
    """
    w = Worker(predictor_ref=_fixture_path("sleep"), tee_output=True)

    try:
        _process(w.setup())

        p1_done = None

        for event in w.predict({"sleep": 0.5}, poll=0.01):
            # We call cancel a WHOLE BUNCH to make sure that we don't propagate
            # any of those cancelations to subsequent predictions, regardless
            # of the internal implementation of exceptions raised inside signal
            # handlers.
            for _ in range(100):
                w.cancel()

            if isinstance(event, Done):
                p1_done = event

        assert p1_done.canceled

        result2 = _process(w.predict({"sleep": 0.1}))

        assert not result2.done.canceled
        assert result2.output == "done in 0.1 seconds"
    finally:
        w.terminate()


def test_cancel_multiple_predictions():
    """
    Multiple predictions cancelled in a row shouldn't be a problem. This test
    is mainly ensuring that the _allow_cancel latch in Worker is correctly
    reset every time a prediction starts.
    """

    w = Worker(predictor_ref=_fixture_path("sleep"), tee_output=True)

    try:
        _process(w.setup())

        dones = []

        for _ in range(5):
            canceled = False

            for event in w.predict({"sleep": 0.5}, poll=0.01):
                if not canceled:
                    w.cancel()
                    canceled = True

                if isinstance(event, Done):
                    dones.append(event)

        assert len(dones) == 5
        assert all([d == Done(canceled=True) for d in dones])
    finally:
        w.terminate()


def test_heartbeats():
    """
    Passing the `poll` keyword argument to predict should result in regular
    heartbeat events which allow the caller to do other stuff while waiting on
    completion.
    """
    w = Worker(predictor_ref=_fixture_path("sleep"), tee_output=False)

    try:
        _process(w.setup())

        result = _process(w.predict({"sleep": 0.5}, poll=0.1))

        assert result.heartbeat_count > 0
    finally:
        w.terminate()


def test_heartbeats_cancel():
    """
    Heartbeats should happen even when we cancel the prediction.
    """

    w = Worker(predictor_ref=_fixture_path("sleep"), tee_output=False)

    try:
        _process(w.setup())

        heartbeat_count = 0
        start = time.time()

        canceled = False
        for event in w.predict({"sleep": 10}, poll=0.1):
            if isinstance(event, Heartbeat):
                heartbeat_count += 1
            if time.time() - start > 0.5:
                if not canceled:
                    w.cancel()
                    canceled = True

        elapsed = time.time() - start

        assert elapsed < 2
        assert heartbeat_count > 0
    finally:
        w.terminate()


def test_graceful_shutdown():
    """
    On shutdown, the worker should finish running the current prediction, and
    then exit.
    """

    w = Worker(predictor_ref=_fixture_path("sleep"), tee_output=False)

    try:
        _process(w.setup())

        events = w.predict({"sleep": 1}, poll=0.1)

        # get one event to make sure we've started the prediction
        assert isinstance(next(events), Heartbeat)

        w.shutdown()

        result = _process(events)

        assert result.output == "done in 1 seconds"
    finally:
        w.terminate()


class WorkerState(RuleBasedStateMachine):
    """
    This is a Hypothesis-driven rule-based state machine test. It is intended
    to ensure that any sequence of calls to the public API of Worker leaves the
    instance in an expected state.

    In short: any call should either throw InvalidStateException or should do
    what the caller asked.

    See https://hypothesis.readthedocs.io/en/latest/stateful.html for more on
    stateful testing with Hypothesis.
    """

    def __init__(self):
        super().__init__()
        self.worker = Worker(_fixture_path("steps"), tee_output=False)

        self.setup_generator = None
        self.setup_events = []

        self.predict_generator = None
        self.predict_events = []
        self.predict_payload = None

    @rule(sleep=st.floats(min_value=0, max_value=0.5))
    def wait(self, sleep):
        time.sleep(sleep)

    @rule()
    def setup(self):
        try:
            self.setup_generator = self.worker.setup()
            self.setup_events = []
        except InvalidStateException:
            pass

    @precondition(lambda x: x.setup_generator)
    @rule(n=st.integers(min_value=1, max_value=10))
    def read_setup_events(self, n):
        try:
            for _ in range(n):
                event = next(self.setup_generator)
                self.setup_events.append(event)
        except StopIteration:
            self.setup_generator = None

            self._check_setup_events()

    def _check_setup_events(self):
        assert isinstance(self.setup_events[-1], Done)

        print(self.setup_events)
        result = _process(self.setup_events)
        assert result.stdout == "did setup\n"
        assert result.stderr == ""
        assert result.done == Done()

    @rule(name=ST_NAMES, steps=st.integers(min_value=0, max_value=10))
    def predict(self, name, steps):
        try:
            payload = {"name": name, "steps": steps}
            self.predict_generator = self.worker.predict(payload)
            self.predict_payload = payload
            self.predict_events = []
        except InvalidStateException:
            pass

    @precondition(lambda x: x.predict_generator)
    @rule(n=st.integers(min_value=1, max_value=10))
    def read_predict_events(self, n):
        try:
            for _ in range(n):
                event = next(self.predict_generator)
                self.predict_events.append(event)
        except StopIteration:
            self.predict_generator = None
            self._check_predict_events()

    def _check_predict_events(self):
        assert isinstance(self.predict_events[-1], Done)

        payload = self.predict_payload
        print(self.predict_events)
        result = _process(self.predict_events)

        expected_stdout = ["START\n"]
        for i in range(payload["steps"]):
            expected_stdout.append(f"STEP {i+1}\n")
        expected_stdout.append("END\n")

        assert result.stdout == "".join(expected_stdout)
        assert result.stderr == ""
        assert result.output == f"NAME={payload['name']}"
        assert result.done == Done()

    # @rule(r=consumes(predict_result))
    def cancel(self, r):
        if isinstance(r, InvalidStateException):
            return

        self.worker.cancel()
        result = _process(r)

        # We'd love to be able to assert result.done.canceled here, but we
        # simply can't guarantee that we canceled the worker in time. Perhaps
        # in future we can guarantee this with a slower fixture.
        assert result.done

    def teardown(self):
        self.worker.shutdown()
        # cheat a bit to make sure we drain the events pipe
        list(self.worker._wait())
        # really make sure everything is shut down and cleaned up
        self.worker.terminate()


TestWorkerState = WorkerState.TestCase
