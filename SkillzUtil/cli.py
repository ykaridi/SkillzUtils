from SkillzUtil import batch_pvp
import argparse
import random
import subargparse
import SkillzUtil.config as configuration

subparsers = subargparse.subparser_decorator()


@subparsers("run-games")
def sample(parser):
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


@subparsers()
def config(parser):
    def action(args):
        configuration.append_to_config("user", args.user)
        configuration.append_to_config("password", args.password)
        configuration.append_to_config("connection_type", args.connection_type)
        configuration.append_to_config("tournament_number", args.tournament)
        configuration.append_to_config("headless", args.headless)
        configuration.append_to_config("authenticate", True)

    parser.add_argument("user", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("tournament", type=int,
                        help="The index of the tournament in your current tournaments list")
    parser.add_argument("-type", "--connection_type", choices=['idm', 'local'], default='idm', required=True)
    parser.add_argument("-hl", "--headless", dest="headless", action='store_const',
                        const=True, default=False, help="Run chrome in headless mode when possible")
    return action


@subparsers()
def purge(parser):
    def action(args):
        configuration.write_to_config({})

    return action


def main():
    parser = argparse.ArgumentParser(prog='SkillzUtil')
    subparsers.bind(parser)
    args = parser.parse_args()
    parser.handle(args)
