import hashlib
import hmac
import os
import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import aiomysql
import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator

load_dotenv()
UTC = timezone.utc
def now(): return datetime.now(UTC).replace(tzinfo=None)
def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def uid(): return str(uuid.uuid4())
def pin_hash(pin): return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()
def mobile(value):
    digits = re.sub(r'[^0-9+]', '', value.strip())
    if re.fullmatch(r'[0-9]{10}', digits): digits = '+91' + digits
    elif re.fullmatch(r'91[0-9]{10}', digits): digits = '+' + digits
    elif digits.startswith('00'): digits = '+' + digits[2:]
    if not re.fullmatch(r'\+[1-9][0-9]{7,14}', digits): raise ValueError('Invalid mobile number')
    return digits
def tz(value):
    try: ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError): raise ValueError('Unsupported timezone')
    return value
def otp_verifier(mob,purpose,code):
    return hmac.new(os.environ['OTP_SECRET'].encode(), f'{mob}:{purpose}:{code}'.encode(), hashlib.sha256).hexdigest()

class MobilePurpose(BaseModel):
    mobile: str
    purpose: str
    @field_validator('mobile')
    @classmethod
    def valid_mobile(cls,v): return mobile(v)
    @field_validator('purpose')
    @classmethod
    def valid_purpose(cls,v):
        if v not in ('signup','recovery'): raise ValueError('Invalid purpose')
        return v
class Verify(MobilePurpose):
    challenge_id: str
    code: str = Field(pattern=r'^\d{4,6}$')
class GrantBase(BaseModel):
    mobile: str
    grant: str
    @field_validator('mobile')
    @classmethod
    def valid_mobile(cls,v): return mobile(v)
class Signup(GrantBase):
    pin: str = Field(pattern=r'^\d{4}$')
    full_name: str = Field(min_length=1,max_length=120)
    curriculum_code: str
    avatar_seed: str | None = None
    school_name: str | None = None
    guardian_name: str | None = None
    guardian_mobile_e164: str | None = None
    guardian_email: str | None = None
    timezone: str = 'Asia/Kolkata'
    @field_validator('full_name')
    @classmethod
    def valid_name(cls,v):
        if v is None: return v
        if not v.strip(): raise ValueError('Student name is required')
        return v.strip()
    @field_validator('timezone')
    @classmethod
    def valid_tz(cls,v): return tz(v)
    @field_validator('guardian_mobile_e164')
    @classmethod
    def valid_guardian(cls,v): return mobile(v) if v else None
class Login(BaseModel):
    mobile: str
    pin: str = Field(pattern=r'^\d{4}$')
    remember_me: bool = False
    @field_validator('mobile')
    @classmethod
    def valid_mobile(cls,v): return mobile(v)
class Reset(GrantBase):
    new_pin: str = Field(pattern=r'^\d{4}$')
class ProfilePatch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    full_name: str | None = Field(default=None,min_length=1,max_length=120)
    avatar_seed: str | None = None
    school_name: str | None = None
    guardian_name: str | None = None
    guardian_mobile_e164: str | None = None
    guardian_email: str | None = None
    timezone: str | None = None
    @field_validator('full_name')
    @classmethod
    def valid_name(cls,v):
        if v is None: raise ValueError('Student name is required')
        if not v.strip(): raise ValueError('Student name is required')
        return v.strip()
    @field_validator('timezone')
    @classmethod
    def valid_tz(cls,v): return tz(v) if v else v
    @field_validator('guardian_mobile_e164')
    @classmethod
    def valid_guardian(cls,v): return mobile(v) if v else v

app = FastAPI(title='SchollyGo v2 Account API')
origins = [os.getenv('FRONTEND_ORIGIN','http://localhost:5173')]
if os.getenv('APP_ENV','development') != 'production':
    origins += ['http://localhost:5173','http://127.0.0.1:5173']
app.add_middleware(CORSMiddleware,allow_origins=list(dict.fromkeys(origins)),allow_methods=['*'],allow_headers=['*'])

