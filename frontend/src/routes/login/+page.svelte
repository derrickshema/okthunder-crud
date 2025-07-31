<script lang="ts">
    import { goto } from '$app/navigation';
    import { accessToken } from '$lib/stores/authStore'; // Import the store

    let username = '';
    let password = '';
    let message = '';
    let isError = false;

    // If already authenticated, redirect away from login
    accessToken.subscribe(token => {
        if (token) {
            goto('/'); // Redirect to a protected page or home
        }
    });

    async function handleSubmit() {
        message = ''; // Clear previous messages
        isError = false;

        try {
            // Note: FastAPI's OAuth2PasswordRequestForm expects form-urlencoded data
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch('http://localhost:8000/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded', // Important for OAuth2PasswordRequestForm
                },
                body: formData.toString(),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token); // Store the token
                accessToken.set(data.access_token); // Update the Svelte store
                message = 'Login successful!';
                isError = false;
                await goto('/'); // Redirect to a protected page
            } else {
                const errorData = await response.json();
                message = `Login failed: ${errorData.detail || 'Unknown error'}`;
                isError = true;
            }
        } catch (error) {
            message = 'Network error or server unreachable.';
            isError = true;
            console.error('Login error:', error);
        }
    }
</script>

<div class="max-w-md mx-auto mt-10 p-8 bg-white rounded-xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-center text-gray-800">Login</h2>

    <form on:submit|preventDefault={handleSubmit}>
        <div class="mb-4">
            <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Username:</label>
            <input
                type="text"
                id="username"
                bind:value={username}
                required
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
                placeholder="Enter your username"
            />
        </div>
        <div class="mb-6">
            <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
            <input
                type="password"
                id="password"
                bind:value={password}
                required
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
                placeholder="Enter your password"
            />
        </div>
        <div class="flex items-center justify-between">
            <button
                type="submit"
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200 w-full"
            >
                Log In
            </button>
        </div>
    </form>

    {#if message}
        <p class="mt-4 p-3 rounded-lg text-sm {isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}">
            {message}
        </p>
    {/if}

    <p class="mt-6 text-center text-gray-600 text-sm">
        Don't have an account? <a href="/signup" class="text-blue-600 hover:underline">Sign up here</a>.
    </p>
</div>