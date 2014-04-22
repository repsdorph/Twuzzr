__author__ = 'Repsdorph'
__version__ = 0.1

import twitter


class TwitterHandler:
    """
    Takes care of different calls to Twitter.
    """

    def __init__(self):
        consumer_key = ''
        consumer_secret = ''
        oauth_token = ''
        oauth_token_secret = ''

        self.auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                                        consumer_key, consumer_secret)

        #Log in.
        self.oauth_login()

    def oauth_login(self):
        """
        Generates the login procedure.
        """

        self.twitter_api = twitter.Twitter(auth=self.auth)

    def get_retweets(self, tweet_id):
        """
        Returns retweets from userID

        :param tweet_id: Twitter tweet id
        :type tweet_id: int
        """

        return self.twitter_api.statuses.retweets._id(_id=tweet_id)

    def twitter_search(self, q, max_results=200, **kw):
        """
        See https://dev.twitter.com/docs/api/1.1/get/search/tweets and
        https://dev.twitter.com/docs/using-search for details on advanced
        search criteria that may be useful for keyword arguments

        See https://dev.twitter.com/docs/api/1.1/get/search/tweets

        :param q:
        :param max_results:
        :param kw:
        :return:
        """
        search_results = self.twitter_api.search.tweets(q=q, count=100, **kw)

        statuses = search_results['statuses']

        # Iterate through batches of results by following the cursor until we
        # reach the desired number of results, keeping in mind that OAuth users
        # can "only" make 180 search queries per 15-minute interval. See
        # https://dev.twitter.com/docs/rate-limiting/1.1/limits
        # for details. A reasonable number of results is ~1000, although
        # that number of results may not exist for all queries.

        # Enforce a reasonable limit
        max_results = min(1000, max_results)

        for _ in range(10): # 10*100 = 1000
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError, e: # No more results when next_results doesn't exist
                break

            # Create a dictionary from next_results, which has the following form:
            # ?max_id=313519052523986943&q=NCAA&include_entities=1
            kwargs = dict([ kv.split('=')
                            for kv in next_results[1:].split("&") ])

            search_results = self.twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']

            if len(statuses) > max_results:
                break

        return statuses

th = TwitterHandler()
#print(len(th.get_retweets(32412)))

print((th.get_retweets(453657888934727680)[0]))