export interface AvailableModel {
    name: string
    description: string
    endpoint_extension: string
}

export interface PredictionContextType {
    apiStatus : 'ready' | 'predicting' | 'not_available'
    selectedModel : string
    availableModels: AvailableModel[]
    grid : number[][]
    mostRecentPrediction : number[]
    setSelectedModel : (model: string) => void
    setGridValue : (row: number, col: number, value: number) => void
    getPrediction : () => Promise<void>
}
