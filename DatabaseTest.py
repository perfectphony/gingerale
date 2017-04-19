from datetime import datetime, timedelta

class Database:

    def get_polls(self):
        return [
            {
                "id": 500,
                "question": "Should United Airlines fire Oscar Munoz?",
                "options": [
                    {"option": 0, "text": "Yes"},
                    {"option": 1, "text": "No"}
                ],
                "votes": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "option": 0
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "option": 0
                    }
                ],
                "gift_id": 1000,
                "reward_tokens": 10
            },
            {
                "id": 501,
                "question": "Is Chocolate better than Vanilla?",
                "options": [
                    {"option": 0, "text": "Yes"},
                    {"option": 1, "text": "No"}
                ],
                "votes": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "option": 0
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "option": 0
                    }
                ],
                "gift_id": 1001,
                "reward_tokens": 10
            }
        ]

    def get_users(self):
        return [
            {
                "id": 100,
                "name": "woot",
                "tokens": 5,
                "status": "active"
            },
            {
                "id": 101,
                "name": "chu",
                "tokens": 10,
                "status": "active"
            }
        ]

    def get_prizes(self):
        return [
            {
                "id": 1000,
                "desc": "$5 Starbucks Giftcard",
                "requirement": 100000,
                "winner_user_id": -1,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 10
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 20
                    }
                ]
            },
            {
                "id": 1001,
                "desc": "$20 BestBuy Giftcard",
                "requirement": 200000,
                "winner_user_id": -1,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 10
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 10
                    }
                ]
            },
            {
                "id": 998,
                "gift_type": "raffle",
                "desc": "$5 Target Giftcard",
                "bids": 10000,
                "requirement": 50000,
                "winner_user_id": 100,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 10
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 10
                    }
                ]
            },
            {
                "id": 999,
                "gift_type": "accretion",
                "desc": "$20 GameStop Giftcard",
                "bids": 10000,
                "requirement": 200000,
                "winner_user_id": 100,
                "entries": [
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 100,
                        "tokens": 10
                    },
                    {
                        "timestamp": datetime.utcnow() + timedelta(days=-1),
                        "user_id": 101,
                        "tokens": 10
                    }
                ]
            },
        ]
