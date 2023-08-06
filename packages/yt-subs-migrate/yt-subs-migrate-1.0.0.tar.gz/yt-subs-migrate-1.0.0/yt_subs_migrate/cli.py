import argparse
import pathlib


class Cli:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="yt-subs-migrate",
            description="Migrate YouTube subscriptions from one account to another",
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=True,
        )

        self.parser.add_argument(
            "-s",
            "--source-channel-id",
            type=str,
            required=True,
            help="source channel's ID",
        )

        self.parser.add_argument(
            "-c",
            "--client-secret",
            type=pathlib.Path,
            required=True,
            help="client secret of destination account",
        )

        self.parser.add_argument(
            "-T",
            "--test",
            type=bool,
            default=False,
            help="only fetch information, don't migrate",
        )

        self.args = self.parser.parse_args()