@app.on_event('startup')
async def startup():
    production = os.getenv('APP_ENV') == 'production'
    if len(os.getenv('OTP_SECRET','')) < 32: raise RuntimeError('OTP_SECRET must have at least 32 characters')
    if production and (os.getenv('DEV_OTP_ENABLED') == 'true' or not all(os.getenv(k) for k in ('SMS_API_URL','SMS_API_KEY','SMS_SENDER_ID'))):
        raise RuntimeError('Production requires configured SMS sender and disabled development OTP')
    if not production and os.getenv('DEV_OTP_ENABLED') != 'true' and not all(os.getenv(k) for k in ('SMS_API_URL','SMS_API_KEY','SMS_SENDER_ID')):
        raise RuntimeError('Configure an SMS sender or enable development OTP')
    app.state.pool = await aiomysql.create_pool(host=os.getenv('DB_HOST','127.0.0.1'),port=int(os.getenv('DB_PORT','3306')),user=os.environ['DB_USER'],password=os.environ['DB_PASSWORD'],db=os.getenv('DB_NAME','schollygoappv2'),autocommit=False,init_command="SET time_zone = '+00:00'")
@app.on_event('shutdown')
async def shutdown():
    app.state.pool.close(); await app.state.pool.wait_closed()
async def db():
    async with app.state.pool.acquire() as conn:
        try: yield conn
        finally: await conn.rollback()
async def query(conn,sql,args=(),one=False):
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(sql,args)
        return await cur.fetchone() if one else await cur.fetchall()
async def execute(conn,sql,args=()):
    async with conn.cursor() as cur: await cur.execute(sql,args)

async def send_sms(mob,code):
    if os.getenv('DEV_OTP_ENABLED') == 'true':
        path = Path(os.getenv('DEV_OTP_FILE','./dev-otps.log'))
        with path.open('a',encoding='utf8') as f: f.write(f'{datetime.now(UTC).isoformat()} {mob} {code}\n')
        return
    import httpx
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(os.environ['SMS_API_URL'],headers={'Authorization':'Bearer '+os.environ['SMS_API_KEY']},json={'to':mob,'message':f'Your SchollyGo code is {code}','sender':os.environ['SMS_SENDER_ID']})
        response.raise_for_status()

def safe(row):
    fields = ('id','mobile_e164','full_name','avatar_seed','curriculum_code','school_name','guardian_name','guardian_mobile_e164','guardian_email','timezone')
    result = {k:row[k] for k in fields}
    result['curriculum'] = {k:row[k] for k in ('name','board','stream','medium','grade','type')}
    return result
PROFILE = '''SELECT u.*,c.name,c.board,c.stream,c.medium,c.grade,c.type FROM users u JOIN curriculums c ON c.code=u.curriculum_code'''
async def session(conn,user_id,remember):
    token = secrets.token_urlsafe(48); expiry = datetime(9999,12,31,23,59,59) if remember else now()+timedelta(hours=12)
    await execute(conn,'INSERT INTO auth_sessions (id,user_id,token_hash,remember_me,created_at,expires_at) VALUES (%s,%s,%s,%s,%s,%s)',(uid(),user_id,digest(token),remember,now(),expiry))
    return {'token':token,'expires_at':expiry.isoformat()+'Z','remember_me':remember}
async def current(authorization: str | None = Header(default=None), conn=Depends(db)):
    token = authorization[7:] if authorization and authorization.startswith('Bearer ') else ''
    if not token: raise HTTPException(401,'Authentication required')
    row = await query(conn,PROFILE+''' JOIN auth_sessions s ON s.user_id=u.id WHERE s.token_hash=%s AND s.revoked_at IS NULL AND s.expires_at>%s AND u.status='active' ''',(digest(token),now()),True)
    if not row: raise HTTPException(401,'Session expired')
    return row,token

@app.get('/health')
async def health(): return {'status':'ok'}
@app.get('/curriculums')
async def curriculums(conn=Depends(db)):
    return await query(conn,'SELECT code,name,board,stream,medium,grade,type FROM curriculums WHERE is_active=TRUE ORDER BY sequence_order,code')

