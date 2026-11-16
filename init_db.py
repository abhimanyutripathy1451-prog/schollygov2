"""Create only the configured v2 database and apply the additive baseline."""
import asyncio
import os
from pathlib import Path
import aiomysql
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name('.env'))
async def main():
    name=os.getenv('DB_NAME','schollygoappv2')
    if name!='schollygoappv2' and not name.startswith('schollygoappv2_test'):
        raise SystemExit('Refusing database outside schollygoappv2 or schollygoappv2_test*')
    conn=await aiomysql.connect(host=os.getenv('DB_HOST','127.0.0.1'),port=int(os.getenv('DB_PORT','3306')),user=os.environ['DB_USER'],password=os.environ['DB_PASSWORD'],autocommit=True)
    try:
        async with conn.cursor() as cur:
            await cur.execute(f'CREATE DATABASE IF NOT EXISTS `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_bin')
            await cur.execute(f'USE `{name}`')
            await cur.execute('SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s',(name,))
            existing={r[0] for r in await cur.fetchall()}
            expected={'curriculums','users','auth_sessions','otp_challenges'}
            if existing-expected: raise SystemExit(f'Unexpected tables in {name}: {sorted(existing-expected)}; inspect manually')
            sql=(Path(__file__).parent/'sql/001_baseline.sql').read_text()
            for statement in sql.split(';'):
                if statement.strip(): await cur.execute(statement)
            if os.getenv('SEED_DEV')=='true':
                for statement in (Path(__file__).parent/'sql/seed_dev.sql').read_text().split(';'):
                    if statement.strip(): await cur.execute(statement)
        print(f'Initialized {name}')
    finally: conn.close()
if __name__=='__main__': asyncio.run(main())
