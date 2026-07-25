<template>
    <Transition name="start-menu">
        <div v-if="visible" class="start-menu window">
            <div class="side-banner">
                <span class="side-banner-text">
                    Windows <span class="thin">98</span>
                </span>
            </div>

            <ul class="menu-list">
                <template v-for="item in items" :key="item.id">
                    <hr v-if="item.divider" />
                    <li class="menu-item" @click="$emit('select', item)">
                        <img :src="item.icon" :alt="item.title" class="menu-icon" />
                        <span class="menu-label">{{ item.title }}</span>
                        <span v-if="item.submenu" class="menu-arrow">▶</span>
                    </li>
                </template>
            </ul>
        </div>
    </Transition>
</template>

<script setup>
import programsIcon from '../assets/icons/file_program_group-0.png'
import favoritesIcon from '../assets/icons/directory_favorites-0.png'
import documentsIcon from '../assets/icons/directory_open_file_mydocs-1.png'
import settingsIcon from '../assets/icons/settings_gear-0.png'
import findIcon from '../assets/icons/magnifying_glass-0.png'
import helpIcon from '../assets/icons/help_book_small-0.png'
import logoffIcon from '../assets/icons/key_win-1.png'
import shutdownIcon from '../assets/icons/shut_down_normal-0.png'

defineProps({
    visible: {
        type: Boolean,
        default: true,
    },
})
defineEmits(['select'])

// Хардкод пунктов меню — без реального функционала, просто для визуала
const items = [
    { id: 'programs', title: 'Programs', icon: programsIcon, submenu: true },
    { id: 'favorites', title: 'Favorites', icon: favoritesIcon, submenu: true },
    { id: 'documents', title: 'Documents', icon: documentsIcon, submenu: true },
    { id: 'settings', title: 'Settings', icon: settingsIcon, submenu: true },
    { id: 'find', title: 'Find', icon: findIcon, submenu: true },
    { id: 'help', title: 'Help', icon: helpIcon },
    { id: 'logoff', title: 'Log Off...', icon: logoffIcon, divider: true },
    { id: 'shutdown', title: 'Shut Down...', icon: shutdownIcon },
]
</script>

<style scoped>
.start-menu {
    position: fixed;
    left: 2px;
    bottom: var(--taskbar-height);
    display: flex;
    width: 200px;
    transform-origin: bottom left;
}

.start-menu-enter-active {
    transition: transform 0.08s ease-out, opacity 0.15s ease-out;
}

.start-menu-enter-from {
    opacity: 0;
    transform: scaleY(0.05);
}

.side-banner {
    width: 12%;
    flex-shrink: 0;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding: 8px 0;
    background: linear-gradient(180deg, #000080 70%, #0F7ECD, #000080);
}

.side-banner-text {
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    color: #fff;
    font-weight: bold;
    font-size: 16px;
    letter-spacing: 1px;
    font-family: "Pixelated MS Sans Serif", serif;
    user-select: none;
}

.side-banner-text .thin {
    font-weight: lighter;
    margin-top: -4px;
}

.menu-list {
    flex: 1;
    list-style: none;
    padding: 2px;
    margin: 0;
}

.menu-list hr {
    margin: 2px 0;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 6px;
    cursor: pointer;
    user-select: none;
    font-size: 12px;
}

.menu-item:hover {
    background: #0a246a;
    color: #fff;
}

.menu-icon {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
}

.menu-label {
    flex: 1;
}

.menu-arrow {
    font-size: 10px;
}
</style>