@app.post('/auth/otp/request')
async def request_otp(payload: MobilePurpose, request: Request, conn=Depends(db)):
    mob,purpose = payload.mobile,payload.purpose; instant=now(); ip=digest(request.client.host if request.client else 'unknown')
    await conn.begin()
    ip_count=(await query(conn,'SELECT COUNT(*) n FROM otp_challenges WHERE request_ip_hash=%s AND created_at>%s',(ip,instant-timedelta(hours=1)),True))['n']
    prior=await query(conn,'SELECT created_at FROM otp_challenges WHERE mobile_e164=%s AND purpose=%s ORDER BY created_at DESC LIMIT 1',(mob,purpose),True)
    mobile_count=(await query(conn,'SELECT COUNT(*) n FROM otp_challenges WHERE mobile_e164=%s AND created_at>%s',(mob,instant-timedelta(hours=1)),True))['n']
    if ip_count>=30 or mobile_count>=5 or prior and prior['created_at']>instant-timedelta(seconds=60):
        await conn.commit(); raise HTTPException(429,'Please wait before requesting another code')
    user=await query(conn,'SELECT id FROM users WHERE mobile_e164=%s',(mob,),True)
    if (purpose=='signup' and user) or (purpose=='recovery' and not user):
        await conn.commit(); return {'message':'If eligible, a code has been sent','challenge_id':uid(),'code_length':4 if os.getenv('DEV_OTP_ENABLED') == 'true' else 6}
    code='1234' if os.getenv('DEV_OTP_ENABLED') == 'true' else f'{secrets.randbelow(1000000):06d}'; challenge=uid()
    await execute(conn,'INSERT INTO otp_challenges (id,mobile_e164,purpose,verifier,attempts_remaining,expires_at,created_at,request_ip_hash) VALUES (%s,%s,%s,%s,5,%s,%s,%s)',(challenge,mob,purpose,otp_verifier(mob,purpose,code),instant+timedelta(minutes=5),instant,ip))
    try: await send_sms(mob,code)
    except Exception:
        await conn.rollback(); raise HTTPException(503,'Code delivery unavailable')
    await conn.commit(); return {'message':'If eligible, a code has been sent','challenge_id':challenge,'code_length':len(code)}

@app.post('/auth/otp/verify')
async def verify(payload: Verify, conn=Depends(db)):
    await conn.begin()
    row=await query(conn,'SELECT * FROM otp_challenges WHERE id=%s FOR UPDATE',(payload.challenge_id,),True)
    instant=now()
    if len(payload.code) != (4 if os.getenv('DEV_OTP_ENABLED') == 'true' else 6): raise HTTPException(400,'Invalid or expired code')
    if not row or row['mobile_e164']!=payload.mobile or row['purpose']!=payload.purpose or row['expires_at']<=instant or row['consumed_at'] or row['verified_at'] or row['attempts_remaining']==0:
        raise HTTPException(400,'Invalid or expired code')
    if not hmac.compare_digest(row['verifier'],otp_verifier(payload.mobile,payload.purpose,payload.code)):
        await execute(conn,'UPDATE otp_challenges SET attempts_remaining=attempts_remaining-1 WHERE id=%s',(row['id'],)); await conn.commit()
        raise HTTPException(400,'Invalid or expired code')
    grant=secrets.token_urlsafe(48)
    await execute(conn,'UPDATE otp_challenges SET verified_at=%s,grant_hash=%s,grant_expires_at=%s WHERE id=%s',(instant,digest(grant),instant+timedelta(minutes=10),row['id']))
    await conn.commit(); return {'grant':grant,'expires_at':(instant+timedelta(minutes=10)).isoformat()+'Z'}

async def consume(conn,grant,mob,purpose):
    row=await query(conn,'SELECT id FROM otp_challenges WHERE grant_hash=%s AND mobile_e164=%s AND purpose=%s AND verified_at IS NOT NULL AND consumed_at IS NULL AND grant_expires_at>%s FOR UPDATE',(digest(grant),mob,purpose,now()),True)
    if not row: raise HTTPException(400,'Invalid or expired verification grant')
    await execute(conn,'UPDATE otp_challenges SET consumed_at=%s WHERE id=%s',(now(),row['id']))

