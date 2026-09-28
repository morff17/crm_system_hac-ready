export default function BarChart({ data }) {
    const items = data?.length ? data : [{name:'Нет данных',value:1}];
    const max = Math.max(...items.map((d) => d.value || 0), 1);
    return <div className="bg-white rounded-2xl border border-gray-100 p-6"><div className="flex items-center justify-between mb-6"><h3 className="font-semibold text-gray-800">Вузы по регионам</h3></div><div className="flex items-end justify-between gap-3 h-40">{items.slice(0,8).map((item,i)=><div key={i} className="flex flex-col items-center gap-2 flex-1 min-w-0"><div className="w-full flex items-end justify-center h-32"><div className="w-8 rounded-t-lg bg-violet-300" style={{height:`${Math.max((item.value/max)*100,4)}%`}} /></div><span title={item.name} className="text-[10px] text-gray-400 truncate w-full text-center">{item.name}</span></div>)}</div></div>;
}
