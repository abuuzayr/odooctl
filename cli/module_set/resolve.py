from __future__ import print_function

from gronexctl.cli import Base

class Resolve(Base):

    def __init__(self, parser):
        from os import getcwd
        from os import path

        super(self.__class__, self).__init__('resolve', parser)
        self.parser.add_argument(
            '-d', '--directory',
            default=path.join(getcwd(), 'sets'),
        )
        self.parser.add_argument('yml')

    def dispatch(self, parsed_args, raw_args):
        from os import path

        from gronexctl.module_set import ModuleSet

        ms = ModuleSet(
            path.join(
                parsed_args.directory,
                "{0}.yml".format(parsed_args.yml),
            )
        )
        ms.resolve()

        print('Dependencies:')
        print(ms.absolute_dependencies)
        print()
        print('Addon Dependencies:')
        for l in ms.absolute_addon_dependencies:
            print(l)


def parser_init(parser):
    return Resolve(parser)
