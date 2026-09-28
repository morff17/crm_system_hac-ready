export default function StatCard({ title, value, growth, growthColor = 'green', iconBg }) {
    const colors = {
        green: 'text-emerald-500',
        blue: 'text-blue-500',
        pink: 'text-pink-500',
    };

    return (
        <div className="bg-white rounded-2xl border border-gray-100 p-5 flex flex-col justify-between min-h-[120px]">
            <div className="flex items-start justify-between">
                <div className={`w-10 h-10 rounded-lg ${iconBg}`} />
                <span className={`text-xs font-medium ${colors[growthColor]}`}>{growth}</span>
            </div>
            <div className="mt-3">
                <div className="text-xs text-gray-500 mb-1">{title}</div>
                <div className="text-2xl font-bold text-gray-800">{value}</div>
            </div>
        </div>
    );
}