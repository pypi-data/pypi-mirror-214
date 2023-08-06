import time

from loguru import logger as logger

from souJpg.comm.redisOps import RedisOps


def png2jpg():
    from PIL import Image

    im = Image.open("testImages/kt_test.png")
    rgb_im = im.convert("RGB")
    rgb_im.save("testImages/kt_test.jpg")


if __name__ == "__main__":
    # host='gpu0.dev.yufei.com'
    # r = redis.Redis(host=host, port=6379, db=0)
    # r.set('foo', 'bar')
    # value=r.get('foo')
    # logger.info(value)
    # redisOps = RedisOps()
    # keydict = {
    #     "1": "12_1 34_2 45_3 88_4",
    #     "2": "120_1 3_2 4_3 88_4",
    #     "3": "11_1 4_2 234_3 88_4",
    # }
    # redisOps.mset(keydict=keydict)
    # keys = ["1", "2", "3", "euemCssxRJ7Watpb7RCjXj"]
    # logger.info(redisOps.mget(keys=keys))
    # userKey = "userId"
    # redisOps.set(key=userKey, value=userKey, ex=2)
    # logger.info(redisOps.get(userKey))
    # time.sleep(3)
    # logger.info(redisOps.get(userKey))
    # queueName = "testQueue"
    # redisOps.lpush(key=queueName, value=1)
    # redisOps.lpush(key=queueName, value=2)
    # logger.info(redisOps.rpop(key=queueName))
    # logger.info(redisOps.rpop(key=queueName))

    # bfName = "cuckoo2"
    # # redisOps.bfPush(bfName,'1')
    # # redisOps.bfPush(bfName,'1000')
    # # redisOps.bfPush(bfName,'1')
    # logger.info(redisOps.bfExist(bfName, "1"))
    # logger.info(redisOps.bfExist(bfName, "10"))
    png2jpg()
