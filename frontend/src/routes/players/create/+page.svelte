<script>
    import { goto } from '$app/navigation';
    import { accessToken } from '$lib/stores/authStore';

    let players = [];
    let isLoading = true;
    let message = '';
    let isError = false;

    // New player form data
    let newPlayer = {
        first_name: '',
        last_name: '',
        age: null,
        height: '',
        position: '',
        bio: ''
    };

    // Function to add a new player
    async function addPlayer() {
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
            const response = await fetch('http://localhost:8000/player/create', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newPlayer)
            });

            if (response.ok) {
                const player = await response.json();
                players.push(player);
                message = 'Player added successfully!';
                isError = false;
            } else if (response.status === 401) {
                message = 'Authentication failed. Please log in again.';
                isError = true;
                localStorage.removeItem('access_token'); // Clear invalid token
                accessToken.set(null); // Update store
                goto('/login'); // Redirect to login
            } else {
                const errorData = await response.json();
                message = `Failed to add player: ${errorData.detail || 'Unknown error'}`;
                isError = true;
            }
        } catch (error) {
            message = 'Network error or server unreachable.';
            isError = true;
            console.error('Add player error:', error);
        } finally {
            isLoading = false;
        }
    }
</script>
<div>
    <form on:submit|preventDefault={addPlayer} class="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
        {#if message}
            <p class={isError ? 'text-red-600' : 'text-green-600'}>{message}</p>
        {/if}

        {#if isLoading}
            <p class="text-blue-600">Adding player...</p>
        {/if}
        <h2 class="text-3xl font-bold mb-6 text-center text-gray-800">Create New Player</h2>
        
        <div class="mb-4">
            <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
            <input type="text" id="first_name" bind:value={newPlayer.first_name} class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500" required />
        </div>

        <div class="mb-4">
            <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
            <input type="text" id="last_name" bind:value={newPlayer.last_name} class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500" required />
        </div>

        <div class="mb-4">
            <label for="age" class="block text-sm font-medium text-gray-700">Age</label>
            <input type="number" id="age" bind:value={newPlayer.age} class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500" required />
        </div>

        <div class="mb-4">
            <label for="height" class="block text-sm font-medium text-gray-700">Height</label>
            <input type="text" id="height" bind:value={newPlayer.height} class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500" required />
        </div>

        <div class="mb-4">
            <label for="position" class="block text-sm font-medium text-gray-700">Position</label>
            <input type="text" id="position" bind:value={newPlayer.position} class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500" required />
        </div>

        <div class="mb-4">
            <label for="bio" class="block text-sm font-medium text-gray-700">Bio</label>
            <textarea id="bio" bind:value={newPlayer.bio} class="w-full border-gray-300 rounded-md shadow-sm focus:border"></textarea> 
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded hover:bg-blue-600">Add Player</button>
        <button type="button" on:click={() => goto('/players')} class="w-full mt-4 bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded hover:bg-gray-400">Cancel</button>
    </form>
</div>