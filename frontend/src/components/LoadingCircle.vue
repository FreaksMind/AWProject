<script setup>
const props = defineProps({
    loading: {
        type: Boolean,
        required: true,
        default: "true"
    }
});
</script>

<template>
    <div v-if="loading"><v-progress-circular color="blue-lighten-3" indeterminate :size="58"></v-progress-circular></div>
</template>

<style scoped>

</style>