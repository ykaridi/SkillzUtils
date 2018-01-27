from SkillzUtil import batch_pvp
import argparse
import random
import SkillzUtil.config as config


def make_registrar():
    registry = {}

    def get_entry(d, *path):
        if isinstance(path[0], list) or isinstance(path[0], tuple):
            path = path[0]
        entry = d
        for k in path:
            if k in entry:
                entry = entry[k]
            else:
                return None
        return entry

    def set_entry(d, v, *path):
        if isinstance(path[0], list) or isinstance(path[0], tuple):
            path = path[0]
        entry = d
        for k in path[:-1]:
            if k in entry:
                entry = entry[k]
            else:
                entry[k] = {}
                entry = entry[k]
        entry[path[-1]] = v

    def registrar(*path):
        def wrapper(func):
            set_entry(registry, func, path)
            return func     # normally a decorator returns a wrapped function,
                            # but here we return func unmodified, after registering it
        return wrapper
    registrar.all = registry
    return registrar


subparsers = make_registrar()


@subparsers("run-games", "sample")
def run_games_sample(parser):
    def action(args):
        args.sample_size = getattr(args, "sample-size")

        def get_selector():
            if args.selector == 'top':
                return lambda arr: arr[:args.sample_size]
            elif args.selector == 'random':
                return lambda arr: random.sample(arr, args.sample_size)

        batch_pvp.run(args.log, get_selector())
    parser.add_argument('sample-size', type=int, help='The number of rounds to sample')
    parser.add_argument('--selector', choices=['random', 'top'], default='random')
    parser.add_argument('--log', type=str, required=True, help="Log file path")
    return action


@subparsers("config")
def config(parser):
    def action(args):
        config.append_to_config("email", args.email)
        config.append_to_config("passwrd", args.password)
        config.append_to_config("tournament_number", args.tournament)
        config.append_to_config("headless", args.headless)

    parser.add_argument("email", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("tournament", type=int,
                        help="The index of the tournament in your current tournaments list")
    parser.add_argument("-hf", "--headless", dest="headless", action='store_const',
                        const=True, default=False, help="Run chrome in headless mode when possible")
    return action


def main():
    def configure_help(parser, path):
        parser.set_defaults(func=lambda x: parser.parse_args(reversed(path + ["-h"])))

    def configure_parser(d, parser, path):
        configure_help(parser, path)
        sps = parser.add_subparsers(title='subcommands',
                              description='valid subcommands')
        for k,v in d.items():
            if isinstance(v, dict):
                lp = sps.add_parser(k)
                configure_parser(v, lp, path + [k])
            else:
                lp = sps.add_parser(k)
                action = v(lp)
                lp.set_defaults(func=action)
    parser = argparse.ArgumentParser(prog='SkillzUtil')
    configure_parser(subparsers.all, parser, ["SkillzUtil"])
    args = parser.parse_args()
    args.func(args)
