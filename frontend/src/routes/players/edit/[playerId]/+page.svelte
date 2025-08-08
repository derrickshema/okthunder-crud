<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';

	let playerId: string;
	let player = {
		id: null,
		first_name: '',
		last_name: '',
		age: null,
		height: '',
		position: '',
		bio: ''
	};

	let error = '';
	let isLoading = false;
	let isSubmitting = false;

	// Load player data when page mounts
	onMount(async () => {
		playerId = page.params.playerId;

		const token = localStorage.getItem('access_token');
		if (!token) {
			goto('/login');
			return;
		}

		isLoading = true;
		try {
			const res = await fetch(`http://localhost:8000/player/${playerId}`, {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			});
			if (res.ok) {
				player = await res.json();
			} else {
				error = 'Failed to fetch player data.';
			}
		} catch (err) {
			error = 'Error loading player.';
			console.error(err);
		} finally {
			isLoading = false;
		}
	});

	async function updatePlayer() {
		error = '';
		isSubmitting = true;

		const token = localStorage.getItem('access_token');
		if (!token) {
			goto('/login');
			return;
		}

		try {
			const res = await fetch(`http://localhost:8000/player/${playerId}`, {
				method: 'PUT',
				headers: {
					'Authorization': `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(player)
			});

			if (res.ok) {
				goto('/players'); // Redirect on success
			} else {
				const data = await res.json();
				error = data.detail || 'Update failed.';
			}
		} catch (err) {
			error = 'Network error';
			console.error(err);
		} finally {
			isSubmitting = false;
		}
	}
</script>

{#if isLoading}
	<p class="text-blue-600">Loading player data...</p>
{:else}
	<form on:submit|preventDefault={updatePlayer} class="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
		<h2 class="text-3xl font-bold mb-6 text-center text-gray-800">Edit Player</h2>

		{#if error}
			<p class="text-red-600">{error}</p>
		{/if}

		<div class="mb-4">
			<label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
			<input id="first_name" bind:value={player.first_name} required />
		</div>

		<div class="mb-4">
			<label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
			<input id="last_name" bind:value={player.last_name} required />
		</div>

		<div class="mb-4">
			<label for="age" class="block text-sm font-medium text-gray-700">Age</label>
			<input type="number" id="age" bind:value={player.age} required />
		</div>

		<div class="mb-4">
			<label for="height" class="block text-sm font-medium text-gray-700">Height</label>
			<input id="height" bind:value={player.height} required />
		</div>

		<div class="mb-4">
			<label for="position" class="block text-sm font-medium text-gray-700">Position</label>
			<input id="position" bind:value={player.position} required />
		</div>

		<div class="mb-4">
			<label for="bio" class="block text-sm font-medium text-gray-700">Bio</label>
			<textarea id="bio" bind:value={player.bio}></textarea>
		</div>

		<button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded" disabled={isSubmitting}>
			{isSubmitting ? 'Updating...' : 'Update Player'}
		</button>
		<button type="button" on:click={() => goto('/players')} class="ml-2 bg-gray-300 px-4 py-2 rounded">
			Cancel
		</button>
	</form>
{/if}