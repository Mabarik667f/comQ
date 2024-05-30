<script>
import SearchChat from "@/components/SearchChat";
export default {
    components: {
        SearchChat
    }
}
</script>

<template>
    <div class="chats-header">
        
        <com-button :class="'menu-button'">&#9776;</com-button>
        <SearchChat></SearchChat>
    </div>
</template>

<style scoped>
.chats-header {
    display: flex;
    flex-direction: row;
}
.menu-button {
    --bs-btn-color: #333; /* Цвет текста кнопки (темно-серый) */
    --bs-btn-bg: #f8f9fa; /* Цвет фона кнопки (светло-серый) */
    --bs-btn-border-color: #ced4da; /* Цвет рамки кнопки (серый) */
    --bs-btn-hover-color: #fff; /* Цвет текста при наведении (белый) */
    --bs-btn-hover-bg: #6c757d; /* Цвет фона при наведении (темно-серый) */
    --bs-btn-hover-border-color: #6c757d; /* Цвет рамки при наведении (темно-серый) */
    --bs-btn-focus-shadow-rgb: 49, 132, 253; /* Тень при фокусе (синий) */
    --bs-btn-active-color: #fff; /* Цвет текста при активном состоянии (белый) */
    --bs-btn-active-bg: #343a40; /* Цвет фона при активном состоянии (темно-серый) */
    --bs-btn-active-border-color: #343a40; /* Цвет рамки при активном состоянии (темно-серый) */
    --bs-btn-active-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125); /* Тень при активном состоянии */
    --bs-btn-disabled-color: #6c757d; /* Цвет текста для отключенного состояния (серый) */
    --bs-btn-disabled-bg: #f8f9fa; /* Цвет фона для отключенного состояния (светло-серый) */
    --bs-btn-disabled-border-color: #f8f9fa; /* Цвет рамки для отключенного состояния (светло-серый) */

}
</style>