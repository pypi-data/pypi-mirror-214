from yt_subs_migrate.cli import Cli
from yt_subs_migrate.subscriptions import Subscriptions, Channel

import sys


def main():
    cli = Cli()

    subscriptions = Subscriptions(cli.args.client_secret)

    source_channel_list: list[Channel] = subscriptions.list_channels(
        cli.args.source_channel_id
    )
    dest_channel_list: list[Channel] = subscriptions.list_channels()

    delta_channel_list: list[Channel] = list(
        set(source_channel_list) - set(dest_channel_list)
    )

    if len(delta_channel_list) > 1:
        print("\nThere are %d channels to migrate." % (len(delta_channel_list)))
    elif len(delta_channel_list) == 1:
        print("\nThere is %d channels to migrate." % (len(delta_channel_list)))

    if not cli.args.test and len(delta_channel_list) > 0:
        subscriptions.insert_channels(delta_channel_list)


if __name__ == "__main__":
    sys.exit(main())
