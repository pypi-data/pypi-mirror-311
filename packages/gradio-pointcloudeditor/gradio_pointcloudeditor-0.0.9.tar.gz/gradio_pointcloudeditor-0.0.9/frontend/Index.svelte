<script lang="ts">
	import { onMount, onDestroy } from "svelte";
	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import * as THREE from "three";
	import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
	import type {
		Point,
		PointCloudData,
		EditorState,
		ColorPickerState,
	} from "./shared/types";
	import { Box3, BoxHelper, Vector3, Matrix4 } from "three";

	export let elem_id: string = "";
	export let elem_classes: string[] = [];
	export let visible: boolean = true;
	export let value: PointCloudData | null = null;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let point_size: number = 0.2;
	export let clear_color: number[] | null = null; // Set clear_color to null by default
	export let gradio: Gradio<{
		change: never;
		upload: never;
		edit: never;
	}>;
	export let up_axis: "X" | "Y" | "Z" = "Y";
	export let forward_axis: "X" | "Y" | "Z" = "Z";
	export let lock_scale_x: boolean = false;
	export let lock_scale_y: boolean = false;
	export let lock_scale_z: boolean = false;

	let editorContainer: HTMLDivElement;
	let scene: THREE.Scene;
	let camera: THREE.PerspectiveCamera;
	let renderer: THREE.WebGLRenderer;
	let controls: OrbitControls;
	let points: THREE.Points;
	let raycaster: THREE.Raycaster;
	let mouse: THREE.Vector2;
	let plane: THREE.Plane;
	let planeNormal: THREE.Vector3;
	let planePoint: THREE.Vector3;
	let boundingBox: THREE.Box3;
	let boxHelper: THREE.BoxHelper;
	let isScalingMode = false;
	let scaleStartPoint: THREE.Vector3;
	let originalPoints: Float32Array;
	let currentScale = new Vector3(1, 1, 1);
	let dragStartScale: Vector3;
	let scalingCenter: THREE.Vector3;
	let coordinate_system = {
		up: "Y" as "X" | "Y" | "Z", // Default from backend
		forward: "Z" as "X" | "Y" | "Z", // Default from backend
	};
	let scale_locks = {
		x: false,
		y: false,
		z: false,
	};

	// Track previous point size
	let previousPointSize = 0;

	// Add this to track previous coordinate system state
	let previousCoordinateSystem = {
		up: "Y" as "X" | "Y" | "Z",
		forward: "Z" as "X" | "Y" | "Z",
	};

	$: coordinate_system = {
		up: up_axis,
		forward: forward_axis,
	};
	$: scale_locks = {
		x: lock_scale_x,
		y: lock_scale_y,
		z: lock_scale_z,
	};

	// Modify the reactive statement to check for actual changes
	$: if (
		coordinate_system &&
		points &&
		(coordinate_system.up !== previousCoordinateSystem.up ||
			coordinate_system.forward !== previousCoordinateSystem.forward)
	) {
		updateCoordinateSystem();
		// Update previous state after the change
		previousCoordinateSystem = { ...coordinate_system };
	}

	function getBackgroundColor() {
		// Assuming gradio.theme.backgroundColor is available
		return gradio.theme === "light" ? [1, 1, 1] : [0.94, 0.94, 0.94];
	}

	// Add a computed value for the background color
	$: backgroundColor = clear_color ? clear_color : getBackgroundColor();

	const HOVER_SCALE = 2;

	let state: EditorState = {
		hoveredPoint: null,
		lastSelectedPoint: null,
		dragging: false,
		currentIndex: null,
	};

	// Add a computed value that updates when point_size changes
	$: hoverPointSize = point_size * HOVER_SCALE;

	let selectedPoints: number[] = []; // For multiselection

	// Add this to track shift key state
	let shiftPressed = false;

	// Add reactive statement to update raycaster threshold based on point size
	$: if (raycaster) {
		raycaster.params.Points.threshold = point_size * HOVER_SCALE * 0.25; // Scale factor can be adjusted
	}

	let currentData: PointCloudData | null = null; // Add this to track current state

	// Modify the value reactive statement to only load on external updates
	$: if (value) {
		if (
			!currentData ||
			JSON.stringify(value) !== JSON.stringify(currentData)
		) {
			onWindowResize();
			loadPointCloudData(value);
			currentData = value;
			centerCamera();
		}
	}

	// Add reactive statements to handle prop changes
	$: if (point_size && points && point_size !== previousPointSize) {
		previousPointSize = point_size;
		updateAllPointSizes(point_size);
	}

	onMount(() => {
		initScene();
		initEvents();

		if (value) {
			loadPointCloudData(value);
			if (
				!currentData ||
				JSON.stringify(value) !== JSON.stringify(currentData)
			) {
				currentData = value;
				centerCamera();
			}
		}

		animate();
	});

	onDestroy(() => {
		cleanup();
	});

	function initScene() {
		// Scene setup
		scene = new THREE.Scene();
		scene.background = new THREE.Color(...backgroundColor);

		camera = new THREE.PerspectiveCamera(
			60,
			editorContainer.clientWidth / editorContainer.clientHeight,
			1,
			1000,
		);
		camera.position.set(1.25, 7, 7);
		camera.lookAt(scene.position);

		renderer = new THREE.WebGLRenderer({ antialias: true });
		renderer.setSize(
			editorContainer.clientWidth,
			editorContainer.clientHeight,
		);
		editorContainer.appendChild(renderer.domElement);

		controls = new OrbitControls(camera, renderer.domElement);

		// Initialize raycaster without static threshold
		raycaster = new THREE.Raycaster();
		mouse = new THREE.Vector2();
		plane = new THREE.Plane();
		planeNormal = new THREE.Vector3();
		planePoint = new THREE.Vector3();

		updateCoordinateSystem();
		previousCoordinateSystem = { ...coordinate_system };
	}

	function initEvents() {
		window.addEventListener("resize", onWindowResize);
		editorContainer.addEventListener("mousemove", onMouseMove);
		editorContainer.addEventListener("mousedown", onMouseDown);
		editorContainer.addEventListener("mouseup", onMouseUp);
		// Add shift key tracking
		window.addEventListener("keydown", (e) => {
			if (e.key === "Shift") shiftPressed = true;
		});
		window.addEventListener("keyup", (e) => {
			if (e.key === "Shift") shiftPressed = false;
		});
	}

	function cleanup() {
		window.removeEventListener("resize", onWindowResize);
		editorContainer.removeEventListener("mousemove", onMouseMove);
		editorContainer.removeEventListener("mousedown", onMouseDown);
		editorContainer.removeEventListener("mouseup", onMouseUp);
		window.removeEventListener("keydown", (e) => {
			if (e.key === "Shift") shiftPressed = true;
		});
		window.removeEventListener("keyup", (e) => {
			if (e.key === "Shift") shiftPressed = false;
		});

		if (renderer) {
			renderer.dispose();
		}
		if (points) {
			points.geometry.dispose();
			(points.material as THREE.Material).dispose();
		}
	}

	function loadPointCloudData(data: PointCloudData) {
		if (
			!data ||
			!data.positions ||
			!data.colors ||
			data.positions.length === 0
		)
			return;

		const positions = new Float32Array(data.positions.length * 3);
		const colors = new Float32Array(data.positions.length * 3);
		const sizes = new Float32Array(data.positions.length);

		data.positions.forEach((pos, i) => {
			// Position
			positions[i * 3] = pos[0]; // x
			positions[i * 3 + 1] = pos[1]; // y
			positions[i * 3 + 2] = pos[2]; // z

			// Color
			colors[i * 3] = data.colors[i][0]; // r
			colors[i * 3 + 1] = data.colors[i][1]; // g
			colors[i * 3 + 2] = data.colors[i][2]; // b

			// Size
			sizes[i] = selectedPoints.includes(i) ? hoverPointSize : point_size;
		});

		const geometry = new THREE.BufferGeometry();
		geometry.setAttribute(
			"position",
			new THREE.BufferAttribute(positions, 3),
		);
		geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
		geometry.setAttribute("pointSize", new THREE.BufferAttribute(sizes, 1));

		if (points) {
			scene.remove(points);
		}

		const pointsMaterial = new THREE.PointsMaterial({
			vertexColors: true,
			sizeAttenuation: true,
			size: point_size,
			alphaTest: 0.5,
		});

		// Add shader modification for point size attribute
		pointsMaterial.onBeforeCompile = (shader) => {
			shader.vertexShader = shader.vertexShader
				.replace(
					"uniform float size;",
					"uniform float size;\nattribute float pointSize;",
				)
				.replace(
					"gl_PointSize = size;",
					"gl_PointSize = size * pointSize * 2.0;",
				);
		};

		points = new THREE.Points(geometry, pointsMaterial);
		scene.add(points);

		// Create bounding box after adding points
		createBoundingBox();
	}

	function onWindowResize() {
		if (!editorContainer) return;
		camera.aspect =
			editorContainer.clientWidth / editorContainer.clientHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(
			editorContainer.clientWidth,
			editorContainer.clientHeight,
		);
	}

	function onMouseMove(event: MouseEvent) {
		if (!points) return;

		const rect = editorContainer.getBoundingClientRect();
		mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
		mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
		raycaster.setFromCamera(mouse, camera);

		// Handle dragging
		if (state.dragging && selectedPoints.length > 0) {
			if (raycaster.ray.intersectPlane(plane, planePoint)) {
				// Store initial planePoint if not set
				if (!state.lastPlanePoint) {
					state.lastPlanePoint = planePoint.clone();
					return;
				}

				const delta = new THREE.Vector3().subVectors(
					planePoint,
					state.lastPlanePoint,
				);

				selectedPoints.forEach((index) => {
					const position = new THREE.Vector3();
					position.fromBufferAttribute(
						points.geometry.attributes.position,
						index,
					);
					position.add(delta);
					points.geometry.attributes.position.setXYZ(
						index,
						position.x,
						position.y,
						position.z,
					);
				});
				points.geometry.attributes.position.needsUpdate = true;
				state.lastPlanePoint.copy(planePoint);
				dispatchChange();
			}
			return;
		}

		// Handle hover effect
		const intersects = raycaster.intersectObject(points);
		const sizes = points.geometry.attributes.pointSize;

		// Reset previous hovered point size if it's not selected
		if (
			state.hoveredPoint !== null &&
			!selectedPoints.includes(state.hoveredPoint)
		) {
			sizes.setX(state.hoveredPoint, point_size);
			sizes.needsUpdate = true;
		}

		// Set new hovered point
		if (intersects.length > 0) {
			const index = intersects[0].index;
			if (!selectedPoints.includes(index)) {
				sizes.setX(index, hoverPointSize);
				sizes.needsUpdate = true;
			}
			state.hoveredPoint = index;
		} else {
			state.hoveredPoint = null;
		}
	}

	function dispatchChange() {
		if (!points) return;

		const positions = points.geometry.attributes.position;
		const colors = points.geometry.attributes.color;
		const positionData: number[][] = [];
		const colorData: number[][] = [];

		for (let i = 0; i < positions.count; i++) {
			positionData.push([
				positions.getX(i),
				positions.getY(i),
				positions.getZ(i),
			]);
			colorData.push([colors.getX(i), colors.getY(i), colors.getZ(i)]);
		}

		const data = {
			positions: positionData,
			colors: colorData,
		};

		// Create deep copies of the data
		currentData = data;
		value = data;

		// Dispatch the event to Gradio
		gradio.dispatch("edit");
	}

	function animate() {
		requestAnimationFrame(animate);
		if (isScalingMode && boxHelper) {
			boxHelper.visible = true; // Ensure visibility during scaling mode
			boxHelper.update();
		}
		if (controls.enabled) {
			controls.update();
		}
		renderer.render(scene, camera);
	}

	function onMouseDown(event: MouseEvent) {
		if (isScalingMode) {
			const rect = editorContainer.getBoundingClientRect();
			mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
			mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

			raycaster.setFromCamera(mouse, camera);
			scaleStartPoint = new Vector3();
			raycaster.ray.intersectPlane(plane, scaleStartPoint);

			// Store the scale at the start of this drag
			dragStartScale = currentScale.clone();

			editorContainer.addEventListener("mousemove", handleScaling);
			return;
		}

		// Don't process if clicking inside color picker
		const colorPicker = document.querySelector(".color-picker");
		if (colorPicker?.contains(event.target as Node)) {
			return;
		}

		const rect = editorContainer.getBoundingClientRect();
		mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
		mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
		raycaster.setFromCamera(mouse, camera);

		const intersects = raycaster.intersectObject(points);
		if (intersects.length > 0) {
			state.currentIndex = intersects[0].index;

			if (shiftPressed) {
				// Multi-select mode
				const index = state.currentIndex;
				const isSelected = selectedPoints.includes(index);

				if (isSelected) {
					// Deselect point
					unhighlightPoint(index);
					selectedPoints = selectedPoints.filter((i) => i !== index);
				} else {
					// Add to selection
					selectedPoints = [...selectedPoints, index];
					highlightPoint(index);
				}
				state.lastSelectedPoint = index;
			} else {
				// Single select mode
				clearSelection();
				selectedPoints = [state.currentIndex];
				highlightPoint(state.currentIndex);
				state.lastSelectedPoint = state.currentIndex;
			}

			// Set up the plane for dragging
			const position = new THREE.Vector3();
			position.fromBufferAttribute(
				points.geometry.attributes.position,
				state.currentIndex,
			);
			planeNormal.copy(camera.position).sub(position).normalize();
			plane.setFromNormalAndCoplanarPoint(planeNormal, position);

			// Show color picker
			showColorPicker(event);

			state.dragging = true;
			controls.enabled = false;
		} else {
			// Clicked empty space
			if (!shiftPressed) {
				clearSelection();
				const colorPicker = document.querySelector(".color-picker");
				if (colorPicker) {
					colorPicker.classList.add("hidden");
				}
			}
			state.currentIndex = null;
			state.lastSelectedPoint = null;

			controls.enabled = true;
		}
	}

	function onMouseUp(event: MouseEvent) {
		if (isScalingMode) {
			editorContainer.removeEventListener("mousemove", handleScaling);
			scaleStartPoint = null;
			dragStartScale = null;
			return;
		}

		if (state.dragging) {
			points?.geometry.computeBoundingSphere();
			// Update bounding box only after drag is complete
			if (boundingBox && points) {
				boundingBox.setFromObject(points);
			}
		}
		state.dragging = false;
		state.currentIndex = null;
		state.lastPlanePoint = undefined;
		controls.enabled = true;
	}

	// Add new function to update all point sizes
	function updateAllPointSizes(size: number) {
		if (!points) return;
		const sizes = points.geometry.attributes.pointSize;
		for (let i = 0; i < sizes.count; i++) {
			if (!selectedPoints.includes(i)) {
				sizes.setX(i, size);
			}
		}
		sizes.needsUpdate = true;

		// Update the material's base size
		(points.material as THREE.PointsMaterial).size = size;
	}

	// Add these helper functions
	function highlightPoint(index: number) {
		if (!points) return;
		const sizes = points.geometry.attributes.pointSize;
		sizes.setX(index, hoverPointSize);
		sizes.needsUpdate = true;
	}

	function unhighlightPoint(index: number) {
		if (!points) return;
		const sizes = points.geometry.attributes.pointSize;
		sizes.setX(index, point_size);
		sizes.needsUpdate = true;
	}

	function clearSelection() {
		selectedPoints.forEach((index) => {
			unhighlightPoint(index);
		});
		selectedPoints = [];
	}

	function showColorPicker(event: MouseEvent) {
		const colorPicker = document.querySelector(".color-picker");
		if (!colorPicker || selectedPoints.length === 0 || !points) return;

		// Get the last selected point's position
		const index = selectedPoints[selectedPoints.length - 1];
		const position = new THREE.Vector3();
		position.fromBufferAttribute(
			points.geometry.attributes.position,
			index,
		);

		// Project the 3D position to 2D screen coordinates
		const screenPosition = position.clone();
		screenPosition.project(camera);

		// Convert to pixel coordinates relative to the editor container
		const rect = editorContainer.getBoundingClientRect();
		const x = ((screenPosition.x + 1) / 2) * rect.width;
		const y = ((-screenPosition.y + 1) / 2) * rect.height;

		// Position the color picker with offset, keeping it within the editor bounds
		colorPicker.classList.remove("hidden");
		(colorPicker as HTMLElement).style.left = `${x + 20}px`; // 20px offset right
		(colorPicker as HTMLElement).style.top = `${y - 20}px`; // 20px offset up

		// Update color picker values
		const colors = points.geometry.attributes.color;
		updateColorPickerValues(
			colors.getX(index),
			colors.getY(index),
			colors.getZ(index),
		);
	}

	// Add color picker HTML and functionality
	function updateColorPickerValues(r: number, g: number, b: number) {
		// Update color picker inputs with the given RGB values
		// Implementation depends on your color picker UI components
		const colorPicker = document.querySelector(".color-picker");
		if (!colorPicker) return;

		// Update color preview
		const preview = colorPicker.querySelector(
			".color-preview",
		) as HTMLElement;
		if (preview) {
			preview.style.backgroundColor = `rgb(${r * 255}, ${g * 255}, ${b * 255})`;
		}

		// Update sliders
		const redSlider = colorPicker.querySelector(
			".red-slider",
		) as HTMLInputElement;
		const greenSlider = colorPicker.querySelector(
			".green-slider",
		) as HTMLInputElement;
		const blueSlider = colorPicker.querySelector(
			".blue-slider",
		) as HTMLInputElement;

		if (redSlider) redSlider.value = r.toString();
		if (greenSlider) greenSlider.value = g.toString();
		if (blueSlider) blueSlider.value = b.toString();

		// Update number inputs
		const redNumber = colorPicker.querySelector(
			".red-number",
		) as HTMLInputElement;
		const greenNumber = colorPicker.querySelector(
			".green-number",
		) as HTMLInputElement;
		const blueNumber = colorPicker.querySelector(
			".blue-number",
		) as HTMLInputElement;

		if (redNumber) redNumber.value = Math.round(r * 255).toString();
		if (greenNumber) greenNumber.value = Math.round(g * 255).toString();
		if (blueNumber) blueNumber.value = Math.round(b * 255).toString();
	}

	// Add these utility functions
	function normalizedToInt(value: number): number {
		return Math.round(value * 255);
	}

	function intToNormalized(value: number): number {
		return value / 255;
	}

	function rgbToHex(r: number, g: number, b: number): string {
		const toHex = (n: number) => {
			const hex = n.toString(16);
			return hex.length === 1 ? "0" + hex : hex;
		};
		return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
	}

	function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
		const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
		return result
			? {
					r: parseInt(result[1], 16),
					g: parseInt(result[2], 16),
					b: parseInt(result[3], 16),
				}
			: null;
	}

	// Add function to update all inputs and point colors
	function updateAllInputs(event: Event) {
		const colorPicker = document.querySelector(".color-picker");
		if (!colorPicker || selectedPoints.length === 0) return;

		const target = event.target as HTMLInputElement;
		const isSlider = target.type === "range";
		const isNumber = target.type === "number";
		const isHex = target.classList.contains("hex-input");

		let r: number, g: number, b: number;

		if (isHex) {
			const rgb = hexToRgb(target.value);
			if (!rgb) return;
			r = intToNormalized(rgb.r);
			g = intToNormalized(rgb.g);
			b = intToNormalized(rgb.b);
		} else {
			const redSlider = colorPicker.querySelector(
				".red-slider",
			) as HTMLInputElement;
			const greenSlider = colorPicker.querySelector(
				".green-slider",
			) as HTMLInputElement;
			const blueSlider = colorPicker.querySelector(
				".blue-slider",
			) as HTMLInputElement;
			const redNumber = colorPicker.querySelector(
				".red-number",
			) as HTMLInputElement;
			const greenNumber = colorPicker.querySelector(
				".green-number",
			) as HTMLInputElement;
			const blueNumber = colorPicker.querySelector(
				".blue-number",
			) as HTMLInputElement;
			const hexInput = colorPicker.querySelector(
				".hex-input",
			) as HTMLInputElement;

			if (isSlider) {
				r = parseFloat(redSlider.value);
				g = parseFloat(greenSlider.value);
				b = parseFloat(blueSlider.value);

				// Update number inputs
				redNumber.value = normalizedToInt(r).toString();
				greenNumber.value = normalizedToInt(g).toString();
				blueNumber.value = normalizedToInt(b).toString();
			} else if (isNumber) {
				r = intToNormalized(parseInt(redNumber.value));
				g = intToNormalized(parseInt(greenNumber.value));
				b = intToNormalized(parseInt(blueNumber.value));

				// Update sliders
				redSlider.value = r.toString();
				greenSlider.value = g.toString();
				blueSlider.value = b.toString();
			}

			// Update hex input
			hexInput.value = rgbToHex(
				normalizedToInt(r),
				normalizedToInt(g),
				normalizedToInt(b),
			);
		}

		// Only update the preview, not the actual points
		const preview = colorPicker.querySelector(
			".color-preview",
		) as HTMLElement;
		preview.style.backgroundColor = `rgb(${normalizedToInt(r)}, ${normalizedToInt(g)}, ${normalizedToInt(b)})`;
	}

	// Add new function to apply colors
	function applyColors() {
		const colorPicker = document.querySelector(".color-picker");
		if (!colorPicker || selectedPoints.length === 0 || !points) return;

		// Get current color values from inputs
		const redSlider = colorPicker.querySelector(
			".red-slider",
		) as HTMLInputElement;
		const greenSlider = colorPicker.querySelector(
			".green-slider",
		) as HTMLInputElement;
		const blueSlider = colorPicker.querySelector(
			".blue-slider",
		) as HTMLInputElement;

		const r = parseFloat(redSlider.value);
		const g = parseFloat(greenSlider.value);
		const b = parseFloat(blueSlider.value);

		// Update point colors
		selectedPoints.forEach((index) => {
			const colors = points.geometry.attributes.color;
			colors.setXYZ(index, r, g, b);
		});
		points.geometry.attributes.color.needsUpdate = true;

		// Hide color picker and clear selection
		colorPicker.classList.add("hidden");
		clearSelection();
		dispatchChange();
	}

	// Add this function definition
	function centerCamera() {
		if (!points || !camera || !controls) return;

		// Get the bounding sphere
		const boundingSphere = new THREE.Sphere();
		points.geometry.computeBoundingSphere();
		boundingSphere.copy(points.geometry.boundingSphere);

		// Define basis vectors based on coordinate system selection
		const basisVectors = {
			X: new Vector3(1, 0, 0),
			Y: new Vector3(0, 1, 0),
			Z: new Vector3(0, 0, 1),
			"-X": new Vector3(-1, 0, 0),
			"-Y": new Vector3(0, -1, 0),
			"-Z": new Vector3(0, 0, -1),
		};

		const upVector = basisVectors[coordinate_system.up];
		const forwardVector = basisVectors[coordinate_system.forward];

		// Calculate camera distance based on bounding sphere
		const fov = camera.fov * (Math.PI / 180);
		const distance = (boundingSphere.radius * 2) / Math.tan(fov / 2);

		// Position camera along forward direction
		const position = boundingSphere.center
			.clone()
			.add(forwardVector.clone().multiplyScalar(distance * 1.5));

		// Update camera
		camera.position.copy(position);
		camera.up.copy(upVector);
		camera.lookAt(boundingSphere.center);

		// Dispose and recreate controls
		controls.dispose();
		controls = new OrbitControls(camera, renderer.domElement);

		// Update controls
		controls.update();
	}

	function createBoundingBox() {
		if (!points) return;

		// Create bounding box
		boundingBox = new Box3().setFromObject(points);

		// Create visible box helper
		if (boxHelper) scene.remove(boxHelper);
		boxHelper = new BoxHelper(points, 0xff0000);
		boxHelper.visible = false; // Hidden by default
		scene.add(boxHelper);
	}

	function toggleScalingMode() {
		isScalingMode = !isScalingMode;
		if (!points || !boxHelper) return;

		boxHelper.visible = true;

		if (isScalingMode) {
			// Create a deep copy of the position array
			originalPoints = Float32Array.from(
				points.geometry.attributes.position.array,
			);
			currentScale = new Vector3(1, 1, 1);
			controls.enabled = false;

			// Calculate and store the center point once
			scalingCenter = boundingBox.getCenter(new Vector3());

			// Determine a stable plane normal
			const worldUp = new Vector3(0, 1, 0);
			const cameraDirection = camera.getWorldDirection(new Vector3());

			// Check if the camera is near the poles
			if (Math.abs(cameraDirection.y) > 0.9) {
				// Use a stable normal when near the poles
				planeNormal.copy(worldUp);
			} else {
				// Use the camera's direction otherwise
				planeNormal.copy(cameraDirection);
			}

			plane.setFromNormalAndCoplanarPoint(planeNormal, scalingCenter);
		} else {
			originalPoints = Float32Array.from(
				points.geometry.attributes.position.array,
			);
			controls.enabled = true;
			boxHelper.visible = false;
			scalingCenter = null;
		}
	}

	function handleScaling(event: MouseEvent) {
		if (!isScalingMode || !points || !boundingBox) return;

		const rect = editorContainer.getBoundingClientRect();

		// Check if mouse is outside bounds
		if (
			event.clientX < rect.left ||
			event.clientX > rect.right ||
			event.clientY < rect.top ||
			event.clientY > rect.bottom
		) {
			onMouseUp(event);
			return;
		}

		mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
		mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

		raycaster.setFromCamera(mouse, camera);

		if (scaleStartPoint) {
			const currentPoint = new Vector3();
			raycaster.ray.intersectPlane(plane, currentPoint);

			const delta = currentPoint.sub(scaleStartPoint);

			// Get camera's orientation vectors
			const cameraRight = new Vector3();
			const cameraUp = new Vector3();
			const cameraForward = new Vector3();
			camera.matrixWorld.extractBasis(
				cameraRight,
				cameraUp,
				cameraForward,
			);
			cameraForward.multiplyScalar(-1);

			// Project delta onto camera's view plane
			const horizontalDelta = delta.dot(cameraRight);
			const verticalDelta = delta.dot(cameraUp);

			// Calculate scale factors based on camera orientation and lock settings
			const scaleFactor = 0.25;

			const scaleX =
				1 +
				Math.sign(horizontalDelta) *
					Math.abs(
						horizontalDelta * cameraRight.x +
							verticalDelta * cameraUp.x,
					) *
					scaleFactor;
			const scaleY =
				1 +
				Math.sign(verticalDelta) *
					Math.abs(
						horizontalDelta * cameraRight.y +
							verticalDelta * cameraUp.y,
					) *
					scaleFactor;
			const scaleZ =
				1 +
				Math.sign(horizontalDelta) *
					Math.abs(
						horizontalDelta * cameraRight.z +
							verticalDelta * cameraUp.z,
					) *
					scaleFactor;

			// Apply scaling relative to drag start scale
			// Create new scale vector starting with locked values (1 = no scale)
			const newScaleX = scale_locks.x
				? currentScale.x
				: dragStartScale.x * scaleX;
			const newScaleY = scale_locks.y
				? currentScale.y
				: dragStartScale.y * scaleY;
			const newScaleZ = scale_locks.z
				? currentScale.z
				: dragStartScale.z * scaleZ;

			const positions = points.geometry.attributes.position;

			for (let i = 0; i < positions.count; i++) {
				const point = new Vector3(
					originalPoints[i * 3],
					originalPoints[i * 3 + 1],
					originalPoints[i * 3 + 2],
				);

				const toPoint = point.clone().sub(scalingCenter);
				const scaledPoint = scalingCenter
					.clone()
					.add(
						toPoint.multiply(
							new Vector3(newScaleX, newScaleY, newScaleZ),
						),
					);

				positions.setXYZ(
					i,
					scaledPoint.x,
					scaledPoint.y,
					scaledPoint.z,
				);
			}

			currentScale.set(newScaleX, newScaleY, newScaleZ);
			positions.needsUpdate = true;

			// Update the points object
			points.geometry.computeBoundingBox();
			points.geometry.computeBoundingSphere();

			// Update bounding box and box helper
			boundingBox.copy(points.geometry.boundingBox);
			if (boxHelper) {
				boxHelper.visible = true; // Ensure box is visible
				boxHelper.update();
			}

			dispatchChange();
			renderer.render(scene, camera);
		}
	}

	// Update the updateCoordinateSystem function to use the prop
	function updateCoordinateSystem() {
		console.log("updateCoordinateSystem");
		if (!points || !camera || !controls) return;

		// Define basis vectors based on coordinate system selection
		const basisVectors = {
			X: new Vector3(1, 0, 0),
			Y: new Vector3(0, 1, 0),
			Z: new Vector3(0, 0, 1),
			"-X": new Vector3(-1, 0, 0),
			"-Y": new Vector3(0, -1, 0),
			"-Z": new Vector3(0, 0, -1),
		};

		const upVector = basisVectors[coordinate_system.up];
		const forwardVector = basisVectors[coordinate_system.forward];

		if (!upVector || !forwardVector) {
			console.error(
				"Invalid coordinate system configuration:",
				coordinate_system,
			);
			return;
		}

		// Get the current distance from camera to target
		const distance = camera.position.length();

		// Position camera along the forward direction
		camera.position.copy(forwardVector.clone().multiplyScalar(distance));
		camera.up.copy(upVector);
		camera.lookAt(0, 0, 0);

		// Dispose and recreate controls
		controls.dispose();
		controls = new OrbitControls(camera, renderer.domElement);

		// Update controls
		controls.update();
	}
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{container}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}

	<div class="point-cloud-editor" bind:this={editorContainer}>
		<div class="color-picker hidden">
			<div class="color-preview"></div>
			<input type="text" class="hex-input" placeholder="#FFFFFF" />
			<div class="color-row">
				<label>R:</label>
				<input
					type="range"
					min="0"
					max="1"
					step="0.01"
					value="1"
					class="red-slider"
					on:input={updateAllInputs}
				/>
				<input
					type="number"
					min="0"
					max="255"
					value="255"
					class="red-number"
					on:input={updateAllInputs}
				/>
			</div>
			<div class="color-row">
				<label>G:</label>
				<input
					type="range"
					min="0"
					max="1"
					step="0.01"
					value="1"
					class="green-slider"
					on:input={updateAllInputs}
				/>
				<input
					type="number"
					min="0"
					max="255"
					value="255"
					class="green-number"
					on:input={updateAllInputs}
				/>
			</div>
			<div class="color-row">
				<label>B:</label>
				<input
					type="range"
					min="0"
					max="1"
					step="0.01"
					value="1"
					class="blue-slider"
					on:input={updateAllInputs}
				/>
				<input
					type="number"
					min="0"
					max="255"
					value="255"
					class="blue-number"
					on:input={updateAllInputs}
				/>
			</div>
			<button class="apply-color" on:click={applyColors}>Apply</button>
		</div>
	</div>

	<div class="button-container">
		<button on:click={centerCamera}>Center Camera</button>
		<button on:click={toggleScalingMode}>
			{#if isScalingMode}Exit Scale Mode{:else}Enter Scale Mode{/if}
		</button>
	</div>
</Block>

<style>
	.point-cloud-editor {
		width: 100%;
		height: 500px;
		position: relative;
		background: #f0f0f0;
	}

	.color-picker {
		position: absolute;
		background: white;
		padding: 15px;
		border-radius: 8px;
		z-index: 1000;
		border: 1px solid #ccc;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		width: 250px;
	}

	.color-preview {
		width: 100%;
		height: 30px;
		border-radius: 4px;
		margin-bottom: 10px;
		border: 1px solid #ccc;
	}

	.color-row {
		display: flex;
		align-items: center;
		margin-bottom: 10px;
		padding: 0 10px;
		gap: 8px;
	}

	.color-row label {
		min-width: 20px;
		flex-shrink: 0;
	}

	.color-row input[type="range"] {
		flex: 1;
		min-width: 100px;
	}

	.color-row input[type="number"] {
		width: 55px;
		padding: 2px 4px;
		text-align: right;
		flex-shrink: 0;
	}

	.hidden {
		display: none;
	}

	.hex-input {
		width: 100%;
		padding: 5px;
		font-size: 14px;
		border: 1px solid #ccc;
		border-radius: 4px;
		margin-bottom: 10px;
	}

	.apply-color {
		width: 100%;
		padding: 10px;
		font-size: 14px;
		border: none;
		border-radius: 4px;
		background-color: #34a853;
		color: #fff;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	.apply-color:hover {
		background-color: #0f9d58;
	}

	.button-container {
		position: absolute;
		bottom: 20px;
		left: 20px;
		display: flex;
		gap: 10px;
		padding: 10px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 8px;
	}

	button {
		padding: 8px 16px;
		background: #4caf50;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	button:hover {
		background: #45a049;
	}
</style>
