import { useContext } from "react";
import { PredictionContext, type PredictionContextType } from "../PredictionContext";

function ModelSelector() {
    const { selectedModel, setSelectedModel } = useContext(PredictionContext) as PredictionContextType;

    const handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newModel = event.target.value as 'dense' | 'convolutional';
        setSelectedModel(newModel);
    }

    return (
        <div className="app-shell__selector">
            <label>Select a model:</label>
            <select value={selectedModel} onChange={handleModelChange}>
                <option value="dense">Dense</option>
                <option value="convolutional">Convolutional</option>
            </select>
        </div>
    );
}

export default ModelSelector;