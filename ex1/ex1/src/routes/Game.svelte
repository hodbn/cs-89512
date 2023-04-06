<script lang="ts">
	function randomChoice<T>(arr: T[]) {
	    return arr[Math.floor(arr.length * Math.random())];
	}
	enum PersonKind {
		NONE,
		S1,
		S2,
		S3,
		S4,
	}
	class GameOfGossip {
		w: number;
		h: number;
		grid: PersonKind[];

		constructor(w: number, h: number, p: number) {
			this.w = w
			this.h = h
			this.grid = []
			this.initialize(p)
		}

		initialize(p: number) {
			for(let i = 0; i < this.w * this.h; i++) {
				if (Math.random() < (1-p)) {
					this.grid[i] = PersonKind.NONE
					continue;
				}
				this.grid[i] = randomChoice([PersonKind.S1, PersonKind.S2, PersonKind.S3, PersonKind.S4])
			}
		}

		rows() {
			return Array.from({ length: this.h }, (_, i) =>
				this.grid.slice(i * this.w, i * this.w + this.w)
			);
		}
	}
	const g = new GameOfGossip(100, 100, 0.5)
</script>

<div class="grid grid-cols-[repeat({g.h},_minmax(0,_1fr))] grid-rows-[repeat({g.w},_minmax(0,_1fr))] bg-blue-100 text-xs">
	{#each g.grid as cell}
	<div
		class="w-2 h-2"
		class:bg-blue-100="{cell === PersonKind.NONE}"
		class:bg-red-100="{cell === PersonKind.S1}"
		class:bg-red-200="{cell === PersonKind.S2}"
		class:bg-red-300="{cell === PersonKind.S3}"
		class:bg-red-400="{cell === PersonKind.S4}"
	></div>
	{/each}
</div>

<style lang="postcss">
</style>
