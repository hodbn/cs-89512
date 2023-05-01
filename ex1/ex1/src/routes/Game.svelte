<script lang="ts">
	const randomChoice = <T>(arr: T[]) => arr[Math.floor(arr.length * Math.random())];
	const WIDTH = 100;
	const HEIGHT = 100;
	enum PersonKind {
		S1 = 'S1',
		S2 = 'S2',
		S3 = 'S3',
		S4 = 'S4'
	}
	type Person = {
		kind: PersonKind;
		willGossip: boolean;
		cooldown: number;
		exposed: boolean;
	};
	type Cell = Person | undefined;
	const initializeState = (p: number) => {
		const initializePopulation = (n: number, p: number) => {
			const shouldPopulate = () => Math.random() < p;
			const getRandomPersonKind = (_) =>
				randomChoice([PersonKind.S1, PersonKind.S2, PersonKind.S3, PersonKind.S4]);
			const getRandomPersonKindClusters = (i: number) => {
				const [x, y] = indexToCoords(i);
				if (x >= WIDTH / 2 && y < HEIGHT / 2) {
					return PersonKind.S2;
				}
				if (x < WIDTH / 2 && y >= HEIGHT / 2) {
					return PersonKind.S3;
				}
				if (x >= WIDTH / 2 && y >= HEIGHT / 2) {
					return PersonKind.S4;
				}
				if (x < WIDTH / 2 && y < HEIGHT / 2) {
					return PersonKind.S1;
				}
			};
			const getRandomPersonKindStripes = (i: number) => {
				const [x, y] = indexToCoords(i);
				if (x % 4 === 0) {
					return PersonKind.S4;
				}
				if (x % 3 === 0) {
					return PersonKind.S3;
				}
				if (x % 2 === 0) {
					return PersonKind.S2;
				}
				return PersonKind.S1;
			};
			const populate = (i: number) => ({
				kind: getRandomPersonKind(i),
				willGossip: false,
				cooldown: 0,
				exposed: false
			});
			return new Array(n)
				.fill(undefined)
				.map((_, i) => (shouldPopulate() ? populate(i) : undefined));
		};
		const chooseInitialGossiper = (state: Cell[]) => {
			const population = state.reduce(
				(acc, val) => (val === undefined ? acc : [...acc, val]),
				[] as Person[]
			);
			return randomChoice(population);
		};
		const n = WIDTH * HEIGHT;
		const state = initializePopulation(n, p);
		const person = chooseInitialGossiper(state);
		person.willGossip = true;
		person.exposed = true;
		return state;
	};
	const indexToCoords = (i: number) => [i % WIDTH, Math.floor(i / HEIGHT)];
	const coordsToStr = (coords: number[]) => {
		const padCoord = (i: number) => i.toString().padStart(2, ' ');
		return `[${padCoord(coords[0])},${padCoord(coords[1])}]`;
	};
	const indexToCoordsStr = (i: number) => coordsToStr(indexToCoords(i));
	const getNeighbors = (i: number) => {
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
	const isPerson = (c: Cell): c is Person => {
		return c !== undefined;
	};
	const gossipProbability = (p: Person, moreSuggestible: boolean) => {
		const probabilities = {
			[PersonKind.S1]: 1,
			[PersonKind.S2]: 2 / 3,
			[PersonKind.S3]: 1 / 3,
			[PersonKind.S4]: 0
		};
		const suggestibleKinds = {
			[PersonKind.S1]: PersonKind.S1,
			[PersonKind.S2]: PersonKind.S1,
			[PersonKind.S3]: PersonKind.S2,
			[PersonKind.S4]: PersonKind.S3
		};
		const temporaryKind = moreSuggestible ? suggestibleKinds[p.kind] : p.kind;
		return probabilities[temporaryKind];
	};
	const isPopulated = (state: Cell[], i: number) => {
		return isPerson(state[i]);
	};
	const shouldGossip = (p: Person, heardCount: number) => {
		return Math.random() <= gossipProbability(p, heardCount >= 2);
	};
	const getNextState = (state: Cell[], l: number) => {
		const isGossiper = (c: Cell, i: number) => {
			return isPerson(c) && c.willGossip ? [i] : [];
		};
		const getGossipTargets = (i: number) => {
			const neighbors = getNeighbors(i);
			const existingNeighbors = neighbors.filter((i) => isPopulated(state, i));
			// writeLog(`${indexToCoordsStr(i)}: passing to ${existingNeighbors}`);
			return existingNeighbors;
		};
		const decideIfToGossip = (p: Person, i: number, heardCount: number) => {
			if (heardCount === 0) {
				return false;
			}
			const wantsToGossip =
				(!p.willGossip || l === 0) && p.cooldown === 0 && shouldGossip(p, heardCount);
			// if (wantsToGossip) {
			// 	writeLog(`${indexToCoordsStr(i)}: decides to gossip`);
			// } else {
			// 	writeLog(`${indexToCoordsStr(i)}: decides not to gossip (cooldown: ${p.cooldown})`);
			// }
			return wantsToGossip;
		};
		const gossipers = state.flatMap(isGossiper);
		const gossipTargets = gossipers.flatMap(getGossipTargets);
		const gossipCounters = gossipTargets.reduce(
			(acc, num) => ((acc[num] = (acc[num] || 0) + 1), acc),
			{} as { [key: string]: number }
		);
		const nextState = state.map((c, i) =>
			isPerson(c)
				? ({
						...c,
						willGossip: decideIfToGossip(c, i, gossipCounters[i] ?? 0),
						cooldown: gossipers.includes(i) ? l : Math.max(0, c.cooldown - 1),
						exposed: c.exposed || gossipTargets.includes(i)
				  } as Person)
				: undefined
		);
		return { nextState, numGossipers: gossipers.length };
	};

	let p = 0.5;
	let l = 3;
	let maxGen = 100;
	type HistoryRecord = {
		generation: number;
		numGossipers: number;
		totalExposed: number;
	};
	let history = [] as HistoryRecord[];
	let lastResult = '';
	export let activeGossipers: number;
	export let exposureRate = 0.0;
	export let generation = 0;
	export let gameNumber = 0;
	export let selectedIndex = 0;
	let state: Cell[] = initializeState(p);
	$: activeGossipers = state.filter((c) => isPerson(c) && c.willGossip === true).length;
	export let playHandle = -1;
	let log = '';
	let logElement: HTMLTextAreaElement;
	const writeLog = (msg: string) => {
		const record = `game=${gameNumber} gen=${generation} | ${msg}`;
		const limit = 10 * 1000;
		if (log.length > limit) {
			const trimmedLog = log.substr(-limit);
			const firstNl = trimmedLog.indexOf('\n');
			if (firstNl !== -1) {
				log = trimmedLog.substr(firstNl);
			}
		}
		if (log !== '') {
			log += '\n';
		}
		log += record;
		setTimeout(() => {
			logElement.scroll({ top: logElement.scrollHeight, behavior: 'instant' });
		});
	};
	const singleStepGame = () => {
		const { nextState, numGossipers } = getNextState(state, l);
		const population = nextState.filter(isPerson);
		const totalPopulation = population.length;
		const exposedPopulation = population.filter((c) => c.exposed);
		exposureRate = exposedPopulation.length / totalPopulation;
		history.push({ generation, numGossipers, totalExposed: exposedPopulation.length });
		state = nextState;
		generation++;
		setTimeout(() => {
			writeLog(`active gossipers: ${activeGossipers}`);
			if (activeGossipers === 0 || generation === maxGen) {
				setRunning(false);
				gameState = GameState.END;
				lastResult = JSON.stringify(
					{
						l,
						p,
						totalPopulation,
						activeGossipers,
						generation,
						maxGen,
						history
					},
					null,
					2
				);
				history = [];
				writeLog('game ended');
			}
		});
	};
	const resetGame = () => {
		gameNumber++;
		generation = 0;
		exposureRate = 0.0;
		state = initializeState(p);
		writeLog('game restarted');
	};
	let isRunning: boolean;
	$: isRunning = playHandle !== -1;
	const toggleRunning = () => {
		if (isRunning === true) {
			writeLog('game paused');
		} else {
			writeLog('game continued');
		}
		setRunning(!isRunning);
	};
	let runInterval = 500;
	const setRunning = (mode: boolean) => {
		if (mode === true) {
			if (!isRunning) {
				playHandle = setInterval(() => {
					singleStepGame();
				}, runInterval);
			}
		} else {
			if (isRunning) {
				clearInterval(playHandle);
				playHandle = -1;
			}
		}
	};
	enum GameState {
		INITIAL,
		ALIVE,
		END
	}
	let gameState = GameState.ALIVE;
	const handleClickStartRestartGame = () => {
		setRunning(false);
		resetGame();
		gameState = GameState.ALIVE;
	};
	const handleClickSingleStep = () => {
		setRunning(false);
		singleStepGame();
	};
	const handleClickRunPause = () => {
		toggleRunning();
	};
	const handleLogClear = () => {
		log = '';
	};
	const handleLastResultClear = () => {
		lastResult = '';
	};
	const handleLastResultCopy = () => {
		navigator.clipboard.writeText(lastResult);
	};
</script>

<div class="w-full flex justify-between">
	<div class="flex flex-col space-y-2">
		<h1 class="text-lg">Controls</h1>
		<table class="border-spacing-2 border-separate">
			<tr>
				<th class="text-start">Game params</th>
				<td class="text-end">
					<div class="flex justify-between space-x-2">
						<div class="flex rounded-md shadow-sm flex-grow">
							<span
								class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 px-3 text-gray-500 text-xs"
								>P =</span
							>
							<input
								type="text"
								class="block w-10 min-w-[2rem] flex-1 rounded-none rounded-r-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 text-xs"
								placeholder="Density"
								bind:value={p}
							/>
						</div>
						<div class="flex rounded-md shadow-sm flex-grow">
							<span
								class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 px-3 text-gray-500 text-xs"
								>L =</span
							>
							<input
								type="text"
								class="block w-10 min-w-[1rem] flex-1 rounded-none rounded-r-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 text-xs"
								placeholder="Cooldown"
								bind:value={l}
							/>
						</div>
					</div>
				</td>
				<td>
					<div class="flex rounded-md shadow-sm">
						<span
							class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 px-3 text-gray-500 text-xs"
							>MaxGen =</span
						>
						<input
							type="number"
							class="block w-10 min-w-[3rem] flex-1 rounded-none rounded-r-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 text-xs"
							placeholder="Cooldown"
							bind:value={maxGen}
						/>
					</div>
				</td>
			</tr>
			<tr>
				<th class="text-start">Game state</th>
				<td class="text-end">{gameState === GameState.ALIVE ? 'Alive' : 'Ended'}</td>
				<td>
					<button
						type="button"
						class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
						on:click={handleClickStartRestartGame}
						>{gameState === GameState.INITIAL ? 'Start' : 'Restart'}</button
					>
				</td>
			</tr>
			<tr>
				<th class="text-start">Exposure rate</th>
				<td class="text-end">{(exposureRate * 100).toFixed(2)}%</td>
				<td />
			</tr>
			<tr>
				<th class="text-start">Game number</th>
				<td class="text-end">{gameNumber}</td>
				<td />
			</tr>
			<tr>
				<th class="text-start">Generation</th>
				<td class="text-end">{generation}</td>
				<td>
					<button
						type="button"
						class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
						disabled={gameState !== GameState.ALIVE}
						on:click={handleClickSingleStep}>Single step</button
					>
				</td>
			</tr>
			<tr>
				<th class="text-start">Run interval</th>
				<td class="text-end">
					<div class="flex rounded-md shadow-sm">
						<input
							type="text"
							class="block w-6 flex-1 rounded-none rounded-l-md text-end border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 text-xs"
							placeholder="interval"
							bind:value={runInterval}
						/>
						<span
							class="inline-flex items-center rounded-r-md border border-l-0 border-gray-300 px-3 text-gray-500 text-xs"
							>ms</span
						>
					</div>
				</td>
				<td>
					<button
						type="button"
						class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
						disabled={gameState !== GameState.ALIVE}
						on:click={handleClickRunPause}>{isRunning ? 'Pause' : 'Run'}</button
					>
				</td>
			</tr>
			<tr>
				<th class="text-start">Active gossipers</th>
				<td class="text-end">{activeGossipers}</td>
				<td />
			</tr>
			<tr>
				<th class="text-start">Selected cell</th>
				<td class="text-end min-w-[6rem] font-mono"
					>{state[selectedIndex]?.kind ?? 'Empty'} {indexToCoordsStr(selectedIndex)}</td
				>
				<td />
			</tr>
		</table>
		<div class="flex justify-between">
			<h1 class="text-lg">Message log</h1>
			<button
				type="button"
				class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
				on:click={handleLogClear}>Clear</button
			>
		</div>
		<textarea
			bind:this={logElement}
			class="h-full min-w-[30rem] font-mono flex-grow block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 text-xs"
			>{log}</textarea
		>
		<div class="flex justify-between">
			<h1 class="text-lg">Last game result</h1>
			<div>
				<button
					type="button"
					class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
					on:click={handleLastResultCopy}>Copy</button
				>
				<button
					type="button"
					class="rounded bg-white px-2 py-1 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
					on:click={handleLastResultClear}>Clear</button
				>
			</div>
		</div>
		<textarea
			class="h-full min-w-[30rem] font-mono flex-grow block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 text-xs"
			>{lastResult}</textarea
		>
	</div>
	<div class="flex flex-col space-y-2">
		<h1 class="text-lg">Legend</h1>
		<div class="flex space-x-4 text-sm">
			<div class="flex">
				<div class="mr-2">General population:</div>
				<div class="px-1 bg-gray-100">S1</div>
				<div class="px-1 bg-gray-200">S2</div>
				<div class="px-1 bg-gray-300">S3</div>
				<div class="px-1 bg-gray-400">S4</div>
			</div>
			<div class="flex">
				<div class="mr-2">Gossipers:</div>
				<div class="px-1 bg-red-300">S1</div>
				<div class="px-1 bg-red-400">S2</div>
				<div class="px-1 bg-red-500">S3</div>
				<div class="px-1 bg-red-600">S4</div>
			</div>
		</div>
		<div
			class="grid gap-0.5 grid-cols-[repeat(100,_minmax(0,_1fr))] grid-rows-[repeat(100,_minmax(0,_1fr))] bg-white border border-gray-500 shadow-xl text-xs"
		>
			{#each state as cell, i (i)}
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
					on:mouseover={() => {
						selectedIndex = i;
					}}
					on:focus={() => {
						selectedIndex = i;
					}}
				/>
			{/each}
		</div>
	</div>
</div>

<style lang="postcss">
</style>
