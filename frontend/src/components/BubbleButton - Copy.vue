<script setup>
const props = defineProps({
    label: {
        type: String,
        required: true,
        default: "Button"
    }
});
</script>

<template>
    <div class="submit-button" v-text="props.label" />
</template>

<style scoped>
.submit-button {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border: 1px solid white;
    border-radius: 8px;
    padding: 0.5em;
    line-height: 1;
    cursor: pointer;
    user-select: none;
    width: 75px;
    transition: background-color 0.2s ease-in-out;
}

.submit-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
</style>