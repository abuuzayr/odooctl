def main(args=None):
    from argparse import ArgumentParser
    from sys import argv

    from gronexctl.cli import module_set

    if args is None:
        args = argv[1:]

    p = ArgumentParser()
    sp = p.add_subparsers(title='Commands', dest='command')

    module_set.parser_init(sp)
    parsed = p.parse_args(args)

    return parsed.func(parsed, args)

def run_main(args=None):
    try:
        return main(args)
    except KeyboardInterrupt:
        print()
        pass

if __name__ == '__main__':
    from sys import exit
    exit(run_main())
