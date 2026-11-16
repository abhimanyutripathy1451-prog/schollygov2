"""Run with DB_NAME=schollygoappv2_test and DEV_OTP_ENABLED=true."""
import asyncio
import os
import httpx
from backend.main import app

async def main():
    assert os.getenv('DB_NAME','').startswith('schollygoappv2_test')
    os.environ['DEV_OTP_ENABLED']='true'
    await app.router.startup()
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as client:
            async def code(): return '1234'
            choices={row['code'] for row in (await client.get('/curriculums')).json()}
            assert {'CBSE_G5','CBSE_G11_COM'} <= choices
            assert 'CBSE_G6' not in choices
            mob='9'+str(__import__('secrets').randbelow(10**9)).zfill(9)
            r=await client.post('/auth/otp/request',json={'mobile':mob,'purpose':'signup'}); assert r.status_code==200,r.text
            challenge=r.json()['challenge_id']
            assert r.json()['code_length']==4 and await code()=='1234'
            assert (await client.post('/auth/otp/verify',json={'mobile':mob,'purpose':'signup','challenge_id':challenge,'code':'0000'})).status_code==400
            r=await client.post('/auth/otp/verify',json={'mobile':mob,'purpose':'signup','challenge_id':challenge,'code':await code()}); assert r.status_code==200,r.text
            grant=r.json()['grant']
            assert (await client.post('/auth/otp/verify',json={'mobile':mob,'purpose':'signup','challenge_id':challenge,'code':await code()})).status_code==400
            r=await client.post('/auth/signup',json={'mobile':mob,'grant':grant,'pin':'0001','full_name':'Student','curriculum_code':'CBSE_G5'}); assert r.status_code==200,r.text
            token=r.json()['token']; assert r.json()['expires_at'].startswith('9999'); assert r.json()['user']['mobile_e164']=='+91'+mob
            assert (await client.post('/auth/signup',json={'mobile':mob,'grant':grant,'pin':'0001','full_name':'Student','curriculum_code':'CBSE_G5'})).status_code==400
            headers={'Authorization':'Bearer '+token}
            assert (await client.get('/auth/me',headers=headers)).status_code==200
            assert (await client.patch('/auth/profile',headers=headers,json={'mobile_e164':'+919999999999'})).status_code==422
            r=await client.patch('/auth/profile',headers=headers,json={'school_name':'Test school'}); assert r.status_code==200 and r.json()['school_name']=='Test school',r.text
            r=await client.post('/auth/login',json={'mobile':mob,'pin':'0001','remember_me':True}); assert r.status_code==200,r.text
            other=r.json()['token']; assert r.json()['remember_me']
            assert (await client.post('/auth/logout',headers=headers)).status_code==200
            assert (await client.get('/auth/me',headers=headers)).status_code==401
            assert (await client.get('/auth/me',headers={'Authorization':'Bearer '+other})).status_code==200
            r=await client.post('/auth/otp/request',json={'mobile':mob,'purpose':'recovery'}); assert r.status_code==200,r.text
            r=await client.post('/auth/otp/verify',json={'mobile':mob,'purpose':'recovery','challenge_id':r.json()['challenge_id'],'code':await code()}); assert r.status_code==200,r.text
            r=await client.post('/auth/reset-pin',json={'mobile':mob,'grant':r.json()['grant'],'new_pin':'0123'}); assert r.status_code==200,r.text
            assert (await client.get('/auth/me',headers={'Authorization':'Bearer '+other})).status_code==401
            assert (await client.post('/auth/login',json={'mobile':mob,'pin':'0001'})).status_code==401
            assert (await client.post('/auth/login',json={'mobile':mob,'pin':'0123'})).status_code==200
            for _ in range(4): assert (await client.post('/auth/login',json={'mobile':mob,'pin':'9999'})).status_code==401
            assert (await client.post('/auth/login',json={'mobile':mob,'pin':'9999'})).status_code==423
            assert (await client.post('/auth/login',json={'mobile':mob,'pin':'0123'})).status_code==423
        print('API acceptance: PASS')
    finally: await app.router.shutdown()

if __name__=='__main__': asyncio.run(main())
