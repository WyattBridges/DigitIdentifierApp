import { useContext, useEffect, useReducer, useRef, useState } from "react";
import { PredictionContext, type PredictionContextType } from "../PredictionContext";
import penIcon from "../assets/pen-tool.svg";
import radiusIcon from "../assets/radius-tool.svg";
import clearIcon from "../assets/clear-tool.svg";

const GRID_SIZE = 28;
const MIN_PIXEL_VALUE = 0;
const MAX_PIXEL_VALUE = 255;
const MIN_BRUSH_RADIUS = 1;
const MAX_BRUSH_RADIUS = 10;
const DEFAULT_PEN_VALUE = 255;
const DEFAULT_BRUSH_RADIUS = 3;

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

function GrayscalePainter() {
	const { grid, setGridValue } = useContext(PredictionContext) as PredictionContextType;
	const [penValue, setPenValue] = useState(DEFAULT_PEN_VALUE);
	const [brushRadius, setBrushRadius] = useState(DEFAULT_BRUSH_RADIUS);
	const isDrawing = useRef(false);
	const [, forceRender] = useReducer((value: number) => value + 1, 0);

	useEffect(() => {
		const stopDrawing = () => {
			isDrawing.current = false;
		};

		window.addEventListener("pointerup", stopDrawing);
		window.addEventListener("pointercancel", stopDrawing);

		return () => {
			window.removeEventListener("pointerup", stopDrawing);
			window.removeEventListener("pointercancel", stopDrawing);
		};
	}, []);

	const paintAtCell = (centerRow: number, centerCol: number) => {
		const radiusSquared = brushRadius * brushRadius;

		for (let row = centerRow - brushRadius; row <= centerRow + brushRadius; row += 1) {
			if (row < 0 || row >= GRID_SIZE) continue;

			for (let col = centerCol - brushRadius; col <= centerCol + brushRadius; col += 1) {
				if (col < 0 || col >= GRID_SIZE) continue;

				const distanceSquared = (row - centerRow) ** 2 + (col - centerCol) ** 2;
				if (distanceSquared <= radiusSquared) {
					setGridValue(row, col, penValue);
				}
			}
		}

		forceRender();
	};

	const handlePointerDown = (row: number, col: number) => {
		isDrawing.current = true;
		paintAtCell(row, col);
	};

	const handlePointerEnter = (row: number, col: number) => {
		if (!isDrawing.current) return;
		paintAtCell(row, col);
	};

	const clearCanvas = () => {
		for (let row = 0; row < GRID_SIZE; row += 1) {
			for (let col = 0; col < GRID_SIZE; col += 1) {
				setGridValue(row, col, MIN_PIXEL_VALUE);
			}
		}

		forceRender();
	};

	return (
		<section className="painter">
			<div className="painter__header">
				<div>
					<p className="painter__eyebrow">Canvas</p>
					<h2>28 by 28 grayscale grid</h2>
				</div>
				<button className="painter__clear" type="button" onClick={clearCanvas}>
					<img src={clearIcon} alt="" aria-hidden="true" />
					Clear canvas
				</button>
			</div>

			<div className="painter__controls">
				<label className="painter__control">
					<span className="painter__control-label">
						<img src={penIcon} alt="" aria-hidden="true" />
						Pen brightness
					</span>
					<input
						type="range"
						min={MIN_PIXEL_VALUE}
						max={MAX_PIXEL_VALUE}
						step={1}
						value={penValue}
						onChange={(event) => setPenValue(clamp(Number(event.target.value), MIN_PIXEL_VALUE, MAX_PIXEL_VALUE))}
					/>
					<strong>{penValue}</strong>
				</label>

				<label className="painter__control">
					<span className="painter__control-label">
						<img src={radiusIcon} alt="" aria-hidden="true" />
						Brush radius
					</span>
					<input
						type="range"
						min={MIN_BRUSH_RADIUS}
						max={MAX_BRUSH_RADIUS}
						step={1}
						value={brushRadius}
						onChange={(event) => setBrushRadius(clamp(Number(event.target.value), MIN_BRUSH_RADIUS, MAX_BRUSH_RADIUS))}
					/>
					<strong>{brushRadius}px</strong>
				</label>
			</div>

			<div className="painter__canvas" aria-label="Grayscale drawing grid" role="img">
				{grid.map((row, rowIndex) =>
					row.map((value, colIndex) => (
						<div
							key={`${rowIndex}-${colIndex}`}
							className="painter__pixel"
							data-row={rowIndex}
							data-col={colIndex}
							onPointerDown={() => handlePointerDown(rowIndex, colIndex)}
							onPointerEnter={() => handlePointerEnter(rowIndex, colIndex)}
							style={{ backgroundColor: `rgb(${value}, ${value}, ${value})` }}
						/>
					)),
				)}
			</div>

			<p className="painter__hint">
				Drag across the grid to paint. Brightness writes values between 0 and 255, and radius controls the circular brush size.
			</p>
		</section>
	);
}

export default GrayscalePainter;
