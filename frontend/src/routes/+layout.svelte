
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
	import '../app.css';
	import { accessToken } from '$lib/stores/authStore';
	
	let { children } = $props();

    // A Svelte store to hold the access token globally
    // This will allow components to react to login/logout status
    //export const accessToken = writable<string | null>(null);

    // Function to check for token in localStorage on component mount
    onMount(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            accessToken.set(token); // Set the store if token exists
        }
    });

    // Function to handle user logout
    const logout = async () => {
        localStorage.removeItem('access_token'); // Remove token from localStorage
        accessToken.set(null); // Clear the store
        await goto('/login'); // Redirect to login page
    };

    // Derived store to check if user is authenticated
    const isAuthenticated = $derived($accessToken !== null);

    // Optional: Redirect to login if trying to access protected routes without token
    // This is a basic client-side check. For full protection, server-side checks are crucial.
    $effect(() => {
        if (!isAuthenticated && $page.url.pathname.startsWith('/players')) {
            goto('/login');
        }
    });
</script>

<nav class="bg-gray-800 p-4 text-white shadow-md">
    <div class="container mx-auto flex justify-between items-center">
        <a href="/" class="text-xl font-bold text-blue-300 hover:text-blue-200">OKC Thunder App</a>
        <ul class="flex space-x-4">
            {#if !isAuthenticated}
                <li><a href="/signup" class="hover:text-gray-300 transition-colors duration-200">Sign Up</a></li>
                <li><a href="/login" class="hover:text-gray-300 transition-colors duration-200">Login</a></li>
            {:else}
                <li><a href="/players" class="hover:text-gray-300 transition-colors duration-200">Players</a></li>
                <li><button onclick={logout} class="hover:text-gray-300 transition-colors duration-200">Logout</button></li>
            {/if}
        </ul>
    </div>
</nav>

<main class="container mx-auto p-6">
    {@render children()}
</main>


