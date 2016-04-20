class Base(object):

    def __init__(self, command, parser):
        self.parser = parser.add_parser(command)

        def make_func(o):
            def f(parsed_args, raw_args):
                o.dispatch(parsed_args, raw_args)
            return f

        self.parser.set_defaults(func=make_func(self))


    def dispatch(self, parsed_args, raw_args):
        pass
