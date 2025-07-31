<script lang="ts">
    import { goto } from '$app/navigation';
    import { accessToken } from '$lib/stores/authStore'; // Import the store

    let username = '';
    let password = '';
    let email = '';
    let message = '';
    let isError = false;

    // If already authenticated, redirect away from signup
    accessToken.subscribe(token => {
        if (token) {
            goto('/'); // Redirect to a protected page or home
        }
    });

    async function handleSubmit() {
        message = ''; // Clear previous messages
        isError = false;

        try {
            const response = await fetch('http://localhost:8000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, email }),
            });

            if (response.ok) {
                const data = await response.json();
                message = `User '${data.username}' registered successfully! You can now log in.`;
                isError = false;
                // Optional: Clear form or redirect
                username = '';
                password = '';
                email = '';
                await goto('/login'); // Redirect to login after successful registration
            } else {
                const errorData = await response.json();
                message = `Registration failed: ${errorData.detail || 'Unknown error'}`;
                isError = true;
            }
        } catch (error) {
            message = 'Network error or server unreachable.';
            isError = true;
            console.error('Signup error:', error);
        }
    }
</script>

<div class="max-w-md mx-auto mt-10 p-8 bg-white rounded-xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-center text-gray-800">Sign Up</h2>

    <form on:submit|preventDefault={handleSubmit}>
        <div class="mb-4">
            <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Username:</label>
            <input
                type="text"
                id="username"
                bind:value={username}
                required
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
                placeholder="Choose a username"
            />
        </div>
        <div class="mb-4">
            <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
            <input
                type="password"
                id="password"
                bind:value={password}
                required
                minlength="8"
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
                placeholder="Enter your password"
            />
        </div>
        <div class="mb-6">
            <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email (Optional):</label>
            <input
                type="email"
                id="email"
                bind:value={email}
                class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
                placeholder="Enter your email"
            />
        </div>
        <div class="flex items-center justify-between">
            <button
                type="submit"
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-colors duration-200 w-full"
            >
                Register
            </button>
        </div>
    </form>

    {#if message}
        <p class="mt-4 p-3 rounded-lg text-sm {isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}">
            {message}
        </p>
    {/if}

    <p class="mt-6 text-center text-gray-600 text-sm">
        Already have an account? <a href="/login" class="text-blue-600 hover:underline">Log in here</a>.
    </p>
</div>
