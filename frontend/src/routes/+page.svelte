<script lang="ts">
    import { accessToken } from '$lib/stores/authStore'; // Import the accessToken store
    import { goto } from '$app/navigation';
</script>

<div class="max-w-2xl mx-auto mt-16 p-8 bg-white rounded-xl shadow-lg text-center">
    <h1 class="text-4xl font-extrabold text-gray-900 mb-6">Welcome to the OKC Thunder App!</h1>

    {#if !$accessToken}
        <!-- Content for unauthenticated users -->
        <p class="text-lg text-gray-700 mb-8">
            Manage your favorite OKC Thunder players. Please log in or sign up to get started.
        </p>
        <div class="flex flex-col sm:flex-row justify-center gap-4">
            <a
                href="/login"
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors duration-200 text-lg"
            >
                Log In
            </a>
            <a
                href="/signup"
                class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-lg shadow-md transition-colors duration-200 text-lg"
            >
                Sign Up
            </a>
        </div>
    {:else}
        <!-- Content for authenticated users -->
        <p class="text-lg text-gray-700 mb-8">
            You're logged in! Head over to the players page to manage the roster.
        </p>
        <a
            href="/players"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors duration-200 text-lg"
        >
            Go to Players Page
        </a>
    {/if}
</div>