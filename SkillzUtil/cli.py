from SkillzUtil import batch_pvp
import argparse
import random
from SkillzUtil.util import *
import subargparse

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
    parser = argparse.ArgumentParser(prog='SkillzUtil')
    subparsers.bind(parser)
    args = parser.parse_args()
    parser.handle(args)
