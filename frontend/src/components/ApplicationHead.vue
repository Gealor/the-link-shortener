<template>
    <div class="bar-header bar-header--menu">
        <!-- Меню -->
        <div class="separator">
            <div class="vertical-separator-white"></div>
        </div>
        <div
            v-for="(elem, index) in listTools"
            class="menuitem"
            :tabindex="index"
        >
            <span class="mnemonic">{{ elem[0] }}</span>{{ elem.slice(1) }}
        </div>
    </div>

    <!-- Действия -->
    <div class="bar-header bar-header--actions">
        <div class="separator">
            <div class="vertical-separator-white"></div>
        </div>

        <template v-for="btn in toolbarButtons" :key="btn.id">
            <div v-if="btn.divider" class="separator">
                <div class="vertical-separator-black"></div>
            </div>
            <div class="toolbar-btn">
                <img :src="btn.icon" :alt="btn.title" class="toolbar-icon" />
                <span class="toolbar-label">{{ btn.title }}</span>
            </div>
        </template>
    </div>

    <!-- Поиск -->
    <div class="bar-header bar-header--search">
        <div class="separator">
            <div class="vertical-separator-white"></div>
        </div>
        <div>
            <span class="mnemonic">A</span>ddress
        </div>
        <div class="field-border url-field">
            <img :src="icon" alt="InternetExplorerIcon" class="little-icon">
            <span class="url-text">{{ url }}</span>
            <button class="url-dropdown">▼</button>
        </div>
    </div>
</template>

<script setup>
import stopIcon from "../assets/icons/msg_error-2.png"
import homeIcon from "../assets/icons/homepage-1.png"
import searchIcon from "../assets/icons/search_web-1.png"
import favoriteIcon from "../assets/icons/directory_favorites_small-1.png"
import historyIcon from "../assets/icons/directory_closed_history-1.png"
import mailIcon from "../assets/icons/mailbox_world-1.png"
import printIcon from "../assets/icons/printer-1.png"

defineProps({
    url: { type: String, default: '' },
    icon: { type: String }
})

const listTools = ["Edit", "Edit", "View", "Favorites", "Tools", "Help"]

// Разделитель указывается прямо в объекте кнопки — рендерится перед ней
const toolbarButtons = [
    { id: 'stop', title: 'Stop', icon: stopIcon },
    { id: 'home', title: 'Home', icon: homeIcon },
    { id: 'search', title: 'Search', icon: searchIcon, divider: true },
    { id: 'favorite', title: 'Favorite', icon: favoriteIcon },
    { id: 'history', title: 'History', icon: historyIcon },
    { id: 'mail', title: 'Mail', icon: mailIcon, divider: true },
    { id: 'print', title: 'Print', icon: printIcon },
]
</script>

<style scoped>
.bar-header {
    width: calc(100% + 16px);
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0px;
    margin: -8px -8px 8px -8px;
    box-sizing: border-box;
    background: silver; /* стандартный win98-фон */
    border-top: 2px solid #fff;
    border-left: 2px solid #fff;
    border-right: 2px solid #5c5c5c;
    border-bottom: 2px solid #5c5c5c;
}

.bar-header--menu,
.bar-header--search {
    height: 30px;
}

.bar-header--actions {
    height: 45px;
}

.toolbar-btn {
    display: flex;
    flex-direction: column;       /* иконка сверху, текст снизу */
    align-items: center;
    justify-content: center;
    gap: 2px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 2px 10px;
    min-width: 48px;
}

.toolbar-icon {
    width: 24px;
    height: 24px;
    filter: grayscale(100%);
}

.mnemonic {
    text-decoration: underline;
}

.menuitem {
    cursor: pointer;
    padding: 1px 5px;
    border: 1px solid transparent;
    user-select: none;
}

.menuitem:active {
    outline: 1px dotted #000000;
    outline-offset: -1px;
}

/* URL-field */
.url-field {
    display: flex;
    align-items: center;
    padding-left: 4px;
    height: 95%;
    width: 100%;
}

.url-text {
    flex: 1;  /* занимает всё свободное место, прижимая кнопку вправо */
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.url-dropdown {
    margin-top: 2px;
    min-width: unset;
    min-height: unset;
    width: 1px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>