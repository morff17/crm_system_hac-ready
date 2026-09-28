import { useEffect,useState } from 'react';
import { Navigate } from 'react-router-dom';
import { api,getToken } from '../api';
export default function ProtectedRoute({children}){const [state,setState]=useState(getToken()?'loading':'no');useEffect(()=>{if(state==='loading')api('/api/auth/me').then(()=>setState('ok')).catch(()=>setState('no'));},[]);if(state==='loading')return <div className="min-h-screen grid place-items-center text-gray-500">Проверка сессии…</div>;return state==='ok'?children:<Navigate to="/login" replace/>;}
