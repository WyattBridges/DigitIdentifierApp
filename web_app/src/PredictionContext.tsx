import { createContext, useState, useRef, useEffect } from "react";

export interface PredictionContextType {
    apiStatus : 'ready' | 'predicting' | 'not_available'
    selectedModel : 'dense' | 'convolutional'
    grid : number[][]
    mostRecentPrediction : number[]
    setSelectedModel : (model: 'dense' | 'convolutional') => void
    setGridValue : (row: number, col: number, value: number) => void
    setPredictionValue : (index: number, value: number) => void
}

export const PredictionContext = createContext<PredictionContextType | undefined>(undefined);

export const PredictionProvider = ({ children }: { children: React.ReactNode }) => {
    const [apiStatus, setApiStatus] = useState<'ready' | 'predicting' | 'not_available'>('not_available');
    const [selectedModel, setSelectedModel] = useState<'dense' | 'convolutional'>('dense');
    const grid = useRef<number[][]>(Array(28).fill(Array(28).fill(0)));
    const mostRecentPrediction = useRef<number[]>(Array(10).fill(0));

    // Define callbacks for updating grid and prediction values
    const setGridValue = (row: number, col: number, value: number) => {
        grid.current[row][col] = value;
    }

    const setPredictionValue = (index: number, value: number) => {
        mostRecentPrediction.current[index] = value;
    }

    // Fetch API status on mount
    const checkApiStatus = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/health");
            const data = await response.json();
            if (data.status == "ok") setApiStatus("ready");
        } catch (error) {
            console.error("Error fetching API status:", error);
            setApiStatus('not_available');
        }
    };

    useEffect(() => {
        checkApiStatus();
    }, []);

    // Return the provider with the context value
    return (
        <PredictionContext.Provider value={{ apiStatus, selectedModel, grid: grid.current, mostRecentPrediction: mostRecentPrediction.current, setSelectedModel, setGridValue, setPredictionValue }}>
            {children}
        </PredictionContext.Provider>
    );
}