@app.post('/auth/signup')
async def signup(payload: Signup,conn=Depends(db)):
    await conn.begin()
    await consume(conn,payload.grant,payload.mobile,'signup')
    curriculum=await query(conn,'SELECT code FROM curriculums WHERE code=%s AND is_active=TRUE',(payload.curriculum_code,),True)
    if not curriculum: raise HTTPException(400,'Invalid or inactive curriculum')
    instant=now(); user_id=uid()
    try:
        await execute(conn,'''INSERT INTO users (id,mobile_e164,pin_hash,mobile_verified_at,full_name,avatar_seed,curriculum_code,school_name,guardian_name,guardian_mobile_e164,guardian_email,timezone,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(user_id,payload.mobile,pin_hash(payload.pin),instant,payload.full_name.strip(),payload.avatar_seed,payload.curriculum_code,payload.school_name,payload.guardian_name,payload.guardian_mobile_e164,payload.guardian_email,payload.timezone,instant,instant))
    except aiomysql.IntegrityError:
        await conn.rollback(); raise HTTPException(409,'Mobile number already registered')
    auth=await session(conn,user_id,True); row=await query(conn,PROFILE+' WHERE u.id=%s',(user_id,),True)
    await conn.commit(); return {**auth,'user':safe(row)}

@app.post('/auth/login')
async def login(payload: Login,conn=Depends(db)):
    await conn.begin()
    row=await query(conn,PROFILE+' WHERE u.mobile_e164=%s FOR UPDATE',(payload.mobile,),True)
    instant=now()
    if not row: raise HTTPException(401,'Invalid mobile number or PIN')
    if row['status']!='active': raise HTTPException(403,'Account disabled')
    if row['locked_until'] and row['locked_until']>instant: raise HTTPException(423,'Account temporarily locked')
    if not bcrypt.checkpw(payload.pin.encode(),row['pin_hash'].encode()):
        failures=row['login_failures']+1; lock=instant+timedelta(minutes=15) if failures>=5 else None
        await execute(conn,'UPDATE users SET login_failures=%s,locked_until=%s WHERE id=%s',(failures,lock,row['id']))
        await conn.commit(); raise HTTPException(423 if lock else 401,'Account temporarily locked' if lock else 'Invalid mobile number or PIN')
    await execute(conn,'UPDATE users SET login_failures=0,locked_until=NULL WHERE id=%s',(row['id'],))
    auth=await session(conn,row['id'],payload.remember_me); await conn.commit()
    return {**auth,'user':safe(row)}

@app.get('/auth/me')
async def me(auth=Depends(current)): return safe(auth[0])
@app.patch('/auth/profile')
async def profile(payload: ProfilePatch, auth=Depends(current), conn=Depends(db)):
    changes=payload.model_dump(exclude_unset=True)
    if not changes: return safe(auth[0])
    await conn.begin()
    await execute(conn,'UPDATE users SET '+','.join(f'{k}=%s' for k in changes)+',updated_at=%s WHERE id=%s',(*changes.values(),now(),auth[0]['id']))
    row=await query(conn,PROFILE+' WHERE u.id=%s',(auth[0]['id'],),True)
    await conn.commit(); return safe(row)
@app.post('/auth/reset-pin')
async def reset_pin(payload: Reset,conn=Depends(db)):
    await conn.begin()
    user=await query(conn,'SELECT id FROM users WHERE mobile_e164=%s FOR UPDATE',(payload.mobile,),True)
    if not user: raise HTTPException(400,'Invalid or expired verification grant')
    await consume(conn,payload.grant,payload.mobile,'recovery')
    instant=now()
    await execute(conn,'UPDATE users SET pin_hash=%s,login_failures=0,locked_until=NULL,updated_at=%s WHERE id=%s',(pin_hash(payload.new_pin),instant,user['id']))
    await execute(conn,'UPDATE auth_sessions SET revoked_at=%s WHERE user_id=%s AND revoked_at IS NULL',(instant,user['id']))
    await conn.commit(); return {'message':'PIN reset. Please log in.'}
@app.post('/auth/logout')
async def logout(authorization: str | None = Header(default=None),conn=Depends(db)):
    token=authorization[7:] if authorization and authorization.startswith('Bearer ') else ''
    if token:
        await conn.begin(); await execute(conn,'UPDATE auth_sessions SET revoked_at=%s WHERE token_hash=%s AND revoked_at IS NULL',(now(),digest(token))); await conn.commit()
    return {'message':'Signed out'}
