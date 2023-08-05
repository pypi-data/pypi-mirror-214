import { CategoricalPalette, ConstantPalette, ContinuousPalette } from '../palettes';
export interface ColorsState {
    constantPalette: ConstantPalette;
    categoricalPalette: CategoricalPalette;
    continuousPalette: ContinuousPalette;
    useRobustColorScales: boolean;
    setConstantPalette: (palette?: ConstantPalette) => void;
    setCategoricalPalette: (palette?: CategoricalPalette) => void;
    setContinuousPalette: (palette?: ContinuousPalette) => void;
    setUseRobustColorScales: (useRobust: boolean) => void;
}
export declare const useColors: import("zustand").UseBoundStore<Omit<import("zustand").StoreApi<ColorsState>, "persist"> & {
    persist: {
        setOptions: (options: Partial<import("zustand/middleware").PersistOptions<ColorsState, any>>) => void;
        clearStorage: () => void;
        rehydrate: () => void | Promise<void>;
        hasHydrated: () => boolean;
        onHydrate: (fn: (state: ColorsState) => void) => () => void;
        onFinishHydration: (fn: (state: ColorsState) => void) => () => void;
        getOptions: () => Partial<import("zustand/middleware").PersistOptions<ColorsState, any>>;
    };
}>;
