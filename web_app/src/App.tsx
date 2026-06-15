import "./App.css";
import { useContext } from "react";
import {type PredictionContextType, PredictionContext} from "./PredictionContext";

function App() {
  const { apiStatus } = useContext(PredictionContext) as PredictionContextType;

  return (
    <>
      <section id="center"></section>

      <h1>API Status: {apiStatus}</h1>

      <div className="ticks"></div>

      <section id="spacer"></section>
    </>
  );
}

export default App;
