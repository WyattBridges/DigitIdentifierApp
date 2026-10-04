import { useContext } from "react";
import { PredictionContext } from "../PredictionContext";
import { type AvailableModel, type PredictionContextType } from "../types";

function ModelSelector() {
    const { selectedModel, setSelectedModel, availableModels } = useContext(PredictionContext) as PredictionContextType;

    const handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedModel(event.target.value);
    }

    return (
        <div className="app-shell__selector">
            <label>Select a model:</label>
            <select value={selectedModel} onChange={handleModelChange}>
                {availableModels.map((model: AvailableModel) => (
                    <option key={model.name} value={model.endpoint_extension} title={model.description}>
                        {model.name}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default ModelSelector;