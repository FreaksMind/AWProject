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
    <v-btn class="submit-button"
        v-bind="activatorProps"
        v-text="props.label"
        variant="flat"
        ></v-btn>
</template>

<style scoped>
.submit-button {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    /* border: 1px solid white; */
    border-radius: 15px;
    padding: 1.5em 2em;
    line-height: 1;
    cursor: pointer;
    user-select: none;
    width: auto;
    transition: background-color 0.2s ease-in-out;
    text-transform:none !important;
    background-color: #004d40;
    color: #ffffff;

}

.submit-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
</style>