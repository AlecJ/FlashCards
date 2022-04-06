<template>
    <div id="modal-container" :style="{ left: this.isRevealed ? '0vw' : '100vw' }">
        <slot />
    </div>
    <div id="lightbox" @click="this.toggleLightbox(false)"
         :style="{ left: this.isRevealed ? '0' : '100vw' }" />
</template>

<script>
export default {
    props: {
        isRevealed: Boolean,
        toggleLightbox: Function,
    },
};

</script>

<style>
#modal-container {
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;

    display: grid;
    align-items: center;
    justify-items: center;
}

#lightbox {
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;

    background-color: rgba(49, 49, 49, 0.95);
    z-index: 1;


}


</style>