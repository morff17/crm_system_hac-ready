const API_BASE = process.env.REACT_APP_API_BASE || '';
export const getToken = () => localStorage.getItem('access_token');
export const getRefreshToken = () => localStorage.getItem('refresh_token');
export function clearAuth(){localStorage.removeItem('access_token');localStorage.removeItem('refresh_token');}
let refreshing = null;
async function refreshAccess(){
  if(refreshing) return refreshing;
  const rt=getRefreshToken(); if(!rt) return false;
  refreshing=fetch(`${API_BASE}/api/auth/refresh`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh_token:rt})})
    .then(async r=>{if(!r.ok) throw new Error(); const d=await r.json();localStorage.setItem('access_token',d.access_token);if(d.refresh_token)localStorage.setItem('refresh_token',d.refresh_token);return true;})
    .catch(()=>{clearAuth();return false;}).finally(()=>{refreshing=null});
  return refreshing;
}
export async function api(path, options = {}, retry=true){
  const headers=new Headers(options.headers||{});const token=getToken();if(token)headers.set('Authorization',`Bearer ${token}`);
  if(options.body && !(options.body instanceof FormData) && !headers.has('Content-Type'))headers.set('Content-Type','application/json');
  let res=await fetch(`${API_BASE}${path}`,{...options,headers});
  if(res.status===401 && retry && await refreshAccess()) return api(path,options,false);
  if(res.status===401){clearAuth();if(window.location.pathname!=='/login')window.location.href='/login';}
  if(!res.ok){let detail=`HTTP ${res.status}`;try{const j=await res.json();detail=j.detail||detail;}catch(_){}throw new Error(detail)}
  const ct=res.headers.get('content-type')||'';return ct.includes('application/json')?res.json():res;
}
export async function login(login,password){const res=await fetch(`${API_BASE}/api/auth/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({login,password})});if(!res.ok)throw new Error('Неверный логин или пароль');const d=await res.json();localStorage.setItem('access_token',d.access_token);if(d.refresh_token)localStorage.setItem('refresh_token',d.refresh_token);return d;}
async function download(path,filename){const res=await api(path);const blob=await res.blob();const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
export async function downloadReport(format,params={}){const qs=new URLSearchParams({format,...Object.fromEntries(Object.entries(params).filter(([,v])=>v!==''&&v!=null))});return download(`/api/reports/export?${qs}`,`crm-report.${format}`)}
export async function downloadChart(format,params={}){const qs=new URLSearchParams({format,...Object.fromEntries(Object.entries(params).filter(([,v])=>v!==''&&v!=null&&v!==undefined))});qs.delete('columns');return download(`/api/reports/chart?${qs}`,`crm-chart.${format}`)}
export async function downloadAttachment(id,name='attachment'){return download(`/api/attachments/${id}`,name)}
