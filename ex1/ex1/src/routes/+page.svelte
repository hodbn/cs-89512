<script>
	import Game from './Game.svelte';
</script>

<svelte:head>
	<title>Game of Gossip</title>
	<link rel="stylesheet" href="https://rsms.me/inter/inter.css">
</svelte:head>

<section>
	<Game />
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}
</style>
