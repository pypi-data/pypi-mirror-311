from a1_loggermanager import default_console_logger as logger
from argparse import ArgumentParser, Namespace
import sys

class MyArgparse(ArgumentParser):

    args: Namespace

    def add_args(self, args_config):
        for k, v in args_config.items(): 
            self.add_argument(k, **v)

    def parse_args(self):
        try:
            self.args = super().parse_args()
            logger.info(f"parse_args::self.args: {self.args}")
        except:
            print(f'parser error')
            sys.exit(1)



def main() -> None: 
    logger.debug('main()')

    mc = MainClass()
    mc.parse_args()
    mc.set_args()
 
def func1(str):
    logger.info(f"func1(); str: {str}")

def func2(str):
    logger.info(f"func2(); str: {str}")


class MainClass():

    ap : MyArgparse
    args_config = {
        'pos1': {'help': 'Help for pos1',},
        '--flag1': {'help': 'Help for flag1',},
        '--flag2': {
            'action': 'store_true', 
            'help': 'Help for flag2; (action = store_true)'},
        '--flag3': {'help': 'Help for flag3',},
        '--logging_level': {
            'help': 'Set logging level (DEBUG|INFO|WARNING|ERROR|CRITICAL)',
            'choices': ['debug', 'info', 'warning', 'error', 'critical'],
            'type': str.lower },
        '--command1': {'help': 'Help for command1',},
        '--attr1': {'help': 'Help for attr1',}
    }

    def __init__(self):
        logger.debug('MainClass.__init__()')


    def parse_args(self):
        self.ap = MyArgparse(add_help=True)
        self.ap.add_args(self.args_config)
        self.ap.parse_args()

    def set_args(self):
        # set logger level if req'd
        if (self.ap.args.logging_level is not None): 
            try:
                logging_level = self.ap.args.logging_level.upper()
                logger.setLevel(logging_level)
                logger.info(f"Logging level set to {logging_level}")
            except:
                logger.error(f"Invalid logging-level: {logging_level}")
        if (self.ap.args.command1 is not None):
            command1 = self.ap.args.command1
        if (self.ap.args.attr1 is not None):
            attr1 = self.ap.args.attr1
        if command1 == 'func1':
            func1(attr1)
        elif command1 == 'func2':
            func2(attr1)


