import "./App.css";
import { useContext } from "react";
import {type PredictionContextType, PredictionContext} from "./PredictionContext";
import GrayscalePainter from "./components/GrayscalePainter";
import ModelSelector from "./components/ModelSelector";
import ResultsDisplay from "./components/ResultsDisplay";

function App() {
  const { apiStatus, selectedModel, mostRecentPrediction, getPrediction } = useContext(PredictionContext) as PredictionContextType;

  const handlePrediction = async () => {
    await getPrediction();
    console.log("Full Prediction Results:");
    console.log(mostRecentPrediction);
  };

  return (
    <main className="app-shell">
      <section className="app-shell__intro">
        <p className="app-shell__eyebrow">Digit Identifier App</p>
        <h1>Sketch a digit in grayscale</h1>
        <p>
          Paint on a 28 by 28 pixel grid, tune the brush, and send the canvas to the {selectedModel} model when you are ready.
        </p>
      </section>

      <GrayscalePainter />

      <section className="app-shell__footer">
        <div className="app-shell__status">
          <span>API status</span>
          <strong>{apiStatus}</strong>
        </div>

        <ModelSelector />

        <button className="app-shell__predict" type="button" onClick={handlePrediction} disabled={apiStatus !== "ready"}>
          Get Prediction
        </button>
      </section>
      <ResultsDisplay />
    </main>
  );
}

export default App;
