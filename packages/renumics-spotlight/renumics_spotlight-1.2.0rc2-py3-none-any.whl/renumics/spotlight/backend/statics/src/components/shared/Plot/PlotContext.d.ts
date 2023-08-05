import * as d3 from 'd3';
import { Dispatch, MutableRefObject, RefObject, SetStateAction } from 'react';
import { Margin, Point2d } from './types';
interface PlotContextValue {
    canvas: HTMLCanvasElement | null;
    svgRef: RefObject<SVGSVGElement>;
    width: number;
    height: number;
    margin: Margin;
    plotAreaWidth: number;
    plotAreaHeight: number;
    transformRef: MutableRefObject<d3.ZoomTransform>;
    transform: d3.ZoomTransform;
    setTransform: Dispatch<SetStateAction<d3.ZoomTransform>>;
    zoom: ReturnType<typeof d3.zoom>;
    isPointHighlighted: (index: number) => boolean;
    setHighlightedPoint: (index: number | undefined) => void;
    hoveredIndex: number | undefined;
    setHoveredIndex: (index: number | undefined) => void;
    xRange: [number, number];
    yRange: [number, number];
    xScale: d3.ScaleLinear<number, number>;
    yScale: d3.ScaleLinear<number, number>;
    setXScale: Dispatch<SetStateAction<d3.ScaleLinear<number, number>>>;
    setYScale: Dispatch<SetStateAction<d3.ScaleLinear<number, number>>>;
    points: Point2d[];
}
declare const PlotContext: import("react").Context<PlotContextValue>;
export default PlotContext;
