import { Link } from 'react-router-dom';
import { useEffect,useState } from 'react';
import { api } from '../api';
import haclogo from './haclogo.png'
const menuItems=[
 {label:'Главная',path:'/home'}, 
 {label:'Вузы',path:'/institutions'}, 
 {label:'Аналитика',path:'/analytics'}, 
 {label:'Администрирование',path:'/admin'}, 
 {label:'Документация',path:'/help'}
];
export default function Sidebar({activeItem='Главная'}){
 const [me,setMe]=useState(null);useEffect(()=>{api('/api/auth/me').then(setMe).catch(()=>{})},[]);
 const roles=me?.roles||[]; const items=menuItems.filter(x=>x.path!='/admin'||roles.includes('admin'));
 const initials=(me?.name||me?.username||'CRM').split(' ').slice(0,2).map(x=>x[0]).join('').toUpperCase();
 return <aside className="hidden md:flex w-64 bg-white border-r border-gray-200 flex-col shrink-0">
  <div className="px-6 py-6 flex flex-col items-start gap-1">
    <img src={haclogo} alt="Ростелеком" className="h-14 w-auto object-contain"/>
    <div className="text-[12px] text-gray-400">ИТ Школа CRM</div></div>
  <nav className="flex-1 px-3 space-y-1">{items.map(item=><Link key={item.label} to={item.path} className={`block px-3 py-2.5 rounded-lg text-sm ${item.label===activeItem?'bg-violet-50 text-violet-700 font-medium':'text-gray-600 hover:bg-gray-50'}`}>{item.label}</Link>)}</nav>
  <div className="p-4 border-t border-gray-100 flex items-center gap-3"><div className="w-9 h-9 rounded-full bg-violet-100 text-violet-600 grid place-items-center text-xs font-semibold">{initials}</div><div className="min-w-0"><div className="text-sm font-medium text-gray-800 truncate">{me?.name||me?.username||'Пользователь'}</div><div className="text-[11px] text-gray-400 truncate">{roles.join(', ')||'—'}</div></div></div>
 </aside>
}
