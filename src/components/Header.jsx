import { useEffect,useState } from 'react';
import { useNavigate,Link } from 'react-router-dom';
import { api,clearAuth } from '../api';
export default function Header(){
 const navigate=useNavigate();const [me,setMe]=useState(null);const [q,setQ]=useState('');const [open,setOpen]=useState(false);
 useEffect(()=>{api('/api/auth/me').then(setMe).catch(()=>{})},[]);const logout=()=>{clearAuth();navigate('/login')};const initials=(me?.name||me?.username||'CRM').split(' ').slice(0,2).map(x=>x[0]).join('').toUpperCase();
 const search=e=>{e.preventDefault();navigate(`/institutions?q=${encodeURIComponent(q)}`)};
 return <header className="relative flex items-center gap-3 px-4 md:px-6 py-4 bg-white border-b border-gray-100">
  <button onClick={()=>setOpen(!open)} className="md:hidden px-3 py-2 rounded-lg border text-sm">Меню</button>
  <form onSubmit={search} className="flex-1 max-w-md"><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Поиск по вузам..." className="w-full px-3 py-2 text-sm rounded-lg border border-gray-200 outline-none focus:border-violet-400"/></form>
  <div className="flex-1"/><div className="text-xs text-gray-500 hidden lg:block">{me?.name||me?.username}</div><button onClick={logout} title="Выйти" className="w-9 h-9 rounded-full bg-violet-100 text-violet-600 text-xs font-semibold">{initials}</button>
  {open&&<div className="absolute z-50 top-full left-3 right-3 bg-white border rounded-xl shadow-lg p-2 md:hidden"><Link onClick={()=>setOpen(false)} className="block p-3" to="/home">Главная</Link><Link onClick={()=>setOpen(false)} className="block p-3" to="/institutions">Вузы</Link><Link onClick={()=>setOpen(false)} className="block p-3" to="/analytics">Аналитика</Link>{me?.roles?.includes('admin')&&<Link onClick={()=>setOpen(false)} className="block p-3" to="/admin">Администрирование</Link>}<Link onClick={()=>setOpen(false)} className="block p-3" to="/help">Документация</Link></div>}
 </header>
}
