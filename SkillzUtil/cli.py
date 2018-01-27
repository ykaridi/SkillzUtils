from SkillzUtil import batch_pvp
import argparse
import random
import SkillzUtil.config as config


def configure_help(parser):
    parser.set_defaults(func=lambda x: parser.parse_args(["-h"]))


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
                    batch_pvp.run(args.log, get_selector())

                parser.add_argument('sample-size', type=int, help='The number of rounds to sample')
                parser.add_argument('--selector', choices=['random', 'top'], default='random')
                parser.add_argument('--log', type=str, required=True, help="Log file path")
                parser.set_defaults(func=sample_action)
            subparsers = parser.add_subparsers(title='subcommands',
                                           description='valid subcommands')
            define_sample(subparsers.add_parser('sample'))
            configure_help(parser)

        def define_config(parser):
            def config_action(args):
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
            parser.set_defaults(func=config_action)

        parser = argparse.ArgumentParser(prog='SkillzUtil.py')
        subparsers = parser.add_subparsers(title='subcommands',
                                           description='valid subcommands')

        define_run_games(subparsers.add_parser('run-games'))
        define_config(subparsers.add_parser('config'))
        configure_help(parser)
        return parser

    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
