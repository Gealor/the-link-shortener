<template>
    <div
        v-if="visible"
        class="task-context-menu window"
        :style="{ left: x + 'px', bottom: y + 'px' }"
    >
        <div class="menu-item menu-item--default" @click="$emit('close')">Close</div>
    </div>
</template>

<script setup>
defineProps({
    visible: {
        type: Boolean,
        default: false,
    },
    x: {
        type: Number,
        default: 0,
    },
    y: {
        type: Number,
        default: 0,
    },
})
defineEmits(['close'])
</script>

<style scoped>
.task-context-menu {
    position: fixed;
    z-index: var(--z-taskbar);
    min-width: 100px;
    padding: 2px;
}

.menu-item {
    padding: 3px 20px 3px 8px;
    font-size: 12px;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
}

.menu-item:hover:not(.disabled) {
    background: #0a246a;
    color: #fff;
}

.menu-item.disabled {
    color: #808080;
    cursor: default;
}

.menu-item--default {
    font-weight: bold;
}
</style>
