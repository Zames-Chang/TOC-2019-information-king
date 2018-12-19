from fsm import TocMachine

def build_fsm(id):
    machine = TocMachine(
        states=[
            'init',
            'point0',
            'point1',
            'point2',
            'point3',
            'final'
        ],
        transitions=[
            {
                'trigger': 'start',
                'source': 'init',
                'dest': 'point0',
            },
            {
                'trigger': 'end',
                'source': [
                    'init',
                    'point0',
                    'point1',
                    'point2',
                    'point3'
                ],
                'dest': 'init',
            },
            {
                'trigger': 'move',
                'source': 'point0',
                'dest': 'point1',
            },
            {
                'trigger': 'move',
                'source': 'point1',
                'dest': 'point2',
            },
            {
                'trigger': 'move',
                'source': 'point2',
                'dest': 'point3',
            },
            {
                'trigger': 'move',
                'source': 'point3',
                'dest': 'final',
            },
            {
                'trigger': 'back',
                'source': [
                    'point0',
                    'point1',
                    'point2',
                    'point3',
                    'final'
                ],
                'dest': 'init'
            }
        ],
        initial='init',
        auto_transitions=False,
        show_conditions=True,
    )
    machine.id = id
    return machine