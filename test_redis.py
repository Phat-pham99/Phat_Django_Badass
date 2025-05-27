from upstash_redis import Redis

redis = Redis(url="https://alive-ghoul-41419.upstash.io", token="AaHLAAIjcDE0ZTcwMThiNTFjYWY0N2MyYWM4MzM1NDQxOGRjYTFmOXAxMA")

redis.set("var1", "Suprise motherfucker 👊🎬 ")
print(redis.get("var1"))