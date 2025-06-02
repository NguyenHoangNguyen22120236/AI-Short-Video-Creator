import '../styles/TextEffectTab.css';

export default function TextEffectTab({textEffects, selectedEffect, setSelectedEffect}) {
    return (
        <div className="text-effect-panel">
            <label htmlFor="textEffect">Text Effect</label>
            <select
            id="textEffect"
            value={selectedEffect ?? ""}
            onChange={(e) => setSelectedEffect(e.target.value)}
            >
            <option value="">None</option>
            {textEffects.map((effect) => (
                <option key={effect} value={effect}>
                {effect}
                </option>
            ))}
            </select>
        </div>
        
    )
}