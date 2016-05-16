from gronexctl.cli import Base


class Install(Base):

    def __init__(self, parser):
        from os import getcwd
        from os import path

        super(self.__class__, self).__init__('install', parser)
        self.parser.add_argument(
            '-d', '--directory',
            default=path.join(getcwd(), 'sets'),
        )
        self.parser.add_argument(
            '-D', '--database',
            default='odoo',
        )
        self.parser.add_argument(
            '-H', '--host-string',
            required=True,
        )
        self.parser.add_argument(
            '-u', '--username',
            default='admin',
        )
        self.parser.add_argument('yml', nargs='+')


    def dispatch(self, parsed_args, raw_args):
        from os import path
        from getpass import getpass

        from erppeek import Client

        from gronexctl.module_set import ModuleSet

        password = getpass()

        for yml in parsed_args.yml:
            client = Client(
                parsed_args.host_string,
                db=parsed_args.database,
                user=parsed_args.username,
                password=password,
            )

            ms = ModuleSet(
                path.join(
                    parsed_args.directory,
                    "{0}.yml".format(yml),
                )
            )

            ms.resolve()

            for l in ms.absolute_addon_dependencies:
                client.install(*l)



def parser_init(parser):
    return Install(parser)
