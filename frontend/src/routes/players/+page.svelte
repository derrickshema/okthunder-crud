<script lang="ts">
    import { onMount } from 'svelte';
    import { accessToken } from '$lib/stores/authStore'; // <-- UPDATED: Import from new store file
    import { goto } from '$app/navigation';

    let players: any[] = [];
    let message = '';
    let isError = false;
    let isLoading = true;

    // Function to fetch players from the protected API endpoint
    async function fetchPlayers() {
        isLoading = true;
        message = '';
        isError = false;

        const token = localStorage.getItem('access_token');

        if (!token) {
            message = 'You are not authenticated. Please log in.';
            isError = true;
            isLoading = false;
            goto('/login'); // Redirect if no token
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/player/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`, // Send the JWT token
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                players = await response.json();
                message = 'Players loaded successfully!';
                isError = false;
            } else if (response.status === 401) {
                message = 'Authentication failed. Please log in again.';
                isError = true;
                localStorage.removeItem('access_token'); // Clear invalid token
                accessToken.set(null); // Update store
                goto('/login'); // Redirect to login
            } else {
                const errorData = await response.json();
                message = `Failed to load players: ${errorData.detail || 'Unknown error'}`;
                isError = true;
            }
        } catch (error) {
            message = 'Network error or server unreachable.';
            isError = true;
            console.error('Fetch players error:', error);
        } finally {
            isLoading = false;
        }
    }

    // Fetch players when the component mounts or when accessToken changes
    onMount(() => {
        // Only fetch if token is present in the store
        accessToken.subscribe(token => {
            if (token) {
                fetchPlayers();
            } else if (!isLoading) { // If not loading and token is null, it means we logged out or were redirected
                 players = []; // Clear players if logged out
                 message = 'Please log in to view players.';
                 isError = false;
            }
        })(); // Immediately invoke the subscribe callback
    });

    // Function to handle player creation (redirect to create page)
    function createPlayer() {
        goto('/players/create');
    }

    // Function to handle player edit (placeholder for now)
    async function editPlayer(playerId: number) {
        // This function can be implemented to open a modal or redirect to an edit form page
        goto(`/players/edit/${playerId}`);
    }

    // Function to handle player deletion (placeholder for now)
    async function deletePlayer(playerId: number) {
        // This function can be implemented to confirm deletion and call the API
        isLoading = true;
        message = '';
        isError = false;

        const token = localStorage.getItem('access_token');

        if (!token) {
            message = 'You are not authenticated. Please log in.';
            isError = true;
            isLoading = false;
            goto('/login'); // Redirect if no token
            return;
        }
        try {
            const response = await fetch(`http://localhost:8000/player/${playerId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                players = players.filter(player => player.id !== playerId);
                message = 'Player deleted successfully!';
                isError = false;
            } else if (response.status === 401) {
                message = 'Authentication failed. Please log in again.';
                isError = true;
                localStorage.removeItem('access_token'); // Clear invalid token
                accessToken.set(null); // Update store
                goto('/login'); // Redirect to login
            } else {
                const errorData = await response.json();
                message = `Failed to delete player: ${errorData.detail || 'Unknown error'}`;
                isError = true;
            }
        } catch (error) {
            message = 'Network error or server unreachable.';
            isError = true;
            console.error('Delete player error:', error);
        }finally {
            isLoading = false;
        }
    }
</script>

<div class="max-w-4xl mx-auto mt-10 p-8 bg-white rounded-xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-center text-gray-800">OKC Thunder Players</h2>
    <button onclick={createPlayer} class="bg-blue-500 text-white font-semibold py-2 px-4 mb-4">+ Add New Player</button>

    {#if isLoading}
        <p class="text-center text-blue-600">Loading players...</p>
    {:else if isError}
        <p class="mt-4 p-3 rounded-lg text-sm bg-red-100 text-red-700">
            {message}
        </p>
    {:else if players.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each players as player (player.id)}
                <div class="border border-gray-200 rounded-lg p-4 shadow-sm bg-gray-50">
                    <img src={player.image_url || 'https://placehold.co/150x150/CCCCCC/FFFFFF?text=No+Image'} alt="{player.first_name} {player.last_name}" class="w-24 h-24 rounded-full mx-auto mb-4 object-cover">
                    <h3 class="text-xl font-semibold text-center mb-1">{player.first_name} {player.last_name}</h3>
                    <p class="text-gray-600 text-center text-sm">Age: {player.age} | Height: {player.height} | Position: {player.position}</p>
                    <p class="text-gray-500 text-center text-xs mt-2">{player.bio}</p>
                    <div class="mt-4 flex justify-center space-x-2">
                        <button onclick={()=>editPlayer(player.id)} class="bg-blue-500 text-white font-semibold py-1 px-3 rounded hover:bg-blue-600">Edit</button>
                        <button onclick={()=>deletePlayer(player.id)} class="bg-red-500 text-white font-semibold py-1 px-3 rounded hover:bg-red-600">Delete</button>
                    </div>
                </div>
            {/each}
        </div>
    {:else}
        <p class="text-center text-gray-500">No players found. Try adding some after logging in!</p>
    {/if}
</div>