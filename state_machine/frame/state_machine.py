import tasko

from StateMachineConfig import config, TaskMap, TransitionFunctionMap


def typecheck_props(state_name, task_name, props):
    # pylint: disable=unidiomatic-typecheck
    # using isinstance makes bools be considered ints.
    if type(props['Interval']) == int:
        props['Interval'] = float(props['Interval'])
    if type(props['Interval']) != float:
        raise ValueError(
            f'{state_name}->{task_name}->Interval should be int or float not {type(props["Interval"])}')

    if type(props['Priority']) == int:
        props['Priority'] = float(props['Interval'])
    if type(props['Priority']) != float:
        raise ValueError(
            f'{state_name}->{task_name}->Priority should be int or float not {type(props["Priority"])}')

    if type(props['ScheduleLater']) != bool:
        raise ValueError(
            f'{state_name}->{task_name}->ScheduleLater should be bool not {type(props["ScheduleLater"])}')


def validate_config(config):
    """Validates that the config file is well formed"""
    for state_name, state in config.items():
        for task_name, props in state['Tasks'].items():
            if task_name not in TaskMap:
                raise ValueError(
                    f'{task_name} defined in the {state_name} state, but {task_name} is not defined')
            if 'Interval' not in props:
                raise ValueError(f'Interval value not defined in {state_name}')
            if 'Priority' not in props:
                raise ValueError(f'Priority value not defined in {state_name}')
            if 'ScheduleLater' not in props:
                props['ScheduleLater'] = False  # default to false
            typecheck_props(state_name, task_name, props)
        if 'StepsTo' not in state:
            raise ValueError(
                f'The state {state_name} does not have StepsTo defined')
        if not isinstance(state['StepsTo'], list):
            raise ValueError(
                f'{state_name}->StepsTo should be bool list not {type(state["StepsTo"])}')
        for item in state['StepsTo']:
            if not isinstance(item, str):
                raise ValueError(
                    f'{state_name}->StepsTo should be bool list, but it contains an element of the wrong type')
            if item not in config:
                raise ValueError(
                    f'{state_name}->StepsTo defines a transition to {item} but {item} state is not defined'
                )
        if 'EnterFunctions' not in state:
            state['EnterFunctions'] = []
        prop = state['EnterFunctions']
        if not isinstance(prop, list):
            raise ValueError(f'{state_name}->EnterFunctions should be an array not {type(prop)}')

        if 'ExitFunctions' not in state:
            state['ExitFunctions'] = []
        prop = state['ExitFunctions']
        if not isinstance(prop, list):
            raise ValueError(f'{state_name}->EnterFunctions should be an array not {type(prop)}')
        valid_keys = {'Tasks', 'StepsTo', 'EnterFunctions', 'ExitFunctions'}
        for key in state.keys():
            if key not in valid_keys:
                raise ValueError(f'{state_name}->{key} should not be defined, choose one of {valid_keys}')


class StateMachine:
    """Singleton State Machine Class"""

    def __init__(self, cubesat, start_state):
        self.config = config
        validate_config(config)

        self.state = start_state

        # allow access to cubesat object
        self.cubesat = cubesat

        # create shared asyncio object
        self.tasko = tasko

        # supports legacy code, only the state machine should use tasko
        cubesat.tasko = tasko

        # init task objects
        self.tasks = {key: task(cubesat) for key, task in TaskMap.items()}

        # set scheduled tasks to none
        self.scheduled_tasks = {}

        # Make state machine accesible to cubesat
        cubesat.state_machine = self

        # switch to start state, and start event loop
        self.switch_to(start_state, force=True)
        self.tasko.run()

    def stop_all(self):
        """Stops all running tasko processes"""
        for _, task in self.scheduled_tasks.items():
            task.stop()

    def switch_to(self, state_name, force=False):
        """Switches the state of the cubesat to the new state"""

        # prevent (or force) illegal transitions
        if not(state_name in self.config[self.state]['StepsTo'] or force):
            raise ValueError(
                f'You cannot transition from {self.state} to {state_name}')

        # execute transition functions
        for fn in config[self.state]['ExitFunctions']:
            print('fn', fn)
            fn = TransitionFunctionMap[fn]
            fn(self.state, state_name, self.cubesat)
        for fn in config[state_name]['EnterFunctions']:
            fn = TransitionFunctionMap[fn]
            fn(self.state, state_name, self.cubesat)

        # reschedule tasks
        self.stop_all()
        self.scheduled_tasks = {}
        self.state = state_name
        state_config = self.config[state_name]

        for task_name, props in state_config['Tasks'].items():
            if props['ScheduleLater']:
                schedule = self.tasko.schedule_later
            else:
                schedule = self.tasko.schedule

            frequency = 1 / props['Interval']
            priority = props['Priority']
            task_fn = self.tasks[task_name].main_task

            self.scheduled_tasks[task_name] = schedule(
                frequency, task_fn, priority)