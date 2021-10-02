# -*- coding: utf-8 -*-
import asyncio
import uvloop
import alog
import time
import records

from databases import Database

from concurrent import futures



async def query():
    # https://github.com/python-gino/gino/issues/70
    # https://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/
    # https://dadruid5.com/2017/07/20/checking-and-increasing-the-max-connections-in-postgresql/
    DATABASE_URL = 'postgresql://localhost/chairco'
    async with Database(DATABASE_URL) as database:
        query = 'select pg_sleep(1);'
        rows = await database.fetch_all(query=query)
        #alog.info(rows[0])


async def main():
    tasks = [asyncio.create_task(query()) for i in range(5)]
    await asyncio.gather(*tasks)



def seq_query(i):
    conn = records.Database('postgresql://localhost/chairco')
    rows = conn.query('select pg_sleep(1);')
    #alog.info(f"{i}= {rows[0]}")


def seq_main():
    for i in range(10):
       seq_query(i)


def concurrent_main():
    with futures.ThreadPoolExecutor() as executor:
        for future in executor.map(seq_query, range(5)):
            pass


if __name__ == '__main__':

    
    start = time.time()
    uvloop.install()
    asyncio.run(main())
    alog.info(f"asyncio+uvloop cost: {time.time() - start}")

    

    start = time.time()
    seq_main()
    alog.info(f"sequence cost: {time.time() - start}")
    

    
    start = time.time()
    concurrent_main()
    alog.info(f"concurrent cost: {time.time() - start}")
    

