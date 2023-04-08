<script lang="ts">
	const randomChoice = <T>(arr: T[]) => arr[Math.floor(arr.length * Math.random())];
	const WIDTH = 100;
	const HEIGHT = 100;
	enum PersonKind {
		S1,
		S2,
		S3,
		S4
	}
	type PersonState = {
		kind: PersonKind;
		willGossip: boolean;
		cooldown: number;
	};
	type Cell = PersonState | undefined;
	const initializeState = (p: number) => {
		const initializePopulation = (n: number, p: number) => {
			const shouldPopulate = () => Math.random() < 1 - p;
			const getRandomPersonKind = () =>
				randomChoice([PersonKind.S1, PersonKind.S2, PersonKind.S3, PersonKind.S4]);
			const populate = () => ({
				kind: getRandomPersonKind(),
				willGossip: false,
				cooldown: 0
			});
			return new Array(n).fill(undefined).map(() => (shouldPopulate() ? populate() : undefined));
		};
		const chooseInitialGossiper = (state: Cell[]) => {
			const population = state.reduce(
				(acc, val) => (val === undefined ? acc : [...acc, val]),
				[] as PersonState[]
			);
			return randomChoice(population);
		};
		const n = WIDTH * HEIGHT;
		const state = initializePopulation(n, p);
		const person = chooseInitialGossiper(state);
		person.willGossip = true;
		return state;
	};
	const getNeighbors = (i: number) => {
		const indexToCoords = (i: number) => [i % WIDTH, Math.floor(i / HEIGHT)];
		const validCoords = ([x, y]: number[]) => x >= 0 && y >= 0 && x < WIDTH && y < HEIGHT;
		const coordsToIndex = ([x, y]: number[]) => y * WIDTH + x;
		const [x, y] = indexToCoords(i);
		const coords = [
			[x - 1, y - 1],
			[x, y - 1],
			[x + 1, y - 1],
			[x - 1, y + 0],
			[x + 1, y + 0],
			[x - 1, y + 1],
			[x, y + 1],
			[x + 1, y + 1]
		].filter(validCoords);
		return coords.map(coordsToIndex);
	};
	const isPerson = (c: Cell): c is PersonState => {
		return c !== undefined;
	};
	const gossipProbability = (p: PersonState, believeMore: boolean) => {
		const probabilities = {
			[PersonKind.S1]: 1,
			[PersonKind.S2]: 2 / 3,
			[PersonKind.S3]: 1 / 3,
			[PersonKind.S4]: 0
		};
		const temporaryKinds = {
			[PersonKind.S1]: PersonKind.S1,
			[PersonKind.S2]: PersonKind.S1,
			[PersonKind.S3]: PersonKind.S2,
			[PersonKind.S4]: PersonKind.S3
		};
		const temporaryKind = believeMore ? temporaryKinds[p.kind] : p.kind;
		return probabilities[temporaryKind];
	};
	const isPopulated = (state: Cell[], i: number) => {
		return isPerson(state[i]);
	};
	const shouldGossip = (p: PersonState, believeMore: boolean) => {
		return Math.random() <= gossipProbability(p, believeMore);
	};
	const getNextState = (state: Cell[], l: number) => {
		const isGossiper = (c: Cell, i: number) => {
			return isPerson(c) && c.willGossip ? [i] : [];
		};
		const getGossipTargets = (i: number) => {
			const neighbors = getNeighbors(i);
			const existingNeighbors = neighbors.filter((i) => isPopulated(state, i));
			console.log(`${i}: passing to ${existingNeighbors}`);
			return existingNeighbors;
		};
		const decideIfToGossip = (p: PersonState, i: number, heardCount: number) => {
			if (heardCount === 0) {
				return false;
			}
			const decision = p.cooldown === 0 && shouldGossip(p, heardCount > 1);
			if (decision) {
				console.log(`${i}: decides to gossip`);
			} else {
				console.log(`${i}: decides not to gossip (cooldown: ${p.cooldown})`);
			}
			return decision;
		};
		const gossipers = state.flatMap(isGossiper);
		const gossipTargets = gossipers.flatMap(getGossipTargets);
		const gossipCounters = gossipTargets.reduce(
			(acc, val) => [...acc.slice(0, val), acc[val] + 1, ...acc.slice(val + 1)],
			new Array(state.length).fill(0)
		);
		const nextState = state.map((c, i) =>
			isPerson(c)
				? {
						...c,
						willGossip: decideIfToGossip(c, i, gossipCounters[i]),
						cooldown: gossipers.includes(i) ? l : Math.max(0, c.cooldown - 1)
				  }
				: undefined
		);
		return nextState;
	};

	const p = 0.5;
	const l = 3;
	let state: Cell[] = initializeState(p);
	const handleClickNext = () => {
		state = getNextState(state, l);
		console.log(state);
	};
</script>

<div class="w-full">
	<div class="flex space-x-2 items-center">
		<div># of gossipers: {state.filter((c) => isPerson(c) && c.willGossip === true).length}</div>
		<button
			type="button"
			class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
			on:click={handleClickNext}>next</button
		>
	</div>
	<div
		class="grid gap-0.5 grid-cols-[repeat({HEIGHT},_minmax(0,_1fr))] grid-rows-[repeat({WIDTH},_minmax(0,_1fr))] bg-white border border-gray-500 shadow-xl text-xs"
	>
		{#each state as cell}
			<div
				class="w-1.5 h-1.5"
				class:bg-white={cell === undefined}
				class:bg-gray-100={cell?.kind === PersonKind.S1 && !cell.willGossip}
				class:bg-gray-200={cell?.kind === PersonKind.S2 && !cell.willGossip}
				class:bg-gray-300={cell?.kind === PersonKind.S3 && !cell.willGossip}
				class:bg-gray-400={cell?.kind === PersonKind.S4 && !cell.willGossip}
				class:bg-red-300={cell?.kind === PersonKind.S1 && cell.willGossip}
				class:bg-red-400={cell?.kind === PersonKind.S2 && cell.willGossip}
				class:bg-red-500={cell?.kind === PersonKind.S3 && cell.willGossip}
				class:bg-red-600={cell?.kind === PersonKind.S4 && cell.willGossip}
			/>
		{/each}
	</div>
</div>

<style lang="postcss">
</style>
