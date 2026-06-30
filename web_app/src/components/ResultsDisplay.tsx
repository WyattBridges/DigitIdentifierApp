import { useContext } from "react";
import { PredictionContext, type PredictionContextType } from "../PredictionContext";

const digits = Array.from({ length: 10 }, (_, i) => i);

function ResultsDisplay() {
    const { mostRecentPrediction } = useContext(PredictionContext) as PredictionContextType;

    return (
        <>
            <h2>Prediction Results</h2>
            <table className="app-shell_results">
                <thead>
                    <tr>
                        <th className="app-shell_results">Digit</th>
                        <th className="app-shell_results">Probability</th>
                    </tr>
                </thead>
                <tbody>
                    {digits.map((digit, index) => (
                        <tr key={digit}>
                            <td className="app-shell_results">{digit}</td>
                            <td className="app-shell_results">{mostRecentPrediction[index].toFixed(5)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    )
}

export default ResultsDisplay;