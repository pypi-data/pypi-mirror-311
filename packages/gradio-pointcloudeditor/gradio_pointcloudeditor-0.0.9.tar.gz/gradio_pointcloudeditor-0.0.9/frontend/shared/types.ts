import type * as THREE from 'three';

export interface Point {
    position: THREE.Vector3;
    color: THREE.Color;
}

export interface PointCloudData {
    positions: number[][];
    colors: number[][];
}

export interface EditorState {
    hoveredPoint: number | null;
    lastSelectedPoint: number | null;
    dragging: boolean;
    currentIndex: number | null;
}

export interface ColorPickerState {
    red: number;
    green: number;
    blue: number;
    hex: string;
} 