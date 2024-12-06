<script lang="ts">
	import type { PointCloudData } from './shared/types';

	export let value: PointCloudData;
	export let type: "gallery" | "table";
	export let selected = false;

	// Format the points for display
	function formatPoints(data: PointCloudData): string {
		if (!data || !data.positions || !data.colors) return "Empty point cloud";
		
		const points = data.positions.map((pos, i) => {
			const color = data.colors[i];
			return `(${pos.join(', ')}) RGB(${color.join(', ')})`;
		});
		
		return points.length > 3 
			? `${points.slice(0, 3).join('\n')}...` 
			: points.join('\n');
	}
</script>

<div
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
>
	<pre>{formatPoints(value)}</pre>
</div>

<style>
	.gallery {
		padding: var(--size-1) var(--size-2);
	}

	pre {
		margin: 0;
		white-space: pre-wrap;
		font-family: monospace;
		font-size: 0.9em;
	}

	div {
		max-height: 100px;
		overflow-y: auto;
		background: #f5f5f5;
		border-radius: 4px;
		padding: 8px;
	}

	.selected {
		border: 2px solid var(--color-primary);
	}
</style>
