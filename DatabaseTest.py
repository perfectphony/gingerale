from datetime import datetime, timedelta

class Database:

    def get_polls(self):
        return [
            {
                "poll_id": 500,
                "question": "Should United Airlines fire Oscar Munoz?",
                "options": {
                    0: {
                        "answer": "Yes",
                        "count": 100
                    },
                    1: {
                        "answer": "No",
                        "count": 10
                    }
                },
                "gift_id": 1000,
                "tokens": 1
            },
            {
                "poll_id": 501,
                "question": "Is Chocolate better than Vanilla?",
                "options": {
                    0: {
                        "answer": "Yes",
                        "count": 100
                    },
                    1: {
                        "answer": "No",
                        "count": 10
                    }
                },
                "gift_id": 1001,
                "tokens": 1
            }
        ]

    def get_users(self):
        return [
            {
                "user_id": 100,
                "name": "woot",
                "tokens": 5,
                "status": "active"
            },
            {
                "user_id": 101,
                "name": "chu",
                "tokens": 10,
                "status": "active"
            }
        ]

    def get_gifts(self):
        return [
            {
                "gift_id": 1000,
                "gift_type": "raffle",
                "desc": "$5 Starbucks Giftcard",
                "expiration": datetime.utcnow() + timedelta(days=1),
                "winner_user_id": -1,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 1
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 2
                    }
                ]
            },
            {
                "gift_id": 1001,
                "gift_type": "accretion",
                "desc": "$20 BestBuy Giftcard",
                "requirement": 20000,
                "winner_user_id": -1,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 1
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 1
                    }
                ]
            },
            {
                "gift_id": 998,
                "gift_type": "raffle",
                "desc": "$5 Target Giftcard",
                "expiration": datetime.utcnow() + timedelta(days=-1),
                "winner_user_id": 0,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 1
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 1
                    }
                ]
            },
            {
                "gift_id": 999,
                "gift_type": "accretion",
                "desc": "$20 GameStop Giftcard",
                "bids": 10000,
                "requirement": 20000,
                "winner_user_id": 0,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 1
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 1
                    }
                ]
            },
        ]
