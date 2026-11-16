import {test,expect} from '@playwright/test';

test('mobile signup, profile, and logout without learner UI',async({page})=>{
 await page.route('http://127.0.0.1:8001/**',async route=>{
  const path=new URL(route.request().url()).pathname;
  const user={id:'one',mobile_e164:'+919876543210',full_name:'Asha',curriculum_code:'CBSE_G5',curriculum:{name:'CBSE Grade 5 English',board:'CBSE',grade:'5',medium:'English'},timezone:'Asia/Kolkata'};
  const body=path==='/curriculums'?[{code:'CBSE_G5',name:'CBSE Grade 5 English',board:'CBSE',grade:'5',medium:'English'}]:path==='/auth/otp/request'?{challenge_id:'challenge',code_length:4}:path==='/auth/otp/verify'?{grant:'grant'}:path==='/auth/signup'?{token:'token',user,remember_me:false}:path==='/auth/profile'?{...user,full_name:'Asha B'}:{message:'ok'};
  await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(body)});
 });
 await page.goto('/');await page.getByRole('button',{name:'Sign up'}).click();await page.getByLabel('Student name').fill('Asha');await page.getByLabel('Curriculum').selectOption('CBSE_G5');await page.getByLabel('Mobile number').fill('9876543210');for(let i=1;i<=4;i++){await page.getByLabel('PIN digit '+i,{exact:true}).fill(i===4?'1':'0');await page.getByLabel('Confirm PIN digit '+i).fill(i===4?'1':'0')}await page.getByRole('button',{name:'Send code'}).click();await page.getByLabel('Verification code').fill('1234');await page.getByRole('button',{name:'Verify'}).click();await expect(page.getByText('Welcome, Asha')).toBeVisible();await expect(page.getByText(/learner/i)).toHaveCount(0);await page.getByRole('button',{name:'Profile'}).click();await expect(page.getByText('Mobile number: +919876543210')).toBeVisible();await page.getByRole('button',{name:'Log out'}).click();await expect(page.getByRole('heading',{name:'Welcome Back'})).toBeVisible();
});





test('login actions remain usable from narrow phones to desktop',async({page})=>{
 await page.route('http://127.0.0.1:8001/curriculums',route=>route.fulfill({status:200,contentType:'application/json',body:'[]'}));
 for(const width of [320,390,768,1440]){
  await page.setViewportSize({width,height:900});
  await page.goto('/');
  const forgot=page.getByRole('button',{name:'Forgot PIN?'});
  const signup=page.getByRole('button',{name:'Sign up'});
  await expect(forgot).toBeVisible();await expect(signup).toBeVisible();
  const layout=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth,card:document.querySelector('section')!.getBoundingClientRect().bottom,signup:document.querySelector('.signup-prompt')!.getBoundingClientRect().top}));
  expect(layout.page).toBeLessThanOrEqual(layout.viewport);
  expect(layout.signup).toBeGreaterThan(layout.card);
  await forgot.click();await expect(page.getByRole('heading',{name:'Reset PIN'})).toBeVisible();
  await page.getByRole('button',{name:'Back to login'}).click();
  await signup.click();await expect(page.getByRole('heading',{name:'Sign Up'})).toBeVisible();
 }
});

test('refresh starts with clear fields and device sign-in lasts until logout',async({page})=>{
 const user={id:'persisted',mobile_e164:'+919876543210',full_name:'Asha',curriculum_code:'CBSE_G5',curriculum:{name:'CBSE Grade 5 English',board:'CBSE',grade:'5',medium:'English'},timezone:'Asia/Kolkata'};
 await page.route('http://127.0.0.1:8001/**',route=>{const path=new URL(route.request().url()).pathname;const body=path==='/curriculums'?[]:path==='/auth/login'?{token:'persistent-token',remember_me:true,user}:path==='/auth/me'?user:{message:'Signed out'};return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(body)})});
 await page.goto('/');
 await expect(page.getByRole('checkbox')).toHaveCount(0);
 await page.getByLabel('Mobile number').fill('9876543210');
 await page.getByLabel('PIN digit 1',{exact:true}).fill('0');
 await page.getByLabel('PIN digit 2',{exact:true}).fill('0');
 await page.reload();
 await expect(page.getByLabel('Mobile number')).toHaveValue('');
 await expect(page.getByLabel('PIN digit 1',{exact:true})).toHaveValue('');
 await expect(page.getByLabel('PIN digit 2',{exact:true})).toHaveValue('');
 await expect(page.getByLabel('PIN digit 1',{exact:true})).toHaveAttribute('type','text');
 await expect(page.getByLabel('PIN digit 1',{exact:true})).toHaveAttribute('autocomplete','off');
 await expect(page.getByLabel('PIN digit 1',{exact:true})).toHaveClass(/masked/);
 expect(await page.evaluate(()=>document.activeElement?.tagName)).not.toBe('INPUT');
 await page.getByLabel('Mobile number').fill('9876543210');
 for(let i=1;i<=4;i++)await page.getByLabel('PIN digit '+i,{exact:true}).fill(i===4?'1':'0');
 await page.getByRole('button',{name:'Sign in'}).click();
 await expect(page.getByText('Welcome, Asha')).toBeVisible();
 expect(await page.evaluate(()=>localStorage.getItem('sg_auth'))).toContain('persistent-token');
 await page.reload();await expect(page.getByText('Welcome, Asha')).toBeVisible();
 await page.getByRole('button',{name:'Log out'}).click();
 await expect(page.getByRole('heading',{name:'Welcome Back'})).toBeVisible();
 expect(await page.evaluate(()=>localStorage.getItem('sg_auth'))).toBeNull();
});




test('curriculum picker shows loading failures and recovers as a native select',async({page})=>{
 let requests=0;
 await page.route('http://127.0.0.1:8001/curriculums',route=>{requests++;return route.fulfill({status:requests===1?503:200,contentType:'application/json',body:requests===1?'{"detail":"Unavailable"}':'[{"code":"CBSE_G5","name":"CBSE Grade 5","board":"CBSE","grade":"5","medium":"English"},{"code":"CBSE_G11_COM","name":"CBSE Grade 11 Commerce","board":"CBSE","grade":"11","medium":"English"}]'})});
 await page.setViewportSize({width:320,height:800});await page.goto('/');await page.getByRole('button',{name:'Sign up'}).click();
 await expect(page.getByText('Could not load curriculums. Check that the backend is running.')).toBeVisible();
 await page.getByRole('button',{name:'Retry'}).click();
 const picker=page.getByLabel('Curriculum');await expect(picker).toBeEnabled();
 await expect(picker.locator('option')).toHaveCount(3);
 await picker.selectOption('CBSE_G5');
 await expect(page.getByText('CBSE · Grade 5 · English')).toBeVisible();
 expect(await picker.evaluate(el=>getComputedStyle(el).appearance)).toBe('none');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(320);
});
