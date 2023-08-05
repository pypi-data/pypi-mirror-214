import { Color } from 'chroma-js';
import { DataType } from '../datatypes';
type BaseTransferFunction = {
    (val: any): Color;
    paletteName: string;
    kind: 'continuous' | 'categorical' | 'constant';
    dType: DataType;
};
export interface CategoricalTransferFunction extends BaseTransferFunction {
    kind: 'categorical';
    domain: any[];
}
export interface ContinuousTransferFunction extends BaseTransferFunction {
    kind: 'continuous';
    domain: [number, number];
    classBreaks?: number[];
}
export interface ConstantTransferFunction extends BaseTransferFunction {
    kind: 'constant';
}
export type TransferFunction = CategoricalTransferFunction | ContinuousTransferFunction | ConstantTransferFunction;
export declare const createContinuousTransferFunction: (min: number, max: number, dType: DataType, classBreaks?: number[]) => ContinuousTransferFunction;
export declare const createCategoricalTransferFunction: (values: any[], dType: DataType) => CategoricalTransferFunction;
export declare const createConstantTransferFunction: (dType?: DataType) => ConstantTransferFunction;
export declare const useColorTransferFunction: (data: any[], dtype: DataType) => TransferFunction;
export default useColorTransferFunction;
