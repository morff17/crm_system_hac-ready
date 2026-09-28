export default function MetricCard({ title, value, growth }) {
    return (
        <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <div className="text-xs text-gray-500 mb-2">{title}</div>
            <div className="flex items-baseline justify-between">
                <div className="text-2xl font-bold text-gray-800">{value}</div>
                <div className="text-xs font-medium text-emerald-500">{growth}</div>
            </div>
        </div>
    );
}