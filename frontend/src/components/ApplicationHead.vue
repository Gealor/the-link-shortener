<template>
    <div class="bar-header" style="height: 30px;">
        <!-- Меню -->
        <div class="separator">
            <div class="vertical-separator-white"></div>
        </div>
        <div 
            v-for="(elem, index) in listTools" 
            class="menuitem" 
            :tabindex="index"
            style="user-select: none;"
        >
            <span class="mnemonic">{{ elem[0] }}</span>{{ elem.slice(1) }}
        </div>
    </div>

    <!-- Действия -->
    <div class="bar-header" style="height: 45px;">
        <div class="separator">
            <div class="vertical-separator-white"></div>
        </div>
        
        <div class="toolbar-btn">
            <img :src="stopIcon" alt="Stop" class="toolbar-icon" />
            <span class="toolbar-label">Stop</span>
        </div>
        <div class="toolbar-btn">
            <img :src="homeIcon" alt="Home" class="toolbar-icon" />
            <span class="toolbar-label">Home</span>
        </div>

        <div class="separator">
            <div class="vertical-separator-black"></div>
        </div>

        <div class="toolbar-btn">
            <img :src="searchIcon" alt="Search" class="toolbar-icon" />
            <span class="toolbar-label">Search</span>
        </div>
        <div class="toolbar-btn">
            <img :src="favoriteIcon" alt="Favorite" class="toolbar-icon" />
            <span class="toolbar-label">Favorite</span>
        </div>
        <div class="toolbar-btn">
            <img :src="historyIcon" alt="History" class="toolbar-icon" />
            <span class="toolbar-label">History</span>
        </div>

        <div class="separator">
            <div class="vertical-separator-black"></div>
        </div>

        <div class="toolbar-btn">
            <img :src="mailIcon" alt="Mail" class="toolbar-icon" />
            <span class="toolbar-label">Mail</span>
        </div>
        <div class="toolbar-btn">
            <img :src="printIcon" alt="Print" class="toolbar-icon" />
            <span class="toolbar-label">Print</span>
        </div>
    </div>

    <!-- Поиск -->
    <div class="bar-header" style="height: 30px;">
        <div class="separator">
            <div class="vertical-separator-white"></div>
        </div>
        <div>
            <span class="mnemonic">A</span>ddress
        </div>
        <div class="field-border url-field" style="height: 95%; width: 100%;">
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