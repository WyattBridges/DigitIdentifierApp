import { createContext, useState, useRef, useEffect } from "react";
import { type AvailableModel, type PredictionContextType } from "./types";

const createEmptyGrid = () => Array.from({ length: 28 }, () => Array.from({ length: 28 }, () => 0));
const createEmptyPrediction = () => Array.from({ length: 10 }, () => 0);

export const PredictionContext = createContext<PredictionContextType | undefined>(undefined);

export const PredictionProvider = ({ children }: { children: React.ReactNode }) => {
    const [apiStatus, setApiStatus] = useState<'ready' | 'predicting' | 'not_available'>('not_available');
    const [selectedModel, setSelectedModel] = useState<string>('');
    const availableModels = useRef<AvailableModel[]>([]);
    const grid = useRef<number[][]>(createEmptyGrid());
    const mostRecentPrediction = useRef<number[]>(createEmptyPrediction());

    // Define callbacks for updating grid and prediction values
    const setGridValue = (row: number, col: number, value: number) => {
        if (row < 0 || row >= grid.current.length) return;
        if (col < 0 || col >= grid.current[row].length) return;
        const nextValue = Math.max(0, Math.min(255, Math.round(value)));
        grid.current[row][col] = nextValue;
    }

    const setPredictionValue = (index: number, value: number) => {
        mostRecentPrediction.current[index] = value;
    }

    // Fetch API status on startup
    const checkApiStatus = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/health");
            const data = await response.json();
            if (data.status == "ok") setApiStatus("ready");
            else setApiStatus("not_available");
        } catch (error) {
            console.error("Error fetching API status:", error);
            setApiStatus('not_available');
        }
    };

    useEffect(() => {
        checkApiStatus();
    }, []);

    // Fetch available models on startup
    const getAvailableModels = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/available_models");
            const data = await response.json();
            availableModels.current = data["models"].map((model: any) => {
                let m : AvailableModel = {
                    name: model["Name"],
                    description: model["Description"],
                    endpoint_extension: model["Endpoint Extension"]
                };
                return m;
            });
            setSelectedModel(availableModels.current[0]?.endpoint_extension || '');
        }
        catch (error) {
            console.error("Error fetching available models:", error);
        }
    }

    useEffect(() => {
        getAvailableModels();
    }, []);

    // Define function to get predictions from the API
    const getPrediction = async () => {
        if (apiStatus !== 'ready') return;
        setApiStatus('predicting');
        try {
            const response = await fetch(`http://localhost:8000/api/predict/${selectedModel}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    pixels: grid.current.map((row) => [...row])
                })
            });
            const data = await response.json();
            if (data.values) {
                data.values.forEach((value: number, index: number) => {
                    setPredictionValue(index, value);
                });
            } else {
                console.error("Invalid prediction response:", data);
            }
        } catch (error) {
            console.error("Error fetching prediction:", error);
        } finally {
            setApiStatus('ready');
        }
    };

    // Return the provider with the context value
    return (
        <PredictionContext.Provider value={{ apiStatus, selectedModel, grid: grid.current, mostRecentPrediction: mostRecentPrediction.current, setSelectedModel, setGridValue, getPrediction, availableModels: availableModels.current }}>
            {children}
        </PredictionContext.Provider>
    );
}
