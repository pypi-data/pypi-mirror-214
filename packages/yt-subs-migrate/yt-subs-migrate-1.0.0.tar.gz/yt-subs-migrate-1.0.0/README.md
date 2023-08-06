YouTube Subscriptions Migration is a Python program that allow user to migrate their channel subscriptions from one account to another.

## Dependencies.

* google-auth-oauthlib>=1.0.0
* google-api-python-client>=2.89.0
* tqdm

## Usage.

### Command line arguments.

```
usage: yt-subs-migrate [-h] -s SOURCE_CHANNEL_ID -c CLIENT_SECRET [-T TEST]

Migrate YouTube subscriptions from one account to another

options:
  -h, --help            show this help message and exit
  -s SOURCE_CHANNEL_ID, --source-channel-id SOURCE_CHANNEL_ID
                        source channel's ID
  -c CLIENT_SECRET, --client-secret CLIENT_SECRET
                        client secret of destination account
  -T TEST, --test TEST  only fetch information, don't migrate
```

### Run instruction.

1. Setting up OAuth2 and get client secret. You can choose any Google account.
   * Go to [Google Cloud API Credentials](https://console.cloud.google.com/apis/credentials). Create a OAuth client ID with type as a Desktop client. Download the client secret JSON file and.
   * Go to [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) and create one.
      * The scopes must contain:
         * `/auth/userinfo.email`
         * `/auth/userinfo.profile`
         * `/auth/youtube.readonly`
         * `/auth/youtube`
         * `/auth/youtube.force-ssl`
      * You can publish the screen and wait for Google verification. Or add the email of of your destination account as test user so that you don't have to wait (even if the screen is on the same account as the destiantion account).
2. Run the program. You need to supply the source YouTube channel ID and the path to the client secret JSON file.
3. You will be asked to authenticate. **IMPORTANT**, authenticate the **DESTINATION ACCOUNT** - the account you want to migrate subscriptions to - not the source account.
4. Wait for the program to finnish.

### Note.

* Currently, with a normal Google account, YouTube Data API have a limit quota of 10,000 per day. To `insert` a subscriptions costs 50 quotas. To fetch the subscription info cost 1 quota. This means that the program can only migrate about less than 200 subscriptions per day. You might have to re-run the program on multiple days to completely finish the migration.
* The program should not attempt to subscribe to an already subscribed channel.

## License.

The program itself is licensed under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt).