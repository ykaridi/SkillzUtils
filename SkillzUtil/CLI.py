from SkillzUtil import BatchPVP
import argparse
import random


def main():
    def create_parser():
        def define_run_games(parser):
            def define_sample(parser):
                def sample_action(args):
                    args.sample_size = getattr(args, "sample-size")

                    def get_selector():
                        if args.selector == 'top':
                            return lambda arr: arr[:args.sample_size]
                        elif args.selector == 'random':
                            return lambda arr: random.sample(arr, args.sample_size)
                    BatchPVP.run(args.log, get_selector())

                parser.add_argument('sample-size', type=int, help='The number of rounds to sample')
                parser.add_argument('--selector', choices=['random', 'top'], default='random')
                parser.add_argument('--log', type=str, required=True)
                parser.set_defaults(func=sample_action)
            subparsers = parser.add_subparsers()
            define_sample(subparsers.add_parser('sample'))

        parser = argparse.ArgumentParser(prog='CLI.py')
        subparsers = parser.add_subparsers(title='subcommands',
                                           description='valid subcommands')
        define_run_games(subparsers.add_parser('run-games'))
        return parser

    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
