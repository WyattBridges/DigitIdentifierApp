import "./App.css";
import { useContext } from "react";
import {type PredictionContextType, PredictionContext} from "./PredictionContext";

function App() {
  const { apiStatus, mostRecentPrediction, getPrediction } = useContext(PredictionContext) as PredictionContextType;

  return (
    <>
      <section id="center">
        <h1>API Status: {apiStatus}</h1>
      </section>

      <button onClick={() => {
        getPrediction().then(() => {console.log(mostRecentPrediction)});
      }}>Get Prediction</button>

      <div className="ticks"></div>

      <section id="spacer"></section>
    </>
  );
}

export default App;
