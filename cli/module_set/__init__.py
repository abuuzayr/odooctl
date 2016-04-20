from gronexctl.cli import Base

class ModuleSet(Base):

    def __init__(self, parser):
        from argparse import REMAINDER

        super(self.__class__, self).__init__('module-set', parser)

        self.parser.add_argument(
                'arguments', nargs=REMAINDER, help='module-set arguments')


    def dispatch(self, parsed_args, raw_args):
        from argparse import ArgumentParser
        from os import path
        from sys import argv

        from gronexctl.cli.module_set import (
            install,
            resolve
        )

        argv0 = path.split(argv[0])[-1]
        p = ArgumentParser(prog='{0} module-set'.format(argv0))
        sp = p.add_subparsers(title='module-set commands', dest='command')

        install.parser_init(sp)
        resolve.parser_init(sp)

        parsed = p.parse_args(parsed_args.arguments)
        parsed.func(parsed, raw_args)


def parser_init(parser):
    return ModuleSet(parser)
